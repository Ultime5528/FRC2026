import wpilib
from commands2 import Command
from wpilib import DataLogManager

from subsystems.drivetrain import Drivetrain
from ultime.autoproperty import autoproperty


class DiagnoseOdometry(Command):
    position_delta_threshold = autoproperty(0.3)

    def __init__(self, drivetrain: Drivetrain):
        super().__init__()
        self.addRequirements(drivetrain)
        self.drivetrain = drivetrain

        self.timer = wpilib.Timer()
        self.initial_pose = None
        self.final_pose = None

    def initialize(self):
        self.timer.reset()
        self.timer.start()
        self.initial_pose = self.drivetrain.getPose()

    def execute(self):
        if self.timer.get() < 1:
            self.drivetrain.drive(0.1, 0, 0, False)
        elif self.timer.get() < 2:
            self.drivetrain.drive(0, 0.1, 0, False)
        elif self.timer.get() < 3:
            self.drivetrain.drive(-0.1, 0, 0, False)
        elif self.timer.get() < 4:
            self.drivetrain.drive(0, -0.1, 0, False)

    def isFinished(self) -> bool:
        return self.timer.get() > 4

    def end(self, interrupted: bool):
        self.drivetrain.stop()
        self.final_pose = self.drivetrain.getPose()
        magnitude_delta = self.initial_pose.translation().distance(
            self.final_pose.translation()
        )
        DataLogManager.log(
            "Drivetrain diagnostics: magnitude delta " + str(magnitude_delta)
        )
        if magnitude_delta > self.position_delta_threshold:
            self.drivetrain.alert_odometry.set(True)
