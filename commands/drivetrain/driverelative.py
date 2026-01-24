from wpimath.geometry import Translation2d

from subsystems.drivetrain import Drivetrain
from ultime.autoproperty import autoproperty
from ultime.command import Command


class DriveRelative(Command):
    @classmethod
    def right(cls, drivetrain: Drivetrain):
        cmd = cls(drivetrain, Translation2d(0, -1) * drive_relative_properties.speed)
        cmd.setName(DriveRelative.__name__ + ".right")
        return cmd

    @classmethod
    def left(cls, drivetrain: Drivetrain):
        cmd = cls(drivetrain, Translation2d(0, 1) * drive_relative_properties.speed)
        cmd.setName(DriveRelative.__name__ + ".left")
        return cmd

    @classmethod
    def forwards(cls, drivetrain: Drivetrain):
        cmd = cls(drivetrain, Translation2d(1, 0) * drive_relative_properties.speed)
        cmd.setName(DriveRelative.__name__ + ".forwards")
        return cmd

    @classmethod
    def backwards(cls, drivetrain: Drivetrain):
        cmd = cls(drivetrain, Translation2d(-1, 0) * drive_relative_properties.speed)
        cmd.setName(DriveRelative.__name__ + ".backwards")
        return cmd

    def __init__(self, drivetrain: Drivetrain, speed: Translation2d):
        super().__init__()
        self.drivetrain = drivetrain
        self.addRequirements(drivetrain)
        self.speed = speed

    def execute(self):
        self.drivetrain.driveFromStickInputs(self.speed.x, self.speed.y, 0, False)

    def end(self, interrupted: bool):
        self.drivetrain.stop()


class _ClassProperties:
    speed = autoproperty(0.2, subtable=DriveRelative.__name__)


drive_relative_properties = _ClassProperties()
