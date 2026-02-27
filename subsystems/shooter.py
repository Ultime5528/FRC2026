from enum import Enum, auto

import rev
import wpilib
from rev import SparkMaxSim
from wpimath.filter import LinearFilter
from wpimath.system.plant import DCMotor

import ports
from ultime.autoproperty import autoproperty
from ultime.control import pf, feedforward
from ultime.modulerobot import is_simulation
from ultime.subsystem import Subsystem


class IndexerState(Enum):
    Off = auto()
    On = auto()
    Stuck = auto()


class Shooter(Subsystem):
    # 12 volts max divided by max RPM
    flywheel_kF = autoproperty(0.00222222)
    flywheel_kP = autoproperty(0.0)
    flywheel_kS = autoproperty(0.2)
    shooter_tolerance = autoproperty(100.0)

    indexer_rpm = autoproperty(1400.0)
    indexer_rpm_stuck_threshold = autoproperty(50.0)
    indexer_rpm_unstuck = autoproperty(-200.0)
    indexer_delay_unstuck = autoproperty(2.0)
    indexer_delay_stuck_threshold = autoproperty(1.0)
    indexer_kS = autoproperty(0.2)
    indexer_kF = autoproperty(0.002)
    indexer_kP = autoproperty(0.001)

    feeder_speed = autoproperty(0.5)

    def __init__(self):
        super().__init__()

        self._flywheel = rev.SparkMax(
            ports.CAN.shooter_flywheel, rev.SparkMax.MotorType.kBrushless
        )
        self._config = rev.SparkMaxConfig()
        self._config.voltageCompensation(12.0)
        self._flywheel.configure(
            self._config,
            rev.ResetMode.kResetSafeParameters,
            rev.PersistMode.kNoPersistParameters,
        )
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
            self._flywheel_last_rpm_sim = 0.0

    def logValues(self):
        super().logValues()
        self.log("indexer_state", str(self.indexer_state))

    def reset(self):
        self._velocity_filter.reset()
        self._is_at_velocity = False

    def shoot(self, rpm):
        average = self._velocity_filter.calculate(self.getCurrentSpeed())
        self.log("rpm_average", average)
        self.log("rpm_target", rpm)

        error = average - rpm
        self._is_at_velocity = abs(error) <= self.shooter_tolerance

        ff = feedforward(rpm, self.flywheel_kS, self.flywheel_kF)
        voltage = pf(average, rpm, self.flywheel_kS, self.flywheel_kF, self.flywheel_kP)

        voltage = min(ff, voltage)

        self.log("flywheel_voltage", voltage)
        self._flywheel.setVoltage(voltage)

        if is_simulation:
            self._flywheel_last_rpm_sim = rpm

    def sendFuel(self):
        self._feeder.set(self.feeder_speed)

        if self.indexer_state == IndexerState.Off:
            self.indexer_state = IndexerState.On
            self._timer.restart()

        if self.indexer_state == IndexerState.On:
            if (
                self._timer.hasElapsed(self.indexer_delay_stuck_threshold)
                and self.indexer_current_rpm < self.indexer_rpm_stuck_threshold
            ):
                self.indexer_state = IndexerState.Stuck
                self._timer.restart()
            else:
                self._setIndexerRPM(self.indexer_rpm)

        if self.indexer_state == IndexerState.Stuck:
            self._setIndexerRPM(self.indexer_rpm_unstuck)

            if self._timer.hasElapsed(self.indexer_delay_unstuck):
                self.indexer_state = IndexerState.On
                self._timer.restart()

    def stopFuel(self):
        self._indexer.set(0.0)
        self._feeder.set(0.0)
        self.indexer_state = IndexerState.Off

    def _setIndexerRPM(self, target_rpm: float) -> None:
        volts_indexer = pf(
            self.indexer_current_rpm,
            target_rpm,
            self.indexer_kS,
            self.indexer_kF,
            self.indexer_kP,
        )
        self._indexer.setVoltage(volts_indexer)

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
            self._flywheel_last_rpm_sim * 0.1 + self._flywheel_sim.getVelocity() * 0.9
        )
        if self._is_at_velocity and self.indexer_state == IndexerState.On:
            self._updateIndexerSimVelocity(self.indexer_rpm)
        elif self.indexer_state == IndexerState.Stuck:
            self._updateIndexerSimVelocity(self.indexer_rpm_unstuck)

    def _updateIndexerSimVelocity(self, target_rpm: float) -> None:
        self._indexer_sim.setVelocity(
            target_rpm * 0.1 + self._indexer_sim.getVelocity() * 0.9
        )
        if self._is_at_velocity and self.indexer_state == IndexerState.On:
            self._updateIndexerSimVelocity(self.indexer_rpm)
        elif self.indexer_state == IndexerState.Stuck:
            self._updateIndexerSimVelocity(self.indexer_rpm_unstuck)

    def _updateIndexerSimVelocity(self, target_rpm: float) -> None:
        self._indexer_sim.setVelocity(
            target_rpm * 0.1 + self._indexer_sim.getVelocity() * 0.9
        )

    def stop(self):
        self._flywheel.stopMotor()
        self._feeder.stopMotor()
        self._indexer.stopMotor()
        self._is_at_velocity = False
        self.indexer_state = IndexerState.Off

        if is_simulation:
            self._flywheel_last_rpm_sim = 0.0

    def getCurrentSpeed(self) -> float:
        return self.flywheel_current_rpm

    def isAtVelocity(self):
        return self._is_at_velocity
