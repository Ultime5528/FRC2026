from pytest import approx
from commands2 import Command

from commands.guide.move import MoveGuide, ResetGuide
from modules.shootercalcmodule import ShooterCalcModule
from subsystems.guide import Guide
from ultime.autoproperty import autoproperty


class CheckGuide(Command):

    speed_fast = autoproperty(0.15)
    speed_slow = autoproperty(0.05)
    position_tolerance_far = autoproperty(1.5)
    position_tolerance_close = autoproperty(0.5)
    position_unused = autoproperty(-8.0)
    position_used = autoproperty(5.0)

    def __init__(self, guide: Guide, shooter_calc_module: ShooterCalcModule):
        super().__init__()
        self.guide = guide
        self.shooter_calc_module = shooter_calc_module
        self.addRequirements(guide)

    def execute(self):
        if not self.guide.hasReset():
            ResetGuide.down(self.guide).schedule()
        else:
            encoder_position = self.guide.getPosition()
            desired_position = self.getDesiredPosition()
            error = abs(encoder_position - desired_position)
            speed = 0.0

            if error < self.position_tolerance_close:
                speed = 0.0
            elif error < self.position_tolerance_far:
                if encoder_position > desired_position:
                    speed = -self.speed_slow
                else:
                    speed = self.speed_slow
            else:
                if encoder_position > desired_position:
                    speed = -self.speed_fast
                else:
                    speed = self.speed_fast

            self.guide.setSpeed(speed)

    def getDesiredPosition(self) -> float:
        if self.shooter_calc_module.shouldUseGuide():
            return self.position_used
        else:
            return self.position_unused
