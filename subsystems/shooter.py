import rev
import wpilib
from ultime.autoproperty import autoproperty
from ultime.subsystem import Subsystem
import ports


class Shooter(Subsystem):
    shooting_speed = autoproperty(0.2)

    # Add a function to control the speed of the flywheel automatically while shooting
    def __init__(self):
        super().__init__()
        self.flywheel = self.flywheel = rev.SparkMax(
            ports.CAN.shooter_flywheel, rev.SparkMax.MotorType.kBrushless
        )
        self.aligner = self.aligner = rev.SparkMax(
            ports.CAN.shooter_aligner, rev.SparkMax.MotorType.kBrushless
        )
        self.indexer = self.indexer = rev.SparkMax(
            ports.CAN.indexer_motor, rev.SparkMax.MotorType.kBrushless
        )

    def shoot(self):
        self.flywheel.set(self.shooting_speed)
        self.indexer.set(0.1)
        self.aligner.set(0.2)

    def stop_shooting(self):
        self.flywheel.stopMotor()
        self.aligner.stopMotor()
        self.indexer.stopMotor()
