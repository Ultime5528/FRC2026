import math

from wpimath.geometry import Pose2d, Translation2d, Rotation2d, Translation3d
from wpimath.


def computeRobotRotationToAlign(
    robot_pose2d: Pose2d,
    shooter_offset: Translation2d,
    shooter_extremity: Translation2d,
    hubpose: Pose2d,
) -> Rotation2d:

    delta_hub_and_bot = hubpose.translation() - robot_pose2d.translation()
    hub_at_origin = delta_hub_and_bot.rotateBy(-robot_pose2d.rotation())
    shooter_direction = shooter_extremity - shooter_offset

    A = shooter_direction.cross(hub_at_origin)
    B = shooter_direction.dot(hub_at_origin)
    C = shooter_offset.cross(shooter_extremity)

    denom = (A**2) + (B**2)

    # to avoid domain errors
    if abs(C / denom) > 1 or denom == 0:
        return Rotation2d()
    else:
        return Rotation2d(math.atan2(-B, -A) + math.acos(C / denom))

def computeShooterSpeedToShoot(
    robot_pose: Translation3d,
    target_pose: Translation3d,
    shooter_angle: float
) -> float:
    numerator
