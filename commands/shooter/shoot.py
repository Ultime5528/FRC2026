from subsystems.shooter import Shooter
from ultime.command import Command


class Shoot(Command):
    def __init__(self, shooter: Shooter):
        super().__init__()
        self.shooter = shooter
        self.addRequirements(self.shooter)

        self.shooter.setToUnstuck()

        def execute(self):
            speed_rpm = 666.6  # mettre la valeur du calcul d'hayder
            self.shooter.shoot(speed_rpm)

        if self.shooter.isAtVelocity():
            self.shooter.sendFuel()
        else:
            self.shooter.stopFuel()

    def isFinished(self) -> bool:
        return False

    def end(self, interrupted: bool):
        self.shooter.stop()
