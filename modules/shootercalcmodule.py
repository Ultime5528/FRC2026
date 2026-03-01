import math

from wpilib import DriverStation
from wpimath.geometry import Translation3d, Pose3d, Rotation3d, Transform3d, Pose2d, Rotation2d

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
) -> Rotation2d:
    shooter_to_target = (target - shooter_pose3d.translation()).toTranslation2d()
    shooter_to_target_angle = shooter_to_target.angle().radians()
    shooter_angle = shooter_pose3d.rotation().angle
    angle_rad = computeAngleDifferenceRadians(shooter_to_target_angle, shooter_angle)
    return Rotation2d(angle_rad)


def computeRobotRotationToAlign(
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
        angle_rad = normalizeAngleRadians(-(math.atan2(B, A) + math.acos(C / denominator)))

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
        self._interpolator_for_open_guide = LinearInterpolator(
            self.speed_guide_open, self.rpm_guide_open
        )
        self._interpolator_for_closed_guide = LinearInterpolator(
            self.speed_guide_closed, self.rpm_guide_closed
        )

        self._shooter_rpm = 0.0
        self._robot_rotation_angle = Rotation2d()
        self._robot_rotation_angle_simple = Rotation2d()

        self._is_on_red_team = (
            DriverStation.getAlliance() == DriverStation.Alliance.kRed
        )
        if self._is_on_red_team:
            self.team_hub_position = self.red_hub
        else:
            self.team_hub_position = self.blue_hub

        self._robot_pose = Pose2d()
        self._shooter_pose = Pose3d()
        self._target_position = Translation3d()
        self._is_in_our_zone = False
        self._should_use_guide = False
        self._projectile_angle = 0.0
        self._projectile_speed = 0.0

    def getRotationToAlignWithTarget(self) -> Rotation2d:
        return self._robot_rotation_angle

    def getRPM(self) -> float:
        return self._shooter_rpm

    def getProjectileSpeed(self) -> float:
        return self._projectile_speed

    def robotPeriodic(self) -> None:
        self._computeRobotPoseAndShooterPose()
        self._computeIsInOurZone()
        self._computeTargetPosition()

        previous_should_use_guide = self._should_use_guide
        self._computeShouldUseGuide()

        # Uninitialized case
        if self._should_use_guide != previous_should_use_guide:
            if self._should_use_guide:
                MoveGuide.toUsed(self.guide).schedule()
            else:
                MoveGuide.toUnused(self.guide).schedule()

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
        distance_xy = math.hypot(shooter_to_target.x, shooter_to_target.y)

        distance_xy_squared = distance_xy**2

        numerator = gravity * distance_xy_squared
        denominator = (2 * ((math.cos(self._projectile_angle)) ** 2)) * (
                distance_xy * (math.tan(self._projectile_angle)) - shooter_to_target.z
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
            self._shooter_rpm = self._interpolator_for_closed_guide.interpolate(
                self._projectile_speed
            )
        else:
            self._shooter_rpm = self._interpolator_for_open_guide.interpolate(
                self._projectile_speed
            )

    def _computeAngleToAlignWithTarget(self) -> None:
        self._robot_rotation_angle = computeRobotRotationToAlign(
            Pose3d(self._robot_pose),
            self.shooter_offset.translation(),
            self.shooter_extremity,
            self._target_position,
        )

    def _computeAngleToAlignWithTargetSimple(self) -> None:
        self._robot_rotation_angle_simple = computeRobotRotationToAlignSimple(
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
        self.log("_robot_rotation_angle_simple", self._robot_rotation_angle_simple.degrees())
