from pathplannerlib.path import PathPlannerPath
from pathplannerlib.trajectory import PathPlannerTrajectoryState
from wpilib import DriverStation
from wpimath.geometry import Pose2d

from subsystems.drivetrain import Drivetrain
from ultime.autoproperty import autoproperty
from ultime.command import Command


class AlignPreciseAfterPath(Command):
    distance_threshold = autoproperty(0.05)
    rotation_threshold = autoproperty(2.0)

    def __init__(self, drivetrain: Drivetrain, path_or_pose: PathPlannerPath | Pose2d):
        super().__init__()
        self.drivetrain = drivetrain
        self.addRequirements(drivetrain)
        self.path_or_pose = path_or_pose
        self.goal_pose: Pose2d = Pose2d()
        self.controller = self.drivetrain.pp_holonomic_drive_controller
        self.goal_state = PathPlannerTrajectoryState()

    def initialize(self):
        if isinstance(self.path_or_pose, PathPlannerPath):
            if DriverStation.getAlliance() == DriverStation.Alliance.kRed:
                path = self.path_or_pose.flipPath()
            else:
                path = self.path_or_pose

            self.goal_pose = Pose2d(
                path.getPathPoses()[-1].translation(), path.getGoalEndState().rotation
            )
        else:
            self.goal_pose = self.path_or_pose

        self.goal_state.pose = self.goal_pose

    def execute(self):
        current_pose = self.drivetrain.getPose()
        chassis_speed = self.controller.calculateRobotRelativeSpeeds(
            current_pose, self.goal_state
        )
        self.drivetrain.driveFromChassisSpeeds(chassis_speed)

    def isFinished(self) -> bool:
        return (
            self.drivetrain.getPose()
            .translation()
            .distance(self.goal_pose.translation())
            < self.distance_threshold
        ) and (
            self.drivetrain.getEstimatedAngle()
            .relativeTo(self.goal_pose.rotation())
            .degrees()
            < self.rotation_threshold
        )
