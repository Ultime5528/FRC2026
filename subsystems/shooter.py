import rev
from rev import SparkMaxSim
from wpimath.filter import LinearFilter
from wpimath.system.plant import DCMotor
from wpimath.units import kilogram_square_meters

import ports
from ultime.autoproperty import autoproperty
from ultime.control import feedforward, pf
from ultime.modulerobot import is_simulation
from ultime.subsystem import Subsystem


class Shooter(Subsystem):
    kP = 0.1
    kI = 0.0
    kD = 0.0
    kF = 12.0 / 4400  # 12 volts max divided by max RPM

    speed_rpm_indexer = autoproperty(0.5)
    speed_feeder = autoproperty(0.5)
    tolerance = autoproperty(100.0)

    kS_indexer = autoproperty(0.1)
    kF_indexer = autoproperty(0.0)
    kP_indexer = autoproperty(0.0)

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
        self._encoder = self._flywheel.getEncoder()

        self.flywheel_current_rpm = self.createProperty(0.0)

        self._feeder = rev.SparkMax(
            ports.CAN.shooter_feeder, rev.SparkMax.MotorType.kBrushless
        )
        self._indexer = self._indexer = rev.SparkMax(
            ports.CAN.shooter_indexer, rev.SparkMax.MotorType.kBrushless
        )
        self.indexer_current_rpm = self.createProperty(0.0)

        self._indexer_encoder = self._indexer.getEncoder()

        self._velocity_filter = LinearFilter.movingAverage(25)

        self._is_at_velocity = self.createProperty(False)

        if is_simulation:
            self._flywheel_sim = SparkMaxSim(self._flywheel, DCMotor.NEO(1))

    def shoot(self, rpm):
        self._flywheel_controller.setSetpoint(rpm, rev.SparkMax.ControlType.kVelocity)
        average = self._velocity_filter.calculate(self.getCurrentSpeed())
        self.log("rpm_average", average)
        self.log("rpm_target", rpm)
        self._is_at_velocity = abs(average - rpm) < self.tolerance

    def sendFuel(self, rpm):
        volts_indexer = pf(
            self.indexer_current_rpm,
            self.speed_rpm_indexer,
            self.kS_indexer,
            self.kF_indexer,
            self.kP_indexer,
        )
        self._indexer.setVoltage(self.speed_indexer)
        self._feeder.set(self.speed_feeder)

    def readInputs(self):
        if is_simulation:
            self.flywheel_current_rpm = self._flywheel_sim.getVelocity()
        else:
            self.flywheel_current_rpm = self._encoder.getVelocity()

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
        return self.flywheel_current_rpm

    def isAtVelocity(self):
        return self._is_at_velocity
