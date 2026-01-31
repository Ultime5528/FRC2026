import commands2
import wpilib
from commands2 import CommandScheduler
from wpilib import SmartDashboard

from commands.drivetrain.driverelative import DriveRelative
from commands.drivetrain.resetgyro import ResetGyro
from commands.intake.roll import Roll
from modules.autonomous import AutonomousModule
from modules.hardware import HardwareModule
from modules.questtagvision import QuestTagVisionModule
from ultime.module import Module, ModuleList


class DashboardModule(Module):
    def __init__(
        self,
        hardware: HardwareModule,
        quest: QuestTagVisionModule,
        autonomous: AutonomousModule,
        module_list: ModuleList,
    ):
        super().__init__()
        self._hardware = hardware
        self._module_list = module_list
        self.setupCopilotCommands(hardware)
        # self.setupCommands(hardware)
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
        putCommandOnDashboard("Intake", Roll(hardware.intake))


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
