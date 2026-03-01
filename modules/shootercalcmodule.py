import math

from wpilib import DriverStation
from wpimath.geometry import Translation3d, Pose3d, Rotation3d, Transform3d, Pose2d

from commands.guide import MoveGuide
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
    shooter_angle: float,
) -> float:

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


def computeShooterPose(robot_pose: Pose3d, shooter_offset: Transform3d) -> Pose3d:
    return robot_pose.transformBy(shooter_offset)


class ShooterCalcModule(Module):
    long_distance_treshold = autoproperty(6.0)
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

        self.last_robot_pose = Pose2d()
        self.last_shooter_pose = Pose3d()
        self.last_angle_computed = self.createProperty(0.0)
        self.last_angle_simple_computed = self.createProperty(0.0)
        self.last_should_use_guide_computed = self.createProperty(False)
        self.last_rpm_computed = self.createProperty(0.0)
        self.last_speed_computed = self.createProperty(0.0)

    def robotPeriodic(self) -> None:
        current_usage = self.shouldUseGuide()

        if self.guide_usage is not None:
            if current_usage != self.guide_usage:
                if current_usage:
                    MoveGuide.toUsed(self.guide).schedule()
                else:
                    MoveGuide.toUnused(self.guide).schedule()

        self.guide_usage = current_usage

    def _getShooterPose(self) -> Pose3d:
        self.last_robot_pose = self._drivetrain.getPose()
        self.last_shooter_pose = computeShooterPose(
            Pose3d(self.last_robot_pose), self.shooter_offset
        )

        # logging Pose2d and Pose3d not supprted. Add support?
        #self.log("last_robot_pose", self.last_robot_pose)
        #self.log("last_shooter_pose", self.last_shooter_pose)

        return self.last_shooter_pose

    def _getTargetPosition(self) -> Translation3d:
        if self._isInOurZone():
            self.last_target_computed = self._getHubPosition()
        else:
            self.last_target_computed = self._getZonePosition()

        return self.last_target_computed

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
            self.last_is_in_our_zone_computed = self._drivetrain.getPose().x > 11.915394
        else:
            self.last_is_in_our_zone_computed = self._drivetrain.getPose().x < 4.625594

        return self.last_is_in_our_zone_computed

    def getAngleToAlignWithTarget(self) -> float:
        self.last_angle_computed = computeRobotRotationToAlign(
            Pose3d(self._drivetrain.getPose()),
            self.shooter_offset.translation(),
            self.shooter_extremity,
            self._getTargetPosition(),
        )
        return self.last_angle_computed

    def getAngleToAlignWithTargetSimple(self) -> float:
        self.last_angle_simple_computed = computeRobotRotationToAlignSimple(
            self._getShooterPose(),
            self._getTargetPosition(),
        )

        return self.last_angle_simple_computed

    def shouldUseGuide(self) -> bool:
        shooter_postion_xy = self._getShooterPose().translation().toTranslation2d()
        target_positon_xy = self._getTargetPosition().toTranslation2d()

        self.last_should_use_guide_computed = (
            shooter_postion_xy.distance(shooter_postion_xy)
            >= self.long_distance_treshold
        )

        return self.last_should_use_guide_computed

    def getRPM(self) -> float:
        if self.shouldUseGuide():
            self.last_rpm_computed = self._interpolator_for_closed_guide.interpolate(
                self.getSpeedRaw()
            )
        else:
            self.last_rpm_computed = self._interpolator_for_open_guide.interpolate(
                self.getSpeedRaw()
            )

        return self.last_rpm_computed

    def getSpeedRaw(self) -> float:

        shooter_angle = math.radians(70.0)

        if self.shouldUseGuide():
            shooter_angle = math.radians(60.0)

        self.last_speed_computed = computeShooterSpeedToShoot(
            self._getShooterPose().translation(),
            self._getTargetPosition(),
            shooter_angle,
        )

        return self.last_speed_computed
