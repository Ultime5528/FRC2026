#!/usr/bin/env python3
import wpilib

from modules.autonomous import AutonomousModule
from modules.control import ControlModule
from modules.dashboard import DashboardModule
from modules.hardware import HardwareModule
from modules.logging import LoggingModule
from modules.propertysavechecker import PropertySaveCheckerModule
from modules.questtagvision import QuestTagVisionModule
from ultime.modulerobot import ModuleRobot


class Robot(ModuleRobot):
    # robotInit fonctionne mieux avec les tests que __init__
    def __init__(self):
        super().__init__()

        wpilib.LiveWindow.disableAllTelemetry()
        wpilib.DriverStation.silenceJoystickConnectionWarning(True)
        self.enableLiveWindowInTest(False)

        self.hardware = HardwareModule()

        self.control = ControlModule(self.hardware)

        self.autonomous = AutonomousModule(self.hardware)

        self.quest_vision = QuestTagVisionModule(self.hardware.drivetrain)

        self.dashboard = DashboardModule(
            self.hardware, self.quest_vision, self.autonomous, self.modules
        )
        self.logging = LoggingModule()
        self.property_save_checker = PropertySaveCheckerModule()

        self.addModules(
            self.hardware,
            self.quest_vision,
            self.control,
            self.autonomous,
            self.dashboard,
            self.logging,
            self.property_save_checker,
        )
