import commands2
from commands2 import ParallelCommandGroup
from commands2.cmd import repeatingSequence, sequence, parallel

from commands.drivetrain.drivealign import DriveAlign
from commands.feeder.grabfuel import GrabFuel
from commands.pivot.move import ManualMovePivot
from commands.shooter.shoot import Shoot
from modules.shootercalcmodule import ShooterCalcModule
from subsystems.drivetrain import Drivetrain
from subsystems.feeder import Feeder
from subsystems.pivot import Pivot
from subsystems.shooter import Shooter
from ultime.command import WaitCommand


class AlignShoot(ParallelCommandGroup):
    def __init__(
        self,
        shooter: Shooter,
        drivetrain: Drivetrain,
        pivot: Pivot,
        feeder: Feeder,
        xbox_remote: commands2.button.CommandXboxController,
        shooter_calc_module: ShooterCalcModule,
    ):
        super().__init__()
        self.addCommands(
            Shoot(shooter, shooter_calc_module),
            DriveAlign(drivetrain, shooter_calc_module, xbox_remote),
            GrabFuel(feeder),
            sequence(
                WaitCommand(2.0),
                parallel(
                    repeatingSequence(
                        ManualMovePivot.up(pivot).withTimeout(0.4),
                        ManualMovePivot.down(pivot).withTimeout(0.2),
                        WaitCommand(0.4),
                    ),
                ),
            ),
        )
