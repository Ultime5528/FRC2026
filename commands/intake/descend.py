from ultime.command import Command
from subsystems.intake import Intake


class Descend(Command):
    def __init__(self, intake: Intake):
        super().__init__()
        self.intake = intake
        self.addRequirements(intake)

    def execute(self):
        self.intake.descend_pivot()

    def isFinished(self) -> bool:
        return self.intake.isSwitchMinPressed()

    def end(self, interrupted: bool):
        self.intake.stop_pivot()
