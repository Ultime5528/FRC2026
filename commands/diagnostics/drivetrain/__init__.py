from commands2 import SequentialCommandGroup

from commands.diagnostics.drivetrain.odometry import DiagnoseOdometry
from commands.diagnostics.drivetrain.swerve import DiagnoseSwerveModule
from subsystems.drivetrain import Drivetrain
from ultime.command import ignore_requirements


@ignore_requirements(["drivetrain"])
class DiagnoseDrivetrain(SequentialCommandGroup):
    def __init__(self, drivetrain: Drivetrain):
        super().__init__(
            *(
                DiagnoseSwerveModule(
                    location,
                    swerve_module,
                    drivetrain.alerts_drive_encoder[location],
                    drivetrain.alerts_turning_motor[location],
                )
                for location, swerve_module in drivetrain.swerve_modules.items()
            ),
            DiagnoseOdometry(drivetrain),
        )
