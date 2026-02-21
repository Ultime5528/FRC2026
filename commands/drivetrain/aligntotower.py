from commands.drivetrain.driverelative import DriveRelative
from subsystems.drivetrain import Drivetrain
from ultime.autoproperty import autoproperty
from ultime.command import Command


class AlignToTower(Command):
    speed = autoproperty(0.05)

    def __init__(self, drivetrain: Drivetrain):
        super().__init__()
        self.drivetrain = drivetrain
        self.addRequirements(self.drivetrain)

    def execute(self):
        if self.drivetrain.seesTowerLeft():
            self.drivetrain.driveFromStickInputs(
                0, self.speed, 0, False
            )
        elif self.drivetrain.seesTowerRight():
            self.drivetrain.driveFromStickInputs(
                0, -self.speed, 0, False
            )
        else:
            self.drivetrain.stop()

    def isFinished(self) -> bool:
        return self.drivetrain.alignedToTower() or (
            not self.drivetrain.seesTowerRight() and not self.drivetrain.seesTowerLeft()
        )

    def end(self, interrupted: bool):
        self.drivetrain.stop()
