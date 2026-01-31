import wpilib
from ultime.command import Command
from subsystems.shooter import Shooter
from ultime.autoproperty import autoproperty


class Shoot(Command):

    def __init__(self, shooter: Shooter):
        super().__init__()
        self.shooter = shooter
        self.addRequirements(self.shooter)

    def execute(self):
      self.shooter.shoot()

    def isFinished(self) -> bool:
        return False

    def end(self, interrupted: bool):
        self.shooter.stop_shooting()