import rev
from rev import SparkMaxSim
from wpilib import RobotBase
from wpimath.system.plant import DCMotor
from wpimath.filter import LinearFilter

from ultime.autoproperty import autoproperty
from ultime.subsystem import Subsystem
import ports


class Shooter(Subsystem):
    kP = 0.1
    kI = 0.0
    kD = 0.0
    kF = 12.0 / 4400  # 12 volts max divided by max RPM

    indexer_speed = autoproperty(0.5)
    feeder_speed = autoproperty(0.5)
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
        self._encoder = self._flywheel.getEncoder()

        self._feeder = rev.SparkMax(
            ports.CAN.shooter_aligner, rev.SparkMax.MotorType.kBrushless
        )
        self._indexer = self._indexer = rev.SparkMax(
            ports.CAN.indexer_motor, rev.SparkMax.MotorType.kBrushless
        )
        self._velocity_filter = LinearFilter.movingAverage(25)
        self._is_at_velocity = False

        if RobotBase.isSimulation():
            self._flywheel_sim = SparkMaxSim(self._flywheel, DCMotor.NEO(1))

    def shoot(self, rpm):
        self._flywheel_controller.setSetpoint(rpm, rev.SparkMax.ControlType.kVelocity)
        average = self._velocity_filter.calculate(self.getCurrentSpeed())
        speed_rpm = 666.6  # Mettre la valeur du Hayder ici
        self._is_at_velocity = abs(average - speed_rpm) < self.tolerance

    def sendFuel(self):
        if self._is_at_velocity:
            self._indexer.setVoltage(self.indexer_speed)
            self._feeder.setVoltage(self.feeder_speed)
        else:
            pass

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
        if RobotBase.isSimulation():
            return self._flywheel_sim.getVelocity()
        else:
            return self._encoder.getVelocity()
