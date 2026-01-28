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
from ultime.tests import RobotTestController


def test_ResetGyro(robot_controller: RobotTestController, robot: Robot):
    robot_controller.startTeleop()
    robot_controller.wait(0.5)
    cmd = ResetGyro(robot.hardware.drivetrain, robot.quest_vision)
    cmd.schedule()
    robot_controller.wait(0.5)
    assert not cmd.isScheduled()


def test_ResetPose(robot_controller: RobotTestController, robot: Robot):
    robot_controller.startTeleop()
    robot_controller.wait(0.5)
    cmd = ResetPose(robot.hardware.drivetrain, Pose2d())
    cmd.schedule()
    robot_controller.wait(0.5)
    assert not cmd.isScheduled()


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
    drive = DriveField(drivetrain, robot.hardware.controller)
    reset_pose = ResetPose(drivetrain, Pose2d())

    robot_controller.startTeleop()

    # tests the robot moving plus the slow trigger
    slow_cmd = drive
    reset_cmd = reset_pose
    slow_cmd.schedule()
    xbox_remote.setLeftStickButton(True)
    robot_controller.wait(0.4)
    xbox_remote.setLeftStickButton(False)
    init_pose = drivetrain.getPose().translation()
    reset_cmd.schedule()
    xbox_remote.setRightBumperButton(True)
    xbox_remote.setLeftStickButton(True)
    robot_controller.wait(0.4)
    xbox_remote.setLeftStickButton(False)
    fin_pose = drivetrain.getPose().translation()
    assert fin_pose.x != init_pose.x
    assert fin_pose.y != init_pose.y
