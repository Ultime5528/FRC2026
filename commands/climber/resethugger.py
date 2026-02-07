import wpilib
from commands2 import Command

from subsystems.climber import Climber


class ResetHugger(Command):
    def __init__(self, climber : Climber):
        super().__init__()
        self.climber = climber
        self.addRequirements(climber)
        self.climber.hugger_maximal_moving_time = self.timer
        self.timer = wpilib.Timer()

    def initialize(self):
        self.timer.reset()
        self.timer.start()
        self.climber.unhug()

    def isFinished(self) -> bool:
        return self.timer.hasElapsed(self.climber.hugger_maximal_moving_time)

    def end(self, interrupted: bool):
        self.timer.stop()