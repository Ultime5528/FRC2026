import commands2
import wpilib
from commands2 import CommandScheduler
from wpilib import SmartDashboard

from commands.drivetrain.driverelative import DriveRelative
from commands.drivetrain.resetgyro import ResetGyro
from commands.guide import ManualMoveGuide, ResetGuide, MoveGuide
from commands.feeder.grabfuel import GrabFuel
from commands.pivot.maintainpivot import MaintainPivot
from commands.feeder.ejectfuel import EjectFuel
from commands.pivot.move import MovePivot, ResetIntake, ManualMovePivot
from modules.autonomous import AutonomousModule
from modules.hardware import HardwareModule
from modules.questvision import QuestVisionModule
from ultime.module import Module, ModuleList


class DashboardModule(Module):
    def __init__(
        self,
        hardware: HardwareModule,
        quest: QuestVisionModule,
        autonomous: AutonomousModule,
        module_list: ModuleList,
    ):
        super().__init__()
        self._hardware = hardware
        self._module_list = module_list
        self.setupCopilotCommands(hardware)
        self.setupCommands(hardware)
        putCommandOnDashboard("Drivetrain", ResetGyro(hardware.drivetrain, quest))

        SmartDashboard.putData("AutoChooser", autonomous.auto_chooser)

    def setupCopilotCommands(self, hardware: HardwareModule):
        pass

    def setupCommands(self, hardware):
        """
        Groups
        """
        # putCommandOnDashboard("Drivetrain", ResetGyro(hardware.drivetrain, ))
        putCommandOnDashboard("Drivetrain", DriveRelative.left(hardware.drivetrain))
        putCommandOnDashboard("Drivetrain", DriveRelative.right(hardware.drivetrain))
        putCommandOnDashboard("Drivetrain", DriveRelative.forwards(hardware.drivetrain))
        putCommandOnDashboard(
            "Drivetrain", DriveRelative.backwards(hardware.drivetrain)
        )

        """
        GUIDE
        """
        putCommandOnDashboard("Guide", ManualMoveGuide.up(hardware.guide))
        putCommandOnDashboard("Guide", ManualMoveGuide.down(hardware.guide))
        putCommandOnDashboard("Guide", ResetGuide.down(hardware.guide))
        putCommandOnDashboard("Guide", MoveGuide.toOpen(hardware.guide))
        putCommandOnDashboard("Guide", MoveGuide.toClose(hardware.guide))

        """
        Intake
        """
        putCommandOnDashboard("Intake", GrabFuel(hardware.feeder))
        putCommandOnDashboard("Intake", EjectFuel(hardware.feeder))
        putCommandOnDashboard("Intake", MovePivot.toUp(hardware.pivot))
        putCommandOnDashboard("Intake", MovePivot.toDown(hardware.pivot))
        putCommandOnDashboard("Intake", ResetIntake.up(hardware.pivot))
        putCommandOnDashboard("Intake", ManualMovePivot.up(hardware.pivot))
        putCommandOnDashboard("Intake", ManualMovePivot.down(hardware.pivot))
        putCommandOnDashboard("Intake", MaintainPivot(hardware.pivot))

    def robotInit(self) -> None:
        for subsystem in self._hardware.subsystems:
            wpilib.SmartDashboard.putData(subsystem.getName(), subsystem)

        wpilib.SmartDashboard.putData("Gyro", self._hardware.drivetrain._gyro)
        wpilib.SmartDashboard.putData(
            "CommandScheduler", CommandScheduler.getInstance()
        )
        wpilib.SmartDashboard.putData("PDP", self._hardware.pdp)

        for module in self._module_list.modules:
            if module.redefines_init_sendable:
                """
                If a module keeps a reference to a subsystem or the HardwareModule,
                it should be wrapped in a weakref.proxy(). For example,
                self.hardware = proxy(hardware)
                """
                print("Putting on dashboard:", module.getName())
                wpilib.SmartDashboard.putData(module.getName(), module)


def putCommandOnDashboard(
    sub_table: str, cmd: commands2.Command, name: str = None, suffix: str = " commands"
) -> commands2.Command:
    if not isinstance(sub_table, str):
        raise ValueError(
            f"sub_table should be a str: '{sub_table}' of type '{type(sub_table)}'"
        )

    if suffix:
        sub_table += suffix

    sub_table += "/"

    if name is None:
        name = cmd.getName()
    else:
        cmd.setName(name)

    wpilib.SmartDashboard.putData(sub_table + name, cmd)

    return cmd
