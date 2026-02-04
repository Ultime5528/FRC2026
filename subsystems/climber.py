from enum import Enum, auto

from rev import SparkMax, SparkBase, SparkMaxSim
from wpilib import RobotBase
from wpimath._controls._controls.plant import DCMotor

import ports
from ultime.autoproperty import autoproperty
from ultime.subsystem import Subsystem
from ultime.switch import Switch


class Climber(Subsystem):
    class State(Enum):
        Unknown = auto()
        Ready = auto()
        Climbed = auto()
        Moving = auto()

    speed = autoproperty(0.5)
    position_conversion_factor = autoproperty(0.2)
    height_max = autoproperty(0.215)

    def __init__(self):
        super().__init__()

        self._motor = SparkMax(ports.CAN.climber_motor, SparkMax.MotorType.kBrushless)
        self._encoder = self._motor.getEncoder()
        self._switch = Switch(Switch.Type.NormallyClosed, ports.DIO.climber_switch)

        self.state = self.State.Unknown
        self._was_switch_pressed = False

    def periodic(self) -> None:
        pass

    def simulationPeriodic(self) -> None:
        distance = self._motor.get()
        self._sim_encoder.setPosition(
            self._sim_encoder.getPosition() + distance / self.position_conversion_factor
        )

        if self.getPosition() <= 0.0:
            self._switch.setSimPressed()
        else:
            self._switch.setSimUnpressed()

    def stop(self):
        self._motor.stopMotor()

    def moveDown(self):
        self.setSpeed(-self.speed)

    def moveUp(self):
        if not self.state == self.State.Unknown:
            self.setSpeed(self.speed)

    def getRawEncoderPosition(self):
        return self._encoder.getPosition()

    def getPosition(self):
        return self.position_conversion_factor * (
            self.getRawEncoderPosition() + self._offset
        )

    def isDown(self):
        return self.switch.isPressed()

    def setOffset(self):
        self._offset = (
                self.height_max / self.position_conversion_factor
                - self.getRawEncoderPosition()
        )
