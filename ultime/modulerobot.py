from typing import Final

import commands2
from wpilib import RobotBase

from ultime.module import ModuleList, Module


class ModuleRobot(commands2.TimedCommandRobot):
    period: Final[float] = 0.02

    def __init__(self):
        super().__init__(self.period)
        self.modules = ModuleList()

    def addModules(self, *modules: Module):
        self.modules.addModules(*modules)

    def robotInit(self):
        self.modules.robotInit()

        if RobotBase.isSimulation():
            self.modules.simulationInit()

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
