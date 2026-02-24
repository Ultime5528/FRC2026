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
    hub_position: Translation3d,
) -> float:
    shooter_to_hub = (hub_position - shooter_pose3d.translation()).toTranslation2d()
    shooter_to_hub_angle = shooter_to_hub.angle().radians()
    shooter_angle = shooter_pose3d.rotation().angle
    return computeAngleDifferenceRadians(shooter_to_hub_angle, shooter_angle)


def computeRobotRotationToAlign(
    robot_pose3d: Pose3d,
    shooter_offset_origin: Translation3d,
    shooter_extremity_origin: Translation3d,
    hub_pose: Translation3d,
) -> float:

    delta_hub_and_bot = hub_pose - robot_pose3d.translation()
    hub_at_origin = delta_hub_and_bot.rotateBy(-robot_pose3d.rotation())
    shooter_direction = shooter_extremity_origin - shooter_offset_origin

    A = -(shooter_direction.x * hub_at_origin.y - shooter_direction.y * hub_at_origin.x)
    B = -(shooter_direction.x * hub_at_origin.x + shooter_direction.y * hub_at_origin.y)
    C = (
        shooter_offset_origin.x * shooter_extremity_origin.y
        - shooter_offset_origin.y * shooter_extremity_origin.x
    )

    denominator = math.sqrt((A**2) + (B**2))

    # to avoid domain errors
    if abs(C / denominator) > 1 or denominator == 0:
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

    distance_shooter_xy = math.hypot(shooter_position.x, shooter_position.y)
    distance_target_xy = math.hypot(target_position.x, target_position.y)
    delta_xy = distance_target_xy - distance_shooter_xy
    delta_z = target_position.z - shooter_position.z

    distance_xy_squared = delta_xy**2

    numerator = gravity * distance_xy_squared
    denominator = (2 * ((math.cos(shooter_angle)) ** 2)) * (
        delta_xy * (math.tan(shooter_angle)) - delta_z
    )

    if denominator == 0.0:
        return -1.0
    else:
        return math.sqrt(numerator / denominator)


def shouldUseGuide(
    robot_pose: Translation3d, target_pose: Translation3d, long_shoot_zone: float
) -> bool:
    if (
        target_pose.toTranslation2d().distance(robot_pose.toTranslation2d())
        >= long_shoot_zone
    ):
        return True
    else:
        return False


def computeShooterPosition(
    robot_pose: Pose3d, shooter_offset: Transform3d
) -> Translation3d:
    return robot_pose.transformBy(shooter_offset).translation()


class ShooterCalcModule(Module):
    long_zone = autoproperty(6.0)
    red_hub = Translation3d(4.625594, 4.034536, 3.057144)
    blue_hub = Translation3d(11.915394, 4.034536, 3.057144)
    shooter_offset = Transform3d(
        -0.1525, -0.271, 0.5, Rotation3d(Translation3d(0, 0, 1), 0)
    )
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
        self._interpolator_for_open_guide = LinearInterpolator(
            self.speed_guide_open, self.rpm_guide_open
        )
        self._interpolator_for_closed_guide = LinearInterpolator(
            self.speed_guide_closed, self.rpm_guide_closed
        )

    def robotPeriodic(self) -> None:
        if self.shouldUseGuide():
            MoveGuide.toUsed(self.guide)
        else:
            MoveGuide.toUnused(self.guide)

    def _getShooterPose(self) -> Translation3d:
        shooter_pose = computeShooterPosition(
            Pose3d(self._drivetrain.getPose()), self.shooter_offset
        )
        return shooter_pose

    def _getHubPosition(self) -> Translation3d:
        if DriverStation.getAlliance() == DriverStation.Alliance.kRed:
            return self.red_hub
        else:
            return self.blue_hub

    def getAngleToAlignWithTarget(self) -> float:
        return computeRobotRotationToAlign(
            Pose3d(self._drivetrain.getPose()),
            self.shooter_offset.translation(),
            self.shooter_extremity,
            self._getHubPosition(),
        )

    def getAngleToAlignWithTargetSimple(self) -> float:
        return computeRobotRotationToAlignSimple(
            Pose3d(self._getShooterPose(), self.shooter_offset.rotation()),
            self._getHubPosition(),
        )

    def shouldUseGuide(self) -> bool:
        return shouldUseGuide(
            self._getShooterPose(),
            self._getHubPosition(),
            self.long_zone,
        )

    def getRPM(self) -> float:
        if self.shouldUseGuide():
            return self._interpolator_for_open_guide.interpolate(self.getRPMRaw())
        else:
            return self._interpolator_for_closed_guide.interpolate(self.getRPMRaw())

    def getRPMRaw(self) -> float:
        return computeShooterSpeedToShoot(
            self._getShooterPose(), self._getHubPosition(), self.long_zone
        )
