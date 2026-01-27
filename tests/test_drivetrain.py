import commands2.button
import wpilib.simulation
from commands2.button import CommandGenericHID
from pyfrc.util import yesno

from commands.drivetrain.driverelative import DriveRelative
from commands.drivetrain.resetgyro import ResetGyro
from commands.drivetrain.resetpose import ResetPose
from commands.drivetrain.drive import DriveField
from wpimath.geometry import Pose2d
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
    drive = DriveField(drivetrain, wpilib.simulation.XboxControllerSim(robot.hardware.drivetrain))
    xbox_remote = wpilib.simulation.XboxControllerSim(robot.hardware.controller)

    robot_controller.startTeleop()

    slow_cmd = drive.execute()
    slow_cmd.schedule()
    xbox_remote.setRightBumperButton(True)
