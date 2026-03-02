from pathplannerlib.path import (
    PathPlannerPath,
    PathConstraints,
    IdealStartingState,
    GoalEndState,
)
from pathplannerlib.util import FlippingUtil
from wpimath.geometry import Pose2d, Rotation2d
from wpimath.units import degreesToRadians

"""
Tower constants
"""
FlippingUtil.symmetryType = FlippingUtil.symmetryType.kRotational
_constraints_for_tower = PathConstraints(
    maxVelocityMps=1.0,
    maxAccelerationMpsSq=1.0,
    maxAngularVelocityRps=degreesToRadians(10.0),
    maxAngularAccelerationRpsSq=degreesToRadians(10.0),
)

_tower_position_left = 4.675
_tower_position_right = 2.825

_tower_distance_from_for_first_pose = 0.30
_tower_initial_velocity = 0.0

_tower_ideal_starting_state_left = IdealStartingState(
    velocity=_tower_initial_velocity, rotation=Rotation2d.fromDegrees(90.0)
)
_tower_ideal_starting_state_right = IdealStartingState(
    velocity=_tower_initial_velocity, rotation=Rotation2d.fromDegrees(-90.0)
)
_tower_ideal_ending_state_left = GoalEndState(
    velocity=0.0, rotation=Rotation2d.fromDegrees(90.0)
)
_tower_ideal_ending_state_right = GoalEndState(
    velocity=0.0, rotation=Rotation2d.fromDegrees(-90.0)
)

"""
Tower Waypoints
"""
_to_tower_ready_left_waypoints = PathPlannerPath.waypointsFromPoses(
    [
        Pose2d(
            1.070,
            (_tower_position_left + _tower_distance_from_for_first_pose),
            Rotation2d.fromDegrees(-90.0),
        ),
        Pose2d(1.070, _tower_position_left, Rotation2d.fromDegrees(-90.0)),
    ]
)

_to_tower_ready_right_waypoints = PathPlannerPath.waypointsFromPoses(
    [
        Pose2d(
            1.070,
            (_tower_position_right - _tower_distance_from_for_first_pose),
            Rotation2d.fromDegrees(90.0),
        ),
        Pose2d(1.070, _tower_position_right, Rotation2d.fromDegrees(90.0)),
    ]
)

"""
Tower Paths
"""
to_tower_ready_left_path = PathPlannerPath(
    waypoints=_to_tower_ready_left_waypoints,
    constraints=_constraints_for_tower,
    ideal_starting_state=_tower_ideal_starting_state_left,
    goal_end_state=_tower_ideal_ending_state_left,
)
to_tower_ready_right_path = PathPlannerPath(
    waypoints=_to_tower_ready_right_waypoints,
    constraints=_constraints_for_tower,
    ideal_starting_state=_tower_ideal_starting_state_right,
    goal_end_state=_tower_ideal_ending_state_right,
)
