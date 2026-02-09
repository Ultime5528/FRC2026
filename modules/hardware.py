import commands2
from wpilib import PowerDistribution

from commands.drivetrain.drive import DriveField
from subsystems.drivetrain import Drivetrain
from subsystems.guide import Guide
from subsystems.intake import Intake
from ultime.module import Module
from ultime.subsystem import Subsystem


class HardwareModule(Module):
    def __init__(self):
        super().__init__()
        self.subsystems: list[Subsystem] = []

        self.controller = commands2.button.CommandXboxController(0)
        self.panel_1 = commands2.button.CommandJoystick(1)
        self.panel_2 = commands2.button.CommandJoystick(2)

        self.drivetrain = self.addSubsystem(Drivetrain())
        self.drivetrain.setDefaultCommand(DriveField(self.drivetrain, self.controller))

        self.guide = self.addSubsystem(Guide())

        self.pdp = PowerDistribution()

    def addSubsystem[T: Subsystem](self, subsystem: T) -> T:
        self.subsystems.append(subsystem)
        return subsystem
