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
    height_max = autoproperty(50.0)

    def __init__(self):
        super().__init__()

        self._motor = SparkMax(ports.CAN.climber_motor, SparkMax.MotorType.kBrushless)
        self.encoder = self._motor.getEncoder()
        self.switch = Switch(Switch.Type.NormallyClosed, ports.DIO.climber_switch)

        self._motor.configure(
            self._config,
            SparkBase.ResetMode.kResetSafeParameters,
            SparkBase.PersistMode.kPersistParameters,
        )

        self.state = self.State.Unknown
        self._prev_is_down = False
        self._has_reset = False
        self._offset = 0.0

        if RobotBase.isSimulation():
            self._sim_height = 5.0
            self._sim_motor = SparkMaxSim(self._motor, DCMotor.NEO(1))
            self._sim_encoder = self._sim_motor.getRelativeEncoderSim()

    def periodic(self) -> None:
        if self._prev_is_down and not self._switch.isPressed():
            self._offset = (
                    self.height_max / self.position_conversion_factor
                    - self.getRawEncoderPosition()
            )
            self._has_reset = True
        self._prev_is_down = self._switch.isPressed()

    def simulationPeriodic(self) -> None:
        distance = self._motor.get()
        self._sim_encoder.setPosition(
            self._sim_encoder.getPosition() + distance / self.position_conversion_factor
        )

        if self.getPosition() >= 90:
            self._switch.setSimPressed()
        else:
            self._switch.setSimUnpressed()

    def stop(self):
        self._motor.stopMotor()

    def climb(self):
        self.setSpeed(self.speed)

    def release(self):
        self.setSpeed(-self.speed)

    def getRawEncoderPosition(self):
        return self._encoder.getPosition()

    def getPosition(self):
        return self.position_conversion_factor * (
            self.getRawEncoderPosition() + self._offset
        )

    def isClimbed(self):
        return self.switch.isPressed()


