import math

from wpilib import DriverStation
from wpimath import units
from wpimath.geometry import Rotation2d, Translation3d, Pose3d, Rotation3d, Transform3d

from subsystems.drivetrain import Drivetrain
from ultime.autoproperty import autoproperty
from ultime.linearinterpolator import LinearInterpolator
from ultime.module import Module

red_hub = Translation3d(4.625594, 4.034536, 3.057144)
blue_hub = Translation3d(11.915394, 4.034536, 3.057144)


def computeRobotRotationToAlign(
    robot_pose3d: Pose3d,
    shooter_offset: Transform3d,
    hub_pose: Translation3d,
) -> Rotation2d:

    shooter_extremity = Translation3d(
        (math.cos(shooter_offset.rotation().y) + shooter_offset.translation().x),
        (math.sin(shooter_offset.rotation().y) + shooter_offset.translation().y),
        2,
    )

    delta_hub_and_bot = hub_pose - robot_pose3d.translation()
    hub_at_origin = delta_hub_and_bot.rotateBy(-robot_pose3d.rotation())
    shooter_direction = shooter_extremity - shooter_offset.translation()

    A = shooter_direction.cross(hub_at_origin)
    B = shooter_direction.dot(hub_at_origin)
    C = shooter_offset.translation().cross(shooter_extremity)

    denominator = (A**2) + (B**2)

    # to avoid domain errors
    if abs(C / denominator) > 1 or denominator == 0:
        return Rotation2d()
    else:
        return robot_pose3d.toPose2d().rotation() + Rotation2d(
            math.atan2(-B, -A) + math.acos(C / denominator)
        )


def computeShooterSpeedToShoot(
    shooter_position: Translation3d,
    target_position: Translation3d,
    long_shoot_zone: float,
) -> float:

    if target_position.distance(shooter_position) >= long_shoot_zone:
        shooter_angle = math.radians(60.0)
    else:
        shooter_angle = math.radians(70.0)

    gravity = float(units.standard_gravity)

    delta_x = target_position.x - shooter_position.x
    delta_y = target_position.y - shooter_position.y
    delta_z = target_position.z - target_position.z

    distance_xy = math.hypot(delta_x, delta_y)

    distance_xy_squared = distance_xy**2

    numerator = gravity * distance_xy_squared
    denominator = (2 * (math.cos(shooter_angle)) ** 2) * (
        distance_xy * (math.cos(shooter_angle)) - delta_z
    )

    if denominator == 0.0:
        return -1.0
    else:
        return numerator / denominator


def shouldUseGuide(
    robot_pose: Translation3d, target_pose: Translation3d, long_shoot_zone: float
) -> bool:
    if target_pose.distance(robot_pose) >= long_shoot_zone:
        return True
    else:
        return False


def computeShooterPosition(
    robot_pose: Pose3d, shooter_pose: Transform3d
) -> Translation3d:
    return (robot_pose.transformBy(shooter_pose)).translation()


class ShooterCalcModule(Module):
    long_zone = autoproperty(6.0)
    red_hub = Translation3d(4.625594, 4.034536, 3.057144)
    blue_hub = Translation3d(11.915394, 4.034536, 3.057144)
    shooter_offset = Transform3d(-0.6, -0.5, 0.0, Rotation3d(0, 180, 0))
    speed_guide_open = autoproperty([4.0, 6.0, 7.0, 9.5, 11.0, 14.0])
    rpm_guide_open = autoproperty([501.24, 751.86, 877.17, 1190.445, 1378.41, 1754.34])
    speed_guide_closed = autoproperty([3.5, 5.0, 5.5, 7.0, 9.0, 11.5])
    rpm_guide_closed = autoproperty(
        [501.24, 751.86, 877.17, 1190.445, 1378.41, 1754.34]
    )

    def __init__(
        self,
        drivetrain: Drivetrain,
    ):
        super().__init__()
        self._drivetrain = drivetrain
        self._interpolator_for_open_guide = LinearInterpolator(
            self.speed_guide_open, self.rpm_guide_open
        )
        self._interpolator_for_closed_guide = LinearInterpolator(
            self.speed_guide_closed, self.rpm_guide_closed
        )

    def _getShooterPose(self) -> Translation3d:
        return computeShooterPosition(self._drivetrain.getPose(), self.shooter_offset)

    def _getTargetPose(self) -> Translation3d:
        if DriverStation.getAlliance() == DriverStation.Alliance.kRed:
            return self.red_hub
        else:
            return self.blue_hub

    def _getAngleToAlignWithTarget(self) -> Rotation2d:
        return computeRobotRotationToAlign(
            self._drivetrain.getPose(),
            self.shooter_offset,
            self._getTargetPose(),
        )

    def shouldUseGuide(self) -> bool:
        return shouldUseGuide(
            self._drivetrain.getPose().translation(),
            self._getTargetPose(),
            self.long_zone,
        )

    def getRPM(self) -> float:
        if self.shouldUseGuide():
            return self._interpolator_for_open_guide.interpolate(
                computeShooterSpeedToShoot(
                    self._getShooterPose(), self._getTargetPose(), self.long_zone
                )
            )
        else:
            return self._interpolator_for_closed_guide.interpolate(
                computeShooterSpeedToShoot(
                    self._getShooterPose(), self._getTargetPose(), self.long_zone
                )
            )
