import math

from wpimath.geometry import Pose2d, Translation2d, Rotation2d, Translation3d
from wpimath import units


def computeRobotRotationToAlign(
    robot_pose2d: Pose2d,
    shooter_offset: Translation2d,
    shooter_extremity: Translation2d,
    hub_pose: Pose2d,
) -> Rotation2d:

    delta_hub_and_bot = hub_pose.translation() - robot_pose2d.translation()
    hub_at_origin = delta_hub_and_bot.rotateBy(-robot_pose2d.rotation())
    shooter_direction = shooter_extremity - shooter_offset

    A = shooter_direction.cross(hub_at_origin)
    B = shooter_direction.dot(hub_at_origin)
    C = shooter_offset.cross(shooter_extremity)

    denominator = (A**2) + (B**2)

    # to avoid domain errors
    if abs(C / denominator) > 1 or denominator == 0:
        return Rotation2d()
    else:
        return Rotation2d(math.atan2(-B, -A) + math.acos(C / denominator))


def computeShooterSpeedToShoot(
    robot_pose: Translation3d, target_pose: Translation3d, shooter_angle: float
) -> float:

    gravity = float(units.standard_gravity)

    delta_x = target_pose.x - robot_pose.x
    delta_y = target_pose.y - robot_pose.y

    numerator = gravity * (delta_x**2)
    denominator = (2 * (math.cos(shooter_angle)) ** 2) * (
        delta_x * (math.cos(shooter_angle)) - delta_y
    )

    if denominator == 0:
        return -1
    else:
        return numerator / denominator
