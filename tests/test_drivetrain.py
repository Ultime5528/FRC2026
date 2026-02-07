import commands2.button
import wpilib.simulation
from commands2.button import CommandGenericHID
from pyfrc.util import yesno

from commands.drivetrain.driverelative import DriveRelative
from commands.drivetrain.resetgyro import ResetGyro
from commands.drivetrain.resetpose import ResetPose
from commands.drivetrain.drive import DriveField
from wpimath.geometry import Pose2d, Translation2d
from robot import Robot
from ultime.command import with_timeout
from ultime.tests import RobotTestController


def test_ResetGyro(robot_controller: RobotTestController, robot: Robot):
    drivetrain = robot.hardware.drivetrain
    xbox_remote = wpilib.simulation.XboxControllerSim(0)

    robot_controller.startTeleop()

    reset_cmd = ResetGyro(drivetrain, robot.quest_vision)
    robot_controller.run_command(reset_cmd.withTimeout(0.1), 3.0)
    init_pose = drivetrain.getPose()
    drive_cmd = DriveField(drivetrain, robot.hardware.controller)
    xbox_remote.setRightX(-1)
    robot_controller.run_command(drive_cmd.withTimeout(2.0), 3.0)
    reset_cmd = ResetGyro(drivetrain, robot.quest_vision)
    robot_controller.run_command(reset_cmd.withTimeout(0.1), 3.0)
    assert drivetrain.getPose().rotation() == init_pose.rotation()


def test_ResetPose(robot_controller: RobotTestController, robot: Robot):
    robot_controller.startTeleop()
    drivetrain = robot.hardware.drivetrain

    drive_cmd = DriveRelative.right(drivetrain)
    robot_controller.run_command(drive_cmd.withTimeout(2.0), 3.0)
    reset_cmd = ResetPose(drivetrain, Pose2d())
    robot_controller.run_command(reset_cmd.withTimeout(0.1), 3.0)
    assert drivetrain.getPose() == Pose2d()


def test_drive_relative(robot_controller: RobotTestController, robot: Robot):
    drivetrain = robot.hardware.drivetrain

    robot_controller.startTeleop()

    # Move left
    left_cmd = DriveRelative.left(drivetrain)
    left_cmd.schedule()
    robot_controller.wait_until(lambda: drivetrain.getPose().Y() >= 1, 5.0)

    # Move right
    right_cmd = DriveRelative.right(drivetrain)
    right_cmd.schedule()
    robot_controller.wait_until(lambda: drivetrain.getPose().Y() <= 0, 5.0)

    # Move forwards
    left_cmd = DriveRelative.forwards(drivetrain)
    left_cmd.schedule()
    robot_controller.wait_until(lambda: drivetrain.getPose().X() >= 1, 5.0)

    # Move backwards
    right_cmd = DriveRelative.backwards(drivetrain)
    right_cmd.schedule()
    robot_controller.wait_until(lambda: drivetrain.getPose().X() <= 0, 5.0)


def test_drivefield(robot_controller: RobotTestController, robot: Robot):
    drivetrain = robot.hardware.drivetrain
    xbox_remote = wpilib.simulation.XboxControllerSim(0)

    robot_controller.startTeleop()

    # tests the robot moving plus the slow trigger
    drive_cmd = DriveField(drivetrain, robot.hardware.controller)
    xbox_remote.setLeftX(1)
    robot_controller.run_command(drive_cmd.withTimeout(2.0), 3.0)

    init_pose = drivetrain.getPose().translation()
    reset_cmd = ResetPose(drivetrain, Pose2d())
    robot_controller.run_command(reset_cmd.withTimeout(0.1), 3.0)
    xbox_remote.setRightBumperButton(True)
    drive_cmd = DriveField(drivetrain, robot.hardware.controller)
    xbox_remote.setLeftX(1)
    robot_controller.run_command(drive_cmd.withTimeout(2.0), 3.0)
    fin_pose = drivetrain.getPose().translation()
    assert fin_pose.x < init_pose.x
