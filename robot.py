#!/usr/bin/env python3
import wpilib
from wpilib.simulation import RoboRioSim, DriverStationSim

from commands.guide.checkguide import CheckGuide
from modules.autonomous import AutonomousModule
from modules.control import ControlModule
from modules.dashboard import DashboardModule
from modules.gamespecifics import GameSpecifics
from modules.hardware import HardwareModule
from modules.led import LEDModule
from modules.logging import LoggingModule
from modules.positionestimator import PositionEstimator
from modules.propertysavechecker import PropertySaveCheckerModule
from modules.questvision import QuestVisionModule
from modules.shootercalcmodule import ShooterCalcModule
from modules.sysidmodule import SysIDModule
from modules.tagvision import TagVisionModule
from ultime.modulerobot import ModuleRobot, is_simulation


class Robot(ModuleRobot):
    # robotInit fonctionne mieux avec les tests que __init__
    def __init__(self):
        super().__init__()

        wpilib.LiveWindow.disableAllTelemetry()
        wpilib.DriverStation.silenceJoystickConnectionWarning(True)
        # self.enableLiveWindowInTest(False)

        self.hardware = self.addModule(HardwareModule())

        self.quest_vision = self.addModule(QuestVisionModule(self.hardware.drivetrain))
        self.camera_front = self.addModule(
            TagVisionModule.front(self.hardware.drivetrain)
        )
        self.camera_back = self.addModule(
            TagVisionModule.back(self.hardware.drivetrain)
        )
        self.position_estimator = self.addModule(
            PositionEstimator(
                self.hardware.drivetrain,
                self.quest_vision,
                self.camera_front,
                self.camera_back,
            )
        )

        self.shooter_calc_module = self.addModule(
            ShooterCalcModule(self.hardware.drivetrain, self.hardware.guide)
        )
        self.hardware.guide.setDefaultCommand(
            CheckGuide(self.hardware.guide, self.shooter_calc_module)
        )

        self.game_specific = self.addModule(GameSpecifics())

        self.led = self.addModule(LEDModule(self.hardware, self.position_estimator, self.game_specific))

        self.autonomous = self.addModule(
            AutonomousModule(self.hardware, self.shooter_calc_module)
        )

        self.control = self.addModule(
            ControlModule(self.hardware, self.shooter_calc_module)
        )

        self.dashboard = self.addModule(
            DashboardModule(
                self.hardware, self.autonomous, self.modules, self.shooter_calc_module
            )
        )
        self.logging = self.addModule(LoggingModule())
        self.property_save_checker = self.addModule(PropertySaveCheckerModule())

        self.sys_id = self.addModule(SysIDModule(self.hardware.drivetrain))

        if is_simulation:
            RoboRioSim.setVInVoltage(12.5)
