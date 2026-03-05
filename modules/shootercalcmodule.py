import math

from wpilib import DriverStation
from wpimath.geometry import (
    Translation3d,
    Pose3d,
    Rotation3d,
    Transform3d,
    Pose2d,
    Rotation2d,
)

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


def computeRobotRotationToAlign(
    shooter_pose3d: Pose3d,
    target: Translation3d,
) -> Rotation2d:
    shooter_to_target = (target - shooter_pose3d.translation()).toTranslation2d()
    shooter_to_target_angle = shooter_to_target.angle().radians()
    shooter_angle = shooter_pose3d.rotation().z
    angle_rad = computeAngleDifferenceRadians(shooter_to_target_angle, shooter_angle)
    return Rotation2d(angle_rad)


def computeRobotRotationToAlignExact(
    robot_pose3d: Pose3d,
    shooter_offset_origin: Translation3d,
    shooter_extremity_origin: Translation3d,
    target: Translation3d,
) -> Rotation2d:

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

    angle_rad = 0.0

    # to avoid domain errors
    if abs(denominator) >= 1.0e-6 and abs(C / denominator) <= 1.0:
        angle_rad = normalizeAngleRadians(
            -(math.atan2(B, A) + math.acos(C / denominator))
        )

    return Rotation2d(angle_rad)


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
    long_distance_treshold = autoproperty(2.5)
    red_hub = Translation3d(11.915394, 4.034536, 1.510284)
    blue_hub = Translation3d(4.625594, 4.034536, 1.510284)
    shooter_offset = Transform3d(-0.14, 0.245, 0.5, Rotation3d.fromDegrees(0, 0, -3.0))
    speed_guide_open = autoproperty([5.45, 6.3, 6.67, 6.8, 7.2])
    rpm_guide_open = autoproperty([2500.0, 2750.0, 2900.0, 3350.0, 3800.0])
    speed_guide_closed = autoproperty([6.1, 6.48, 6.8, 7.2, 7.7, 8.0, 8.3, 8.4])
    rpm_guide_closed = autoproperty(
        [2600.0, 2850.0, 3050.0, 3225.0, 3550.0, 4050.0, 4500.0, 4700.0]
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

        self._shooter_rpm = 0.0
        self._robot_rotation_angle = Rotation2d()

        self._is_on_red_team = False
        self.team_hub_position = self.red_hub

        self._robot_pose = Pose2d()
        self._shooter_pose = Pose3d()
        self._target_position = Translation3d()
        self._is_in_our_zone = False
        self._should_use_guide = False
        self._projectile_angle = 0.0
        self._projectile_speed = 0.0
        self.distance_xy = 0.0

    def getRotationToAlignWithTarget(self) -> Rotation2d:
        return self._robot_rotation_angle

    def computeRotationToAlignWithTargetExact(self) -> Rotation2d:

        shooter_extremity = (
            Translation3d(0.5, 0.0, 0.0).rotateBy(self.shooter_offset.rotation())
            + self.shooter_offset.translation()
        )

        return computeRobotRotationToAlignExact(
            Pose3d(self._robot_pose),
            self.shooter_offset.translation(),
            shooter_extremity,
            self._target_position,
        )

    def getRPM(self) -> float:
        return self._shooter_rpm

    def getProjectileSpeed(self) -> float:
        return self._projectile_speed

    def shouldUseGuide(self) -> bool:
        return self._should_use_guide

    def robotPeriodic(self) -> None:
        self._is_on_red_team = (
            DriverStation.getAlliance() == DriverStation.Alliance.kRed
        )
        if self._is_on_red_team:
            self.team_hub_position = self.red_hub
        else:
            self.team_hub_position = self.blue_hub

        self._computeRobotPoseAndShooterPose()
        self._computeIsInOurZone()
        self._computeTargetPosition()

        self._computeShouldUseGuide()

        # TODO Uninitialized case

        self._computeShooterExitAngle()
        self._computeProjectileSpeed()
        self._computeShooterRPM()
        self._computeAngleToAlignWithTarget()

    def _computeRobotPoseAndShooterPose(self) -> None:
        self._robot_pose = self._drivetrain.getPose()
        self._shooter_pose = computeShooterPose(
            Pose3d(self._robot_pose), self.shooter_offset
        )

    def _computeIsInOurZone(self) -> None:
        if self._is_on_red_team:
            self._is_in_our_zone = self._drivetrain.getPose().x > 11.915394
        else:
            self._is_in_our_zone = self._drivetrain.getPose().x < 4.625594

    def _computeTargetPosition(self) -> None:
        if self._is_in_our_zone:
            self._target_position = self.team_hub_position
        else:
            self._target_position = self._getZonePosition()

    def _getZonePosition(self) -> Translation3d:
        if self._robot_pose.y < 4.034663:
            y = 2.0173315
        else:
            y = 6.0519945

        if self._is_on_red_team:
            x = 14.228191
        else:
            x = 2.312797

        return Translation3d(x, y, 0.0)

    def _computeShouldUseGuide(self) -> None:
        shooter_postion_xy = self._shooter_pose.translation().toTranslation2d()
        target_positon_xy = self._target_position.toTranslation2d()

        self._should_use_guide = (
            target_positon_xy.distance(shooter_postion_xy)
            >= self.long_distance_treshold
        )

    def _computeShooterExitAngle(self) -> None:
        if self._should_use_guide:
            self._projectile_angle = math.radians(60.0)
        else:
            self._projectile_angle = math.radians(70.0)

    def _computeProjectileSpeed(self) -> None:
        gravity = 9.80665

        shooter_to_target = self._target_position - self._shooter_pose.translation()
        self.distance_xy = math.hypot(shooter_to_target.x, shooter_to_target.y)

        distance_xy_squared = self.distance_xy**2

        numerator = gravity * distance_xy_squared
        denominator = (2 * ((math.cos(self._projectile_angle)) ** 2)) * (
            self.distance_xy * (math.tan(self._projectile_angle)) - shooter_to_target.z
        )

        if abs(denominator) < 1.0e-6:
            self._projectile_speed = 0.0
            return

        speed_squared = numerator / denominator

        if speed_squared < 0.0:
            self._projectile_speed = 0.0
            return

        self._projectile_speed = math.sqrt(speed_squared)

    def _computeShooterRPM(self) -> None:
        if self._should_use_guide:
            self._interpolator_for_closed_guide.setPointsX(self.speed_guide_closed)
            self._interpolator_for_closed_guide.setPointsY(self.rpm_guide_closed)
            self._shooter_rpm = self._interpolator_for_closed_guide.interpolate(
                self._projectile_speed
            )
        else:
            self._interpolator_for_open_guide.setPointsX(self.speed_guide_open)
            self._interpolator_for_open_guide.setPointsY(self.rpm_guide_open)
            self._shooter_rpm = self._interpolator_for_open_guide.interpolate(
                self._projectile_speed
            )

    def _computeAngleToAlignWithTarget(self) -> None:
        self._robot_rotation_angle = computeRobotRotationToAlign(
            self._shooter_pose, self._target_position
        )

    def logValues(self):
        # logging Pose2d and Pose3d not supprted. Add support?
        robot_position = self._robot_pose.translation()
        self.log("robot_position_x", robot_position.x)
        self.log("robot_position_y", robot_position.y)
        self.log("target_position_x", self._target_position.x)
        self.log("target_position_y", self._target_position.y)
        self.log("is_in_our_zone", self._is_in_our_zone)
        self.log("should_use_guide", self._should_use_guide)
        self.log("shooter_exit_angle", self._projectile_angle)
        self.log("projectile_speed", self._projectile_speed)
        self.log("_robot_rotation_angle", self._robot_rotation_angle.degrees())
        self.log("target_distance_xy", self.distance_xy)
