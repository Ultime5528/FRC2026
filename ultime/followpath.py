__all__ = ["FollowPath"]

import math

from commands2 import Command
from pathplannerlib.config import RobotConfig
from pathplannerlib.path import PathPlannerPath
from pathplannerlib.telemetry import PPLibTelemetry
from pathplannerlib.trajectory import PathPlannerTrajectoryState
from wpilib import DriverStation
from wpimath._controls._controls.trajectory import Trajectory
from wpimath.geometry import Rotation2d, Pose2d

from commands.drivetrain.drivetoposes import DriveToPoses
from subsystems.drivetrain import Drivetrain
from ultime.autoproperty import autoproperty
from ultime.command import DeferredCommand


def shouldFlipPath():
    # Boolean supplier that controls when the path will be mirrored for the red alliance
    # This will flip the path being followed to the red side of the field.
    # THE ORIGIN WILL REMAIN ON THE BLUE SIDE
    return DriverStation.getAlliance() == DriverStation.Alliance.kRed


def pathToPoses(path: PathPlannerPath) -> list[Pose2d]:
    states = path.getIdealTrajectory(RobotConfig.fromGUISettings()).getStates()
    poses = []

    previous_pose: Pose2d = states[0].pose
    for value, state in enumerate(states):
        if value == 0:
            poses.append(state.pose)
        elif value == len(states) - 1:
            poses.append(state.pose)
        else:
            if previous_pose.translation().distance(state.pose.translation()) >= 0.1:
                poses.append(state.pose)
                previous_pose = state.pose
    if (
        poses[-2].translation().distance(poses[-1].translation()) <= 0.1
        and len(poses) > 2
    ):
        poses.remove(poses[-2])

    return poses


class FollowPathWithDriveToPoses(DeferredCommand):
    def __init__(self, path: PathPlannerPath, drivetrain: Drivetrain):
        super().__init__()
        self.drivetrain = drivetrain
        self.poses = pathToPoses(path)
        self.flipped_poses = pathToPoses(path.flipPath())
        self.addRequirements(drivetrain)

    def createCommand(self) -> Command:
        return DriveToPoses(self.drivetrain, self.getPoses())

    def getPoses(self) -> list[Pose2d]:
        return self.flipped_poses if shouldFlipPath() else self.poses


class FollowPathCustom(Command):
    delta_t = autoproperty(0.08)
    pos_tolerance = autoproperty(0.3)
    rot_tolerance = autoproperty(0.5)

    def __init__(self, pathplanner_path: PathPlannerPath, drivetrain: Drivetrain):
        super().__init__()
        self.sampled_trajectory = None
        self.drivetrain = drivetrain
        self.pathplanner_path_base = pathplanner_path
        self.addRequirements(drivetrain)
        self.sampled_trajectory: list[PathPlannerTrajectoryState] = []
        self.current_goal = 0
        self.flipped_path = pathplanner_path.flipPath()

    def initialize(self):
        self.current_goal = 0
        self.sampled_trajectory = []

        pathplanner_path = (
            self.flipped_path if shouldFlipPath() else self.pathplanner_path_base
        )
        PPLibTelemetry.setCurrentPath(pathplanner_path)
        trajectory = pathplanner_path.getIdealTrajectory(RobotConfig.fromGUISettings())
        states = []
        for state in trajectory.getStates():
            # Calculate acceleration from velocity change if needed
            acceleration = 0.0  # Or calculate based on velocity differences
            heading_rad = state.heading.radians()
            states.append(
                Trajectory.State(
                    state.timeSeconds,
                    state.linearVelocity,
                    acceleration,
                    state.pose,
                    heading_rad,
                )
            )
        self.drivetrain._field.getObject("traj").setTrajectory(Trajectory(states))
        for i in range(math.ceil(trajectory.getEndState().timeSeconds / self.delta_t)):
            self.sampled_trajectory.append(trajectory.sample(i * self.delta_t))

    def execute(self):
        PPLibTelemetry.setCurrentPose(self.drivetrain.getPose())
        PPLibTelemetry.setTargetPose(
            Pose2d(
                self.sampled_trajectory[self.current_goal].pose.X(),
                self.sampled_trajectory[self.current_goal].pose.Y(),
                self.sampled_trajectory[self.current_goal].pose.rotation(),
            )
        )
        position_error = (
            self.sampled_trajectory[self.current_goal].pose.translation()
            - self.drivetrain.getPose().translation()
        )
        rotation_error: Rotation2d = (
            self.sampled_trajectory[self.current_goal].pose.rotation()
            - self.drivetrain.getPose().rotation()
        )
        if (
            math.hypot(position_error.X(), position_error.Y()) <= self.pos_tolerance
            and rotation_error.degrees() <= self.rot_tolerance
        ):
            self.current_goal += 1
        else:
            PPLibTelemetry.setVelocities(
                math.hypot(
                    self.drivetrain.getRobotRelativeChassisSpeeds().vx,
                    self.drivetrain.getRobotRelativeChassisSpeeds().vy,
                ),
                math.copysign(
                    min(
                        self.sampled_trajectory[self.current_goal].linearVelocity,
                        abs(position_error.X()),
                    ),
                    position_error.X(),
                ),
                rotation_error.radians(),
                self.drivetrain.getRobotRelativeChassisSpeeds().omega,
            )
            self.drivetrain.drive(
                math.copysign(
                    min(
                        self.sampled_trajectory[self.current_goal].linearVelocity,
                        abs(
                            position_error.X()
                            * self.sampled_trajectory[self.current_goal].linearVelocity
                        ),
                    ),
                    position_error.X(),
                ),
                math.copysign(
                    min(
                        self.sampled_trajectory[self.current_goal].linearVelocity,
                        abs(
                            position_error.Y()
                            * self.sampled_trajectory[self.current_goal].linearVelocity
                        ),
                    ),
                    position_error.Y(),
                ),
                rotation_error.radians(),
                True,
            )

    def isFinished(self) -> bool:
        return self.current_goal >= len(self.sampled_trajectory)

    def end(self, interrupted: bool):
        self.drivetrain.drive(0, 0, 0, True)

        if interrupted:
            self.current_goal = 0
            self.sampled_trajectory = []


# This is the final command that should be used in the robot code
class FollowPath(FollowPathWithDriveToPoses):
    pass


# Alternative
# class FollowPath(FollowPathCustom):
#     pass
