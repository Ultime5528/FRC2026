from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional

from rev import (
    SparkMax,
    ResetMode,
    PersistMode,
    SparkBase,
    ClosedLoopSlot,
    SparkClosedLoopController,
)
from wpimath.geometry import Rotation2d

from ultime.swerve import swerveconfig


@dataclass
class SwerveInputs:
    drive_position_meters: float = 0.0
    drive_velocity_meters_per_sec: float = 0.0
    drive_applied_volts: float = 0.0

    turn_raw_angle_radians: float = 0.0


@dataclass
class SwerveOutputs:
    drive_voltage: Optional[float] = None
    drive_velocity_meters_per_sec: Optional[float] = None
    drive_ff_volts: Optional[float] = None

    turn_voltage: Optional[float] = None
    turn_position: Optional[Rotation2d] = None

    def reset(self):
        self.drive_voltage = None
        self.drive_velocity_meters_per_sec = None
        self.drive_ff_volts = None

        self.turn_voltage = None
        self.turn_position = None


class SwerveIO(ABC):
    @abstractmethod
    def updateInputs(self, inputs: SwerveInputs):
        pass

    @abstractmethod
    def sendOutputs(self, outputs: SwerveOutputs):
        pass


class SwerveIOSpark(SwerveIO):
    def __init__(
        self,
        drive_motor_port,
        turning_motor_port,
    ):
        self._driving_motor = SparkMax(drive_motor_port, SparkMax.MotorType.kBrushless)
        self._turning_motor = SparkMax(
            turning_motor_port, SparkMax.MotorType.kBrushless
        )

        self._driving_encoder = self._driving_motor.getEncoder()
        self._turning_encoder = self._turning_motor.getAbsoluteEncoder()

        self._driving_motor.configure(
            swerveconfig.driving_config,
            ResetMode.kResetSafeParameters,
            PersistMode.kPersistParameters,
        )

        self._turning_motor.configure(
            swerveconfig.turning_config,
            ResetMode.kResetSafeParameters,
            PersistMode.kPersistParameters,
        )

        self._driving_closed_loop_controller = (
            self._driving_motor.getClosedLoopController()
        )
        self._turning_closed_loop_controller = (
            self._turning_motor.getClosedLoopController()
        )

    def updateInputs(self, inputs: SwerveInputs):
        inputs.drive_position_meters = self._driving_encoder.getPosition()
        inputs.drive_velocity_meters_per_sec = self._driving_encoder.getVelocity()
        inputs.drive_applied_volts = (
            self._driving_motor.getBusVoltage() * self._driving_motor.getAppliedOutput()
        )

        inputs.turn_raw_angle_radians = self._turning_encoder.getPosition()

    def sendOutputs(self, outputs: SwerveOutputs):
        drive_voltage = outputs.drive_voltage
        drive_velocity_meters_per_sec = outputs.drive_velocity_meters_per_sec
        drive_ff_volts = outputs.drive_ff_volts

        turn_voltage = outputs.turn_voltage
        turn_position = outputs.turn_position

        if drive_voltage is not None:
            self._driving_motor.setVoltage(drive_voltage)
        elif (
            drive_velocity_meters_per_sec is not None
            and drive_velocity_meters_per_sec is not None
        ):
            self._driving_closed_loop_controller.setReference(
                drive_velocity_meters_per_sec,
                SparkBase.ControlType.kVelocity,
                ClosedLoopSlot.kSlot0,
                drive_ff_volts,
                SparkClosedLoopController.ArbFFUnits.kVoltage,
            )

        if turn_voltage is not None:
            self._turning_motor.setVoltage(turn_voltage)
        elif turn_position is not None:
            self._turning_closed_loop_controller.setReference(
                turn_position.radians(), SparkBase.ControlType.kPosition
            )
