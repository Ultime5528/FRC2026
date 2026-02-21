from pytest import approx

from commands.shooter.manualshoot import ManualShoot, manual_shoot_properties
from commands.shooter.prepareshoot import PrepareShoot
from commands.shooter.shoot import Shoot
from robot import Robot
from ultime.tests import RobotTestController


def test_ports(robot: Robot):
    assert robot.hardware.shooter._flywheel.getDeviceId() == 14
    assert robot.hardware.shooter._feeder.getDeviceId() == 13
    assert robot.hardware.shooter._indexer.getDeviceId() == 12


def test_ManualShoot(robot_controller: RobotTestController, robot: Robot):
    shooter = robot.hardware.shooter
    rpm_tolerance = manual_shoot_properties.speed_rpm * 0.01

    robot_controller.startTeleop()

    assert shooter._flywheel_controller.getSetpoint() == 0
    assert shooter._indexer.get() == 0
    assert shooter._feeder.get() == 0

    cmd = ManualShoot(shooter)
    cmd.schedule()
    robot_controller.wait_one_frame()

    assert cmd.isScheduled()

    assert shooter._flywheel_controller.getSetpoint() > 0

    robot_controller.wait_until(lambda: shooter.isAtVelocity(), 10.0)

    assert shooter._flywheel_controller.getSetpoint() > 0
    assert shooter._indexer.get() == approx(shooter.speed_indexer)
    assert shooter._feeder.get() == approx(shooter.speed_feeder)

    robot_controller.wait(10.0)

    assert shooter.getCurrentSpeed() == approx(
        manual_shoot_properties.speed_rpm, abs=rpm_tolerance
    )


def test_prepareShoot(robot_controller: RobotTestController, robot: Robot):
    shooter = robot.hardware.shooter

    robot_controller.startTeleop()

    assert shooter._flywheel_controller.getSetpoint() == 0
    assert shooter._indexer.get() == 0
    assert shooter._feeder.get() == 0

    cmd = PrepareShoot(shooter)
    cmd.schedule()
    robot_controller.wait_one_frame()

    assert cmd.isScheduled()

    assert shooter._flywheel_controller.getSetpoint() > 0
    assert shooter._indexer.get() == 0
    assert shooter._feeder.get() == 0

    robot_controller.wait(10.0)

    assert shooter._flywheel_controller.getSetpoint() == approx(
        shooter.getCurrentSpeed(), abs=10.0
    )


def test_shoot(robot_controller: RobotTestController, robot: Robot):
    shooter = robot.hardware.shooter

    robot_controller.startTeleop()

    assert shooter._flywheel_controller.getSetpoint() == 0
    assert shooter._indexer.get() == 0
    assert shooter._feeder.get() == 0

    cmd = Shoot(shooter)
    cmd.schedule()
    robot_controller.wait_one_frame()

    assert cmd.isScheduled()

    assert shooter._flywheel_controller.getSetpoint() > 0

    robot_controller.wait_until(shooter.isAtVelocity, 10.0)

    assert shooter._indexer.get() == approx(shooter.speed_indexer)
    assert shooter._feeder.get() == approx(shooter.speed_feeder)
