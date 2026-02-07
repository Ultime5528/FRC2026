import wpilib
from ultime.command import Command
from subsystems.shooter import Shooter
from ultime.autoproperty import autoproperty


class Shoot(Command):

    def __init__(self, shooter: Shooter):
        super().__init__()
        self.shooter = shooter
        self.addRequirements(self.shooter)

    def initialize(self):
        pass

    def execute(self):
        speed_rpm = 666.6  # mettre la valeur du calcul d'hayder
        self.shooter.shoot(speed_rpm)
        self.shooter.sendFuel()

    def isFinished(self) -> bool:
        return False

    def end(self, interrupted: bool):
        self.shooter.stop()
