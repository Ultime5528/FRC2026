from commands2 import SequentialCommandGroup
from commands2.cmd import deadline, sequence
from wpimath.geometry import Pose2d, Rotation2d, Transform2d

from commands.drivetrain.drivetoposes import DriveToPoses
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

        angle = shooter_calc_module.getAngleToAlignWithTarget()
        transform = Transform2d(0.0, 0.0, Rotation2d(angle))

        rotated_robot_pose = [robot_pose + transform]

        def goto(pose: list[Pose2d]):
            return DriveToPoses(drivetrain, pose)

        self.addCommands(
            sequence(
                deadline(
                    PrepareShoot(shooter, shooter_calc_module), goto(rotated_robot_pose)
                ),
                Shoot(shooter, shooter_calc_module),
            )
        )
