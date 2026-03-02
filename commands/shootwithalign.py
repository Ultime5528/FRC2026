from commands2 import SequentialCommandGroup, Command
from commands2.cmd import deadline, sequence, race
from wpimath.geometry import Pose2d, Rotation2d, Transform2d

from commands.drivetrain.drivealign import DriveAlign
from commands.drivetrain.drivetoposes import DriveToPoses
from commands.shooter.prepareshoot import PrepareShoot
from commands.shooter.shoot import Shoot
from modules.hardware import HardwareModule
from modules.shootercalcmodule import ShooterCalcModule
from subsystems.drivetrain import Drivetrain
from subsystems.shooter import Shooter


class ShootWithAlign(SequentialCommandGroup):
    def __init__(
        self,
        shooter: Shooter,
        drivetrain: Drivetrain,
        xbox_remote,
        shooter_calc_module: ShooterCalcModule,
    ):
        super().__init__()
        self.addCommands(
            race(
                Shoot(shooter, shooter_calc_module),
                DriveAlign(drivetrain, shooter_calc_module, xbox_remote),
                # TODO condition d'arrêt
            ),
        )
