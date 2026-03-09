from commands2.cmd import parallel

from commands.autonomous.towerclimb import TowerClimb
from commands.climber.move import MoveClimber, ManualMoveClimber, ResetClimber
from commands.drivetrain.driverelative import DriveRelative
from commands.drivetrain.resetgyro import ResetGyro
from commands.feeder.grabfuel import GrabFuel
from commands.feeder.ejectfuel import EjectFuel
from commands.hugandclimb import HugAndClimb
from commands.hugger.unhug import Unhug
from commands.pivot.move import ManualMovePivot
from commands.resetall import ResetAll
from commands.retractandunhug import RetractAndUnhug
from commands.shooter.shoot import Shoot
from commands.alignshoot import AlignShoot
from modules.hardware import HardwareModule
from modules.shootercalcmodule import ShooterCalcModule
from ultime.module import Module


class ControlModule(Module):
    def __init__(
        self,
        hardware: HardwareModule,
        shooter_calc_module: ShooterCalcModule,
    ):
        super().__init__()

        """
        Pilot's buttons
        """
        hardware.controller.povLeft().whileTrue(DriveRelative.left(hardware.drivetrain))
        hardware.controller.povRight().whileTrue(
            DriveRelative.right(hardware.drivetrain)
        )
        hardware.controller.povUp().whileTrue(
            DriveRelative.forwards(hardware.drivetrain)
        )
        hardware.controller.povDown().whileTrue(
            DriveRelative.backwards(hardware.drivetrain)
        )

        hardware.controller.leftBumper().whileTrue(TowerClimb.right(hardware))

        """
        Copilot's panel
        """

        # Intake
        hardware.panel_1.povRight().whileTrue(ManualMovePivot.down(hardware.pivot))

        hardware.panel_1.povLeft().whileTrue(ManualMovePivot.up(hardware.pivot))

        hardware.panel_1.povUp().whileTrue(GrabFuel(hardware.feeder))

        # Shooter
        hardware.panel_1.povDown().whileTrue(
            AlignShoot(
                hardware.shooter,
                hardware.drivetrain,
                hardware.pivot,
                hardware.feeder,
                hardware.controller,
                shooter_calc_module,
            )
        )

        # Climber
        hardware.panel_1.button(6).onTrue(
            parallel(MoveClimber.toReady(hardware.climber), Unhug(hardware.hugger))
        )

        # TODO Ancien bouton Reset du climber, libre pour autre chose
        # hardware.panel_1.button(4).onTrue(
        #     HugAndClimb(hardware.climber, hardware.hugger)
        # )

        hardware.panel_1.button(3).onTrue(ResetClimber.down(hardware.climber))

        hardware.panel_1.button(5).onTrue(ResetClimber.down(hardware.climber))

        # ResetGyro

        hardware.panel_1.button(2).onTrue(ResetGyro(hardware.drivetrain))

        # ResetAll

        hardware.panel_1.button(1).onTrue(
            ResetAll(hardware.climber, hardware.hugger, hardware.guide)
        )
