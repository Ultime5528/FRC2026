import wpilib
from ultime.command import Command
from subsystems.shooter import Shooter
from ultime.autoproperty import autoproperty


class PrepareShoot(Command):
    rpm_range = autoproperty(150)

    def __init__(self, shooter: Shooter, end_stop: bool = False):
        super().__init__()
        self.shooter = shooter
        self.end_stop = end_stop
        self.addRequirements(self.shooter)

    def initialize(self):
        pass

    def execute(self):
        speed_rpm = 666.6  # mettre la valeur du calcul d'hayder
        self.shooter.shoot(speed_rpm)

    def isFinished(self) -> bool:
        return False

    def end(self, interrupted: bool):
        if self.end_stop:
            self.shooter.stop()
