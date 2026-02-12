import math

from hal import AllianceStationID
from wpilib.simulation import DriverStationSim
from wpimath.geometry import Pose2d

from modules.shootercalcmodule import ShooterCalcModule
from commands.drivetrain.resetpose import ResetPose
from robot import Robot
from ultime.tests import RobotTestController


def test_ShooterPower(robot_controller: RobotTestController, robot: Robot):
    shooter_calc_module = ShooterCalcModule(robot.hardware.drivetrain)
    red_hub = shooter_calc_module.red_hub
    robot_controller.startTeleop()
    robot_controller.run_command(ResetPose(robot.hardware.drivetrain,Pose2d((red_hub.x)-4.0, (red_hub.y)-3.0)), 3.0)
    robot_controller.wait(0.2)
    angle = shooter_calc_module._getAngleToAlignWithTarget()
    rpm = shooter_calc_module.getRPM()
    assert