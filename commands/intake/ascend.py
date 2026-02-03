from ultime.command import Command
from subsystems.intake import Intake


class Ascend(Command):
    def __init__(self, intake: Intake):
        super().__init__()
        self.intake = intake
        self.addRequirements(intake)

    def execute(self):
        self.intake.ascend_pivot()

    def isFinished(self) -> bool:
        return self.intake.isSwitchMaxPressed()

    def end(self, interrupted: bool):
        self.intake.stop_pivot()
