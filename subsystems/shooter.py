import rev
from rev import SparkMaxSim
from wpimath.filter import LinearFilter
from wpimath.system.plant import DCMotor
from wpimath.units import kilogram_square_meters

import ports
from ultime.autoproperty import autoproperty
from ultime.control import feedforward, pf, clamp
from ultime.modulerobot import is_simulation
from ultime.subsystem import Subsystem


class Shooter(Subsystem):
    kP = autoproperty(0.0)
    kI = autoproperty(0.0)
    kD = autoproperty(0.0)
    kS_shooter = autoproperty(0.2)
    # 12 volts max divided by max RPM
    kF = autoproperty(0.00222222)

    speed_feeder = autoproperty(0.5)
    speed_rpm_indexer = autoproperty(1400.0)
    tolerance = autoproperty(1000.0)

    kS_indexer = autoproperty(0.2)
    kF_indexer = autoproperty(0.002)
    kP_indexer = autoproperty(0.001)

    def __init__(self):
        super().__init__()

        self._flywheel = rev.SparkMax(
            ports.CAN.shooter_flywheel, rev.SparkMax.MotorType.kBrushless
        )
        self._feeder = rev.SparkMax(
            ports.CAN.shooter_feeder, rev.SparkMax.MotorType.kBrushless
        )
        self._indexer = rev.SparkMax(
            ports.CAN.shooter_indexer, rev.SparkMax.MotorType.kBrushless
        )

        self.updatePIDFConfig()

        self._indexer.setInverted(True)
        self._indexer_config = rev.SparkMaxConfig()
        self._indexer_config.voltageCompensation(12.0)
        self._indexer.configure(
            self._indexer_config,
            rev.ResetMode.kResetSafeParameters,
            rev.PersistMode.kNoPersistParameters,
        )

        self._flywheel_controller = self._flywheel.getClosedLoopController()
        self._encoder = self._flywheel.getEncoder()
        self._indexer_encoder = self._indexer.getEncoder()

        self.flywheel_current_rpm = self.createProperty(0.0)

        self.indexer_current_rpm = self.createProperty(0.0)

        self._velocity_filter = LinearFilter.movingAverage(25)

        self._is_at_velocity = self.createProperty(False)

        if is_simulation:
            self._flywheel_sim = SparkMaxSim(self._flywheel, DCMotor.NEO(1))

    def updatePIDFConfig(self):
        self._config = rev.SparkMaxConfig()
        self._config.voltageCompensation(12.0)
        self._config.closedLoop.pidf(self.kP, self.kI, self.kD, self.kF)
        self._flywheel.configure(
            self._config,
            rev.ResetMode.kResetSafeParameters,
            rev.PersistMode.kNoPersistParameters,
        )

    def reset(self):
        self._velocity_filter.reset()
        self._is_at_velocity = False

    def shoot(self, rpm):
        average = self._velocity_filter.calculate(self.getCurrentSpeed())
        self.log("rpm_average", average)
        self.log("rpm_target", rpm)

        error = average - rpm

        if error > self.tolerance:
            self._is_at_velocity = False
            voltage = 0.0
        elif error < -self.tolerance:
            self._is_at_velocity = False
            voltage = 12.0
        else:
            self._is_at_velocity = True
            ff_volts = feedforward(rpm, self.kS_shooter, self.kF)
            if error < rpm:
                voltage = ff_volts + (12 - ff_volts) * ((-error) / self.tolerance)
            else:
                voltage = ff_volts * (1 - (error / self.tolerance))
            voltage = clamp(voltage, 0.0, 12.0)

        self.log("flywheel_voltage", voltage)
        self._flywheel.setVoltage(voltage)

    def sendFuel(self):
        volts_indexer = pf(
            self.indexer_current_rpm,
            self.speed_rpm_indexer,
            self.kS_indexer,
            self.kF_indexer,
            self.kP_indexer,
        )
        self._indexer.setVoltage(volts_indexer)
        self._feeder.set(self.speed_feeder)

    def stopFuel(self):
        self._indexer.set(0.0)
        self._feeder.set(0.0)

    def readInputs(self):
        self.indexer_current_rpm = self._indexer_encoder.getVelocity()

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
