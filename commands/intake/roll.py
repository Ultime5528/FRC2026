import wpilib
from ultime.command import Command
from subsystems.intake import Intake
from ultime.autoproperty import autoproperty


class Roll(Command):

    def __init__(self, intake):
        self.intake = intake

    def execute(self):
        self.intake.roll()

    @staticmethod
    def isFinished(self) -> bool:
        return False

    def end(self, interrupted: bool):
        self.intake.stop_intake()





