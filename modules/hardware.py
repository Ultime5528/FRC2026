import commands2
from wpilib import PowerDistribution

from commands.climber.maintainclimber import MaintainClimber
from commands.drivetrain.drive import DriveField
from commands.pivot.maintainpivot import MaintainPivot
from subsystems.climber import Climber
from subsystems.drivetrain import Drivetrain
from subsystems.feeder import Feeder
from subsystems.guide import Guide
from subsystems.hugger import Hugger
from subsystems.pivot import Pivot
from subsystems.shooter import Shooter
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

        self.climber = self.addSubsystem(Climber())
        self.hugger = self.addSubsystem(Hugger())
        self.guide = self.addSubsystem(Guide())
        self.shooter = self.addSubsystem(Shooter())
        self.feeder = self.addSubsystem(Feeder())
        self.pivot = self.addSubsystem(Pivot())
        #self.pivot.setDefaultCommand(MaintainPivot(self.pivot))

        self.pdp = PowerDistribution()

    def teleopInit(self) -> None:
        self.shooter.updatePIDFConfig()

    def addSubsystem[T: Subsystem](self, subsystem: T) -> T:
        self.subsystems.append(subsystem)
        return subsystem
