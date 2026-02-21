from subsystems.shooter import Shooter
from ultime.command import Command
from modules.shootercalcmodule import ShooterCalcModule


class PrepareShoot(Command):
    def __init__(self, shooter: Shooter,shooter_calc_module: ShooterCalcModule, end_stop: bool = False):
        super().__init__()
        self.shooter = shooter
        self.shooter_calc_module = shooter_calc_module
        self.end_stop = end_stop
        self.addRequirements(self.shooter)

    def execute(self):
        speed_rpm = self.shooter_calc_module.getRPM()
        self.shooter.shoot(speed_rpm)

    def isFinished(self) -> bool:
        return False

    def end(self, interrupted: bool):
        if self.end_stop:
            self.shooter.stop()
