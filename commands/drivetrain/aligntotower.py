import wpilib

from commands.drivetrain.driverelative import DriveRelative
from subsystems.drivetrain import Drivetrain
from ultime.autoproperty import autoproperty
from ultime.command import Command


class AlignToTower(Command):
    speed_side = autoproperty(0.1)
    speed_front = autoproperty(0.1)
    time = autoproperty(0.3)

    def __init__(self, drivetrain: Drivetrain):
        super().__init__()
        self.drivetrain = drivetrain
        self.addRequirements(self.drivetrain)
        self.timer = wpilib.Timer()

    def initialize(self):
        self.timer.reset()

    def execute(self):
        if self.drivetrain.alignedToTower():
            self.drivetrain.driveFromStickInputs(-self.speed_front, 0, 0, False)
            self.timer.start()
        else:
            self.timer.reset()
            self.timer.stop()
            if self.drivetrain.seesTowerLeft():
                self.drivetrain.driveFromStickInputs(
                    -self.speed_front, -self.speed_side, 0, False
                )
            elif self.drivetrain.seesTowerRight():
                self.drivetrain.driveFromStickInputs(
                    -self.speed_front, self.speed_side, 0, False
                )
            else:
                self.drivetrain.driveFromStickInputs(-self.speed_front, 0, 0, False)

    def isFinished(self) -> bool:
        return self.timer.hasElapsed(self.time)

    def end(self, interrupted: bool):
        self.timer.stop()
        self.drivetrain.stop()
