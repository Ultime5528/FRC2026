from pytest import approx

from commands.shooter.manualshoot import ManualShoot
from robot import Robot
from ultime.tests import RobotTestController


def test_ports(robot: Robot):
    robot.hardware.shooter._flywheel.getDeviceId() == 9
    robot.hardware.shooter._feeder.getDeviceId() == 10
    robot.hardware.shooter._indexer.getDeviceId() == 13


def test_ManualShoot(robot_controller: RobotTestController, robot: Robot):
    shooter = robot.hardware.shooter

    robot_controller.startTeleop()

    assert shooter._flywheel_controller.getSetpoint() == 0
    assert shooter._indexer.get() == 0
    assert shooter._feeder.get() == 0

    cmd = ManualShoot(shooter)
    cmd.schedule()
    robot_controller.wait_one_frame()

    assert cmd.isScheduled()

    assert shooter._flywheel_controller.getSetpoint() > 0
    assert shooter._indexer.get() == approx(shooter.speed_indexer)
    assert shooter._feeder.get() == approx(shooter.speed_feeder)

    robot_controller.wait(10.0)

    assert cmd.speed_rpm == approx(shooter.getCurrentSpeed(), abs=10.0)
