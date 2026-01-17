import importlib
import pkgutil
from types import ModuleType
from typing import Dict, Callable

import pytest
from commands2 import Command
from pyfrc.test_support.controller import TestController
from wpilib.simulation import DriverStationSim, stepTiming

from ultime.modulerobot import ModuleRobot


def import_submodules(package, recursive=True) -> Dict[str, ModuleType]:
    """Import all submodules of a module, recursively, including subpackages

    :param package: package (name or actual module)
    :type package: str | module
    :rtype: dict[str, types.ModuleType]
    """
    if isinstance(package, str):
        package = importlib.import_module(package)
    results = {}
    for loader, name, is_pkg in pkgutil.walk_packages(package.__path__):
        full_name = package.__name__ + "." + name
        try:
            results[full_name] = importlib.import_module(full_name)
        except ModuleNotFoundError:
            continue
        if recursive and is_pkg:
            results.update(import_submodules(full_name))
    return results


class RobotTestController:
    def __init__(self, control: TestController):
        self._control = control

    def disableRobot(self):
        DriverStationSim.setDsAttached(True)
        DriverStationSim.setAutonomous(False)
        DriverStationSim.setEnabled(False)
        DriverStationSim.notifyNewData()
        stepTiming(0.05)

    def startTeleop(self):
        DriverStationSim.setDsAttached(True)
        DriverStationSim.setAutonomous(False)
        DriverStationSim.setEnabled(True)
        DriverStationSim.notifyNewData()
        stepTiming(0.05)

    def startAutonomous(self):
        DriverStationSim.setDsAttached(True)
        DriverStationSim.setAutonomous(True)
        DriverStationSim.setEnabled(True)
        DriverStationSim.notifyNewData()
        stepTiming(0.05)

    def startTest(self):
        DriverStationSim.setDsAttached(True)
        DriverStationSim.setTest(True)
        DriverStationSim.setEnabled(True)
        DriverStationSim.notifyNewData()
        stepTiming(0.05)

    def run_command(self, cmd: Command, timeout: float):
        cmd.schedule()
        self.wait_until(lambda: not cmd.isScheduled(), timeout)

    def wait_one_frame(self):
        DriverStationSim.notifyNewData()
        stepTiming(ModuleRobot.period)

    def wait(self, seconds: float, delta: float = 0.02):
        assert seconds > 0

        time = 0.0
        delta = min(seconds, delta)

        while time < seconds:
            DriverStationSim.notifyNewData()
            stepTiming(delta)
            time += delta

    def wait_until(self, cond: Callable[[], bool], timeout: float, delta: float = 0.02):
        time = 0.0
        delta = min(delta, timeout)

        while not cond():
            self.wait(delta)
            time += delta
            assert time < timeout, f"Condition was not reached within {timeout} seconds"


@pytest.fixture(scope="function")
def robot_controller(control: TestController):
    with control.run_robot():
        yield RobotTestController(control)
