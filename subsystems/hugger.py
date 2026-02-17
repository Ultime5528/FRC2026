import wpilib

import ports
from ultime.subsystem import Subsystem


class Hugger(Subsystem):

    def __init__(self):
        super().__init__()

        self.position_hug_left = self.createProperty(100.0)
        self.position_unhug_left = self.createProperty(80.0)
        self.position_hug_right = self.createProperty(80.0)
        self.position_unhug_right = self.createProperty(100.0)
        self.delay_hug = self.createProperty(2.0)

        self._servo_left = wpilib.Servo(ports.PWM.hugger_servo_left)
        self._servo_right = wpilib.Servo(ports.PWM.hugger_servo_right)

    def hug(self):
        self._servo_left.setAngle(self.position_hug_left)
        self._servo_right.setAngle(self.position_hug_right)

    def unhug(self):
        self._servo_left.setAngle(self.position_unhug_left)
        self._servo_right.setAngle(self.position_unhug_right)
