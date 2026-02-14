import math
from typing import Callable

from rev import (
    SparkMax,
    SparkBase,
    SparkSim,
    ClosedLoopSlot,
    SparkClosedLoopController,
    ResetMode,
    PersistMode,
)
from wpilib import RobotBase
from wpilib.simulation import RoboRioSim
from wpimath.geometry import Rotation2d
from wpimath.kinematics import SwerveModulePosition, SwerveModuleState
from wpimath.system.plant import DCMotor
from wpiutil import Sendable, SendableBuilder

from ultime.swerve import swerveconfig
from ultime.timethis import tt


class SwerveModule:
    def __init__(
        self,
        drive_motor_port,
        turning_motor_port,
        chassis_angular_offset: float,
    ):
        self._drive_position_meters: float = 0.0
        self._drive_velocity_meters_per_sec: float = 0.0
        self._drive_applied_volts: float = 0.0
        self._turn_raw_angle_radians: float = 0.0
        self._turn_applied_volts: float = 0.0
        self._module_state: SwerveModuleState = SwerveModuleState()
        self._module_position: SwerveModulePosition = SwerveModulePosition()

        self._driving_motor = SparkMax(drive_motor_port, SparkMax.MotorType.kBrushless)
        self._turning_motor = SparkMax(
            turning_motor_port, SparkMax.MotorType.kBrushless
        )
        self.desired_state = SwerveModuleState(0.0, Rotation2d())

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

        self._chassis_angular_offset = chassis_angular_offset
        self.desired_state.angle = Rotation2d(self._turning_encoder.getPosition())
        self._driving_encoder.setPosition(0.0)

        self.desired_velocity = 0.0

        if RobotBase.isSimulation():
            self.sim_driving_motor = SparkSim(self._driving_motor, DCMotor.NEO())
            self.sim_encoder_drive = self.sim_driving_motor.getRelativeEncoderSim()

            self.sim_turning_motor = SparkSim(self._turning_motor, DCMotor.NEO550())
            self.sim_encoder_turn = self.sim_turning_motor.getAbsoluteEncoderSim()

    def readInputs(self):
        self._drive_position_meters = self._driving_encoder.getPosition()
        self._drive_velocity_meters_per_sec = self._driving_encoder.getVelocity()
        self._drive_applied_volts = (
            self._driving_motor.getBusVoltage() * self._driving_motor.getAppliedOutput()
        )

        self._turn_raw_angle_radians = self._turning_encoder.getPosition()
        self._turn_applied_volts = (
            self._turning_motor.getBusVoltage() * self._turning_motor.getAppliedOutput()
        )

        self._module_state = SwerveModuleState(
            self._drive_velocity_meters_per_sec,
            Rotation2d(self._turn_raw_angle_radians - self._chassis_angular_offset),
        )
        self._module_position = SwerveModulePosition(
            self._drive_position_meters,
            Rotation2d(self._turn_raw_angle_radians - self._chassis_angular_offset),
        )

    def setDriveVoltage(self, voltage: float):
        self._driving_motor.setVoltage(voltage)

    def setTurnVoltage(self, voltage: float):
        self._turning_motor.setVoltage(voltage)

    def setDriveVelocity(
        self, velocity_meters_per_sec: float, accel_meters_per_sec: float
    ):
        if abs(velocity_meters_per_sec) < 0.001:
            self._driving_closed_loop_controller.setReference(
                0.0, SparkBase.ControlType.kVoltage
            )
            self.desired_velocity = 0.0
            return

        direction = 0
        if velocity_meters_per_sec > 0:
            direction = 1
        elif velocity_meters_per_sec < 0:
            direction = -1
        ff_volts = (
            swerveconfig.driveKs * direction
            + swerveconfig.driveKv * velocity_meters_per_sec
            + swerveconfig.driveKa * accel_meters_per_sec
        )

        self._driving_closed_loop_controller.setReference(
            velocity_meters_per_sec,
            SparkBase.ControlType.kVelocity,
            ClosedLoopSlot.kSlot0,
            ff_volts,
            SparkClosedLoopController.ArbFFUnits.kVoltage,
        )

        self.desired_velocity = velocity_meters_per_sec

    def setTurnPosition(self, rotation: Rotation2d):
        self._turning_closed_loop_controller.setReference(
            rotation.radians(), SparkBase.ControlType.kPosition
        )

    def setDesiredSetpoint(
        self, state: SwerveModuleState, accel_meters_per_sec: float = 0.0
    ):
        corrected_desired_state = SwerveModuleState()
        corrected_desired_state.speed = state.speed
        corrected_desired_state.angle = state.angle.rotateBy(
            Rotation2d(self._chassis_angular_offset)
        )

        current_rotation = Rotation2d(self._turning_encoder.getPosition())

        corrected_desired_state.optimize(current_rotation)

        corrected_desired_state.speed *= (
            current_rotation - corrected_desired_state.angle
        ).cos()

        self.setDriveVelocity(corrected_desired_state.speed, accel_meters_per_sec)
        self.setTurnPosition(corrected_desired_state.angle)

    def runCharacterization(self, output: float):
        self.setDriveVoltage(output)
        self.setTurnPosition(Rotation2d())

    def stop(self):
        self.setDriveVoltage(0.0)
        self.setTurnVoltage(0.0)

    def getAngleRandians(self):
        return self._turn_raw_angle_radians

    def getEncoderPosition(self):
        return self._drive_position_meters

    def getVelocity(self):
        return self._drive_velocity_meters_per_sec

    def getPosition(self) -> SwerveModulePosition:
        return self._module_position

    def getState(self) -> SwerveModuleState:
        return self._module_state

    def getDrivingMotorAppliedVoltage(self):
        return self._drive_applied_volts

    def simulationUpdate(self, period: float):
        # Drive motor simulation
        drive_voltage = (
            self._driving_motor.getAppliedOutput() * RoboRioSim.getVInVoltage()
        )
        self.sim_driving_motor.iterate(
            drive_voltage, RoboRioSim.getVInVoltage(), period
        )

        # Update drive encoder
        self.sim_encoder_drive.setPosition(self.sim_driving_motor.getPosition())
        self.sim_encoder_drive.setVelocity(self.sim_driving_motor.getVelocity())

        # Turn motor simulation
        turn_voltage = (
            self._turning_motor.getAppliedOutput() * RoboRioSim.getVInVoltage()
        )
        self.sim_turning_motor.iterate(turn_voltage, RoboRioSim.getVInVoltage(), period)

        # Update turn encoder
        current_turn_pos = self.sim_turning_motor.getPosition()
        # Normalize angle to -π to π
        normalized_pos = ((current_turn_pos + math.pi) % (2 * math.pi)) - math.pi
        self.sim_encoder_turn.setPosition(normalized_pos)
        self.sim_encoder_turn.setVelocity(self.sim_turning_motor.getVelocity())


