import wpilib
from commands2 import Command

from subsystems.climber import Climber


class Unhug(Command):
    def __init__(self, climber: Climber):
        super().__init__()
        self.climber = climber
        self.addRequirements(climber)
        self.timer = wpilib.Timer()

    def initialize(self):
        self.timer.restart()

    def execute(self):
        self.climber.unhug()

    def isFinished(self) -> bool:
        return self.timer.hasElapsed(self.climber.delay_hug)

    def end(self, interrupted: bool):
        self.timer.stop()
