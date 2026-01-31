import math
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional

import hal
from rev import (
    SparkMax,
    ResetMode,
    PersistMode,
    SparkBase,
    ClosedLoopSlot,
    SparkClosedLoopController,
    SparkSim,
)
from wpilib import RobotBase
from wpilib.simulation import RoboRioSim
from wpimath._controls._controls.plant import DCMotor
from wpimath.geometry import Rotation2d

from ultime.io import Io
from ultime.swerve import swerveconfig


@dataclass
class SwerveInputs:
    drive_position_meters: float = 0.0
    drive_velocity_meters_per_sec: float = 0.0
    drive_applied_volts: float = 0.0

    turn_raw_angle_radians: float = 0.0
    turn_applied_volts: float = 0.0


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


class SwerveIO(Io):
    def __init__(self, drive_motor_port, turn_motor_port):
        super().__init__()
        self.drive_motor_port = drive_motor_port
        self.turn_motor_port = turn_motor_port

        self._driving_motor = SparkMax(
            self.drive_motor_port, SparkMax.MotorType.kBrushless
        )
        self._turning_motor = SparkMax(
            self.turn_motor_port, SparkMax.MotorType.kBrushless
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

        self._driving_encoder.setPosition(0.0)

        self.inputs = SwerveInputs()
        self.outputs = SwerveOutputs()


class SwerveIOSim(SwerveIO):
    def __init__(self, drive_motor_port: int, turn_motor_port: int):
        super().__init__(drive_motor_port, turn_motor_port)

        self.sim_driving_motor = SparkSim(self._driving_motor, DCMotor.NEO())
        self.sim_encoder_drive = self.sim_driving_motor.getRelativeEncoderSim()

        self.sim_turning_motor = SparkSim(self._turning_motor, DCMotor.NEO550())
        self.sim_encoder_turn = self.sim_turning_motor.getAbsoluteEncoderSim()

    def updateInputs(self):
        self.inputs.drive_position_meters = self._driving_encoder.getPosition()
        self.inputs.drive_velocity_meters_per_sec = self._driving_encoder.getVelocity()
        self.inputs.drive_applied_volts = (
            self._driving_motor.getBusVoltage() * self._driving_motor.getAppliedOutput()
        )

        self.inputs.turn_raw_angle_radians = self._turning_encoder.getPosition()
        self.inputs.turn_applied_volts = (
            self._turning_motor.getBusVoltage() * self._turning_motor.getAppliedOutput()
        )

        #simulation
        drive_voltage = (
                self._driving_motor.getAppliedOutput() * RoboRioSim.getVInVoltage()
        )
        self.sim_driving_motor.iterate(drive_voltage, RoboRioSim.getVInVoltage(), 0.02)

        # Update drive encoder
        self.sim_encoder_drive.setPosition(self.sim_driving_motor.getPosition())
        self.sim_encoder_drive.setVelocity(self.sim_driving_motor.getVelocity())

        # Turn motor simulation
        turn_voltage = (
                self._turning_motor.getAppliedOutput() * RoboRioSim.getVInVoltage()
        )
        self.sim_turning_motor.iterate(turn_voltage, RoboRioSim.getVInVoltage(), 0.02)

        # Update turn encoder
        current_turn_pos = self.sim_turning_motor.getPosition()
        # Normalize angle to -π to π
        normalized_pos = ((current_turn_pos + math.pi) % (2 * math.pi)) - math.pi
        self.sim_encoder_turn.setPosition(normalized_pos)
        self.sim_encoder_turn.setVelocity(self.sim_turning_motor.getVelocity())

    def sendOutputs(self):
        drive_voltage = self.outputs.drive_voltage
        drive_velocity_meters_per_sec = self.outputs.drive_velocity_meters_per_sec
        drive_ff_volts = self.outputs.drive_ff_volts

        turn_voltage = self.outputs.turn_voltage
        turn_position = self.outputs.turn_position

        if drive_voltage is not None:
            self._driving_motor.setVoltage(drive_voltage)
        elif drive_velocity_meters_per_sec is not None and drive_ff_volts is not None:
            self._driving_closed_loop_controller.setReference(
                drive_velocity_meters_per_sec,
                SparkBase.ControlType.kVelocity,
                ClosedLoopSlot.kSlot0,
                drive_ff_volts,
                SparkClosedLoopController.ArbFFUnits.kVoltage,
            )
        else:
            self._driving_motor.setVoltage(0.0)

        if turn_voltage is not None:
            self._turning_motor.setVoltage(turn_voltage)
        elif turn_position is not None:
            self._turning_closed_loop_controller.setReference(
                turn_position.radians(), SparkBase.ControlType.kPosition
            )
        else:
            self._turning_motor.setVoltage(0.0)

        self.outputs.reset()


class SwerveIOSpark(SwerveIO):
    def __init__(self, drive_motor_port: int, turn_motor_port: int):
        super().__init__(drive_motor_port, turn_motor_port)

    def updateInputs(self):
        self.inputs.drive_position_meters = self._driving_encoder.getPosition()
        self.inputs.drive_velocity_meters_per_sec = self._driving_encoder.getVelocity()
        self.inputs.drive_applied_volts = (
            self._driving_motor.getBusVoltage() * self._driving_motor.getAppliedOutput()
        )

        self.inputs.turn_raw_angle_radians = self._turning_encoder.getPosition()
        self.inputs.turn_applied_volts = (
            self._turning_motor.getBusVoltage() * self._turning_motor.getAppliedOutput()
        )

    def sendOutputs(self):
        drive_voltage = self.outputs.drive_voltage
        drive_velocity_meters_per_sec = self.outputs.drive_velocity_meters_per_sec
        drive_ff_volts = self.outputs.drive_ff_volts

        turn_voltage = self.outputs.turn_voltage
        turn_position = self.outputs.turn_position

        if drive_voltage is not None:
            self._driving_motor.setVoltage(drive_voltage)
        elif drive_velocity_meters_per_sec is not None and drive_ff_volts is not None:
            self._driving_closed_loop_controller.setReference(
                drive_velocity_meters_per_sec,
                SparkBase.ControlType.kVelocity,
                ClosedLoopSlot.kSlot0,
                drive_ff_volts,
                SparkClosedLoopController.ArbFFUnits.kVoltage,
            )
        else:
            self._driving_motor.setVoltage(0.0)

        if turn_voltage is not None:
            self._turning_motor.setVoltage(turn_voltage)
        elif turn_position is not None:
            self._turning_closed_loop_controller.setReference(
                turn_position.radians(), SparkBase.ControlType.kPosition
            )
        else:
            self._turning_motor.setVoltage(0.0)

        self.outputs.reset()
