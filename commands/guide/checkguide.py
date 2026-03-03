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
        self.is_reset_done = False

    def execute(self):
        if not self.guide.hasReset():
            ResetGuide.down(self.guide)
        else:
            self.is_reset_done = True

        if self.is_reset_done:
            if self.shooter_calc_module.shouldUseGuide():
                MoveGuide.toUsed(self.guide).schedule()
            else:
                MoveGuide.toUnused(self.guide).schedule()
