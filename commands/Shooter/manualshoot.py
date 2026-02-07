from subsystems.shooter import Shooter
from ultime.autoproperty import autoproperty
from ultime.command import Command


class Shoot(Command):
    speed_rpm = autoproperty(666.6)

    def __init__(self, shooter: Shooter):
        super().__init__()
        self.shooter = shooter
        self.addRequirements(self.shooter)

    def execute(self):
        self.shooter.shoot(self.speed_rpm)

        if self.shooter.isAtVelocity():
            self.shooter.sendFuel()

    def isFinished(self) -> bool:
        return False

    def end(self, interrupted: bool):
        self.shooter.stop()
