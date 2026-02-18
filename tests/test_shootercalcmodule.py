import math

from hal import AllianceStationID
from wpilib.simulation import DriverStationSim
from wpimath.geometry import Pose2d

from modules.shootercalcmodule import ShooterCalcModule, computeRobotRotationToAlign
from commands.drivetrain.resetpose import ResetPose
from robot import Robot
from ultime.tests import RobotTestController
from wpimath.geometry import Pose3d,Rotation3d,Translation3d,Transform3d


# def test_ShooterPower(robot_controller: RobotTestController, robot: Robot):
#     shooter_calc_module = ShooterCalcModule(robot.hardware.drivetrain)
#     red_hub = shooter_calc_module.red_hub
#     robot_controller.startTeleop()
#     robot_controller.run_command(ResetPose(robot.hardware.drivetrain,Pose2d((red_hub.x)-4.0, (red_hub.y)-3.0)), 3.0)
#     robot_controller.wait(0.2)
#     angle = shooter_calc_module._getAngleToAlignWithTarget()
#     rpm = shooter_calc_module.getRPM()
#     assert

def test_computeRobotRotationToAlign_1():
    robot = Pose3d(2, 3, 0, Rotation3d(Translation3d(0, 0, 1), 0))
    offset = Transform3d(-0.1525, -0.271, 0.5, Rotation3d())
    extrem = Translation3d(0.1525, -0.271, 0.5)
    red_hub = Translation3d(4.625594, 4.034536, 3.057144)
    angle = computeRobotRotationToAlign(robot, offset, extrem, red_hub)
    assert angle == approx(0.0, abs=0.0001)
