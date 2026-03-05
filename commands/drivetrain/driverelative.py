from typing import Union, Callable

from wpimath.geometry import Translation2d

from subsystems.drivetrain import Drivetrain
from ultime.autoproperty import autoproperty
from ultime.command import Command


class DriveRelative(Command):
    @classmethod
    def right(cls, drivetrain: Drivetrain):
        cmd = cls(drivetrain, lambda: Translation2d(0, -1) * drive_relative_properties.speed)
        cmd.setName(DriveRelative.__name__ + ".right")
        return cmd

    @classmethod
    def left(cls, drivetrain: Drivetrain):
        cmd = cls(drivetrain, lambda: Translation2d(0, 1) * drive_relative_properties.speed)
        cmd.setName(DriveRelative.__name__ + ".left")
        return cmd

    @classmethod
    def forwards(cls, drivetrain: Drivetrain):
        cmd = cls(drivetrain, lambda: Translation2d(1, 0) * drive_relative_properties.speed)
        cmd.setName(DriveRelative.__name__ + ".forwards")
        return cmd

    @classmethod
    def backwards(cls, drivetrain: Drivetrain):
        cmd = cls(drivetrain, lambda: Translation2d(-1, 0) * drive_relative_properties.speed)
        cmd.setName(DriveRelative.__name__ + ".backwards")
        return cmd

    def __init__(self, drivetrain: Drivetrain, speed: Union[Translation2d, Callable[[], Translation2d]]):
        super().__init__()
        self.drivetrain = drivetrain
        self.addRequirements(drivetrain)
        self.get_speed = speed if callable(speed) else lambda: speed

    def execute(self):
        speed = self.get_speed()
        self.drivetrain.driveFromStickInputs(speed.x, speed.y, 0, False)

    def end(self, interrupted: bool):
        self.drivetrain.stop()


class _ClassProperties:
    speed = autoproperty(0.2, subtable=DriveRelative.__name__)


drive_relative_properties = _ClassProperties()
