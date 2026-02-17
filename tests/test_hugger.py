from commands.climber.hug import Hug
from commands.climber.unhug import Unhug
from robot import Robot
from subsystems import hugger
from ultime.tests import RobotTestController


def test_ports(robot: Robot):
    hugger = robot.hardware.hugger
    assert hugger._servo_left.getChannel() == 1
    assert hugger._servo_right.getChannel() == 2

def test_settings(robot: Robot):
    hugger = robot.hardware.hugger
    assert hugger.position_hug_left == 100.0
    assert hugger.position_hug_right == 80.0
    assert hugger.position_unhug_left == 80.0
    assert hugger.position_unhug_right == 100.0

def test_hug(robot_controller: RobotTestController, robot: Robot):
    hugger = robot.hardware.hugger

    cmd = Hug(hugger)
    cmd.schedule()

    robot_controller.wait(hugger.delay_hug + 0.1)
    assert not cmd.isScheduled()

def unhug_test(robot_controller: RobotTestController, robot: Robot):
    hugger = robot.hardware.hugger

    cmd = Unhug(hugger)
    cmd.schedule()

    robot_controller.wait(hugger.delay_hug + 0.1)
    assert not cmd.isScheduled()