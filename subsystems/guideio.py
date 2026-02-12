from dataclasses import dataclass
from typing import Optional

import wpilib

import ports
from ultime.io import IO
from ultime.switch import Switch


@dataclass
class GuideInputs:
    motor_output: float = 0.0
    encoder_position: float = 0.0
    switch_pressed: bool = False


@dataclass
class GuideOutputs:
    motor_output: Optional[float] = None

    def reset(self):
        self.motor_output = None


class GuideIO(IO):
    def __init__(self):
        super().__init__()
        self._motor = wpilib.VictorSP(ports.PWM.guide_servo)
        self._motor.setInverted(False)
        self._encoder = wpilib.Encoder(
            ports.DIO.guide_encoder_a, ports.DIO.guide_encoder_b
        )
        self._min_switch = Switch(Switch.Type.NormallyOpen, ports.DIO.guide_switch)

        self.inputs = GuideInputs()
        self.outputs = GuideOutputs()

    def updateInputs(self):
        self.inputs.motor_output = self._motor.get()
        self.inputs.encoder_position = self._encoder.get()
        self.inputs.switch_pressed = self._min_switch.isPressed()

    def sendOutputs(self):
        motor_output = self.outputs.motor_output

        if motor_output is not None:
            self._motor.set(motor_output)

        self.outputs.reset()
