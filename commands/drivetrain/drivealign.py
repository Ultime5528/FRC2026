import math

import commands2.button
from wpilib import DriverStation
from wpimath.geometry import Rotation2d

from modules.shootercalcmodule import ShooterCalcModule
from subsystems.drivetrain import Drivetrain
from ultime.autoproperty import autoproperty
from ultime.command import Command


def apply_center_distance_deadzone(x_dist, y_dist, deadzone):
    hypot = math.hypot(x_dist, y_dist)
    if hypot <= deadzone:
        return 0.0, 0.0, 0.0
    else:
        return x_dist, y_dist, hypot


def apply_linear_deadzone(_input, deadzone):
    if abs(_input) <= deadzone:
        return 0.0
    else:
        return _input


class DriveAlign(Command):
    rotation_deadzone = autoproperty(0.3)
    rotate_speed = autoproperty(0.00375)
    slow_speed_multiplier = autoproperty(0.33)
    moving_deadzone = autoproperty(0.1)

    def __init__(
        self,
        drivetrain: Drivetrain,
        shooter_calc_module : ShooterCalcModule,
        xbox_remote: commands2.button.CommandXboxController,
    ):
        super().__init__()
        self.addRequirements(drivetrain)
        self.xbox_remote = xbox_remote
        self.drivetrain = drivetrain
        self.shooter_calc_module = shooter_calc_module

    def execute(self):
        is_red = DriverStation.getAlliance() == DriverStation.Alliance.kRed

        x_speed, y_speed, _ = apply_center_distance_deadzone(
            self.xbox_remote.getLeftY() * -1,
            self.xbox_remote.getLeftX() * -1,
            self.moving_deadzone,
        )

        rot = self.shooter_calc_module.getRotationToAlignWithTarget()

        rot_speed = (
            rot.degrees()
            * self.rotate_speed
        )

        if is_red:
            x_speed *= -1
            y_speed *= -1

        if self.xbox_remote.rightBumper():
            x_speed *= self.slow_speed_multiplier
            y_speed *= self.slow_speed_multiplier

        self.drivetrain.driveFromStickInputs(x_speed, y_speed, rot_speed, True)

    def end(self, interrupted: bool) -> None:
        self.drivetrain.stop()
