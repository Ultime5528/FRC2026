import wpilib
from wpilib import DriverStation
from wpimath.geometry import Pose2d, Rotation2d

from subsystems.drivetrain import Drivetrain
from ultime.command import Command


class ResetGyro(Command):
    def __init__(self, drivetrain: Drivetrain):
        super().__init__()
        self.drivetrain = drivetrain
        self.addRequirements(drivetrain)
        self.timer = wpilib.Timer()
        self.started_calibrating = False

    def initialize(self):
        self.timer.restart()
        self.started_calibrating = False
        self.drivetrain.stop()

    def execute(self):
        if not self.started_calibrating and self.timer.hasElapsed(2.0):
            self.started_calibrating = True
            self.drivetrain._gyro.calibrate()

    def isFinished(self) -> bool:
        return self.timer.hasElapsed(7.0)

    def end(self, interrupted: bool):
        if not interrupted:
            current = self.drivetrain.getPose()

            if DriverStation.getAlliance() == DriverStation.Alliance.kBlue:
                new_rot = Rotation2d()
            else:
                new_rot = Rotation2d.fromDegrees(180)

            self.drivetrain.resetToPose(Pose2d(current.translation(), new_rot))
