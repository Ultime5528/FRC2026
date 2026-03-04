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

    def execute(self):
        if self.guide.state != self.guide.State.Reset and not self.guide.hasReset():
            self.guide.state = self.guide.State.Reset
            self.command = ResetGuide.down(self.guide)
            self.command.schedule()

        elif (
            self.guide.state != self.guide.State.Used
            and self.shooter_calc_module.shouldUseGuide()
        ):
            self.guide.state = self.guide.State.Used
            self.command = MoveGuide.toUsed(self.guide)
            self.command.schedule()

        elif (
            self.guide.state != self.guide.State.Unused
            and not self.shooter_calc_module.shouldUseGuide()
        ):
            self.guide.state = self.guide.State.Unused
            self.command = MoveGuide.toUnused(self.guide)
            self.command.schedule()
