from subsystems.shooter import Shooter
from ultime.autoproperty import autoproperty
from ultime.command import Command


class ManualPrepareShoot(Command):
    speed_rpm = autoproperty(2500.0)

    def __init__(self, shooter: Shooter):
        super().__init__()
        self.shooter = shooter
        self.addRequirements(self.shooter)

    def execute(self):
        self.shooter.shoot(self.speed_rpm)

    def isFinished(self) -> bool:
        return False

    def end(self, interrupted: bool):
        self.shooter.stop()


class ManualShoot(ManualPrepareShoot):
    def __init__(self, shooter: Shooter):
        super().__init__(shooter)

    def execute(self):
        super().execute()
        if self.shooter.isAtVelocity():
            self.shooter.sendFuel(self.speed_rpm)
        else:
            self.shooter.stopFuel()
