from subsystems.shooter import Shooter
from ultime.autoproperty import autoproperty
from ultime.command import Command


class ManualPrepareShoot(Command):
    def __init__(self, shooter: Shooter):
        super().__init__()
        self.shooter = shooter
        self.addRequirements(self.shooter)

    def execute(self):
        self.shooter.shoot(manual_shoot_properties.speed_rpm)

    def isFinished(self) -> bool:
        return False

    def end(self, interrupted: bool):
        self.shooter.stop()


class ManualShoot(ManualPrepareShoot):
    def __init__(self, shooter: Shooter):
        super().__init__(shooter)

    def initialize(self):
        self.shooter.reset()

    def execute(self):
        super().execute()
        if self.shooter.isAtVelocity():
            self.shooter.sendFuel()
        else:
            self.shooter.stopFuel()


class _ManualShootProperties:
    speed_rpm = autoproperty(2500.0, subtable=ManualShoot.__name__)


manual_shoot_properties = _ManualShootProperties()
