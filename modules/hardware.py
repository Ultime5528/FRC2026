import commands2
from wpilib import PowerDistribution, RobotBase

from commands.drivetrain.drive import DriveField
from subsystems.drivetrain import Drivetrain
from subsystems.drivetrainio import DrivetrainIo, DrivetrainIoSim
from ultime.module import Module
from ultime.subsystem import Subsystem
from ultime.swerve.swervemoduleio import SwerveModuleIo, SwerveModuleIoSim


class HardwareModule(Module):
    def __init__(self):
        super().__init__()
        self.controller = commands2.button.CommandXboxController(0)
        self.panel_1 = commands2.button.CommandJoystick(1)
        self.panel_2 = commands2.button.CommandJoystick(2)

        if RobotBase.isSimulation():
            self.drivetrain = Drivetrain(DrivetrainIoSim())
        else:
            self.drivetrain = Drivetrain(DrivetrainIo())
        self.drivetrain.setDefaultCommand(DriveField(self.drivetrain, self.controller))

        self.pdp = PowerDistribution()

        self.subsystems: list[Subsystem] = [
            self.drivetrain,
        ]
