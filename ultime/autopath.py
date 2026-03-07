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
    maxVelocityMps=0.4,
    maxAccelerationMpsSq=2.0,
    maxAngularVelocityRps=degreesToRadians(10.0),
    maxAngularAccelerationRpsSq=degreesToRadians(10.0),
)

_tower_y_left = 4.595
_tower_y_right = 2.987
_tower_x = 1.021
_tower_y_threshold = 0.2

_tower_distance_from_for_first_pose = 0.45
_tower_initial_velocity = 0.4


"""
Tower States
"""
_tower_ideal_starting_state_left = IdealStartingState(
    velocity=_tower_initial_velocity, rotation=Rotation2d.fromDegrees(90.0)
)
_tower_ideal_starting_state_right = IdealStartingState(
    velocity=_tower_initial_velocity, rotation=Rotation2d.fromDegrees(-90.0)
)
_tower_ideal_ending_state_left = GoalEndState(
    velocity=0.5, rotation=Rotation2d.fromDegrees(90.0)
)
_tower_ideal_ending_state_right = GoalEndState(
    velocity=0.5, rotation=Rotation2d.fromDegrees(-90.0)
)

"""
Tower Waypoints
"""
_to_tower_ready_left_waypoints = PathPlannerPath.waypointsFromPoses(
    [
        Pose2d(
            _tower_x,
            (_tower_y_left + _tower_distance_from_for_first_pose),
            Rotation2d.fromDegrees(-90.0),
        ),
        Pose2d(_tower_x, (_tower_y_left + _tower_y_threshold), Rotation2d.fromDegrees(-90.0)),
    ]
)

_to_tower_ready_right_waypoints = PathPlannerPath.waypointsFromPoses(
    [
        Pose2d(
            _tower_x,
            (_tower_y_right - _tower_distance_from_for_first_pose),
            Rotation2d.fromDegrees(90.0),
        ),
        Pose2d(_tower_x, (_tower_y_right - _tower_y_threshold), Rotation2d.fromDegrees(90.0)),
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
