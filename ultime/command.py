from abc import abstractmethod
from functools import wraps
from typing import Type

import wpilib
from commands2 import Command, CommandScheduler, PrintCommand
from wpilib import Timer, DataLogManager
from wpiutil import SendableBuilder

from ultime.autoproperty import FloatProperty, asCallable
from ultime.timethis import tt


def ignore_requirements(reqs: list[str]):
    def _ignore(actual_cls: Type[Command]) -> Type[Command]:
        setattr(actual_cls, "__ignore_reqs", reqs)
        return actual_cls

    return _ignore


def with_timeout(seconds: float):
    def add_timeout(CommandClass):
        @wraps(CommandClass, updated=())
        class CommandWithTimeout(CommandClass):
            def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)
                self.setName(CommandClass.__name__)
                self.seconds = seconds
                self.timer = Timer()

            def initialize(self):
                super().initialize()
                self.timer.restart()

            def isFinished(self) -> bool:
                return super().isFinished() or self.timer.get() >= self.seconds

            def end(self, interrupted: bool):
                super().end(interrupted)
                self.timer.stop()
                if self.timer.get() >= self.seconds:
                    msg = f"Command {self.getName()} got interrupted after {self.seconds} seconds"
                    wpilib.reportError(msg)
                    DataLogManager.log(msg)

        setattr(CommandWithTimeout, "__wrapped_class", CommandClass)

        return CommandWithTimeout

    return add_timeout


class WaitCommand(Command):
    def __init__(self, seconds: FloatProperty):
        super().__init__()
        self.get_seconds = asCallable(seconds)
        self.timer = wpilib.Timer()

    def initialize(self):
        self.timer.restart()

    def isFinished(self) -> bool:
        return self.timer.hasElapsed(self.get_seconds())


class DeferredCommand(Command):
    """
    Defers Command construction to runtime. Runs the command returned by a supplier when this command
    is initialized, and ends when it ends. Useful for performing runtime tasks before creating a new
    command. If this command is interrupted, it will cancel the command.

    Note that the supplier *must* create a new Command each call. For selecting one of a
    preallocated set of commands, use :class:`commands2.SelectCommand`.
    """

    def __init__(self):
        """

        Creates a new DeferredCommand that directly runs the supplied command when initialized, and
        ends when it ends. Useful for lazily creating commands when the DeferredCommand is initialized,
        such as if the supplied command depends on runtime state. The method `createCommand` will be called
        everytime the command is initialized, so it should return a new Command each time.
        """
        super().__init__()

        self._null_command = PrintCommand(
            f"[DeferredCommand] Supplied command was None!"
        )
        self._command = self._null_command

    @abstractmethod
    def createCommand(self) -> Command:
        raise NotImplementedError("You must implement createCommand")

    def initialize(self):
        cmd = self.createCommand()
        if cmd is not None:
            self._command = cmd
            CommandScheduler.getInstance().registerComposedCommands([self._command])
        self._command.initialize()

    def execute(self):
        self._command.execute()

    def isFinished(self):
        return self._command.isFinished()

    def end(self, interrupted):
        self._command.end(interrupted)
        self._command = self._null_command

    def initSendable(self, builder: SendableBuilder):
        super().initSendable(builder)
        builder.addStringProperty(
            "deferred",
            tt(
                lambda: (
                    "null"
                    if self._command is self._null_command
                    else self._command.getName()
                )
            ),
            lambda _: None,
        )
