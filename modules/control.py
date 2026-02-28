from commands.climber.move import MoveClimber, ManualMoveClimber, ResetClimber
from commands.drivetrain.driverelative import DriveRelative
from commands.drivetrain.resetgyro import ResetGyro
from commands.feeder.grabfuel import GrabFuel
from commands.feeder.ejectfuel import EjectFuel
from commands.hugandclimb import HugAndClimb
from commands.pivot.move import MovePivot
from commands.retractandunhug import RetractAndUnhug
from commands.shooter.shoot import Shoot
from modules.hardware import HardwareModule
from ultime.module import Module


class ControlModule(Module):
    def __init__(
        self,
        hardware: HardwareModule,
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

        """
        Copilot's panel
        """

        # Intake
        hardware.panel_1.povUp().onTrue(MovePivot.toDown(hardware.pivot))

        hardware.panel_1.povDown().onTrue(MovePivot.toUp(hardware.pivot))

        hardware.panel_1.povRight().onTrue(GrabFuel(hardware.feeder))

        # Shooter
        hardware.panel_1.povLeft().onTrue(Shoot(hardware.shooter))

        # Climber
        hardware.panel_1.button(6).onTrue(MoveClimber.toReady(hardware.climber))

        hardware.panel_1.button(4).onTrue(
            HugAndClimb(hardware.climber, hardware.hugger)
        )

        hardware.panel_1.button(3).onTrue(
            RetractAndUnhug(hardware.climber, hardware.hugger)
        )

        hardware.panel_1.button(5).onTrue(ResetClimber.down(hardware.climber))

        # ResetGyro

        hardware.panel_1.button(2).onTrue(
            ResetGyro(hardware.drivetrain)
        )

        # ResetAll

        hardware.panel_1.button(1)