import commands2
from wpilib import PowerDistribution

from commands.drivetrain.drive import DriveField
from subsystems.drivetrain import Drivetrain
from subsystems.intake import Intake
from ultime.module import Module
from ultime.subsystem import Subsystem


class HardwareModule(Module):
    def __init__(self):
        super().__init__()
        self.controller = commands2.button.CommandXboxController(0)
        self.panel_1 = commands2.button.CommandJoystick(1)
        self.panel_2 = commands2.button.CommandJoystick(2)

        self.drivetrain = Drivetrain()
        self.drivetrain.setDefaultCommand(DriveField(self.drivetrain, self.controller))
        self.intake = Intake()
        self.pdp = PowerDistribution()

        self.subsystems: list[Subsystem] = [
            self.drivetrain,
            self.intake,
        ]
