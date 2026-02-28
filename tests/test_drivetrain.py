import commands2.button
import wpilib.simulation
from _pytest.python_api import approx
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

    reset_cmd = ResetGyro(drivetrain)
    robot_controller.run_command(reset_cmd.withTimeout(0.1), 3.0)
    init_pose = drivetrain.getPose()
    drive_cmd = DriveField(drivetrain, robot.hardware.controller)
    xbox_remote.setRightX(-1)
    robot_controller.run_command(drive_cmd.withTimeout(2.0), 3.0)
    reset_cmd = ResetGyro(drivetrain)
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

    drivetrain.resetToPose(Pose2d())

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

    drivetrain.resetToPose(Pose2d())

    # tests the robot moving plus the slow trigger
    drive_cmd = DriveField(drivetrain, robot.hardware.controller)
    xbox_remote.setLeftX(1)
    xbox_remote.setLeftY(1)
    robot_controller.run_command(drive_cmd.withTimeout(10.0), 11.0)

    init_pose = drivetrain.getPose()
    assert abs(init_pose.x) == approx(65.0, abs=3.0)
    assert abs(init_pose.y) == approx(65.0, abs=3.0)

    xbox_remote.setRightBumperButton(True)
    drive_cmd = DriveField(drivetrain, robot.hardware.controller)
    xbox_remote.setLeftX(-1)
    xbox_remote.setLeftY(-1)
    robot_controller.run_command(drive_cmd.withTimeout(10.0), 11.0)

    fin_pose = drivetrain.getPose()
    assert abs(fin_pose.x) == approx(52.0, abs=3.0)
    assert abs(fin_pose.y) == approx(52.0, abs=3.0)
    assert abs(init_pose.y - fin_pose.y) == approx(abs(init_pose.y / 5), abs=3.0)

    robot_controller.run_command(ResetGyro(drivetrain).withTimeout(0.1), 0.3)
    xbox_remote.setRightBumperButton(False)
    xbox_remote.setLeftX(0)
    xbox_remote.setLeftY(0)
    xbox_remote.setRightX(1)

    drive_cmd = DriveField(drivetrain, robot.hardware.controller)
    robot_controller.run_command(drive_cmd.withTimeout(3.0), 4.0)
    assert abs(drivetrain.getPose().rotation().degrees()) == approx(90.0, abs=10.0)
