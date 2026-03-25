from commands.resetall import ResetAll
from robot import Robot
from ultime.tests import RobotTestController


def test_reset_all(robot_controller: RobotTestController, robot: Robot):
    robot_controller.startTeleop()
    climber = robot.hardware.climber
    hugger = robot.hardware.hugger
    guide = robot.hardware.guide

    cmd = ResetAll(climber, hugger)
    robot_controller.run_command(cmd, 10.0)
    robot_controller.wait_one_frame()

    assert climber.hasReset()
    assert guide.hasReset()