class SwerveDriveElasticSendable(Sendable):
    def __init__(
        self,
        module_fl: SwerveModule,
        module_fr: SwerveModule,
        module_bl: SwerveModule,
        module_br: SwerveModule,
        get_robot_angle_radians: Callable[[], float],
    ):
        super().__init__()
        self.module_fl = module_fl
        self.module_fr = module_fr
        self.module_bl = module_bl
        self.module_br = module_br
        self.get_robot_angle_radians = get_robot_angle_radians

    def initSendable(self, builder: SendableBuilder):
        def noop(_):
            pass

        builder.setSmartDashboardType("SwerveDrive")

        builder.addDoubleProperty(
            "Front Left Voltage",
            tt(lambda: self.module_fl.getDrivingMotorAppliedVoltage()),
            noop,
        )
        builder.addDoubleProperty(
            "Front Right Voltage",
            tt(lambda: self.module_fr.getDrivingMotorAppliedVoltage()),
            noop,
        )
        builder.addDoubleProperty(
            "Back Left Voltage",
            tt(lambda: self.module_bl.getDrivingMotorAppliedVoltage()),
            noop,
        )
        builder.addDoubleProperty(
            "Back Right Voltage",
            tt(lambda: self.module_br.getDrivingMotorAppliedVoltage()),
            noop,
        )

        builder.addDoubleProperty(
            "Back Left Desired Velocity",
            tt(lambda: self.module_bl.desired_velocity),
            noop,
        )
        builder.addDoubleProperty(
            "Front Left Desired Velocity",
            tt(lambda: self.module_bl.desired_velocity),
            noop,
        )
        builder.addDoubleProperty(
            "Front Right Desired Velocity",
            tt(lambda: self.module_bl.desired_velocity),
            noop,
        )
        builder.addDoubleProperty(
            "Back Right Desired Velocity",
            tt(lambda: self.module_bl.desired_velocity),
            noop,
        )

        builder.addDoubleProperty(
            "Front Left Angle",
            tt(lambda: self.module_fl.getAngleRandians()),
            noop,
        )
        builder.addDoubleProperty(
            "Front Right Angle",
            tt(lambda: self.module_fr.getAngleRandians()),
            noop,
        )
        builder.addDoubleProperty(
            "Back Left Angle",
            tt(lambda: self.module_bl.getAngleRandians()),
            noop,
        )
        builder.addDoubleProperty(
            "Back Right Angle",
            tt(lambda: self.module_br.getAngleRandians()),
            noop,
        )

        builder.addDoubleProperty(
            "Back Left Velocity", tt(self.module_bl.getVelocity), noop
        )
        builder.addDoubleProperty(
            "Front Left Velocity", tt(self.module_fl.getVelocity), noop
        )
        builder.addDoubleProperty(
            "Front Right Velocity", tt(self.module_fr.getVelocity), noop
        )
        builder.addDoubleProperty(
            "Back Right Velocity", tt(self.module_br.getVelocity), noop
        )

        builder.addDoubleProperty("Robot Angle", tt(self.get_robot_angle_radians), noop)
