import math

import wpilib
import wpimath
from ntcore import NetworkTableInstance
from pathplannerlib.auto import AutoBuilder
from pathplannerlib.config import PIDConstants, RobotConfig
from pathplannerlib.controller import PPHolonomicDriveController
from pathplannerlib.path import PathPlannerPath, PathConstraints
from pathplannerlib.util import DriveFeedforwards
from rev import SparkBase
from wpilib import RobotBase, DriverStation
from wpimath.estimator import SwerveDrive4PoseEstimator
from wpimath.geometry import Pose2d, Translation2d, Rotation2d, Twist2d
from wpimath.kinematics import (
    ChassisSpeeds,
    SwerveDrive4Kinematics,
    SwerveModuleState,
    SwerveDrive4Odometry,
    SwerveModulePosition,
)

import ports
from ultime.alert import AlertType
from ultime.autoproperty import autoproperty
from ultime.gyro import ADIS16470
from ultime.modulerobot import is_simulation
from ultime.subsystem import Subsystem
from ultime.swerve.swerve import SwerveModule, SwerveDriveElasticSendable
from ultime.switch import Switch


class Drivetrain(Subsystem):
    width = 0.597
    length = 0.673
    p_gain_translation = 5.0
    p_gain_rotation = 5.0
    max_angular_speed = autoproperty(25.0)
    max_speed = autoproperty(5.0)

    angular_offset_fl = autoproperty(-1.57)
    angular_offset_fr = autoproperty(0.0)
    angular_offset_bl = autoproperty(3.14)
    angular_offset_br = autoproperty(1.57)

    period_seconds = 0.02

    def __init__(self) -> None:
        super().__init__()
        # Photocells
        self.photocell_left = Switch(
            Switch.Type.NormallyOpen, ports.DIO.drivetrain_photocell_left
        )
        self.photocell_right = Switch(
            Switch.Type.NormallyOpen, ports.DIO.drivetrain_photocell_right
        )

        self._sees_tower_left = self.createProperty(False)
        self._sees_tower_right = self.createProperty(False)

        # Swerve Module motor positions
        self.motor_fl_loc = Translation2d(self.width / 2, self.length / 2)
        self.motor_fr_loc = Translation2d(self.width / 2, -self.length / 2)
        self.motor_bl_loc = Translation2d(-self.width / 2, self.length / 2)
        self.motor_br_loc = Translation2d(-self.width / 2, -self.length / 2)

        self.swerve_module_fl = SwerveModule(
            ports.CAN.drivetrain_motor_driving_fl,
            ports.CAN.drivetrain_motor_turning_fl,
            self.angular_offset_fl,
        )

        self.swerve_module_fr = SwerveModule(
            ports.CAN.drivetrain_motor_driving_fr,
            ports.CAN.drivetrain_motor_turning_fr,
            self.angular_offset_fr,
        )

        self.swerve_module_bl = SwerveModule(
            ports.CAN.drivetrain_motor_driving_bl,
            ports.CAN.drivetrain_motor_turning_bl,
            self.angular_offset_bl,
        )

        self.swerve_module_br = SwerveModule(
            ports.CAN.drivetrain_motor_driving_br,
            ports.CAN.drivetrain_motor_turning_br,
            self.angular_offset_br,
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

        self.pp_holonomic_drive_controller = PPHolonomicDriveController(
            PIDConstants(self.p_gain_translation, 0.0, 0.0),
            PIDConstants(self.p_gain_rotation, 0.0, 0.0),
        )

        """
        Config used in the path following
        """
        config = RobotConfig.fromGUISettings()

        AutoBuilder.configure(
            self.getPose,
            self.resetToPose,
            self.getRobotRelativeChassisSpeeds,
            lambda speeds, feedforwards: self.driveFromChassisSpeeds(
                speeds, feedforwards
            ),
            self.pp_holonomic_drive_controller,
            config,
            self.shouldFlipPath,
            self,
        )

        """
        Config used only when path finding to a pose
        """
        self.pathfinding_constraints = PathConstraints(
            maxVelocityMps=3.0,
            maxAccelerationMpsSq=1.0,
            maxAngularVelocityRps=3.1415,
            maxAngularAccelerationRpsSq=3.1415,
        )

        self._estimated_pose: Pose2d = Pose2d()
        self._estimated_angle: Rotation2d = Rotation2d()
        self._chassis_speed: ChassisSpeeds = ChassisSpeeds()

        # Gyro
        """
        Possibilités : NavX, ADIS16448, ADIS16470, ADXRS, Empty
        """
        self._gyro = ADIS16470()
        # TODO Assert _gyro is subclass of abstract class Gyro
        self.addChild("Gyro", self._gyro)
        self._gyro_angles_radians = self.createProperty(0.0)
        self._gyro_rotation2d: Rotation2d = Rotation2d()

        self._field = wpilib.Field2d()
        wpilib.SmartDashboard.putData("Field", self._field)

        swerve_drive_sendable = SwerveDriveElasticSendable(
            self.swerve_module_fl,
            self.swerve_module_fr,
            self.swerve_module_bl,
            self.swerve_module_br,
            lambda: self._gyro_angles_radians,
        )
        wpilib.SmartDashboard.putData("SwerveDrive", swerve_drive_sendable)

        """
        Pose estimation
        """

        self.swerve_drive_kinematics = SwerveDrive4Kinematics(
            self.motor_fl_loc, self.motor_fr_loc, self.motor_bl_loc, self.motor_br_loc
        )

        self.swerve_odometry = SwerveDrive4Odometry(
            self.swerve_drive_kinematics,
            self._gyro_rotation2d,
            (
                SwerveModulePosition(),
                SwerveModulePosition(),
                SwerveModulePosition(),
                SwerveModulePosition(),
            ),
            Pose2d(0, 0, 0),
        )

        self.swerve_estimator = SwerveDrive4PoseEstimator(
            self.swerve_drive_kinematics,
            self._gyro_rotation2d,
            (
                SwerveModulePosition(),
                SwerveModulePosition(),
                SwerveModulePosition(),
                SwerveModulePosition(),
            ),
            Pose2d(0, 0, 0),
        )

        self.vision_pose = self._field.getObject("Vision Pose")
        self.odometry_pose = self._field.getObject("Odometry Pose")

        """
        Alerts
        """
        self.alerts_faults = {
            location: self.createAlert(
                f"{location} Swerve has active faults/warnings. Check for them on REV Hardware Client.",
                AlertType.Warning,
            )
            for location in self.swerve_modules.keys()
        }

        if is_simulation:
            self.sim_yaw = 0

    def seesTowerLeft(self) -> bool:
        return self._sees_tower_left

    def seesTowerRight(self) -> bool:
        return self._sees_tower_right

    def alignedToTower(self) -> bool:
        return self.seesTowerLeft() and self.seesTowerRight()

    def driveFromStickInputs(
        self,
        x_input: float,
        y_input: float,
        rot_input: float,
        is_field_relative: bool,
    ):
        """

        :param x_input: X axis input, between -1 (backwards) and 1 (forwards).
        :param y_input: Y axis input, between -1 (left) and 1 (right).
        :param rot_input: Z axis input, between -1 (clockwise) and 1 (anti-clockwise).
        :param is_field_relative: True if driving relative to the field (e.g. the pilot's perspective).
        :return:
        """
        x_speed = x_input * self.max_speed
        y_speed = y_input * self.max_speed
        rot_speed = rot_input * self.max_angular_speed

        if is_field_relative:
            chassis_speed = ChassisSpeeds.fromFieldRelativeSpeeds(
                x_speed, y_speed, rot_speed, self.getPose().rotation()
            )
        else:
            chassis_speed = ChassisSpeeds(x_speed, y_speed, rot_speed)

        self.driveFromChassisSpeeds(chassis_speed)

    def driveFromChassisSpeeds(
        self, speed: ChassisSpeeds, ff: DriveFeedforwards = None
    ):
        corrected_chassis_speed = self.correctForDynamics(speed)
        self.chassis_speed_goal = corrected_chassis_speed

        self.chassis_speed_goal_pub.set(corrected_chassis_speed)

        swerve_module_states = self.swerve_drive_kinematics.toSwerveModuleStates(
            corrected_chassis_speed
        )

        SwerveDrive4Kinematics.desaturateWheelSpeeds(
            swerve_module_states, self.max_speed
        )

        if ff is None:
            ff = DriveFeedforwards.zeros(4)

        self.swerve_module_fl.setDesiredSetpoint(
            swerve_module_states[0], ff.accelerationsMPS[0]
        )
        self.swerve_module_fr.setDesiredSetpoint(
            swerve_module_states[1], ff.accelerationsMPS[1]
        )
        self.swerve_module_bl.setDesiredSetpoint(
            swerve_module_states[2], ff.accelerationsMPS[2]
        )
        self.swerve_module_br.setDesiredSetpoint(
            swerve_module_states[3], ff.accelerationsMPS[3]
        )

    def getGyroAngleRadians(self):
        """
        Wrapped between -180 and 180
        """
        return self._gyro_angles_radians

    def getEstimatedAngle(self):
        return self._estimated_angle

    def resetGyro(self):
        self._gyro.reset()

    def getPose(self):
        return self._estimated_pose

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

    def readInputs(self):
        self._sees_tower_left = self.photocell_left.isPressed()
        self._sees_tower_right = self.photocell_right.isPressed()

        self.swerve_module_fl.readInputs()
        self.swerve_module_fr.readInputs()
        self.swerve_module_bl.readInputs()
        self.swerve_module_br.readInputs()

        self._estimated_pose = self.swerve_estimator.getEstimatedPosition()
        self._estimated_angle = self._estimated_pose.rotation()
        self._chassis_speed = self.swerve_drive_kinematics.toChassisSpeeds(
            (
                self.swerve_module_fl.getState(),
                self.swerve_module_fr.getState(),
                self.swerve_module_bl.getState(),
                self.swerve_module_br.getState(),
            )
        )

        self._gyro_angles_radians = self._gyro.getAngle()
        self._gyro_rotation2d = self._gyro.getRotation2d()

    def periodic(self):
        swerve_positions = (
            self.swerve_module_fl.getPosition(),
            self.swerve_module_fr.getPosition(),
            self.swerve_module_bl.getPosition(),
            self.swerve_module_br.getPosition(),
        )

        self.chassis_speed_pub.set(self._chassis_speed)
        self.swerve_estimator.update(self._gyro_rotation2d, swerve_positions)
        self.swerve_odometry.update(self._gyro_rotation2d, swerve_positions)

        self.odometry_pose.setPose(self.swerve_odometry.getPose())
        self._field.setRobotPose(self.swerve_estimator.getEstimatedPosition())

        for location, swerve_module in self.swerve_modules.items():
            if (
                swerve_module._driving_motor.hasActiveFault()
                or swerve_module._turning_motor.hasActiveFault()
                or swerve_module._driving_motor.hasActiveWarning()
                or swerve_module._turning_motor.hasActiveWarning()
            ):
                self.alerts_faults[location].set(True)
            else:
                self.alerts_faults[location].set(False)

    def simulationPeriodic(self):
        self.swerve_module_fl.simulationUpdate(self.period_seconds)
        self.swerve_module_fr.simulationUpdate(self.period_seconds)
        self.swerve_module_bl.simulationUpdate(self.period_seconds)
        self.swerve_module_br.simulationUpdate(self.period_seconds)

        chassis_rotation_speed = self._chassis_speed.omega
        self.sim_yaw += chassis_rotation_speed * self.period_seconds
        self._gyro.setSimAngle(math.degrees(self.sim_yaw))

    def getRobotRelativeChassisSpeeds(self):
        """
        Returns robot relative chassis speeds from current swerve module states
        """
        return self._chassis_speed

    def resetToPose(self, pose: Pose2d):
        self.swerve_estimator.resetPosition(
            self._gyro_rotation2d,
            (
                self.swerve_module_fl.getPosition(),
                self.swerve_module_fr.getPosition(),
                self.swerve_module_bl.getPosition(),
                self.swerve_module_br.getPosition(),
            ),
            pose,
        )

    def addVisionMeasurement(
        self,
        pose: wpimath.geometry.Pose2d,
        timestamp: float,
        std_devs: tuple[float, float, float],
    ):
        self.swerve_estimator.addVisionMeasurement(pose, timestamp, std_devs)
        self.vision_pose.setPose(pose)

    def getCurrentDrawAmps(self):
        return 0.0

    def shouldFlipPath(self):
        return DriverStation.getAlliance() == DriverStation.Alliance.kRed

    def getFollowCommand(self, path: PathPlannerPath):
        return AutoBuilder.followPath(path)

    def getPathFindingCommand(self, pose: Pose2d):
        # TODO adjust the "goal_end_vel" if wanted for a smoother "AlignPreciseAfterPath"
        return AutoBuilder.pathfindToPose(
            pose=pose, constraints=self.pathfinding_constraints, goal_end_vel=0.0
        )

    def getPathFindingFollowPathCommand(self, path: PathPlannerPath):
        return AutoBuilder.pathfindThenFollowPath(
            goal_path=path, pathfinding_constraints=self.pathfinding_constraints
        )

    def logValues(self):
        self.log(
            "speed_goal",
            math.hypot(self.chassis_speed_goal.vx, self.chassis_speed_goal.vy),
        )
        self.log("speed", math.hypot(self._chassis_speed.vx, self._chassis_speed.vy))
