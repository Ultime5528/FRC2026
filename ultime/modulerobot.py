import weakref
from enum import Enum, auto
from typing import Final

import hal
import wpilib
from commands2 import CommandScheduler
from ntcore import NetworkTableInstance
from robotpy_ext.misc import NotifierDelay
from wpilib import RobotBase, Watchdog, SmartDashboard

from ultime.module import ModuleList, Module

is_simulation = wpilib.RobotBase.isSimulation()
is_real = wpilib.RobotBase.isReal()


class ModuleRobot(wpilib.RobotBase):
    class Mode(Enum):
        kNone = auto()
        kDisable = auto()
        kAutonomous = auto()
        kTeleop = auto()
        kTest = auto()

    period: Final[float] = 0.02

    ios = weakref.WeakSet()

    def __init__(self):
        super().__init__()
        self.modules = ModuleList()
        self._called_ds_connected = False
        self._last_mode = ModuleRobot.Mode.kNone
        self._watchdog = Watchdog(self.period, lambda: None)
        self.running = True

    def _loopFunc(self):
        wpilib.DriverStation.refreshData()
        self._watchdog.reset()
        # ds_control_world = wpilib.DSControlWord()

        is_enabled, is_autonomous, is_test = self.getControlState()

        if not is_enabled:
            mode = ModuleRobot.Mode.kDisable
        elif is_autonomous:
            mode = ModuleRobot.Mode.kAutonomous
        elif is_test:
            mode = ModuleRobot.Mode.kTest
        else:
            mode = ModuleRobot.Mode.kTeleop

        # à ajouter si nous voulons mettre une fonction qui est appelée quand la DS se connecte
        # if not self.called_ds_connected and ds_control_world.isDSAttached():
        #    self.called_ds_connected = True
        #    self.driveStationConnected()

        # si le mode change, appeler les fonctions de sortie et d'entrée
        if self._last_mode is not mode:
            # fonctions de sortie
            if self._last_mode is ModuleRobot.Mode.kDisable:
                self.disabledExit()
            elif self._last_mode is ModuleRobot.Mode.kAutonomous:
                self.autonomousExit()
            elif self._last_mode is ModuleRobot.Mode.kTeleop:
                self.teleopExit()
            elif self._last_mode is ModuleRobot.Mode.kTest:
                self.testExit()

            # fonctions d'entrée
            if mode is ModuleRobot.Mode.kDisable:
                self.disabledInit()
                self._watchdog.addEpoch("DisabledInit()")
            elif mode is ModuleRobot.Mode.kAutonomous:
                self.autonomousInit()
                self._watchdog.addEpoch("AutonomousInit()")
            elif mode is ModuleRobot.Mode.kTeleop:
                self.teleopInit()
                self._watchdog.addEpoch("TeleopInit()")
            elif mode is ModuleRobot.Mode.kTest:
                self.testInit()
                self._watchdog.addEpoch("TestInit()")

            self._last_mode = mode

        for io in self.ios:
            io.updateInputs()

        self._watchdog.addEpoch("io.updateInputs()")

        # appeler les fonctions correspondantes au mode du robot
        if mode is ModuleRobot.Mode.kDisable:
            hal.observeUserProgramDisabled()
            self.disabledPeriodic()
            self._watchdog.addEpoch("DisabledPeriodic()")
        elif mode is ModuleRobot.Mode.kAutonomous:
            hal.observeUserProgramAutonomous()
            self.autonomousPeriodic()
            self._watchdog.addEpoch("AutonomousPeriodic()")
        elif mode is ModuleRobot.Mode.kTeleop:
            hal.observeUserProgramTeleop()
            self.teleopPeriodic()
            self._watchdog.addEpoch("TeleopPeriodic()")
        elif mode is ModuleRobot.Mode.kTest:
            hal.observeUserProgramTest()
            self.testPeriodic()
            self._watchdog.addEpoch("TestPeriodic()")

        self.robotPeriodic()
        self._watchdog.addEpoch("RobotPeriodic()")

        CommandScheduler.getInstance().run()
        self._watchdog.addEpoch("CommandScheduler.run()")

        # TODO log everything

        for io in self.ios:
            io.sendOutputs()

        self._watchdog.addEpoch("io.sendOutputs()")

        SmartDashboard.updateValues()
        self._watchdog.addEpoch("SmartDashboard.updateValues()")

        if is_simulation:
            hal.simPeriodicBefore()
            self.simulationPeriodic()
            hal.simPeriodicAfter()
            self._watchdog.addEpoch("SimulationPeriodic()")

        self._watchdog.disable()

        NetworkTableInstance.getDefault().flushLocal()

        if self._watchdog.isExpired():
            wpilib.reportError(f"Loop time  of {self.period}s overrun")
            self._watchdog.printEpochs()

    def startCompetition(self):
        self.robotInit()

        if is_simulation:
            self.simulationInit()

        hal.observeUserProgramStarting()

        with NotifierDelay(self.period) as delay:
            while self.running:
                self._loopFunc()
                delay.wait()

    def endCompetition(self):
        self.running = False

    def addModule(self, module: Module):
        self.modules.addModules(module)
        return module

    def robotInit(self):
        self.modules.robotInit()

        if is_simulation:
            self.modules.simulationInit()

    def driveStationConnected(self):
        pass

    def robotPeriodic(self):
        self.modules.robotPeriodic()

        if is_simulation:
            self.modules.simulationPeriodic()

    def simulationInit(self):
        self.modules.simulationInit()

    def simulationPeriodic(self):
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
