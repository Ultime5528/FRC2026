import math

from _pytest.python_api import approx
from commands2 import Command
from rev import SparkBase

from commands.climber.move import (
    ResetClimber,
    MoveClimber,
    _move_properties,
    ManualMoveClimber,
)
from robot import Robot
from ultime.switch import Switch
from ultime.tests import RobotTestController


def test_ports(robot: Robot):
    climber = robot.hardware.climber
    assert climber._motor.getDeviceId() == 11
    assert climber._switch.getChannel() == 6


def test_settings(robot: Robot):
    climber = robot.hardware.climber
    assert climber._switch.getType() == Switch.Type.NormallyClosed
    assert climber._motor.getMotorType() == SparkBase.MotorType.kBrushless
    assert not climber._motor.getInverted()


def test_reset_climber(robot_controller: RobotTestController, robot: Robot):
    climber = robot.hardware.climber

    robot_controller.startTeleop()

    assert not climber.hasReset()

    cmd = ResetClimber.down(climber)
    cmd.schedule()

    robot_controller.wait_one_frame()

    assert climber.getMotorOutput() < climber.speed_maintain

    robot_controller.wait_until(lambda: climber.isSwitchMinPressed(), 10.0)

    assert climber.getMotorOutput() > climber.speed_maintain

    robot_controller.wait_until(lambda: climber.hasReset(), 5.0)

    assert not cmd.isScheduled()
    assert not climber.isSwitchMinPressed()
    assert climber.getPosition() == approx(0.0, abs=0.02)
    assert climber.hasReset()
    assert climber.getMotorOutput() == approx(climber.speed_maintain, abs=0.01)


def _test_move_climber_common(
    robot_controller: RobotTestController,
    robot: Robot,
    cmd_1: Command,
    final_position_1: float,
    cmd_2: Command,
    final_position_2: float,
):
    climber = robot.hardware.climber
    position_tolerance = climber.position_max * 0.01

    robot_controller.startTeleop()

    cmd_reset_climber = ResetClimber.down(climber)
    robot_controller.run_command(cmd_reset_climber, 10.0)
    robot_controller.wait_one_frame()
    assert not cmd_reset_climber.isScheduled()
    assert climber.hasReset()

    cmd_1.schedule()

    robot_controller.wait_one_frame()
    assert (final_position_1 == 0.0 and climber.getMotorOutput() == 0.0) or (
        math.copysign(1.0, final_position_1) * climber.getMotorOutput()
        > climber.speed_maintain
    )

    robot_controller.run_command(cmd_1, 10.0)
    robot_controller.wait_one_frame()

    assert not cmd_1.isScheduled()
    assert climber.getMotorOutput() == climber.speed_maintain
    assert climber.getPosition() == approx(final_position_1, abs=position_tolerance)

    cmd_2.schedule()

    robot_controller.wait_one_frame()
    assert (
        final_position_2 == climber.getPosition() and climber.getMotorOutput() == 0.0
    ) or (
        math.copysign(1.0, (final_position_2 - climber.getPosition()))
        * climber.getMotorOutput()
        > climber.speed_maintain
    )

    robot_controller.run_command(cmd_2, 10.0)
    robot_controller.wait_one_frame()

    assert not cmd_2.isScheduled()
    assert climber.getMotorOutput() == climber.speed_maintain
    assert climber.getPosition() == approx(final_position_2, abs=position_tolerance)


def test_move_climber_to_ready_to_ready(
    robot_controller: RobotTestController, robot: Robot
):
    climber = robot.hardware.climber
    _test_move_climber_common(
        robot_controller,
        robot,
        MoveClimber.toReady(climber),
        _move_properties.position_ready,
        MoveClimber.toReady(climber),
        _move_properties.position_ready,
    )


def test_move_climber_to_ready_to_retracted(
    robot_controller: RobotTestController, robot: Robot
):
    climber = robot.hardware.climber
    _test_move_climber_common(
        robot_controller,
        robot,
        MoveClimber.toReady(climber),
        _move_properties.position_ready,
        MoveClimber.toRetracted(climber),
        _move_properties.position_retracted,
    )


def test_move_climber_to_ready_to_climbed(
    robot_controller: RobotTestController, robot: Robot
):
    climber = robot.hardware.climber
    _test_move_climber_common(
        robot_controller,
        robot,
        MoveClimber.toReady(climber),
        _move_properties.position_ready,
        MoveClimber.toClimbed(climber),
        _move_properties.position_climbed,
    )


def test_move_climber_to_retracted_to_ready(
    robot_controller: RobotTestController, robot: Robot
):
    climber = robot.hardware.climber
    _test_move_climber_common(
        robot_controller,
        robot,
        MoveClimber.toRetracted(climber),
        _move_properties.position_retracted,
        MoveClimber.toReady(climber),
        _move_properties.position_ready,
    )


