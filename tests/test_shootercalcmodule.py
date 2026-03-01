import math

import numpy
from _pytest.python_api import approx
from wpimath.geometry import Pose2d, Rotation2d, Translation2d, Transform2d
from wpimath.geometry import Pose3d, Rotation3d, Translation3d, Transform3d

from commands.drivetrain.resetpose import ResetPose
from modules.shootercalcmodule import (
    computeRobotRotationToAlign,
    computeRobotRotationToAlignSimple,
)
from robot import Robot
from ultime.tests import RobotTestController


def _test_ShooterCalcModule_common(
    robot_controller: RobotTestController,
    robot: Robot,
    robot_pose: Pose2d,
    speed_solution: float,
    angle_solution: float,
):
    shooter_calc_module = robot.shooter_calc_module
    robot_controller.startTeleop()
    robot_controller.run_command(
        ResetPose(robot.hardware.drivetrain, robot_pose), timeout=3.0
    )

    angle = shooter_calc_module.getAngleToAlignWithTarget()

    transform = Transform2d(0.0, 0.0, angle)

    robot_controller.run_command(
        ResetPose(robot.hardware.drivetrain, robot_pose + transform), timeout=3.0
    )

    speed = shooter_calc_module.getSpeedRaw()

    assert speed == approx(speed_solution, abs=0.01)
    assert angle == approx(angle_solution, abs=0.005)


def test_ShooterCalcModule(robot_controller: RobotTestController, robot: Robot):

    _test_ShooterCalcModule_common(
        robot_controller, robot, Pose2d(2, 3, 0), 7.18366932701, 0.471517850869
    )
    _test_ShooterCalcModule_common(
        robot_controller, robot, Pose2d(2, 5, 0), 7.15792018564, -0.255341218445
    )
    _test_ShooterCalcModule_common(
        robot_controller, robot, Pose2d(1, 2, 0), 8.47220924023, 0.57660113341
    )
    _test_ShooterCalcModule_common(
        robot_controller, robot, Pose2d(3, 4, 0), 5.82183695912, 0.188694113917
    )

    _test_ShooterCalcModule_common(
        robot_controller, robot, Pose2d(5, 1, 0), 6.58517154536, 2.87413979556
    )
    _test_ShooterCalcModule_common(
        robot_controller, robot, Pose2d(6, 2, 0), 7.46975446748, -3.07273010236
    )
    _test_ShooterCalcModule_common(
        robot_controller, robot, Pose2d(8, 3, 0), 9.3604457092, -2.92352375287
    )
    _test_ShooterCalcModule_common(
        robot_controller, robot, Pose2d(5, 5, 0), 6.59960579301, 2.86249712744
    )
    _test_ShooterCalcModule_common(
        robot_controller, robot, Pose2d(6, 6, math.pi), 7.47008754727, 0.0594560464062
    )
    _test_ShooterCalcModule_common(
        robot_controller,
        robot,
        Pose2d(6, 7, 0.5 * math.pi),
        7.5913053378,
        1.89369523653,
    )


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
