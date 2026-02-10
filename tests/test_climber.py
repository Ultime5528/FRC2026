from _pytest.python_api import approx
from rev import SparkBase, SparkBaseConfig

import ports
from commands.climber.resetclimber import ResetClimber
from robot import Robot
from subsystems import climber
from ultime.switch import Switch
from ultime.tests import RobotTestController


def test_ports(robot: Robot):
    climber = robot.hardware.climber
    assert climber._climber_motor.getDeviceId() == 9
    assert climber._hugger_motor_left.getChannel() == 1
    assert climber._hugger_motor_right.getChannel() == 2
    assert climber._switch.getChannel() == 3


def test_settings(robot: Robot):
    climber = robot.hardware.climber
    assert climber._switch.getType() == Switch.Type.NormallyClosed
    assert climber._climber_motor.getMotorType() == SparkBase.MotorType.kBrushless
    assert climber._climber_motor.getInverted() == False


def test_reset_climber(robot_controller: RobotTestController, robot: Robot):
    climber = robot.hardware.climber

    robot_controller.startTeleop()

    cmd = ResetClimber(climber)
    cmd.schedule()

    robot_controller.wait(0.05)

    assert not climber.hasReset()
    assert climber._climber_motor.get() < 0.0

    climber._switch.setSimPressed()

    robot_controller.wait_one_frame()

    assert climber.getPosition() == approx(0.0, abs=0.01)
    assert climber.hasReset()
    assert climber._climber_motor.get() == 0.0
