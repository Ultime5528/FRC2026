import commands2
from commands2 import SequentialCommandGroup
from commands2.cmd import sequence, race, parallel, repeatingSequence

from commands.drivetrain.drivealign import DriveAlign
from commands.pivot.move import MovePivot
from commands.shooter.shoot import Shoot
from modules.shootercalcmodule import ShooterCalcModule
from subsystems.drivetrain import Drivetrain
from subsystems.pivot import Pivot
from subsystems.shooter import Shooter
from ultime.autoproperty import autoproperty
from ultime.command import WaitCommand


class ShootWithAlign(SequentialCommandGroup):
    wait_delay = autoproperty(3.0)

    def init(
        self,
        shooter: Shooter,
        drivetrain: Drivetrain,
        pivot: Pivot,
        xbox_remote: commands2.button.CommandXboxController,
        shooter_calc_module: ShooterCalcModule,
    ):
        super().init()
        self.addCommands(
            race(
                race(
                    Shoot(shooter, shooter_calc_module),
                    DriveAlign(drivetrain, shooter_calc_module, xbox_remote),
                    # TODO condition d'arrêt
                ),
                sequence(
                    WaitCommand(self.wait_delay),
                    repeatingSequence(
                        MovePivot.toUp(pivot),
                        MovePivot.toDown(pivot),
                    ),
                ),
            )
        )
