import wpilib
from wpimath.geometry import Pose2d

from commands.drivetrain.driverelative import DriveRelative
from commands.drivetrain.resetgyro import ResetGyro
from commands.drivetrain.resetpose import ResetPose
from robot import Robot
from ultime.tests import RobotTestController


def test_ResetGyro(robot_controller: RobotTestController, robot: Robot):

    drivetrain = robot.hardware.drivetrain
    xbox_remote = wpilib.simulation.XboxControllerSim(0)

    robot_controller.startTeleop()

    reset_cmd = ResetGyro(drivetrain)
    robot_controller.run_command(reset_cmd, 10.0)
    init_pose = drivetrain.getPose()

    xbox_remote.setRightX(-1)
    robot_controller.wait(1.0)

    # Wait a bit until the robot stops moving
    xbox_remote.setRightX(0.0)
    robot_controller.wait(1.0)

    reset_cmd = ResetGyro(drivetrain)
    robot_controller.run_command(reset_cmd, 10.0)
    assert drivetrain.getPose().rotation() == init_pose.rotation()


def test_ResetPose(robot_controller: RobotTestController, robot: Robot):

    robot_controller.startTeleop()
    drivetrain = robot.hardware.drivetrain

    drivetrain.removeDefaultCommand()

    drive_cmd = DriveRelative.right(drivetrain)
    robot_controller.run_command(drive_cmd.withTimeout(2.0), 3.0)

    # Wait a bit until the robot stops moving
    robot_controller.wait(1.0)

    reset_cmd = ResetPose(drivetrain, Pose2d())
    robot_controller.run_command(reset_cmd, 3.0)
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


# The drivetrain is erratic in sim, so the tests can't possibly work for now.
# All the test should be revised once the bug has been found: no need to use
# abs(...), use way smaller absolute errors, some tests are nonsensical.
# Finally, since the DriveField is the default command for the Drivetrain,
# we shouldn't start a new one for the test.

# def test_drivefield(robot_controller: RobotTestController, robot: Robot):
#     drivetrain = robot.hardware.drivetrain
#     xbox_remote = wpilib.simulation.XboxControllerSim(0)
#
#     robot_controller.startTeleop()
#
#     drivetrain.resetToPose(Pose2d())
#
#     # tests the robot moving plus the slow trigger
#     drive_cmd = DriveField(drivetrain, robot.hardware.controller)
#     xbox_remote.setLeftX(1)
#     xbox_remote.setLeftY(1)
#     robot_controller.run_command(drive_cmd.withTimeout(10.0), 11.0)
#
#     init_pose = drivetrain.getPose()
#     assert abs(init_pose.x) == approx(65.0, abs=3.0)
#     assert abs(init_pose.y) == approx(65.0, abs=3.0)
#
#     xbox_remote.setRightBumperButton(True)
#     drive_cmd = DriveField(drivetrain, robot.hardware.controller)
#     xbox_remote.setLeftX(-1)
#     xbox_remote.setLeftY(-1)
#     robot_controller.run_command(drive_cmd.withTimeout(10.0), 11.0)
#
#     fin_pose = drivetrain.getPose()
#     assert abs(fin_pose.x) == approx(52.0, abs=3.0)
#     assert abs(fin_pose.y) == approx(52.0, abs=3.0)
#     assert abs(init_pose.y - fin_pose.y) == approx(abs(init_pose.y / 5), abs=3.0)
#
#     robot_controller.run_command(ResetGyro(drivetrain).withTimeout(0.1), 0.3)
#     xbox_remote.setRightBumperButton(False)
#     xbox_remote.setLeftX(0)
#     xbox_remote.setLeftY(0)
#     xbox_remote.setRightX(1)
#
#     drive_cmd = DriveField(drivetrain, robot.hardware.controller)
#     robot_controller.run_command(drive_cmd.withTimeout(10.0), 11.0)
#     assert abs(drivetrain.getPose().rotation().degrees()) == approx(90.0, abs=10.0)
