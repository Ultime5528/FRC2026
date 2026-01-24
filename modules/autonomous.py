from _weakref import proxy
from typing import Optional

import commands2
from commands2 import Command
from pathplannerlib.auto import NamedCommands, AutoBuilder
from pathplannerlib.config import RobotConfig, PIDConstants
from pathplannerlib.controller import PPHolonomicDriveController
from wpilib import DriverStation, SmartDashboard, SendableChooser

from modules.hardware import HardwareModule
from ultime.command import WaitCommand
from ultime.module import Module

p_gain_translation = 5.0
p_gain_rotation = 5.0


def registerNamedCommand(command: Command):
    NamedCommands.registerCommand(command.getName(), command)


class AutonomousModule(Module):
    def __init__(self, hardware: HardwareModule):
        super().__init__()
        self.hardware = proxy(hardware)

        self.auto_command: Optional[commands2.Command] = None

        config = RobotConfig.fromGUISettings()

        AutoBuilder.configure(
            hardware.drivetrain.getPose,
            hardware.drivetrain.resetToPose,
            hardware.drivetrain.getRobotRelativeChassisSpeeds,
            lambda speeds, feedforwards: hardware.drivetrain.driveFromChassisSpeeds(
                speeds, feedforwards
            ),
            PPHolonomicDriveController(
                PIDConstants(p_gain_translation, 0.0, 0.0),
                PIDConstants(p_gain_rotation, 0.0, 0.0),
            ),
            config,
            self.shouldFlipPath,
            hardware.drivetrain,
        )

        self.auto_chooser = SendableChooser()
        self.auto_chooser.setDefaultOption("Nothing", WaitCommand(0.0))

    def shouldFlipPath(self):
        return DriverStation.getAlliance() == DriverStation.Alliance.kRed

    def autonomousInit(self):
        self.hardware.drivetrain.swerve_odometry.resetPose(
            self.hardware.drivetrain.getPose()
        )

        self.auto_command: commands2.Command = self.auto_chooser.getSelected()
        if self.auto_command:
            self.auto_command.schedule()

    def autonomousExit(self):
        if self.auto_command:
            self.auto_command.cancel()
