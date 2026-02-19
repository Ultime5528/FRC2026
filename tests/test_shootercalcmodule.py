import math

from _pytest.python_api import approx
from hal import AllianceStationID
from wpilib.simulation import DriverStationSim
from wpimath.geometry import Pose2d

from modules.shootercalcmodule import (
    ShooterCalcModule,
    computeRobotRotationToAlign,
    computeShooterPosition,
    computeRobotRotationToAlignSimple,
)
from commands.drivetrain.resetpose import ResetPose
from robot import Robot
from ultime.tests import RobotTestController
from wpimath.geometry import Pose3d, Rotation3d, Translation3d, Transform3d


# def test_ShooterPower(robot_controller: RobotTestController, robot: Robot):
#     shooter_calc_module = ShooterCalcModule(robot.hardware.drivetrain)
#     red_hub = shooter_calc_module.red_hub
#     robot_controller.startTeleop()
#     robot_controller.run_command(ResetPose(robot.hardware.drivetrain,Pose2d(2,3,0)),timeout=3.0)
#     robot_controller.wait(0.2)
#     angle = shooter_calc_module._getAngleToAlignWithTarget()
#     rpm = shooter_calc_module.getRPM()
#     assert


def test_computeRobotRotationToAlign_1():
    robot = Pose3d(2, 3, 0, Rotation3d(Translation3d(0, 0, 1), 0))
    offset = Translation3d(-0.1525, -0.271, 0.5)
    extreme = Translation3d(0.1525, -0.271, 0.5)
    red_hub = Translation3d(4.625594, 4.034536, 3.057144)
    angle = computeRobotRotationToAlign(robot, offset, extreme, red_hub)
    assert angle == approx((-27.0159828199 * math.pi / 180), abs=0.0001)


def test_zero_angles():
    robot = Pose3d(2, 3, 0, Rotation3d())
    offset = Transform3d(-0.1525, -0.271, 0.5, Rotation3d())
    extreme = Translation3d(0.1525, -0.271, 0.5)
    red_hub = Translation3d(10, 3 - 0.271, 3.057144)
    shooter_pose3d = robot.transformBy(offset)

    angle = computeRobotRotationToAlign(robot, offset.translation(), extreme, red_hub)
    assert angle == approx(0.0, abs=0.0001)

    angleSimple = computeRobotRotationToAlignSimple(shooter_pose3d, red_hub)
    assert angleSimple == approx(0.0, abs=0.0001)
