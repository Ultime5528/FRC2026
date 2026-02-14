from _pytest.python_api import approx

from commands.guide import ResetGuide, MoveGuide, _move_properties
from robot import Robot
from ultime.switch import Switch
from ultime.tests import RobotTestController


def test_ports(robot: Robot):
    guide = robot.hardware.guide

    assert guide._motor.getChannel() == 0
    assert guide._min_switch.getChannel() == 0


def test_settings(robot: Robot):
    guide = robot.hardware.guide

    assert guide._min_switch.getType() == Switch.Type.NormallyOpen
    assert not guide._motor.getInverted()


def test_reset_command(robot_controller: RobotTestController, robot: Robot):
    guide = robot.hardware.guide

    robot_controller.startTeleop()

    assert not guide.isSwitchMinPressed()

    cmd = ResetGuide.down(guide)
    cmd.schedule()
    robot_controller.wait_one_frame()

    assert guide.getMotorOutput() < 0.0

    robot_controller.wait_until(lambda: not cmd.isScheduled(), 10.0)
    robot_controller.wait_one_frame()
    assert not cmd.isScheduled()
    assert not guide.isSwitchMinPressed()
    assert guide.hasReset()
    assert guide.getMotorOutput() == 0.0
    assert guide.getPosition() == approx(0.0, abs=0.02)


def common_test_moveGuide_from_switch_down(
    robot_controller: RobotTestController,
    robot: Robot,
    MoveGuideCommand,
    wanted_position,
):
    guide = robot.hardware.guide

    robot_controller.startTeleop()

    robot_controller.run_command(ResetGuide.down(guide), 10.0)

    robot_controller.run_command(MoveGuideCommand(guide), 10.0)
    robot_controller.wait(1.0)

    assert guide.getMotorOutput() == approx(0.0, abs=0.02)
    assert guide.getPosition() == approx(wanted_position, abs=0.02)


def test_moveGuide_toUsed(robot_controller: RobotTestController, robot: Robot):
    common_test_moveGuide_from_switch_down(
        robot_controller, robot, MoveGuide.toUsed, _move_properties.position_used
    )


def test_moveGuide_toUnused(robot_controller: RobotTestController, robot: Robot):
    common_test_moveGuide_from_switch_down(
        robot_controller, robot, MoveGuide.toUnused, _move_properties.position_unused
    )
