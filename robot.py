#!/usr/bin/env python3
import wpilib

from modules.autonomous import AutonomousModule
from modules.control import ControlModule
from modules.dashboard import DashboardModule
from modules.hardware import HardwareModule
from modules.logging import LoggingModule
from modules.propertysavechecker import PropertySaveCheckerModule
from modules.questvision import QuestVisionModule
from modules.shootercalcmodule import ShooterCalcModule
from modules.sysidmodule import SysIDModule
from ultime.modulerobot import ModuleRobot


class Robot(ModuleRobot):
    # robotInit fonctionne mieux avec les tests que __init__
    def __init__(self):
        super().__init__()

        wpilib.LiveWindow.disableAllTelemetry()
        wpilib.DriverStation.silenceJoystickConnectionWarning(True)
        # self.enableLiveWindowInTest(False)

        self.hardware = self.addModule(HardwareModule())

        self.control = self.addModule(ControlModule(self.hardware))

        self.autonomous = self.addModule(AutonomousModule(self.hardware))

        self.quest_vision = self.addModule(QuestVisionModule(self.hardware.drivetrain))

        self.shooter_calc_module = self.addModule(
            ShooterCalcModule(self.hardware.drivetrain, self.hardware.guide)
        )

        self.dashboard = self.addModule(
            DashboardModule(
                self.hardware,
                self.quest_vision,
                self.shooter_calc_module,
                self.autonomous,
                self.modules,
            )
        )
        self.logging = self.addModule(LoggingModule())
        self.property_save_checker = self.addModule(PropertySaveCheckerModule())

        self.sys_id = self.addModule(SysIDModule(self.hardware.drivetrain))
