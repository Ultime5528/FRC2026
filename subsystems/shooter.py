import rev
from ultime.subsystem import Subsystem
import ports


class Shooter(Subsystem):
    kP = 0.1
    kI = 0.0
    kD = 0.0
    kF = 12.0 / 4400  # 12 volts max divided by max RPM

    # Add a function to control the speed of the flywheel automatically while shooting
    def __init__(self):
        super().__init__()

        self.flywheel = rev.SparkMax(
            ports.CAN.shooter_flywheel, rev.SparkMax.MotorType.kBrushless
        )
        self.config = rev.SparkMaxConfig()
        self.config.closedLoop.pidf(self.kP, self.kI, self.kD, self.kF)
        self.flywheel.configure(
            self.config,
            rev.ResetMode.kResetSafeParameters,
            rev.PersistMode.kNoPersistParameters,
        )
        self.flywheel_controller = self.flywheel.getClosedLoopController()

        self.feeder = rev.SparkMax(
            ports.CAN.shooter_aligner, rev.SparkMax.MotorType.kBrushless
        )
        self.indexer = self.indexer = rev.SparkMax(
            ports.CAN.indexer_motor, rev.SparkMax.MotorType.kBrushless
        )

    def prepare_shoot(self, rpm):
        self.flywheel_controller.setSetpoint(rpm, rev.SparkMax.ControlType.kVelocity)

    def shoot(self):
        self.indexer.set(0.1)
        self.feeder.set(0.2)

    def stop(self):
        self.flywheel.stopMotor()
        self.feeder.stopMotor()
        self.indexer.stopMotor()
