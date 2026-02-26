import rev
from rev import SparkMaxConfig, SparkBaseConfig, ResetMode, PersistMode

import ports
from ultime.autoproperty import autoproperty
from ultime.subsystem import Subsystem


class Feeder(Subsystem):
    speed_grab = autoproperty(-0.5)
    speed_feed = autoproperty(1.0)

    def __init__(self):
        super().__init__()
        self._motor = rev.SparkMax(
            ports.CAN.feeder_motor, rev.SparkMax.MotorType.kBrushless
        )
        self._config = SparkMaxConfig()
        self._config.setIdleMode(SparkBaseConfig.IdleMode.kBrake)
        self._motor.configure(
            self._config,
            ResetMode.kResetSafeParameters,
            PersistMode.kPersistParameters,
        )

    def grab(self):
        self._motor.set(self.speed_grab)

    def eject(self):
        self._motor.set(self.speed_feed)

    def stop(self):
        self._motor.stopMotor()
