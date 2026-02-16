from subsystems.shooter import Shooter
from ultime.autoproperty import autoproperty
from ultime.command import Command


class ManualPrepareShoot(Command):
    def __init__(self, shooter: Shooter):
        super().__init__()
        self.shooter = shooter
        self.addRequirements(self.shooter)

    def execute(self):
        self.shooter.shoot(_manual_shoot_property.speed_rpm)

    def isFinished(self) -> bool:
        return False

    def end(self, interrupted: bool):
        self.shooter.stop()


class ManualShoot(ManualPrepareShoot):
    def __init__(self, shooter: Shooter):
        super().__init__(shooter)

    def execute(self):
        super().execute()
        self.shooter.sendFuel()


class _ManualShootProperty:
    speed_rpm = autoproperty(666.6, subtable=ManualShoot.__name__)


_manual_shoot_property = _ManualShootProperty()
