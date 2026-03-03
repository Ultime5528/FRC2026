from commands2 import Command

from commands.guide.move import MoveGuide, ResetGuide
from modules.shootercalcmodule import ShooterCalcModule
from subsystems.guide import Guide


class CheckGuide(Command):
    def __init__(self, guide: Guide, shooter_calc_module: ShooterCalcModule):
        super().__init__()
        self.guide = guide
        self.shooter_calc_module = shooter_calc_module
        self.addRequirements(guide)

        self.command = None

    def execute(self):

        if self.command is None:

            if not self.guide.hasReset():
                self.command = ResetGuide.down(self.guide)
            elif self.shooter_calc_module.shouldUseGuide():
                self.command = MoveGuide.toUsed(self.guide)
            else:
                self.command = MoveGuide.toUnused(self.guide)

            self.command.schedule()

        elif not self.command.isScheduled():
            self.command = None

