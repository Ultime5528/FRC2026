import math

import rev
from rev import (
    SparkMaxSim,
    SparkMaxConfig,
    SparkMax,
    ResetMode,
    PersistMode,
    SparkBaseConfig,
)
from wpilib import RobotBase
from wpimath._controls._controls.plant import DCMotor

import ports
from ultime.autoproperty import autoproperty
from ultime.control import pf, clamp
from ultime.linear.linearsubsystem import LinearSubsystem
from ultime.modulerobot import is_simulation
from ultime.switch import Switch


class Pivot(LinearSubsystem):
    speed_maintain = autoproperty(1.0)
    min_position = autoproperty(0.0)
    max_position = autoproperty(5.0)
    position_maintain_min = autoproperty(-1.0)
    position_maintain_max = autoproperty(6.5)

    kS = autoproperty(0.3)
    kF = autoproperty(0.002)
    kP = autoproperty(0.0001)
    kG = autoproperty(0.5)

    def __init__(self):
        super().__init__(
            sim_initial_position=1.0,
            should_reset_min=True,
            should_reset_max=False,
            should_block_min_position=False,
            should_block_max_position=False,
            should_block_min_switch=False,
            should_block_max_switch=True,
            sim_motor_to_distance_factor=2.0,
            sim_gravity=0.0,
        )
        self._motor_current_rpm = self.createProperty(0.0)
        self._switch_min_pressed: bool = False
        self._switch_max_pressed: bool = False

        self._motor = rev.SparkMax(
            ports.CAN.pivot_motor, rev.SparkMax.MotorType.kBrushless
        )
        self._config = SparkMaxConfig()
        self._config.setIdleMode(SparkBaseConfig.IdleMode.kBrake)
        self._motor.configure(
            self._config,
            ResetMode.kResetSafeParameters,
            PersistMode.kPersistParameters,
        )
        self._encoder = self._motor.getEncoder()
        self._switch_min = Switch(
            Switch.Type.NormallyClosed, ports.DIO.pivot_switch_min
        )
        self._switch_max = Switch(Switch.Type.NormallyOpen, ports.DIO.pivot_switch_max)

        if is_simulation:
            self._motor_sim = SparkMaxSim(self._motor, DCMotor.NEO(1))
            self._encoder_sim = self._motor_sim.getRelativeEncoderSim()

    def maintain(self):
        position = self.getPosition()

        if self.position_maintain_min <= position <= self.position_maintain_max:
            self._setMotorOutput(self.speed_maintain)
        else:
            self._motor.stopMotor()

    def readInputs(self):
        self._motor_current_rpm = self._encoder.getVelocity()
        self._switch_min_pressed = self._switch_min.isPressed()
        self._switch_max_pressed = self._switch_max.isPressed()

    def stop(self):
        self._motor.stopMotor()

    def getMinPosition(self) -> float:
        return self.min_position

    def getMaxPosition(self) -> float:
        return self.max_position

    def isSwitchMinPressed(self) -> bool:
        return self._switch_min_pressed

    def isSwitchMaxPressed(self) -> bool:
        return self._switch_max_pressed

    def setSimSwitchMinPressed(self, pressed: bool) -> None:
        self._switch_min.setSimValue(pressed)

    def setSimSwitchMaxPressed(self, pressed: bool) -> None:
        self._switch_max.setSimValue(pressed)

    def getEncoderPosition(self) -> float:
        return self._encoder.getPosition()

    def setSimulationEncoderPosition(self, position: float) -> None:
        self._encoder_sim.setPosition(position)

    def getPositionConversionFactor(self) -> float:
        return 1.0

    def _setMotorOutput(self, rpm: float) -> None:
        if abs(rpm) > 1e-6:
            voltage = pf(self.getMotorCurrentRPM(), rpm, self.kS, self.kF, self.kP)
            if self.hasReset():
                angle = clamp(self.getPosition() / self.getMaxPosition(), 0.0, 1.0) * (
                    math.pi / 2
                )
                voltage += math.cos(angle) * self.kG
        else:
            voltage = 0.0
        self._motor.setVoltage(voltage)

    def getMotorCurrentRPM(self):
        return self._motor_current_rpm

    def getMotorOutput(self) -> float:
        return self._motor.getBusVoltage() * self._motor.getAppliedOutput()
