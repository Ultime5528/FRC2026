from commands2 import CommandScheduler
from pytest import approx

from commands.shooter.manualshoot import ManualShoot, manual_shoot_properties
from commands.shooter.prepareshoot import PrepareShoot
from commands.shooter.shoot import Shoot
from modules.shootercalcmodule import ShooterCalcModule
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

    assert shooter.getCurrentSpeed() == 0.0
    assert shooter._indexer.get() == 0.0
    assert shooter._feeder.get() == 0.0

    cmd = ManualShoot(shooter)
    cmd.schedule()
    robot_controller.wait_one_frame()

    assert cmd.isScheduled()

    assert shooter.getCurrentSpeed() == 0.0

    robot_controller.wait_until(lambda: shooter.isAtVelocity(), 10.0)

    assert shooter.getCurrentSpeed() == approx(
        manual_shoot_properties.speed_rpm, abs=rpm_tolerance
    )
    # assert shooter._indexer.get() == approx(shooter.indexer_current_rpm)
    assert shooter._feeder.get() == approx(shooter.feeder_speed)

    CommandScheduler.getInstance().cancel(cmd)

    robot_controller.wait_until(
        lambda: shooter.getCurrentSpeed() == approx(0.0, abs=rpm_tolerance), 10.0
    )

    assert shooter.getCurrentSpeed() == approx(0.0, abs=rpm_tolerance)


def test_prepareShoot(robot_controller: RobotTestController, robot: Robot):
    shooter = robot.hardware.shooter
    shooter_calc_module = ShooterCalcModule(
        robot.hardware.drivetrain, robot.hardware.guide
    )

    rpm_flywheel = 666.6  # TODO mettre la valeur du calcul d'hayder
    rpm_flywheel_tolerance = rpm_flywheel * 0.01

    robot_controller.startTeleop()

    assert shooter.getCurrentSpeed() == 0.0
    assert shooter._indexer.get() == 0.0
    assert shooter._feeder.get() == 0.0

    cmd = PrepareShoot(shooter, shooter_calc_module)
    cmd.schedule()
    robot_controller.wait_one_frame()

    assert cmd.isScheduled()

    assert shooter.getCurrentSpeed() == 0.0
    assert shooter._indexer.get() == 0.0
    assert shooter._feeder.get() == 0.0

    robot_controller.wait_until(
        lambda: shooter.getCurrentSpeed()
        == approx(rpm_flywheel, abs=rpm_flywheel_tolerance),
        10.0,
    )

    assert shooter.getCurrentSpeed() == approx(rpm_flywheel, abs=rpm_flywheel_tolerance)


def test_shoot(robot_controller: RobotTestController, robot: Robot):

    shooter = robot.hardware.shooter
    shooter_calc_module = ShooterCalcModule(
        robot.hardware.drivetrain, robot.hardware.guide
    )

    rpm_indexer_tolerance = shooter.indexer_rpm * 0.01

    robot_controller.startTeleop()

    assert shooter.getCurrentSpeed() == 0.0
    assert shooter._indexer.get() == 0.0
    assert shooter._feeder.get() == 0.0

    cmd = Shoot(shooter, shooter_calc_module)
    cmd.schedule()
    robot_controller.wait_one_frame()

    assert cmd.isScheduled()

    assert shooter.getCurrentSpeed() == 0.0

    assert shooter.indexer_state == IndexerState.Off

    robot_controller.wait_until(lambda: shooter.isAtVelocity(), 10.0)
    robot_controller.wait_one_frame()
    assert shooter.indexer_state == IndexerState.On
    assert shooter.indexer_current_rpm <= shooter.indexer_rpm_stuck_threshold
    assert shooter.isAtVelocity()

    robot_controller.wait_until(
        lambda: shooter.indexer_current_rpm > (shooter.indexer_rpm_stuck_threshold * 2),
        10.0,
    )
    assert shooter.indexer_state == IndexerState.On
    assert shooter.indexer_current_rpm > shooter.indexer_rpm_stuck_threshold
    assert shooter.isAtVelocity()

    robot_controller.wait_until(
        lambda: shooter._timer.hasElapsed(shooter.indexer_delay_stuck_threshold),
        10.0,
    )

    shooter._indexer_sim.setVelocity(0.0)
    robot_controller.wait_one_frame()

    assert shooter.indexer_state == IndexerState.Stuck
    assert shooter.indexer_current_rpm == approx(0.0, abs=rpm_indexer_tolerance)
    assert shooter.isAtVelocity()

    robot_controller.wait(shooter.indexer_delay_unstuck * 0.5)
    assert shooter.indexer_state == IndexerState.Stuck
    assert shooter.indexer_current_rpm == approx(
        shooter.indexer_rpm_unstuck, abs=rpm_indexer_tolerance
    )
    assert shooter.isAtVelocity()

    robot_controller.wait(shooter.indexer_delay_unstuck * 0.5)
    robot_controller.wait_one_frame()
    assert shooter.indexer_state == IndexerState.On
    assert shooter.indexer_current_rpm == approx(
        shooter.indexer_rpm_unstuck, abs=rpm_indexer_tolerance
    )

    robot_controller.wait_one_frame()
    assert shooter.indexer_state == IndexerState.On
    assert shooter.indexer_current_rpm > shooter.indexer_rpm_unstuck
    assert shooter.isAtVelocity()

    robot_controller.wait_until(
        lambda: shooter.indexer_current_rpm
        == approx(shooter.indexer_rpm, abs=rpm_indexer_tolerance),
        10.0,
    )
    assert shooter.indexer_state == IndexerState.On
    assert shooter.indexer_current_rpm == approx(
        shooter.indexer_rpm, abs=rpm_indexer_tolerance
    )
    assert shooter.isAtVelocity()

    assert shooter._feeder.get() == approx(shooter.feeder_speed)
