
from subsystems.shooter import Shooter
from ultime.command import Command


class PrepareShoot(Command):
    def __init__(self, shooter: Shooter, end_stop: bool = False):
        super().__init__()
        self.shooter = shooter
        self.end_stop = end_stop
        self.addRequirements(self.shooter)

    def execute(self):
        speed_rpm = 666.6  # TODO mettre la valeur du calcul d'hayder
        self.shooter.shoot(speed_rpm)

    def isFinished(self) -> bool:
        return False

    def end(self, interrupted: bool):
        if self.end_stop:
            self.shooter.stop()
