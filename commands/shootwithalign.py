from commands2 import SequentialCommandGroup
from commands2.cmd import deadline, sequence
from wpimath.geometry import Pose2d

from commands.drivetrain.drivetoposes import  DriveToPoses
from commands.shooter.prepareshoot import PrepareShoot
from commands.shooter.shoot import Shoot
from modules.hardware import HardwareModule
from modules.shootercalcmodule import ShooterCalcModule



class ShootWithAlign(SequentialCommandGroup):
    def __init__(
        self, hardware: HardwareModule, shooter_calc_module: ShooterCalcModule
    ):
        super().__init__()

        drivetrain = hardware.drivetrain
        shooter = hardware.shooter

        robot_pose = drivetrain.getPose()
        robot_position = robot_pose.translation()
        robot_rotation = robot_pose.rotation()

        angle = ShooterCalcModule.getAngleToAlignWithTarget()

        rotated_robot_pose = [Pose2d(robot_position, robot_rotation + angle)]

        def goto(pose: list[Pose2d]):
            return DriveToPoses(pose, drivetrain)

        self.addCommands(
            sequence(
                deadline(
                    PrepareShoot(shooter, shooter_calc_module), goto(rotated_robot_pose)
                ),
                Shoot(shooter),
            )
        )
