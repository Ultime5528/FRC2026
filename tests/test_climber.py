from _pytest.python_api import approx
from commands2 import Command
from rev import SparkBase

from commands.climber.hug import Hug
from commands.climber.move import (
    ResetClimber,
    MoveClimber,
    _move_properties,
    ManualMoveClimber,
)
from commands.climber.unhug import Unhug
from robot import Robot
from ultime.switch import Switch
from ultime.tests import RobotTestController


def test_ports(robot: Robot):
    climber = robot.hardware.climber
    assert climber._climber_motor.getDeviceId() == 11
    assert climber._hugger_motor_left.getChannel() == 9
    assert climber._hugger_motor_right.getChannel() == 8
    assert climber._switch.getChannel() == 6


def test_settings(robot: Robot):
    climber = robot.hardware.climber
    assert climber._climber_motor.getInverted()
    assert climber._switch.getType() == Switch.Type.NormallyClosed
    assert climber._climber_motor.getMotorType() == SparkBase.MotorType.kBrushless
    assert climber._climber_motor.getInverted() == False


def test_reset_climber(robot_controller: RobotTestController, robot: Robot):
    climber = robot.hardware.climber

    robot_controller.startTeleop()

    assert not climber.hasReset()

    cmd = ResetClimber.down(climber)
    cmd.schedule()

    robot_controller.wait_one_frame()

    assert climber.getMotorOutput() < 0.0

    robot_controller.wait_until(lambda: climber.isSwitchMinPressed(), 5.0)

    assert climber.getMotorOutput() > 0.0

    robot_controller.wait_until(lambda: climber.hasReset(), 5.0)

    assert not cmd.isScheduled()
    assert not climber.isSwitchMinPressed()
    assert climber.getPosition() == approx(0.0, abs=0.02)
    assert climber.hasReset()
    assert climber.getMotorOutput() == 0.0


def _test_move_climber_common(
    robot_controller: RobotTestController,
    robot: Robot,
    cmd: Command,
    final_position: float,
):
    climber = robot.hardware.climber

    robot_controller.startTeleop()

    cmd_reset_climber = ResetClimber.down(climber)
    robot_controller.run_command(cmd_reset_climber, 10.0)
    robot_controller.wait_one_frame()
    assert not cmd_reset_climber.isScheduled()
    assert climber.hasReset()

    cmd.schedule()

    robot_controller.wait_one_frame()
    assert climber.getMotorOutput() > 0.0

    robot_controller.run_command(cmd, 10.0)
    robot_controller.wait_one_frame()

    assert not cmd.isScheduled()
    assert climber.getMotorOutput() == 0.0
    assert climber.getPosition() == approx(final_position, abs=0.02)


def test_move_climber_to_ready(robot_controller: RobotTestController, robot: Robot):
    climber = robot.hardware.climber
    _test_move_climber_common(
        robot_controller,
        robot,
        MoveClimber.toReady(climber),
        _move_properties.position_ready,
    )


def test_move_climber_to_retracted(robot_controller: RobotTestController, robot: Robot):
    climber = robot.hardware.climber
    _test_move_climber_common(
        robot_controller,
        robot,
        MoveClimber.toRetracted(climber),
        _move_properties.position_retracted,
    )


def test_move_climber_to_climbed(robot_controller: RobotTestController, robot: Robot):
    climber = robot.hardware.climber
    _test_move_climber_common(
        robot_controller,
        robot,
        MoveClimber.toClimbed(climber),
        _move_properties.position_climbed,
    )


def _test_manual_move_climber_up(robot_controller: RobotTestController, robot: Robot):
    climber = robot.hardware.climber

    robot_controller.startTeleop()

    cmd_reset_climber = ResetClimber.down(climber)
    robot_controller.run_command(cmd_reset_climber, 10.0)
    robot_controller.wait_one_frame()
    assert not cmd_reset_climber.isScheduled()
    assert climber.hasReset()

    cmd = ManualMoveClimber.up()
    cmd.schedule()

    robot_controller.wait_one_frame()
    assert climber.getMotorOutput() > 0.0

    robot_controller.run_command(cmd, 10.0)
    robot_controller.wait_one_frame()

    assert not cmd.isScheduled()
    assert climber.getMotorOutput() == 0.0
    assert climber.getPosition() == approx(climber.height_max, abs=0.02)


def _test_manual_move_climber_down_with_reset(
    robot_controller: RobotTestController, robot: Robot
):
    climber = robot.hardware.climber

    robot_controller.startTeleop()

    cmd_reset_climber = ResetClimber.down(climber)
    robot_controller.run_command(cmd_reset_climber, 10.0)
    robot_controller.wait_one_frame()
    assert not cmd_reset_climber.isScheduled()
    assert climber.hasReset()

    cmd_manual_move_up = ManualMoveClimber.up()
    cmd_manual_move_up.schedule()

    assert climber.getMotorOutput() > 0.0
    robot_controller.run_command(cmd_manual_move_up, 10.0)
    assert not cmd_manual_move_up.isScheduled()

    cmd = ManualMoveClimber.down()
    cmd.schedule()

    robot_controller.wait_one_frame()
    assert climber.getMotorOutput() < 0.0

    robot_controller.run_command(cmd, 10.0)
    robot_controller.wait_one_frame()

    assert not cmd.isScheduled()
    assert climber.getMotorOutput() == 0.0
    assert climber.getPosition() == approx(0.0, abs=0.02)


def _test_manual_move_climber_down_without_reset(
    robot_controller: RobotTestController, robot: Robot
):
    climber = robot.hardware.climber

    cmd = ManualMoveClimber.down()
    cmd.schedule()

    robot_controller.wait_one_frame()
    assert climber.getMotorOutput() < 0.0

    robot_controller.run_command(cmd, 10.0)

    assert climber.getMotorOutput() == 0.0
    assert climber.isSwitchMinPressed()
    assert not climber.hasReset()
    assert climber.getPosition() == approx(0.0, abs=0.02)


def hug_test(robot_controller: RobotTestController, robot: Robot):
    climber = robot.hardware.climber

    cmd = Hug(climber)
    cmd.schedule()

    robot_controller.wait(climber.delay_hug)
    assert cmd.isFinished()


def unhug_test(robot_controller: RobotTestController, robot: Robot):
    climber = robot.hardware.climber

    cmd = Unhug(climber)
    cmd.schedule()

    robot_controller.wait(climber.delay_hug)
    assert cmd.isFinished()
