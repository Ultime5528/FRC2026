from _weakref import proxy
from typing import Optional

import commands2
from commands2 import Command
from pathplannerlib.auto import NamedCommands
from wpilib import SendableChooser, DriverStation

from commands.autonomous.rushtomiddle import RushToMiddle
from commands.autonomous.shootandclimb import ShootAndClimb
from commands.retractandunhug import RetractAndUnhug
from modules.hardware import HardwareModule
from modules.positionestimator import PositionEstimator
from modules.questvision import QuestVisionModule
from modules.shootercalcmodule import ShooterCalcModule
from ultime.command import WaitCommand
from ultime.module import Module
from ultime.questnav.questnav import QuestNav


def registerNamedCommand(command: Command):
    NamedCommands.registerCommand(command.getName(), command)


class AutonomousModule(Module):
    def __init__(
        self,
        hardware: HardwareModule,
        shooter_calc_module: ShooterCalcModule,
        quest_nav: QuestVisionModule,
        position_estimator: PositionEstimator,
    ):
        super().__init__()
        self.hardware = proxy(hardware)

        self.auto_command: Optional[commands2.Command] = None

        self.auto_chooser = SendableChooser()
        self.auto_chooser.setDefaultOption("Nothing", WaitCommand(0.0))

        self.auto_chooser.addOption(
            "RushToMiddleRight",
            RushToMiddle.rightTrench(
                hardware, shooter_calc_module, quest_nav, position_estimator
            ),
        )
        self.auto_chooser.addOption(
            "RushToMiddleLeft",
            RushToMiddle.leftTrench(
                hardware, shooter_calc_module, quest_nav, position_estimator
            ),
        )
        self.auto_chooser.addOption(
            "ShootAndClimbRight",
            ShootAndClimb.right(
                hardware, shooter_calc_module, quest_nav, position_estimator
            ),
        )
        self.auto_chooser.addOption(
            "ShootAndClimbLeft",
            ShootAndClimb.left(
                hardware, shooter_calc_module, quest_nav, position_estimator
            ),
        )

        self.retract_and_unhug = RetractAndUnhug(hardware.climber, hardware.hugger)

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

    def teleopInit(self) -> None:
        if DriverStation.isFMSAttached():
            self.retract_and_unhug.schedule()
