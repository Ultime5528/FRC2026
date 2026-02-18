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
    shooter_extremity: Translation3d,
    hub_pose: Translation3d,
) -> float:

    delta_hub_and_bot = hub_pose - robot_pose3d.translation()
    hub_at_origin = delta_hub_and_bot.rotateBy(-robot_pose3d.rotation())
    shooter_direction = shooter_extremity - shooter_offset.translation()

    A = shooter_direction.cross(hub_at_origin)
    B = shooter_direction.dot(hub_at_origin)
    C = shooter_offset.translation().cross(shooter_extremity)

    denominator = (A**2) + (B**2)

    # to avoid domain errors
    if abs(C / denominator) > 1 or denominator == 0:
        return 0.0
    else:
        return math.atan2(-B, -A) + math.acos(C / denominator)


def computeShooterSpeedToShoot(
    shooter_position: Translation3d,
    target_position: Translation3d,
    long_shoot_zone: float,
) -> float:

    if target_position.distance(shooter_position) >= long_shoot_zone:
        shooter_angle = 60.0*(math.pi/180)
    else:
        shooter_angle = 70.0*(math.pi/180)

    gravity = 9.80665

    distance_shooter_xy = math.hypot(shooter_position.x,shooter_position.y)
    distance_target_xy = math.hypot(target_position.x,target_position.y)
    delta_xy = distance_target_xy - distance_shooter_xy
    delta_z = target_position.z - shooter_position.z


    distance_xy_squared = delta_xy ** 2

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
    if target_pose.distance(robot_pose) >= long_shoot_zone:
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
    shooter_offset = Transform3d(-0.1525, -0.271, 0.5, Rotation3d(Translation3d(0,0,1),0))
    shooter_extremity = Transform3d(0.1525,-0.271,0.5,Rotation3d(Translation3d(0,0,1),0))
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

    def _getAngleToAlignWithTarget(self) -> float:
        return computeRobotRotationToAlign(
            self._drivetrain.getPose(),
            self.shooter_offset,
            self.shooter_extremity,
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
