from wpilib import DriverStation
from wpimath.geometry import Pose2d, Rotation2d, Pose3d, Rotation3d

from modules.questvision import QuestVisionModule
from subsystems.drivetrain import Drivetrain
from ultime.command import Command


class ResetGyro(Command):
    def __init__(self, drivetrain: Drivetrain):
        super().__init__()
        self.drivetrain = drivetrain
        self.addRequirements(drivetrain)

    def initialize(self):
        current = self.drivetrain.getPose()

        if DriverStation.getAlliance() == DriverStation.Alliance.kBlue:
            new_rot = Rotation2d()
        else:
            new_rot = Rotation2d.fromDegrees(180)

        self.drivetrain.resetToPose(Pose2d(current.translation(), new_rot))

    def isFinished(self) -> bool:
        return True
