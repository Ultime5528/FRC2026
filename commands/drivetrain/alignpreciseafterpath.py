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

    def __init__(self, drivetrain: Drivetrain, path: PathPlannerPath):
        super().__init__()
        self.drivetrain = drivetrain
        self.path = path
        self.after_path_goal: Pose2d = Pose2d()
        self.holonomic_drive_controller = self.drivetrain.pp_holonomic_drive_controller
        self.pathplanner_trajectory = PathPlannerTrajectoryState()

    def initialize(self):
        if DriverStation.getAlliance() == DriverStation.Alliance.kRed:
            path = self.path.flipPath()
        else:
            path = self.path

        self.after_path_goal = Pose2d(path.getPathPoses()[-1].translation(), path.getGoalEndState().rotation)
        self.pathplanner_trajectory.pose = self.after_path_goal

    def execute(self):
        current_pose = self.drivetrain.getPose()
        chassis_speed = self.holonomic_drive_controller.calculateRobotRelativeSpeeds(
            current_pose, self.pathplanner_trajectory
        )
        self.drivetrain.driveFromChassisSpeeds(chassis_speed)

    def isFinished(self) -> bool:
        return (
            self.drivetrain.getPose()
            .translation()
            .distance(self.after_path_goal.translation())
            < self.distance_threshold
        ) and (
            self.drivetrain.getEstimatedAngle().relativeTo(self.after_path_goal.rotation()).degrees() < self.rotation_threshold
        )
