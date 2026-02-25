from commands.drivetrain.driverelative import DriveRelative
from commands.feeder.grabfuel import GrabFuel
from commands.feeder.ejectfuel import EjectFuel
from commands.pivot.move import MovePivot
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

        #Intake
        hardware.panel_2.povUp().onTrue(MovePivot.toDown(hardware.pivot))

        hardware.panel_2.povDown().onTrue(MovePivot.toUp(hardware.pivot))

        hardware.panel_2.povRight().onTrue(GrabFuel(hardware.feeder))

        #Shooter
        hardware.panel_2.povLeft().onTrue(Shoot(hardware.shooter))


