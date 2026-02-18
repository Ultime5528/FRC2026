from commands.resetall import ResetAll
from robot import Robot
from ultime.tests import RobotTestController


def test_reset_all(robot_controller: RobotTestController, robot: Robot):
    robot_controller.startTeleop()
    climber = robot.hardware.climber
    pivot = robot.hardware.pivot
    guide = robot.hardware.guide

    cmd = ResetAll(climber, pivot, guide)
    robot_controller.run_command(cmd, 10.0)
    robot_controller.wait_one_frame()

    assert climber.hasReset()
    assert pivot.hasReset()
    assert guide.hasReset()
