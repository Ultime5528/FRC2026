import math

from wpilib import DriverStation
from wpimath.geometry import Translation3d, Pose3d, Rotation3d, Transform3d


from commands.guide import MoveGuide
from modules import hardware
from subsystems.drivetrain import Drivetrain
from subsystems.guide import Guide
from ultime.autoproperty import autoproperty
from ultime.linearinterpolator import LinearInterpolator
from ultime.module import Module


def normalizeAngleRadians(angle: float) -> float:
    angle_normalized = angle % math.tau
    if angle_normalized >= math.pi:
        angle_normalized -= math.tau
    return angle_normalized


def computeAngleDifferenceRadians(angle1: float, angle2: float) -> float:
    return normalizeAngleRadians(angle1 - angle2)


def computeRobotRotationToAlignSimple(
    shooter_pose3d: Pose3d,
    target: Translation3d,
) -> float:
    shooter_to_target = (target - shooter_pose3d.translation()).toTranslation2d()
    shooter_to_target_angle = shooter_to_target.angle().radians()
    shooter_angle = shooter_pose3d.rotation().angle
    return computeAngleDifferenceRadians(shooter_to_target_angle, shooter_angle)


def computeRobotRotationToAlign(
    robot_pose3d: Pose3d,
    shooter_offset_origin: Translation3d,
    shooter_extremity_origin: Translation3d,
    target: Translation3d,
) -> float:

    robot_to_target = target - robot_pose3d.translation()
    target_at_origin = robot_to_target.rotateBy(-robot_pose3d.rotation())
    shooter_direction = shooter_extremity_origin - shooter_offset_origin

    A = -(
        shooter_direction.x * target_at_origin.y
        - shooter_direction.y * target_at_origin.x
    )
    B = -(
        shooter_direction.x * target_at_origin.x
        + shooter_direction.y * target_at_origin.y
    )
    C = (
        shooter_offset_origin.x * shooter_extremity_origin.y
        - shooter_offset_origin.y * shooter_extremity_origin.x
    )

    denominator = math.sqrt((A**2) + (B**2))

    # to avoid domain errors
    if abs(denominator) < 1.0e-6:
        return 0.0
    elif abs(C / denominator) > 1.0:
        return 0.0
    else:
        return normalizeAngleRadians(-(math.atan2(B, A) + math.acos(C / denominator)))


def computeShooterSpeedToShoot(
    shooter_position: Translation3d,
    target_position: Translation3d,
    long_shoot_zone: float,
) -> float:

    if shouldUseGuide(shooter_position, target_position, long_shoot_zone):
        shooter_angle = math.radians(60.0)
    else:
        shooter_angle = math.radians(70.0)

    gravity = 9.80665

    shooter_to_target = target_position - shooter_position
    distance_xy = math.hypot(shooter_to_target.x, shooter_to_target.y)

    distance_xy_squared = distance_xy**2

    numerator = gravity * distance_xy_squared
    denominator = (2 * ((math.cos(shooter_angle)) ** 2)) * (
        distance_xy * (math.tan(shooter_angle)) - shooter_to_target.z
    )

    if abs(denominator) < 1.0e-6:
        return 0.0

    speed_squared = numerator / denominator

    if speed_squared < 0.0:
        return 0.0

    return math.sqrt(speed_squared)


def shouldUseGuide(
    shooter_postiion: Translation3d, target: Translation3d, long_shoot_zone: float
) -> bool:
    return (
        target.toTranslation2d().distance(shooter_postiion.toTranslation2d())
        >= long_shoot_zone
    )


def computeShooterPosition(
    robot_pose: Pose3d, shooter_offset: Transform3d
) -> Translation3d:
    return robot_pose.transformBy(shooter_offset).translation()


class ShooterCalcModule(Module):
    long_zone = autoproperty(6.0)
    red_hub = Translation3d(11.915394, 4.034536, 1.510284)
    blue_hub = Translation3d(4.625594, 4.034536, 1.510284)
    shooter_offset = Transform3d(-0.1525, -0.271, 0.5, Rotation3d())
    shooter_extremity = Translation3d(0.1525, -0.271, 0.5)
    speed_guide_open = autoproperty([4.0, 6.0, 7.0, 9.5, 11.0, 14.0])
    rpm_guide_open = autoproperty([501.24, 751.86, 877.17, 1190.445, 1378.41, 1754.34])
    speed_guide_closed = autoproperty([3.5, 5.0, 5.5, 7.0, 9.0, 11.5])
    rpm_guide_closed = autoproperty(
        [501.24, 751.86, 877.17, 1190.445, 1378.41, 1754.34]
    )

    def __init__(
        self,
        drivetrain: Drivetrain,
        guide: Guide,
    ):
        super().__init__()
        self._drivetrain = drivetrain
        self.guide = guide
        self.guide_usage = None
        self._interpolator_for_open_guide = LinearInterpolator(
            self.speed_guide_open, self.rpm_guide_open
        )
        self._interpolator_for_closed_guide = LinearInterpolator(
            self.speed_guide_closed, self.rpm_guide_closed
        )

    def robotPeriodic(self) -> None:
        current_usage = self.shouldUseGuide()

        if self.guide_usage is not None:
            if current_usage != self.guide_usage:
                if current_usage:
                    MoveGuide.toUsed(self.guide).schedule()
                else:
                    MoveGuide.toUnused(self.guide).schedule()

        self.guide_usage = current_usage

    def _getShooterPose(self) -> Translation3d:
        shooter_pose = computeShooterPosition(
            Pose3d(self._drivetrain.getPose()), self.shooter_offset
        )
        return shooter_pose

    def _getTargetPosition(self) -> Translation3d:
        if self._isInOurZone():
            return self._getHubPosition()
        else:
            return self._getZonePosition()

    def _getHubPosition(self) -> Translation3d:
        if DriverStation.getAlliance() == DriverStation.Alliance.kRed:
            return self.red_hub
        else:
            return self.blue_hub

    def _getZonePosition(self) -> Translation3d:

        if self._drivetrain.getPose().y < 4.034663:
            y = 2.0173315
        else:
            y = 6.0519945

        if DriverStation.getAlliance() == DriverStation.Alliance.kRed:
            x = 14.228191
        else:
            x = 2.312797

        return Translation3d(x, y, 0.0)

    def _isInOurZone(self) -> bool:
        if DriverStation.getAlliance() == DriverStation.Alliance.kRed:
            return self._drivetrain.getPose().x > 11.915394
        else:
            return self._drivetrain.getPose().x < 4.625594

    def getAngleToAlignWithTarget(self) -> float:
        return computeRobotRotationToAlign(
            Pose3d(self._drivetrain.getPose()),
            self.shooter_offset.translation(),
            self.shooter_extremity,
            self._getTargetPosition(),
        )

    def getAngleToAlignWithTargetSimple(self) -> float:
        return computeRobotRotationToAlignSimple(
            Pose3d(self._getShooterPose(), self.shooter_offset.rotation()),
            self._getTargetPosition(),
        )

    def shouldUseGuide(self) -> bool:
        return shouldUseGuide(
            self._getShooterPose(),
            self._getTargetPosition(),
            self.long_zone,
        )

    def getRPM(self) -> float:
        if self.shouldUseGuide():
            return self._interpolator_for_closed_guide.interpolate(self.getSpeedRaw())
        else:
            return self._interpolator_for_open_guide.interpolate(self.getSpeedRaw())

    def getSpeedRaw(self) -> float:
        return computeShooterSpeedToShoot(
            self._getShooterPose(), self._getTargetPosition(), self.long_zone
        )
