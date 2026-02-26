import numpy
from _pytest.python_api import approx
from wpimath.geometry import Pose2d, Rotation2d
from wpimath.geometry import Pose3d, Rotation3d, Translation3d, Transform3d

from commands.drivetrain.resetpose import ResetPose
from modules.shootercalcmodule import (
    ShooterCalcModule,
    computeRobotRotationToAlign,
    computeRobotRotationToAlignSimple,
)
from robot import Robot
from ultime.tests import RobotTestController


def test_ShooterCalcModule(robot_controller: RobotTestController, robot: Robot):
    shooter_calc_module = ShooterCalcModule(
        robot.hardware.drivetrain, robot.hardware.guide
    )
    robot_controller.startTeleop()
    robot_controller.run_command(
        ResetPose(robot.hardware.drivetrain, Pose2d(2, 3, 0)), timeout=3.0
    )
    robot_controller.wait(0.2)
    angle = shooter_calc_module.getAngleToAlignWithTarget()
    angle_simple = shooter_calc_module.getAngleToAlignWithTargetSimple()
    robot_controller.run_command(
        ResetPose(
            robot.hardware.drivetrain,
            Pose2d(
                robot.hardware.drivetrain.getPose().translation(), Rotation2d(angle)
            ),
        ),
        timeout=3.0,
    )
    rpm = shooter_calc_module.getSpeedRaw()
    assert rpm == approx(11.1779781175, abs=0.01)
    assert angle == approx(0.13114722400913124732706041777946, abs=0.005)
    assert angle_simple == approx(0.13114722400913124732706041777946, abs=0.005)


def test_zero_angles():

    robot_pose3d = Pose3d(2, 3, 0, Rotation3d())
    shooter_offset = Transform3d(-0.1525, -0.271, 0.5, Rotation3d())
    shooter_second_offset = Translation3d(0.1525, -0.271, 0.5)
    target = Translation3d(10, 3 - 0.271, 3.057144)

    angles = numpy.linspace(0, 2 * numpy.pi, 31, endpoint=False)

    for angle in angles:

        rotation = Rotation3d(0, 0, angle)

        rotated_robot_pose3d = robot_pose3d.rotateBy(rotation)
        rotated_target = target.rotateBy(rotation)
        rotated_shooter_pose3d = rotated_robot_pose3d.transformBy(shooter_offset)

        angle_correction = computeRobotRotationToAlign(
            rotated_robot_pose3d,
            shooter_offset.translation(),
            shooter_second_offset,
            rotated_target,
        )
        assert angle_correction == approx(0.0, abs=0.0001)

        angle_correction_simple = computeRobotRotationToAlignSimple(
            rotated_shooter_pose3d, rotated_target
        )
        assert angle_correction_simple == approx(0.0, abs=0.0001)


def _test_counterclockwise_common(added_angle_to_target: float, sign_of_angle):

    robot_pose3d = Pose3d(2, 3, 0, Rotation3d())
    shooter_offset = Transform3d(-0.1525, -0.271, 0.5, Rotation3d())
    shooter_second_offset = Translation3d(0.1525, -0.271, 0.5)
    target = Translation3d(10, 3 - 0.271, 3.057144)

    angles = numpy.linspace(0, 2 * numpy.pi, 31, endpoint=False)

    for angle in angles:
        rotation_robot = Rotation3d(0, 0, angle)
        rotation_target = Rotation3d(0, 0, angle + added_angle_to_target)

        rotated_robot_pose3d = robot_pose3d.rotateBy(rotation_robot)
        rotated_target = target.rotateBy(rotation_target)
        rotated_shooter_pose3d = rotated_robot_pose3d.transformBy(shooter_offset)

        angle_correction = computeRobotRotationToAlign(
            rotated_robot_pose3d,
            shooter_offset.translation(),
            shooter_second_offset,
            rotated_target,
        )

        angle_correction_simple = computeRobotRotationToAlignSimple(
            rotated_shooter_pose3d, rotated_target
        )

        assert angle_correction * sign_of_angle > 0.0
        assert angle_correction_simple * sign_of_angle > 0.0


def test_counterclockwise():
    _test_counterclockwise_common(0.01, 1.0)
    _test_counterclockwise_common(0.1, 1.0)
    _test_counterclockwise_common(1.0, 1.0)
    _test_counterclockwise_common(2.0, 1.0)
    _test_counterclockwise_common(-0.01, -1.0)
    _test_counterclockwise_common(-0.1, -1.0)
    _test_counterclockwise_common(-1.0, -1.0)
    _test_counterclockwise_common(-2.0, -1.0)
