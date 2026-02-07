import ast
import gc
import inspect
import typing
from textwrap import dedent
from typing import List, Type
from unittest.mock import patch

from commands2 import Command, Subsystem, CommandScheduler

from robot import Robot
from ultime.tests.utils import import_submodules, RobotTestController


def get_commands() -> List[Type[Command]]:
    import commands

    results = import_submodules(commands)
    cmds = []

    for mod in results.values():
        for _, cls in inspect.getmembers(mod, inspect.isclass):
            if (
                issubclass(cls, Command)
                and not cls.__module__.startswith("commands2")
                and not cls.__module__.startswith("ultime.command")
                and cls not in cmds
            ):
                cls = getattr(cls, "__wrapped_class", cls)
                cmds.append(cls)
    return cmds


def get_arguments(command: Command):
    return inspect.signature(command.__init__).parameters


def test_arguments():
    for obj in get_commands():
        for name, arg in get_arguments(obj).items():
            if name == "self":
                continue
            assert (
                arg.annotation is not arg.empty
            ), f"Argument {name} of {obj.__name__} has no type annotation"


def test_requirements(robot: Robot):
    gc.collect()

    commands = []
    failures = []

    for obj in gc.get_objects():
        if (
            isinstance(obj, Command)
            and not obj.__class__.__module__.startswith("commands2")
            and not obj.__class__.__module__.startswith("ultime.command")
        ):
            commands.append(obj)

    assert commands, "No found commands"

    for command in commands:
        requirements = command.getRequirements()

        stored_subsystems = []
        for attr_name in dir(command):
            attr = getattr(command, attr_name)
            if isinstance(attr, Subsystem):
                stored_subsystems.append(attr)

        # Check requirements
        for subsystem in stored_subsystems:
            if subsystem not in requirements:
                failures.append(
                    f"{type(command).__name__}: missing {type(subsystem).__name__} in requirements"
                )

        assert not failures, "\n" + "\n".join(f"  - {f}" for f in failures)


def test_command_scheduler_enabled(robot_controller: RobotTestController, robot: Robot):
    robot_controller.startTeleop()
    robot_controller.wait(1.0)

    assert (
        not CommandScheduler.getInstance()._disabled
    ), "CommandScheduler should not be disabled"

    """
    La méthode 'run' du CommandScheduler est passé directement par référence 
    au TimedRobot, donc on ne peut pas la mocker.

    On mock plutôt la fonction periodic d'un subsystem, qui doit uniquement
    être appelé par le scheduler.
    """

    with patch.object(
        robot.hardware.drivetrain,
        "periodic",
        wraps=robot.hardware.drivetrain.periodic,
    ) as mock:
        assert mock.call_count == 0
        robot_controller.wait(1.0)
        assert mock.call_count >= 50
