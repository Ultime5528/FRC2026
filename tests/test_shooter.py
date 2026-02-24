from pytest import approx

from commands.shooter.manualshoot import ManualShoot, manual_shoot_properties
from commands.shooter.prepareshoot import PrepareShoot
from commands.shooter.shoot import Shoot
from robot import Robot
from subsystems.shooter import IndexerState
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
    # assert shooter._indexer.get() == approx(shooter.indexer_current_rpm)
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

    rpm_indexer_tolerance = shooter.speed_rpm_indexer * 0.01

    robot_controller.startTeleop()

    assert shooter._flywheel_controller.getSetpoint() == 0
    assert shooter._indexer.get() == 0
    assert shooter._feeder.get() == 0

    cmd = Shoot(shooter)
    cmd.schedule()
    robot_controller.wait_one_frame()

    assert cmd.isScheduled()

    assert shooter._flywheel_controller.getSetpoint() > 0

    assert shooter.indexer_state == IndexerState.Off

    robot_controller.wait_until(lambda: shooter.isAtVelocity(), 10.0)
    robot_controller.wait_one_frame()
    assert shooter.indexer_state == IndexerState.On
    assert shooter.indexer_current_rpm <= shooter.rpm_indexer_stuck_threshold
    assert shooter.isAtVelocity()

    robot_controller.wait_until(
        lambda: shooter.indexer_current_rpm > (shooter.rpm_indexer_stuck_threshold * 2),
        10.0,
    )
    assert shooter.indexer_state == IndexerState.On
    assert shooter.indexer_current_rpm > shooter.rpm_indexer_stuck_threshold
    assert shooter.isAtVelocity()

    robot_controller.wait_until(
        lambda: shooter._timer.hasElapsed(shooter.delay_indexer_to_stuck_threshold),
        10.0,
    )

    shooter._indexer_sim.setVelocity(0.0)
    robot_controller.wait_one_frame()

    assert shooter.indexer_state == IndexerState.Stuck
    assert shooter.indexer_current_rpm == approx(0.0, abs=rpm_indexer_tolerance)
    assert shooter.isAtVelocity()

    robot_controller.wait(shooter.delay_indexer_unstuck * 0.5)
    assert shooter.indexer_state == IndexerState.Stuck
    assert shooter.indexer_current_rpm == approx(
        shooter.rpm_indexer_to_unstuck, abs=rpm_indexer_tolerance
    )
    assert shooter.isAtVelocity()

    robot_controller.wait(shooter.delay_indexer_unstuck * 0.5)
    robot_controller.wait_one_frame()
    assert shooter.indexer_state == IndexerState.On
    assert shooter.indexer_current_rpm == approx(
        shooter.rpm_indexer_to_unstuck, abs=rpm_indexer_tolerance
    )

    robot_controller.wait_one_frame()
    assert shooter.indexer_state == IndexerState.On
    assert shooter.indexer_current_rpm > shooter.rpm_indexer_to_unstuck
    assert shooter.isAtVelocity()

    robot_controller.wait_until(
        lambda: shooter.indexer_current_rpm
        == approx(shooter.speed_rpm_indexer, abs=rpm_indexer_tolerance),
        10.0,
    )
    assert shooter.indexer_state == IndexerState.On
    assert shooter.indexer_current_rpm == approx(
        shooter.speed_rpm_indexer, abs=rpm_indexer_tolerance
    )
    assert shooter.isAtVelocity()

    assert shooter._feeder.get() == approx(shooter.speed_feeder)
