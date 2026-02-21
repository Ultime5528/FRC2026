from commands import DriveRelative
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
