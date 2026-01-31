import math
from typing import Callable

from rev import SparkSim
from wpilib import RobotBase
from wpilib.simulation import RoboRioSim
from wpimath.geometry import Rotation2d
from wpimath.kinematics import SwerveModulePosition, SwerveModuleState
from wpimath.system.plant import DCMotor
from wpiutil import Sendable, SendableBuilder

from ultime.swerve import swerveconfig
from ultime.swerve.swerveIO import SwerveIO, SwerveInputs, SwerveOutputs
from ultime.timethis import tt


class SwerveModule:
    def __init__(
        self,
        io: SwerveIO,
        chassis_angular_offset: float,
    ):
        self._chassis_angular_offset = chassis_angular_offset

        self.desired_velocity = 0.0

        self._inputs = io.inputs
        self._outputs = io.outputs

    def setDriveVelocity(
        self, velocity_meters_per_sec: float, accel_meters_per_sec: float
    ):
        if abs(velocity_meters_per_sec) < 0.001:
            velocity_meters_per_sec = 0.0

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

        self._outputs.drive_velocity_meters_per_sec = velocity_meters_per_sec
        self._outputs.drive_ff_volts = ff_volts

    def setDesiredSetpoint(
        self, state: SwerveModuleState, accel_meters_per_sec: float = 0.0
    ):
        corrected_desired_state = SwerveModuleState()
        corrected_desired_state.speed = state.speed
        corrected_desired_state.angle = state.angle.rotateBy(
            Rotation2d(self._chassis_angular_offset)
        )

        current_rotation = Rotation2d(self._inputs.turn_raw_angle_radians)

        corrected_desired_state.optimize(current_rotation)

        corrected_desired_state.speed *= (
            current_rotation - corrected_desired_state.angle
        ).cos()

        self.setDriveVelocity(corrected_desired_state.speed, accel_meters_per_sec)
        self._outputs.turn_position = corrected_desired_state.angle

    def runCharacterization(self, output: float):
        self._outputs.drive_voltage = output
        self._outputs.turn_position = Rotation2d()

    def stop(self):
        self._outputs.drive_voltage = 0.0
        self._outputs.turn_voltage = 0.0

    def getPosition(self) -> SwerveModulePosition:
        return SwerveModulePosition(
            self._inputs.drive_position_meters,
            Rotation2d(
                self._inputs.turn_raw_angle_radians - self._chassis_angular_offset
            ),
        )

    def getState(self) -> SwerveModuleState:
        return SwerveModuleState(
            self._inputs.drive_velocity_meters_per_sec,
            Rotation2d(
                self._inputs.turn_raw_angle_radians - self._chassis_angular_offset
            ),
        )

    def getDrivingMotorAppliedVoltage(self):
        return self._inputs.drive_applied_volts

    def getVelocity(self):
        return self._inputs.drive_velocity_meters_per_sec


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
            tt(lambda: self.module_fl.getPosition().angle.radians()),
            noop,
        )
        builder.addDoubleProperty(
            "Front Right Angle",
            tt(lambda: self.module_fr.getPosition().angle.radians()),
            noop,
        )
        builder.addDoubleProperty(
            "Back Left Angle",
            tt(lambda: self.module_bl.getPosition().angle.radians()),
            noop,
        )
        builder.addDoubleProperty(
            "Back Right Angle",
            tt(lambda: self.module_br.getPosition().angle.radians()),
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
