from pytest import approx
from commands2 import Command

from commands.guide.move import MoveGuide, ResetGuide
from modules.shootercalcmodule import ShooterCalcModule
from subsystems.guide import Guide
from ultime.autoproperty import autoproperty


class CheckGuide(Command):

    speed = autoproperty(0.15)
    position_tolerance = autoproperty(0.05)
    position_unused = autoproperty(-8.0)
    position_used = autoproperty(3.0)

    def __init__(self, guide: Guide, shooter_calc_module: ShooterCalcModule):
        super().__init__()
        self.guide = guide
        self.shooter_calc_module = shooter_calc_module
        self.addRequirements(guide)

    def execute(self):
        if not self.guide.hasReset():
            ResetGuide.down(self.guide).schedule()
        else:
            encoder_position = self.guide.getEncoderPosition()
            desired_position = self.getDesiredPosition()

            if encoder_position == approx(desired_position, lambda: self.position_tolerance):
                self.guide.setSpeed(0.0)
            elif encoder_position > desired_position:
                self.guide.setSpeed(-self.speed)
            else:
                self.guide.setSpeed(self.speed)

    def getDesiredPosition(self) -> float:
        if self.shooter_calc_module.shouldUseGuide():
            return self.position_used
        else:
            return self.position_unused