from enum import Enum, auto

import rev
import wpilib
from rev import SparkMaxSim
from wpimath.filter import LinearFilter
from wpimath.system.plant import DCMotor

import ports
from ultime.autoproperty import autoproperty
from ultime.control import pf
from ultime.modulerobot import is_simulation
from ultime.subsystem import Subsystem


class IndexerState(Enum):
    Off = auto()
    On = auto()
    Stuck = auto()


class Shooter(Subsystem):
    kP = autoproperty(0.0)
    kI = autoproperty(0.0)
    kD = autoproperty(0.0)
    # 12 volts max divided by max RPM
    kF = autoproperty(0.00222222)

    rpm_indexer_stuck_threshold = autoproperty(50)
    rpm_indexer_to_unstuck = autoproperty(-200)
    delay_indexer_unstuck = autoproperty(2.0)
    delay_indexer_to_stuck_threshold = autoproperty(1.0)
    speed_feeder = autoproperty(0.5)
    speed_rpm_indexer = autoproperty(1000.0)
    tolerance = autoproperty(100.0)

    kS_indexer = autoproperty(0.2)
    kF_indexer = autoproperty(0.0018)
    kP_indexer = autoproperty(0.001)

    def __init__(self):
        super().__init__()

        self._flywheel = rev.SparkMax(
            ports.CAN.shooter_flywheel, rev.SparkMax.MotorType.kBrushless
        )
        self.updatePIDFConfig()
        self._flywheel_controller = self._flywheel.getClosedLoopController()
        self._flywheel_encoder = self._flywheel.getEncoder()

        self.flywheel_current_rpm = self.createProperty(0.0)

        self._feeder = rev.SparkMax(
            ports.CAN.shooter_feeder, rev.SparkMax.MotorType.kBrushless
        )
        self._indexer = rev.SparkMax(
            ports.CAN.shooter_indexer, rev.SparkMax.MotorType.kBrushless
        )
        self._indexer.setInverted(True)
        self.indexer_current_rpm = self.createProperty(0.0)

        self._indexer_encoder = self._indexer.getEncoder()

        self._velocity_filter = LinearFilter.movingAverage(25)

        self._is_at_velocity = self.createProperty(False)

        self._timer = wpilib.Timer()

        self.indexer_state = IndexerState.Off

        if is_simulation:
            self._flywheel_sim = SparkMaxSim(self._flywheel, DCMotor.NEO(1))
            self._indexer_sim = SparkMaxSim(self._indexer, DCMotor.NEO(1))

    def updatePIDFConfig(self):
        self._config = rev.SparkMaxConfig()
        self._config.closedLoop.pidf(self.kP, self.kI, self.kD, self.kF)
        self._flywheel.configure(
            self._config,
            rev.ResetMode.kResetSafeParameters,
            rev.PersistMode.kNoPersistParameters,
        )

    def logValues(self):
        super().logValues()
        self.log("indexer_state", str(self.indexer_state))

    def shoot(self, rpm):
        self._flywheel_controller.setSetpoint(rpm, rev.SparkMax.ControlType.kVelocity)
        average = self._velocity_filter.calculate(self.getCurrentSpeed())
        self.log("rpm_average", average)
        self.log("rpm_target", rpm)
        self._is_at_velocity = abs(average - rpm) < self.tolerance

    def sendFuel(self):

        self._feeder.set(self.speed_feeder)

        if self.indexer_state == IndexerState.Off:
            self.indexer_state = IndexerState.On
            self._timer.restart()

        if self.indexer_state == IndexerState.On:

            if (
                self._timer.hasElapsed(self.delay_indexer_to_stuck_threshold)
                and self.indexer_current_rpm < self.rpm_indexer_stuck_threshold
            ):
                self.indexer_state = IndexerState.Stuck
                self._timer.restart()
            else:
                volts_indexer = pf(
                    self.indexer_current_rpm,
                    self.speed_rpm_indexer,
                    self.kS_indexer,
                    self.kF_indexer,
                    self.kP_indexer,
                )
                self._indexer.setVoltage(volts_indexer)

        if self.indexer_state == IndexerState.Stuck:
            volts_indexer = pf(
                self.indexer_current_rpm,
                self.rpm_indexer_to_unstuck,
                self.kS_indexer,
                self.kF_indexer,
                self.kP_indexer,
            )
            self._indexer.setVoltage(volts_indexer)

            if self._timer.hasElapsed(self.delay_indexer_unstuck):
                self.indexer_state = IndexerState.On
                self._timer.restart()

    def stopFuel(self):
        self._indexer.set(0.0)
        self._feeder.set(0.0)

    def readInputs(self):
        if is_simulation:
            self.indexer_current_rpm = self._indexer_sim.getVelocity()
        else:
            self.indexer_current_rpm = self._indexer_encoder.getVelocity()

        if is_simulation:
            self.flywheel_current_rpm = self._flywheel_sim.getVelocity()
        else:
            self.flywheel_current_rpm = self._flywheel_encoder.getVelocity()

    def simulationPeriodic(self):
        self._flywheel_sim.setVelocity(
            self._flywheel_controller.getSetpoint() * 0.01
            + self._flywheel_sim.getVelocity() * 0.99
        )
        if self._is_at_velocity and self.indexer_state == IndexerState.On:
            self._indexer_sim.setVelocity(
                self.speed_rpm_indexer * 0.01 + self._indexer_sim.getVelocity() * 0.99
            )
        elif self.indexer_state == IndexerState.Stuck:
            self._indexer_sim.setVelocity(self.rpm_indexer_to_unstuck)

    def stop(self):
        self._flywheel.stopMotor()
        self._feeder.stopMotor()
        self._indexer.stopMotor()
        self._is_at_velocity = False
        self.indexer_state = IndexerState.Off

    def getCurrentSpeed(self) -> float:
        return self.flywheel_current_rpm

    def isAtVelocity(self):
        return self._is_at_velocity
