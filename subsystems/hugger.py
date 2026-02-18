import wpilib

import ports
from ultime.autoproperty import autoproperty
from ultime.subsystem import Subsystem


class Hugger(Subsystem):

    position_hug_left = autoproperty(0.0)
    position_unhug_left = autoproperty(1.0)
    position_hug_right = autoproperty(0.0)
    position_unhug_right = autoproperty(0.0)
    delay_hug = autoproperty(2.0)

    def __init__(self):
        super().__init__()

        self._servo_left = wpilib.Servo(ports.PWM.hugger_servo_left)
        self._servo_right = wpilib.Servo(ports.PWM.hugger_servo_right)

    def hug(self):
        self._servo_left.set(self.position_hug_left)
        self._servo_right.set(self.position_hug_right)

    def unhug(self):
        self._servo_left.set(self.position_unhug_left)
        self._servo_right.set(self.position_unhug_right)
