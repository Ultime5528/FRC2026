import commands2
from wpilib import PowerDistribution, RobotBase

from commands.drivetrain.drive import DriveField
from subsystems.drivetrain import Drivetrain
from ultime.module import Module
from ultime.subsystem import Subsystem
from ultime.swerve.swerveIO import SwerveIOSpark, SwerveIOSim


class HardwareModule(Module):
    def __init__(self):
        super().__init__()
        self.controller = commands2.button.CommandXboxController(0)
        self.panel_1 = commands2.button.CommandJoystick(1)
        self.panel_2 = commands2.button.CommandJoystick(2)

        if RobotBase.isSimulation():
            self.drivetrain = Drivetrain(SwerveIOSim)
        else:
            self.drivetrain = Drivetrain(SwerveIOSpark)
        self.drivetrain.setDefaultCommand(DriveField(self.drivetrain, self.controller))

        self.pdp = PowerDistribution()

        self.subsystems: list[Subsystem] = [
            self.drivetrain,
        ]
