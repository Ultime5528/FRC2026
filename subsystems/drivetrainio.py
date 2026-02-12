from dataclasses import dataclass, field
from typing import Optional
from wpimath.geometry import Rotation2d
from ultime.gyro import ADIS16470
from ultime.io import IO


@dataclass
class DriveTrainInputs:
    gyro_angle_randians: float = 0.0
    gyro_rotation2d: Rotation2d = field(default_factory=Rotation2d)


@dataclass
class DriveTrainOutputs:
    gyro_reset: Optional[bool] = None

    def reset(self):
        self.gyro_reset = None


class DrivetrainIO(IO):
    def __init__(self):
        super().__init__()
        self.gyro = ADIS16470()

        self.inputs = DriveTrainInputs()
        self.outputs = DriveTrainOutputs()

    def updateInputs(self):
        self.inputs.gyro_angle_randians = self.gyro.getAngle()
        self.inputs.gyro_rotation2d = self.gyro.getRotation2d()

    def sendOutputs(self):
        if self.outputs.gyro_reset is not None:
            self.gyro.reset()

        self.outputs.reset()
