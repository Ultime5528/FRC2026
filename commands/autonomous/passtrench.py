from commands2 import Command
from pathplannerlib.path import (
    PathPlannerPath,
    IdealStartingState,
    GoalEndState,
    PathConstraints,
)
from pathplannerlib.util import FlippingUtil
from wpimath.geometry import Pose2d, Rotation2d, Translation2d
from wpimath.units import degreesToRadians

from subsystems.drivetrain import Drivetrain
from ultime.command import DeferredCommand
from ultime.field import mirrorPose

"""
Constants
"""
_constraints_for_trench = PathConstraints(
    maxVelocityMps=3.0,
    maxAccelerationMpsSq=3.0,
    maxAngularVelocityRps=degreesToRadians(10.0),
    maxAngularAccelerationRpsSq=degreesToRadians(10.0),
)

_trench_pose_middle_zone = Pose2d(Translation2d(5.200, 0.570), Rotation2d(0.0))
_trench_pose_alliance_zone = Pose2d(Translation2d(4.020, 0.570), Rotation2d(0.0))

"""
States
"""
_starting_state = IdealStartingState(velocity=3.0, rotation=Rotation2d(0.0))
_goal_end_state = GoalEndState(velocity=3.0, rotation=Rotation2d(0.0))

"""
Waypoints
"""
_trench_from_alliance_zone_to_middle_zone_waypoints = (
    PathPlannerPath.waypointsFromPoses(
        [
            Pose2d(_trench_pose_alliance_zone.translation(), Rotation2d(0.0)),
            Pose2d(_trench_pose_middle_zone.translation(), Rotation2d(0.0)),
        ]
    )
)

_trench_from_middle_zone_to_alliance_zone_waypoints = (
    PathPlannerPath.waypointsFromPoses(
        [
            Pose2d(_trench_pose_middle_zone.translation(), Rotation2d(180.0)),
            Pose2d(
                _trench_pose_alliance_zone.translation(), Rotation2d.fromDegrees(180.0)
            ),
        ]
    )
)

"""
Path
"""
_from_alliance_zone_to_middle_zone_path = PathPlannerPath.fromPathFile(
    "AllianceToMiddle"
)
_from_alliance_zone_to_middle_zone_path.preventFlipping = True

_from_middle_zone_to_alliance_zone_path = PathPlannerPath.fromPathFile(
    "MiddleToAlliance"
)
_from_middle_zone_to_alliance_zone_path.preventFlipping = True

"""
blue_right
blue_left
red_right
red_left
"""
all_trench_poses = [
    _trench_pose_alliance_zone,
    _trench_pose_middle_zone,
    mirrorPose(_trench_pose_alliance_zone),
    mirrorPose(_trench_pose_middle_zone),
    FlippingUtil.flipFieldPose(_trench_pose_alliance_zone),
    FlippingUtil.flipFieldPose(_trench_pose_middle_zone),
    FlippingUtil.flipFieldPose(mirrorPose(_trench_pose_alliance_zone)),
    FlippingUtil.flipFieldPose(mirrorPose(_trench_pose_middle_zone)),
]

all_trench_path = [
    _from_alliance_zone_to_middle_zone_path,
    _from_middle_zone_to_alliance_zone_path,
    _from_alliance_zone_to_middle_zone_path.mirrorPath(),
    _from_middle_zone_to_alliance_zone_path.mirrorPath(),
    _from_alliance_zone_to_middle_zone_path.flipPath(),
    _from_middle_zone_to_alliance_zone_path.flipPath(),
    _from_alliance_zone_to_middle_zone_path.mirrorPath().flipPath(),
    _from_middle_zone_to_alliance_zone_path.mirrorPath().flipPath(),
]


class PassTrench(DeferredCommand):
    def __init__(self, drivetrain: Drivetrain):
        super().__init__()
        self.drivetrain = drivetrain
        self.addRequirements(drivetrain)

    def createCommand(self) -> Command:
        current_pose = self.drivetrain.getPose()
        closest_pose = current_pose.nearest(all_trench_poses)
        index = all_trench_poses.index(closest_pose)
        path = all_trench_path[index]
        return self.drivetrain.getPathFindingFollowPathCommand(path)
