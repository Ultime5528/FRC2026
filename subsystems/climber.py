from enum import Enum, auto

import wpilib
from rev import SparkMax, SparkMaxSim
from wpilib import RobotBase
from wpimath._controls._controls.plant import DCMotor

import ports
from ultime.autoproperty import autoproperty
from ultime.linearsubsystem import LinearSubsystem
from ultime.switch import Switch


class Climber(LinearSubsystem):

    left_angle_min = autoproperty(0.0)
    left_angle_max = autoproperty(45.0)
    right_angle_min = autoproperty(0.0)
    right_angle_max = autoproperty(45.0)
    speed = autoproperty(0.5)
    position_conversion_factor = autoproperty(0.2)
    height_max = autoproperty(0.215)
    hugger_maximal_moving_time = autoproperty(2.0)

    def __init__(self):

        sim_initial_position = self.height_max
        should_reset_min = True
        should_reset_max = False
        should_block_min_position = True
        should_block_max_position = True
        sim_motor_to_distance_factor = self.position_conversion_factor
        sim_gravity = 0.0

        super().__init__(
            sim_initial_position,
            should_reset_min,
            should_reset_max,
            should_block_min_position,
            should_block_max_position,
            sim_motor_to_distance_factor,
            sim_gravity)

        self._climber_motor = SparkMax(ports.CAN.climber_motor, SparkMax.MotorType.kBrushless)
        self._hugger_motor_left = wpilib.Servo(ports.PWM.hugger_motor_left)
        self._hugger_motor_right = wpilib.Servo(ports.PWM.hugger_motor_right)
        self._climber_encoder = self._motor.getEncoder()
        self._switch = Switch(Switch.Type.NormallyClosed, ports.DIO.climber_switch)

        if RobotBase.isSimulation():
            self._sim_height = 5.0
            self._climber_sim_motor = SparkMaxSim(self._motor, DCMotor.NEO(1))
            self._climber_sim_encoder = self._sim_motor.getRelativeEncoderSim()

    def getMinPosition(self) -> float:
        return 0.0

    def getMaxPosition(self) -> float:
        return self.height_max

    def isSwitchMinPressed(self) -> bool:
        return self._switch.isPressed()

    def getEncoderPosition(self) -> float:
        return self._encoder.getPosition()

    def setSimulationEncoderPosition(self, position: float) -> None:
        return self._sim_encoder.getPosition()

    def getPositionConversionFactor(self) -> float:
        return self.position_conversion_factor

    def _setMotorOutput(self, speed: float) -> None:
        self._climber_motor.setSpeed(speed    )

    def getMotorOutput(self) -> float:
        self._climber_motor.get()

    def hug(self):
        self._hugger_motor_left.setAngle(self.left_angle_max)
        self._hugger_motor_right.setAngle(self.right_angle_max)

    def unhug(self):
        self._hugger_motor_left.setAngle(self.left_angle_min)
        self._hugger_motor_right(self.right_angle_min)