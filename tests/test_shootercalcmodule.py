import math

import numpy
from _pytest.python_api import approx
from wpimath.geometry import Pose2d, Transform2d
from wpimath.geometry import Pose3d, Rotation3d, Translation3d, Transform3d

from commands.drivetrain.resetpose import ResetPose
from modules.shootercalcmodule import (
    computeRobotRotationToAlignExact,
    computeRobotRotationToAlign,
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

    # We are calling explicitly shooter_calc_module.computeRotationToAlignWithTargetExact() to
    # get the correct rotation to apply to the robot. shooter_calc_module currently uses an
    # approximation of the angle. The position of the shooter is not exactly aligned, so the
    # distance and the speed will not be accurate. Forcing here the robot to turn with the
    # exact value, and the approximation will recompute all the values for a correction of 0.0 degrees
    # the next frame.
    rotation_to_align_exact = (
        shooter_calc_module.computeRotationToAlignWithTargetExact()
    )

    transform = Transform2d(0.0, 0.0, rotation_to_align_exact)
    robot_controller.wait_one_frame()

    robot_controller.run_command(
        ResetPose(robot.hardware.drivetrain, robot_pose + transform), timeout=3.0
    )

    speed = shooter_calc_module.getProjectileSpeed()

    assert shooter_calc_module.getRotationToAlignWithTarget().radians() == approx(
        0.0, abs=0.005
    )
    assert rotation_to_align_exact.radians() == approx(angle_solution, abs=0.005)
    assert speed == approx(speed_solution, abs=0.01)


def test_ShooterCalcModule(robot_controller: RobotTestController, robot: Robot):

    _test_ShooterCalcModule_common(
        robot_controller, robot, Pose2d(2, 3, 0), 6.46594643286, 0.343500071108
    )
    _test_ShooterCalcModule_common(
        robot_controller, robot, Pose2d(2, 5, 0), 6.44561409639, -0.384948495407
    )
    _test_ShooterCalcModule_common(
        robot_controller, robot, Pose2d(1, 2, 0), 7.50927519393, 0.506611883635
    )
    _test_ShooterCalcModule_common(
        robot_controller, robot, Pose2d(3, 4, 0), 5.8284874285, -0.0728888922415
    )

    _test_ShooterCalcModule_common(
        robot_controller, robot, Pose2d(5, 1, 0), 5.58402302186, 2.74934933836
    )
    _test_ShooterCalcModule_common(
        robot_controller, robot, Pose2d(6, 2, 0), 6.35366507828, 3.12484048514
    )
    _test_ShooterCalcModule_common(
        robot_controller, robot, Pose2d(8, 3, 0), 7.99579383522, -2.95927027617
    )
    _test_ShooterCalcModule_common(
        robot_controller, robot, Pose2d(5, 5, 0), 5.59658848743, 2.73847325989
    )
    _test_ShooterCalcModule_common(
        robot_controller, robot, Pose2d(6, 6, math.pi), 6.353954713, -0.0261464617762
    )
    _test_ShooterCalcModule_common(
        robot_controller,
        robot,
        Pose2d(6, 7, 0.5 * math.pi),
        6.45935313075,
        1.81243172721,
    )


def test_zero_angles(robot_controller: RobotTestController, robot: Robot):

    robot_pose = Pose3d(2, 3, 0, Rotation3d())
    distance_to_target = 10.0

    shooter_pose = robot_pose.transformBy(robot.shooter_calc_module.shooter_offset)
    target_at_origin = Translation3d(distance_to_target, 0.0, 0.0).rotateBy(
        shooter_pose.rotation()
    )
    target = (
        Translation3d(distance_to_target, 0.0, 0.0).rotateBy(shooter_pose.rotation())
        + shooter_pose.translation()
    )

    angles = numpy.linspace(0, 2 * numpy.pi, 31, endpoint=False)

    for angle in angles:

        rotation = Rotation3d(0, 0, angle)
        shooter_offset = robot.shooter_calc_module.shooter_offset
        shooter_extremity = (
            Translation3d(0.5, 0.0, 0.0).rotateBy(shooter_offset.rotation())
            + shooter_offset.translation()
        )

        rotated_robot_pose3d = robot_pose.rotateBy(rotation)
        rotated_target = target.rotateBy(rotation)

        rotated_shooter_pose3d = rotated_robot_pose3d.transformBy(shooter_offset)

        rotation_to_align_exact = computeRobotRotationToAlignExact(
            rotated_robot_pose3d,
            shooter_offset.translation(),
            shooter_extremity,
            rotated_target,
        )

        assert rotation_to_align_exact.radians() == approx(0.0, abs=0.0001)

        rotation_to_align = computeRobotRotationToAlign(
            rotated_shooter_pose3d, rotated_target
        )
        assert rotation_to_align.radians() == approx(0.0, abs=0.0001)


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

        rotation_to_align_exact = computeRobotRotationToAlignExact(
            rotated_robot_pose3d,
            shooter_offset.translation(),
            shooter_second_offset,
            rotated_target,
        )

        rotation_to_align = computeRobotRotationToAlign(
            rotated_shooter_pose3d, rotated_target
        )

        assert rotation_to_align_exact.radians() * sign_of_angle > 0.0
        assert rotation_to_align.radians() * sign_of_angle > 0.0


def test_counterclockwise():
    _test_counterclockwise_common(0.01, 1.0)
    _test_counterclockwise_common(0.1, 1.0)
    _test_counterclockwise_common(1.0, 1.0)
    _test_counterclockwise_common(2.0, 1.0)
    _test_counterclockwise_common(-0.01, -1.0)
    _test_counterclockwise_common(-0.1, -1.0)
    _test_counterclockwise_common(-1.0, -1.0)
    _test_counterclockwise_common(-2.0, -1.0)
