import rev
import wpilib
from rev import SparkMaxSim
from wpimath.filter import LinearFilter
from wpimath.system.plant import DCMotor

import ports
from ultime.autoproperty import autoproperty
from ultime.modulerobot import is_simulation
from ultime.subsystem import Subsystem


class Shooter(Subsystem):

    kP = 0.1
    kI = 0.0
    kD = 0.0
    kF = 12.0 / 4400  # 12 volts max divided by max RPM

    speed_indexer_stuck = autoproperty(0.1)
    speed_indexer_to_unstuck = autoproperty(-0.3)
    speed_indexer = autoproperty(0.5)
    delay_indexer_unstuck = autoproperty(2.0)
    speed_feeder = autoproperty(0.5)
    tolerance = autoproperty(100.0)

    def __init__(self):
        super().__init__()

        self._flywheel = rev.SparkMax(
            ports.CAN.shooter_flywheel, rev.SparkMax.MotorType.kBrushless
        )
        self._config = rev.SparkMaxConfig()
        self._config.closedLoop.pidf(self.kP, self.kI, self.kD, self.kF)
        self._flywheel.configure(
            self._config,
            rev.ResetMode.kResetSafeParameters,
            rev.PersistMode.kNoPersistParameters,
        )
        self._flywheel_controller = self._flywheel.getClosedLoopController()
        self._flywheel_encoder = self._flywheel.getEncoder()

        self.rpm_current = self.createProperty(0.0)

        self._feeder = rev.SparkMax(
            ports.CAN.shooter_feeder, rev.SparkMax.MotorType.kBrushless
        )
        self._indexer = self._indexer = rev.SparkMax(
            ports.CAN.shooter_indexer, rev.SparkMax.MotorType.kBrushless
        )
        self._indexer_encoder = self._indexer.getEncoder()

        self._velocity_filter = LinearFilter.movingAverage(25)

        self._is_at_velocity = self.createProperty(False)

        self._has_surpassed_stuck_speed = False
        self._is_in_unstuck_mode = False
        self._unstuck_timer = wpilib.Timer()

        if is_simulation:
            self._flywheel_sim = SparkMaxSim(self._flywheel, DCMotor.NEO(1))

    def shoot(self, rpm):
        self._flywheel_controller.setSetpoint(rpm, rev.SparkMax.ControlType.kVelocity)
        average = self._velocity_filter.calculate(self.getCurrentSpeed())
        self.log("rpm_average", average)
        self.log("rpm_target", rpm)
        self._is_at_velocity = abs(average - rpm) < self.tolerance

    def sendFuel(self):

        if not self._is_in_unstuck_mode:
            self._has_surpassed_stuck_speed = self._indexer_encoder.getVelocity() > self.speed_indexer_stuck

        if self._is_in_unstuck_mode and not self._unstuck_timer.isRunning():
            self._unstuck_timer.restart()

        if self._is_in_unstuck_mode and self._unstuck_timer.isRunning():
            if self._unstuck_timer.hasElapsed(self.delay_indexer_unstuck):
                self._has_surpassed_stuck_speed = False
                self._is_in_unstuck_mode = False
                self._unstuck_timer.stop()

        if self._is_in_unstuck_mode:
            self._indexer.set(self.speed_indexer_to_unstuck)
        else:
            self._indexer.set(self.speed_indexer)

        self._feeder.set(self.speed_feeder)

    def stopFuel(self):
        self._indexer.set(0.0)
        self._feeder.set(0.0)

    def readInputs(self):
        if is_simulation:
            self.rpm_current = self._flywheel_sim.getVelocity()
        else:
            self.rpm_current = self._flywheel_encoder.getVelocity()

    def simulationPeriodic(self):
        self._flywheel_sim.setVelocity(
            self._flywheel_controller.getSetpoint() * 0.01
            + self._flywheel_sim.getVelocity() * 0.99
        )

    def stop(self):
        self._flywheel.stopMotor()
        self._feeder.stopMotor()
        self._indexer.stopMotor()
        self._is_at_velocity = False

    def getCurrentSpeed(self) -> float:
        return self.rpm_current

    def isAtVelocity(self):
        return self._is_at_velocity

    def setToUnstuck(self):
        self._has_surpassed_stuck_speed = False
        self._is_in_unstuck_mode = False