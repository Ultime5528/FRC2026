import wpilib
from commands2 import Command

from subsystems.hugger import Hugger


class Unhug(Command):
    def __init__(self, hugger: Hugger):
        super().__init__()
        self.hugger = hugger
        self.addRequirements(hugger)
        self.timer = wpilib.Timer()

    def initialize(self):
        self.timer.restart()

    def execute(self):
        self.hugger.unhug()

    def isFinished(self) -> bool:
        return self.timer.hasElapsed(self.hugger.delay_hug)

    def end(self, interrupted: bool):
        self.timer.stop()