def test_move_climber_to_retracted_to_retracted(
    robot_controller: RobotTestController, robot: Robot
):
    climber = robot.hardware.climber
    _test_move_climber_common(
        robot_controller,
        robot,
        MoveClimber.toRetracted(climber),
        _move_properties.position_retracted,
        MoveClimber.toRetracted(climber),
        _move_properties.position_retracted,
    )


def test_move_climber_to_retracted_to_climbed(
    robot_controller: RobotTestController, robot: Robot
):
    climber = robot.hardware.climber
    _test_move_climber_common(
        robot_controller,
        robot,
        MoveClimber.toRetracted(climber),
        _move_properties.position_retracted,
        MoveClimber.toClimbed(climber),
        _move_properties.position_climbed,
    )


def test_move_climber_to_climbed_to_ready(
    robot_controller: RobotTestController, robot: Robot
):
    climber = robot.hardware.climber
    _test_move_climber_common(
        robot_controller,
        robot,
        MoveClimber.toClimbed(climber),
        _move_properties.position_climbed,
        MoveClimber.toReady(climber),
        _move_properties.position_ready,
    )


def test_move_climber_to_climbed_to_retracted(
    robot_controller: RobotTestController, robot: Robot
):
    climber = robot.hardware.climber
    _test_move_climber_common(
        robot_controller,
        robot,
        MoveClimber.toClimbed(climber),
        _move_properties.position_climbed,
        MoveClimber.toRetracted(climber),
        _move_properties.position_retracted,
    )


def test_move_climber_to_climbed_to_climbed(
    robot_controller: RobotTestController, robot: Robot
):
    climber = robot.hardware.climber
    _test_move_climber_common(
        robot_controller,
        robot,
        MoveClimber.toClimbed(climber),
        _move_properties.position_climbed,
        MoveClimber.toClimbed(climber),
        _move_properties.position_climbed,
    )


def test_manual_move_climber_up(robot_controller: RobotTestController, robot: Robot):
    climber = robot.hardware.climber
    position_tolerance = climber.position_max * 0.01

    robot_controller.startTeleop()

    cmd_reset_climber = ResetClimber.down(climber)
    robot_controller.run_command(cmd_reset_climber, 10.0)
    robot_controller.wait_one_frame()
    assert not cmd_reset_climber.isScheduled()
    assert climber.hasReset()

    cmd = ManualMoveClimber.up(climber)
    cmd.schedule()

    robot_controller.wait_one_frame()
    assert climber.getMotorOutput() > climber.speed_maintain

    robot_controller.wait_until(lambda: climber.getMotorOutput() == 0.0, 10.0)

    assert climber.getPosition() == approx(climber.position_max, abs=position_tolerance)


def test_manual_move_climber_down_with_reset(
    robot_controller: RobotTestController, robot: Robot
):
    climber = robot.hardware.climber
    position_tolerance = climber.position_max * 0.01

    robot_controller.startTeleop()

    cmd_reset_climber = ResetClimber.down(climber)
    robot_controller.run_command(cmd_reset_climber, 10.0)
    robot_controller.wait_one_frame()
    assert not cmd_reset_climber.isScheduled()
    assert climber.hasReset()

    cmd_manual_move_up = ManualMoveClimber.up(climber)
    cmd_manual_move_up.schedule()

    robot_controller.wait_one_frame()

    assert climber.getMotorOutput() > climber.speed_maintain
    robot_controller.wait(1.0)

    cmd_manual_move_up.end(True)

    assert climber.getMotorOutput() == 0.0
    assert climber.getPosition() > 0.0

    cmd = ManualMoveClimber.down(climber)
    cmd.schedule()

    # cmd_manual_move_up is still scheduled even if end(True) is called, until
    # cmd is scheduled (because of Subsystem requirements)
    assert not cmd_manual_move_up.isScheduled()

    robot_controller.wait_one_frame()
    assert climber.getMotorOutput() < climber.speed_maintain

    robot_controller.wait(2.0)
    cmd.end(True)

    assert climber.getMotorOutput() == 0.0
    assert climber.getPosition() == approx(0.0, abs=position_tolerance)


def test_manual_move_climber_down_without_reset(
    robot_controller: RobotTestController, robot: Robot
):
    climber = robot.hardware.climber

    robot_controller.startTeleop()

    cmd = ManualMoveClimber.down(climber)
    cmd.schedule()

    robot_controller.wait_one_frame()
    assert climber.getMotorOutput() < climber.speed_maintain

    robot_controller.wait(2.0)
    cmd.end(True)

    assert climber.getMotorOutput() == 0.0
