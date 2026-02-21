import wpilib

from ultime.autoproperty import autoproperty
from ultime.command import Command
from subsystems.drivetrain import Drivetrain


class ForwardPosition(Command):
    delay = autoproperty(1.0)

    def __init__(self, drivetrain: Drivetrain):
        super().__init__()
        self.drivetrain = drivetrain
        self.timer = wpilib.Timer()
        self.addRequirements(drivetrain)

    def initialize(self):
        self.timer.restart()

    def execute(self):
        self.drivetrain.setForwardFormation()

    def isFinished(self) -> bool:
        return self.timer.hasElapsed(self.delay)

    def end(self, interrupted: bool):
        self.drivetrain.stop()
        self.timer.stop()
