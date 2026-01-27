from enum import Enum, auto
from typing import Final

import commands2
import hal
import wpilib
from wpilib import RobotBase, DSControlWord, Watchdog

from ultime.module import ModuleList, Module


class ModuleRobot(wpilib.RobotBase):
    class Mode(Enum):
        kNone = auto()
        kDisable = auto()
        kAutonomous = auto()
        kTeleop = auto()
        kTest = auto()

    period: Final[float] = 0.02

    def __init__(self):
        super().__init__()
        self.modules = ModuleList()
        self._called_ds_connected = False
        self._last_mode = ModuleRobot.Mode.kNone
        self._watchdog = Watchdog(self.period, self.printLoopOverRunMessage())

    def _loopFunc(self):
        wpilib.DriverStation.refreshData()
        ds_control_world = wpilib.DSControlWord()

        #reset watchdog
        is_enabled, is_autonomous, is_test = self.getControlState()
        mode = ModuleRobot.Mode.kNone
        if not is_enabled:
            mode = ModuleRobot.Mode.kDisable
        elif is_autonomous:
            mode = ModuleRobot.Mode.kAutonomous
        elif is_test:
            mode = ModuleRobot.Mode.kTest
        else:
            mode = ModuleRobot.Mode.kTeleop

        #à ajouter si nous voulons mettre une fonction qui est appelée quand la DS se connecte
        #if not self.called_ds_connected and ds_control_world.isDSAttached():
        #    self.called_ds_connected = True
        #    self.driveStationConnected()

        #si le mode change, appeler les fonctions de sortie et d'entrée
        if self._last_mode is not mode:
            #fonctions de sortie
            if self._last_mode is ModuleRobot.Mode.kDisable:
                self.disabledExit()
            elif self._last_mode is ModuleRobot.Mode.kAutonomous:
                self.autonomousExit()
            elif self._last_mode is ModuleRobot.Mode.kTeleop:
                self.teleopExit()
            elif self._last_mode is ModuleRobot.Mode.kTest:
                self.testExit()

            #fonctions d'entrée
            if mode is ModuleRobot.Mode.kDisable:
                self.disabledInit()
            elif mode is ModuleRobot.Mode.kAutonomous:
                self.autonomousInit()
            elif mode is ModuleRobot.Mode.kTeleop:
                self.teleopInit()
            elif mode is ModuleRobot.Mode.kTest:
                self.testInit()

            self._last_mode = mode

        #TODO appeler IO update inputs


        #appeler les fonctions correspondantes au mode du robot
        if mode is ModuleRobot.Mode.kDisable:
            hal.observeUserProgramDisabled()
            self.disabledPeriodic()
        elif mode is ModuleRobot.Mode.kAutonomous:
            hal.observeUserProgramAutonomous()
            self.autonomousPeriodic()
        elif mode is ModuleRobot.Mode.kTeleop:
            hal.observeUserProgramTeleop()
            self.teleopPeriodic()
        elif mode is ModuleRobot.Mode.kTest:
            hal.observeUserProgramTest()
            self.testPeriodic()

        self.robotPeriodic()

        #TODO Scheduler run

        #TODO log everything

        #TODO appeler IO apply outputs




    def addModules(self, *modules: Module):
        self.modules.addModules(*modules)

    def robotInit(self):
        self.modules.robotInit()

        if RobotBase.isSimulation():
            self.modules.simulationInit()

    def driveStationConnected(self):
        pass

    def robotPeriodic(self):
        self.modules.robotPeriodic()

        if RobotBase.isSimulation():
            self.modules.simulationPeriodic()

    def disabledInit(self):
        self.modules.disabledInit()

    def disabledPeriodic(self):
        self.modules.disabledPeriodic()

    def disabledExit(self):
        self.modules.disabledExit()

    def autonomousInit(self):
        self.modules.autonomousInit()

    def autonomousPeriodic(self):
        self.modules.autonomousPeriodic()

    def autonomousExit(self):
        self.modules.autonomousExit()

    def teleopInit(self):
        self.modules.teleopInit()

    def teleopPeriodic(self):
        self.modules.teleopPeriodic()

    def teleopExit(self):
        self.modules.teleopExit()

    def testInit(self):
        self.modules.testInit()

    def testPeriodic(self):
        self.modules.testPeriodic()

    def testExit(self):
        self.modules.testExit()

    def driverStationConnected(self):
        self.modules.driverStationConnected()

    def printLoopOverRunMessage(self):
        wpilib.reportError(f"Loop time  of {self.period}s overrun")