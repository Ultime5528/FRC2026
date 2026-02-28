import modulefinder

import commands2
import wpilib
from commands2 import CommandScheduler
from pathplannerlib.path import PathPlannerPath
from wpilib import SmartDashboard
from wpimath.geometry import Pose2d

from commands.climber.move import ManualMoveClimber, ResetClimber, MoveClimber
from commands.drivetrain.driverelative import DriveRelative
from commands.drivetrain.auto.followpathprecise import FollowPathPrecise
from commands.drivetrain.auto.pathfindprecise import PathFindPrecise
from commands.drivetrain.resetgyro import ResetGyro
from commands.feeder.ejectfuel import EjectFuel
from commands.feeder.grabfuel import GrabFuel
from commands.guide import ManualMoveGuide, ResetGuide, MoveGuide
from commands.hugger.hug import Hug
from commands.hugger.unhug import Unhug
from commands.pivot.maintainpivot import MaintainPivot
from commands.pivot.move import MovePivot, ResetPivot, ManualMovePivot
from commands.resetall import ResetAll
from commands.shooter.manualshoot import ManualShoot, ManualPrepareShoot
from commands.shooter.prepareshoot import PrepareShoot
from commands.shooter.shoot import Shoot
from modules.autonomous import AutonomousModule
from modules.hardware import HardwareModule
from modules.questvision import QuestVisionModule
from modules.shootercalcmodule import ShooterCalcModule
from ultime.log import Logger
from ultime.module import Module, ModuleList


class DashboardModule(Module):
    def __init__(
        self,
        hardware: HardwareModule,
        autonomous: AutonomousModule,
        module_list: ModuleList,
    ):
        super().__init__()
        self._hardware = hardware
        self._module_list = module_list
        self.shooter_calc_module = shooter_calc_module
        self.setupCopilotCommands(hardware)
        self.setupCommands(hardware)
        putCommandOnDashboard("Drivetrain", ResetGyro(hardware.drivetrain))

        SmartDashboard.putData("AutoChooser", autonomous.auto_chooser)

    def setupCopilotCommands(self, hardware: HardwareModule):
        pass

    def setupCommands(self, hardware):
        """
        Drivetrain
        """
        # putCommandOnDashboard("Drivetrain", ResetGyro(hardware.drivetrain, ))
        putCommandOnDashboard("Drivetrain", DriveRelative.left(hardware.drivetrain))
        putCommandOnDashboard("Drivetrain", DriveRelative.right(hardware.drivetrain))
        putCommandOnDashboard("Drivetrain", DriveRelative.forwards(hardware.drivetrain))
        putCommandOnDashboard(
            "Drivetrain", DriveRelative.backwards(hardware.drivetrain)
        )
        path = PathPlannerPath.fromPathFile("Test")
        putCommandOnDashboard(
            "Drivetrain", FollowPathPrecise(hardware.drivetrain, path)
        )
        putCommandOnDashboard(
            "Drivetrain", PathFindPrecise(hardware.drivetrain, Pose2d(8, 4, 0))
        )

        """
        Shooter
        """
        putCommandOnDashboard(
            "Shooter", PrepareShoot(hardware.shooter, self.shooter_calc_module)
        )
        putCommandOnDashboard(
            "Shooter",
            Shoot(hardware.shooter, self.shooter_calc_module),
        )
        putCommandOnDashboard("Shooter", ManualShoot(hardware.shooter))
        putCommandOnDashboard("Shooter", ManualPrepareShoot(hardware.shooter))

        """
        Guide
        """
        putCommandOnDashboard("Guide", ManualMoveGuide.up(hardware.guide))
        putCommandOnDashboard("Guide", ManualMoveGuide.down(hardware.guide))
        putCommandOnDashboard("Guide", ResetGuide.down(hardware.guide))
        putCommandOnDashboard("Guide", MoveGuide.toUsed(hardware.guide))
        putCommandOnDashboard("Guide", MoveGuide.toUnused(hardware.guide))

        """
        Climber
        """
        putCommandOnDashboard("Climber", ManualMoveClimber.up(hardware.climber))
        putCommandOnDashboard("Climber", ManualMoveClimber.down(hardware.climber))
        putCommandOnDashboard("Climber", ResetClimber.down(hardware.climber))
        putCommandOnDashboard("Climber", MoveClimber.toClimbed(hardware.climber))
        putCommandOnDashboard("Climber", MoveClimber.toReady(hardware.climber))
        putCommandOnDashboard("Climber", MoveClimber.toRetracted(hardware.climber))

        """
        Hugger
        """
        putCommandOnDashboard("Hugger", Hug(hardware.hugger))
        putCommandOnDashboard("Hugger", Unhug(hardware.hugger))

        """
        Feeder
        """
        putCommandOnDashboard("Feeder", GrabFuel(hardware.feeder))
        putCommandOnDashboard("Feeder", EjectFuel(hardware.feeder))

        """
        Pivot
        """
        putCommandOnDashboard("Pivot", MovePivot.toUp(hardware.pivot))
        putCommandOnDashboard("Pivot", MovePivot.toDown(hardware.pivot))
        putCommandOnDashboard("Pivot", ResetPivot.down(hardware.pivot))
        putCommandOnDashboard("Pivot", ManualMovePivot.up(hardware.pivot))
        putCommandOnDashboard("Pivot", ManualMovePivot.down(hardware.pivot))
        putCommandOnDashboard("Pivot", MaintainPivot(hardware.pivot))

        """
        Group
        """
        putCommandOnDashboard(
            "Group",
            ResetAll(hardware.climber, hardware.hugger, hardware.pivot, hardware.guide),
        )

    def robotInit(self) -> None:
        for subsystem in self._hardware.subsystems:
            Logger.getInstance().addLoggable(subsystem)

        for module in self._module_list.modules:
            Logger.getInstance().addLoggable(module)

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
