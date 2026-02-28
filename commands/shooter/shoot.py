from modules.shootercalcmodule import ShooterCalcModule
from subsystems.shooter import Shooter
from ultime.command import Command


class Shoot(Command):
    def __init__(self, shooter: Shooter, shooter_calc_module: ShooterCalcModule):
        super().__init__()
        self.shooter = shooter
        self.shooter_calc_module = shooter_calc_module
        self.addRequirements(self.shooter)

    def execute(self):
        speed_rpm = self.shooter_calc_module.getRPM()
        self.shooter.shoot(speed_rpm)

        if self.shooter.isAtVelocity():
            self.shooter.sendFuel()
        else:
            self.shooter.stopFuel()

    def isFinished(self) -> bool:
        return False

    def end(self, interrupted: bool):
        self.shooter.stop()
