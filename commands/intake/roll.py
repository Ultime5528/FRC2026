from ultime.command import Command
from subsystems.intake import Intake


class Roll(Command):

    def __init__(self, intake: Intake):
        self.intake = intake
        self.addRequirements(self.intake)

    def execute(self):
        self.intake.roll()

    def isFinished(self) -> bool:
        return False

    def end(self, interrupted: bool):
        self.intake.stop_intake()
