import math
from typing import List

import wpilib
import wpimath
from ntcore import NetworkTableInstance
from pathplannerlib.util import DriveFeedforwards
from rev import SparkBase
from wpilib import RobotBase, SmartDashboard
from wpimath._controls._controls.controller import PIDController
from wpimath.estimator import SwerveDrive4PoseEstimator
from wpimath.geometry import Pose2d, Translation2d, Rotation2d, Twist2d
from wpimath.kinematics import (
    ChassisSpeeds,
    SwerveDrive4Kinematics,
    SwerveModuleState,
    SwerveDrive4Odometry,
    SwerveModulePosition,
)
from wpiutil import SendableBuilder

import ports
from ultime.alert import AlertType
from ultime.autoproperty import autoproperty
from ultime.gyro import ADIS16470
from ultime.subsystem import Subsystem
from ultime.swerve.swerve import SwerveModule, SwerveDriveElasticSendable
from subsystems.drivetrainio import DrivetrainIo, DrivetrainIoSim
from ultime.timethis import tt


class Drivetrain(Subsystem):
    width = 0.597
    length = 0.673
    max_angular_speed = autoproperty(25.0)
    max_speed = autoproperty(5.0)

    angular_offset_fl = autoproperty(-1.57)
    angular_offset_fr = autoproperty(0.0)
    angular_offset_bl = autoproperty(3.14)
    angular_offset_br = autoproperty(1.57)

    swerve_temperature_threshold = autoproperty(55.0)

    def __init__(self, drivetrain_io: DrivetrainIo | DrivetrainIoSim) -> None:
        super().__init__()
        self.period_seconds = 0.02
        # Swerve Module motor positions
        self.motor_fl_loc = Translation2d(self.width / 2, self.length / 2)
        self.motor_fr_loc = Translation2d(self.width / 2, -self.length / 2)
        self.motor_bl_loc = Translation2d(-self.width / 2, self.length / 2)
        self.motor_br_loc = Translation2d(-self.width / 2, -self.length / 2)

        self.x_controller = PIDController(10, 0, 0)
        self.y_controller = PIDController(10, 0, 0)
        self.heading_controller = PIDController(10, 0, 0)
        self.heading_controller.enableContinuousInput(-math.pi, math.pi)

        self.swerve_module_fl = SwerveModule(
            drivetrain_io.swerve_io_fl, self.angular_offset_fl
        )

        self.swerve_module_fr = SwerveModule(
            drivetrain_io.swerve_io_fr, self.angular_offset_fr
        )

        self.swerve_module_bl = SwerveModule(
            drivetrain_io.swerve_io_bl, self.angular_offset_bl
        )

        self.swerve_module_br = SwerveModule(
            drivetrain_io.swerve_io_fr, self.angular_offset_br
        )

        self.swerve_modules = {
            "FL": self.swerve_module_fl,
            "FR": self.swerve_module_fr,
            "BL": self.swerve_module_bl,
            "BR": self.swerve_module_br,
        }

        self.chassis_speed_goal_pub = (
            NetworkTableInstance.getDefault()
            .getStructTopic("Chassis Speed Goal", ChassisSpeeds)
            .publish()
        )
        self.chassis_speed_goal = ChassisSpeeds()

        self.chassis_speed_pub = (
            NetworkTableInstance.getDefault()
            .getStructTopic("Chassis Speed", ChassisSpeeds)
            .publish()
        )
        self.chassis_speed = ChassisSpeeds()

        # Gyro
        """
        Possibilités : NavX, ADIS16448, ADIS16470, ADXRS, Empty
        """
        self._gyro = ADIS16470()
        # TODO Assert _gyro is subclass of abstract class Gyro
        self.addChild("Gyro", self._gyro)

        self._field = wpilib.Field2d()
        wpilib.SmartDashboard.putData("Field", self._field)

        swerve_drive_sendable = SwerveDriveElasticSendable(
            self.swerve_module_fl,
            self.swerve_module_fr,
            self.swerve_module_bl,
            self.swerve_module_br,
            lambda: self._gyro.getRotation2d().radians(),
        )
        wpilib.SmartDashboard.putData("SwerveDrive", swerve_drive_sendable)

        """
        Pose estimation
        """

        self.swervedrive_kinematics = SwerveDrive4Kinematics(
            self.motor_fl_loc, self.motor_fr_loc, self.motor_bl_loc, self.motor_br_loc
        )

        self.swerve_odometry = SwerveDrive4Odometry(
            self.swervedrive_kinematics,
            self._gyro.getRotation2d(),
            [
                SwerveModulePosition(),
                SwerveModulePosition(),
                SwerveModulePosition(),
                SwerveModulePosition(),
            ],
            Pose2d(0, 0, 0),
        )

        self.swerve_estimator = SwerveDrive4PoseEstimator(
            self.swervedrive_kinematics,
            self._gyro.getRotation2d(),
            [
                SwerveModulePosition(),
                SwerveModulePosition(),
                SwerveModulePosition(),
                SwerveModulePosition(),
            ],
            Pose2d(0, 0, 0),
        )

        self.vision_pose = self._field.getObject("Vision Pose")
        self.odometry_pose = self._field.getObject("Odometry Pose")

        """
        Alerts
        """

        self.alerts_hot = {
            location: self.createAlert(
                f"{location} Swerve is too hot. Allow swerves to cool down.",
                AlertType.Warning,
            )
            for location in self.swerve_modules.keys()
        }

        self.alerts_faults = {
            location: self.createAlert(
                f"{location} Swerve has active faults/warnings. Check for them on REV Hardware Client.",
                AlertType.Warning,
            )
            for location in self.swerve_modules.keys()
        }

        self.alerts_drive_encoder = {
            location: self.createAlert(
                f"{location} Swerve Drive encoder measured velocity is too low.",
                AlertType.Error,
            )
            for location in self.swerve_modules.keys()
        }

        self.alerts_turning_motor = {
            location: self.createAlert(
                f"{location} Swerve turning motor failed to reach desired state.",
                AlertType.Error,
            )
            for location in self.swerve_modules.keys()
        }

        self.alert_odometry = self.createAlert(
            "Odometry failed to calculate robot position accurately.", AlertType.Error
        )

        if RobotBase.isSimulation():
            self.sim_yaw = 0

    def drive(
        self,
        x_speed_input: float,
        y_speed_input: float,
        rot_speed: float,
        is_field_relative: bool,
    ):
        x_speed = x_speed_input * self.max_speed
        y_speed = y_speed_input * self.max_speed
        rot_speed = rot_speed * self.max_angular_speed
        self.driveRaw(x_speed, y_speed, rot_speed, is_field_relative)

    def driveFromChassisSpeeds(
        self, speed: ChassisSpeeds, _ff: DriveFeedforwards = None
    ):
        corrected_chassis_speed = self.correctForDynamics(speed)
        self.chassis_speed_goal = corrected_chassis_speed

        self.chassis_speed_goal_pub.set(corrected_chassis_speed)

        swerve_module_states = self.swervedrive_kinematics.toSwerveModuleStates(
            corrected_chassis_speed
        )

        SwerveDrive4Kinematics.desaturateWheelSpeeds(
            swerve_module_states, self.max_speed
        )
        if _ff is not None:
            self.swerve_module_fl.setDesiredSetpoint(
                swerve_module_states[0], _ff.accelerationsMPS[0]
            )
            self.swerve_module_fr.setDesiredSetpoint(
                swerve_module_states[1], _ff.accelerationsMPS[1]
            )
            self.swerve_module_bl.setDesiredSetpoint(
                swerve_module_states[2], _ff.accelerationsMPS[2]
            )
            self.swerve_module_br.setDesiredSetpoint(
                swerve_module_states[3], _ff.accelerationsMPS[3]
            )
        else:
            self.swerve_module_fl.setDesiredSetpoint(swerve_module_states[0])
            self.swerve_module_fr.setDesiredSetpoint(swerve_module_states[1])
            self.swerve_module_bl.setDesiredSetpoint(swerve_module_states[2])
            self.swerve_module_br.setDesiredSetpoint(swerve_module_states[3])

    def driveFromChassisSpeedsFF(
        self, speeds: ChassisSpeeds, _ff: DriveFeedforwards
    ) -> None:
        self.driveFromChassisSpeeds(speeds, _ff)

    def driveRaw(
        self,
        x_speed: float,
        y_speed: float,
        rot_speed: float,
        is_field_relative: bool,
    ):
        if is_field_relative:
            base_chassis_speed = ChassisSpeeds.fromFieldRelativeSpeeds(
                x_speed, y_speed, rot_speed, self.getPose().rotation()
            )
        else:
            base_chassis_speed = ChassisSpeeds(x_speed, y_speed, rot_speed)

        self.driveFromChassisSpeeds(base_chassis_speed)

    def getGyroAngle(self):
        """
        Wrapped between -180 and 180
        """
        return self._gyro.getAngle()

    def getEstimatedAngle(self):
        return self.getPose().rotation()

    def resetGyro(self):
        self._gyro.reset()

    def getPose(self):
        return self.swerve_estimator.getEstimatedPosition()

    def setForwardFormation(self):
        """
        Points all the wheels to the front
        """
        for swerve in self.swerve_modules.values():
            swerve._turning_closed_loop_controller.setReference(
                swerve._chassis_angular_offset, SparkBase.ControlType.kPosition
            )

    def setSidewaysFormation(self):
        """
        Points all the wheels to the side
        """
        self.swerve_module_fl.setDesiredSetpoint(
            SwerveModuleState(0, Rotation2d.fromDegrees(90))
        )
        self.swerve_module_fr.setDesiredSetpoint(
            SwerveModuleState(0, Rotation2d.fromDegrees(90))
        )
        self.swerve_module_bl.setDesiredSetpoint(
            SwerveModuleState(0, Rotation2d.fromDegrees(90))
        )
        self.swerve_module_br.setDesiredSetpoint(
            SwerveModuleState(0, Rotation2d.fromDegrees(90))
        )

    def setXFormation(self):
        """
        Points all the wheels into the center to prevent movement
        """
        self.swerve_module_fl.setDesiredSetpoint(
            SwerveModuleState(0, Rotation2d.fromDegrees(45))
        )
        self.swerve_module_fr.setDesiredSetpoint(
            SwerveModuleState(0, Rotation2d.fromDegrees(-45))
        )
        self.swerve_module_bl.setDesiredSetpoint(
            SwerveModuleState(0, Rotation2d.fromDegrees(-45))
        )
        self.swerve_module_br.setDesiredSetpoint(
            SwerveModuleState(0, Rotation2d.fromDegrees(45))
        )

    def stop(self):
        self.swerve_module_fr.stop()
        self.swerve_module_fl.stop()
        self.swerve_module_bl.stop()
        self.swerve_module_br.stop()

    def correctForDynamics(
        self, original_chassis_speeds: ChassisSpeeds
    ) -> ChassisSpeeds:
        next_robot_pose: Pose2d = Pose2d(
            original_chassis_speeds.vx * self.period_seconds,
            original_chassis_speeds.vy * self.period_seconds,
            Rotation2d(original_chassis_speeds.omega * self.period_seconds),
        )
        pose_twist: Twist2d = Pose2d().log(next_robot_pose)
        updated_speeds: ChassisSpeeds = ChassisSpeeds(
            pose_twist.dx / self.period_seconds,
            pose_twist.dy / self.period_seconds,
            pose_twist.dtheta / self.period_seconds,
        )
        return updated_speeds

    def periodic(self):
        rotation = self._gyro.getRotation2d()
        swerve_positions = (
            self.swerve_module_fl.getPosition(),
            self.swerve_module_fr.getPosition(),
            self.swerve_module_bl.getPosition(),
            self.swerve_module_br.getPosition(),
        )

        chassis_speed = self.swervedrive_kinematics.toChassisSpeeds(
            (
                self.swerve_module_fl.getState(),
                self.swerve_module_fr.getState(),
                self.swerve_module_bl.getState(),
                self.swerve_module_br.getState(),
            )
        )

        self.chassis_speed_pub.set(chassis_speed)
        self.chassis_speed = chassis_speed
        self.swerve_estimator.update(rotation, swerve_positions)
        self.swerve_odometry.update(rotation, swerve_positions)

        self.odometry_pose.setPose(self.swerve_odometry.getPose())
        self._field.setRobotPose(self.swerve_estimator.getEstimatedPosition())

    # for location, swerve_module in self.swerve_modules.items():
    #     if (
    #         swerve_module._driving_motor.getMotorTemperature()
    #         > self.swerve_temperature_threshold
    #         or swerve_module._turning_motor.getMotorTemperature()
    #         > self.swerve_temperature_threshold
    #     ):
    #         self.alerts_hot[location].set(True)
    #     else:
    #         self.alerts_hot[location].set(False)

    #     if (
    #         swerve_module._driving_motor.hasActiveFault()
    #         or swerve_module._turning_motor.hasActiveFault()
    #         or swerve_module._driving_motor.hasActiveWarning()
    #         or swerve_module._turning_motor.hasActiveWarning()
    #     ):
    #         self.alerts_faults[location].set(True)
    #     else:
    #         self.alerts_faults[location].set(False)

    def simulationPeriodic(self):
        module_states = (
            self.swerve_module_fl.getState(),
            self.swerve_module_fr.getState(),
            self.swerve_module_bl.getState(),
            self.swerve_module_br.getState(),
        )
        chassis_speed = self.swervedrive_kinematics.toChassisSpeeds(module_states)
        chassis_rotation_speed = chassis_speed.omega
        self.sim_yaw += chassis_rotation_speed * self.period_seconds
        self._gyro.setSimAngle(math.degrees(self.sim_yaw))

    def getRobotRelativeChassisSpeeds(self):
        """
        Returns robot relative chassis speeds from current swerve module states
        """
        module_states = (
            self.swerve_module_fl.getState(),
            self.swerve_module_fr.getState(),
            self.swerve_module_bl.getState(),
            self.swerve_module_br.getState(),
        )
        chassis_speed = self.swervedrive_kinematics.toChassisSpeeds(module_states)
        return chassis_speed

    def resetToPose(self, pose: Pose2d):
        self.swerve_estimator.resetPosition(
            self._gyro.getRotation2d(),
            (
                self.swerve_module_fl.getPosition(),
                self.swerve_module_fr.getPosition(),
                self.swerve_module_bl.getPosition(),
                self.swerve_module_br.getPosition(),
            ),
            pose,
        )

    def addVisionMeasurement(
        self, pose: wpimath.geometry.Pose2d, timestamp: float, std_devs: List[float]
    ):
        self.swerve_estimator.addVisionMeasurement(pose, timestamp, std_devs)
        self.vision_pose.setPose(pose)

    def getCurrentDrawAmps(self):
        return 0.0

    def initSendable(self, builder: SendableBuilder) -> None:
        super().initSendable(builder)

        def noop(_):
            pass

        builder.addFloatProperty("GyroAngle", tt(self.getGyroAngle), noop)
        builder.addFloatProperty(
            "SpeedGoal",
            tt(
                lambda: math.hypot(
                    self.chassis_speed_goal.vx, self.chassis_speed_goal.vy
                )
            ),
            noop,
        )
        builder.addFloatProperty(
            "Speed",
            tt(lambda: math.hypot(self.chassis_speed.vx, self.chassis_speed.vy)),
            noop,
        )
