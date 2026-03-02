from commands2 import Command

from commands.guide.guide import MoveGuide
from modules.shootercalcmodule import ShooterCalcModule
from subsystems.guide import Guide


class CheckGuide(Command):
    def __init__(self, guide: Guide, shooter_calc_module: ShooterCalcModule):
        super().__init__()
        self.guide = guide
        self.shooter_calc_module = shooter_calc_module
        self.addRequirements(guide)

    def execute(self):
        if self.shooter_calc_module.shouldUseGuide():
            MoveGuide.toUsed(self.guide).schedule()
        else:
            MoveGuide.toUnused(self.guide).schedule()
