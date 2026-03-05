import commands2
from commands2 import ParallelCommandGroup
from commands2.cmd import repeatingSequence, sequence, parallel

from commands.drivetrain.drivealign import DriveAlign
from commands.feeder.grabfuel import GrabFuel
from commands.pivot.move import MovePivot
from commands.shooter.shoot import Shoot
from modules.shootercalcmodule import ShooterCalcModule
from subsystems.drivetrain import Drivetrain
from subsystems.feeder import Feeder
from subsystems.pivot import Pivot
from subsystems.shooter import Shooter
from ultime.autoproperty import autoproperty
from ultime.command import WaitCommand


class ShootWithAlign(ParallelCommandGroup):
    wait_delay = autoproperty(3.0)
    move_pivot_delay = autoproperty(1.0)

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
            sequence(
                WaitCommand(self.wait_delay),
                parallel(
                    GrabFuel(feeder),
                    MovePivot.toUp(pivot)
                )
            )
            # sequence(
            #     WaitCommand(lambda: self.wait_delay),
            #     repeatingSequence(
            #         MovePivot.toUp(pivot).withTimeout(lambda: self.move_pivot_delay),
            #         MovePivot.toDown(pivot).withTimeout(lambda: self.move_pivot_delay),
            #     ),
            # ),
        )
