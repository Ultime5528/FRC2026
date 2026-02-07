from ultime.command import Command
from subsystems.intake import Intake

import wpilib


class Reset_Intake(Command):
    def __init__(self, intake: Intake):
        super().__init__()
        self.intake = intake
        self.addRequirements(intake)
        self.is_at_zero = False

    def initialize(self):
        self.is_at_zero = False

    def execute(self):
        if self.intake.isSwitchMaxPressed():
            self.intake.deploy_pivot()
            self.is_at_zero = True
        else:
            (self.intake.retreat_pivot())

    def isFinished(self) -> bool:
        return not self.intake.isSwitchMaxPressed() and self.is_at_zero

    def end(self, interrupted: bool):
        self.intake.stop_pivot()
