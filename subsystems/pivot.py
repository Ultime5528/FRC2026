from rev import SparkMaxSim
from wpilib import RobotBase
from wpimath._controls._controls.plant import DCMotor

import ports
import rev
from ultime.autoproperty import autoproperty
from ultime.linear.linearsubsystem import LinearSubsystem
from ultime.switch import Switch


class Pivot(LinearSubsystem):
    speed_maintain = autoproperty(0.2)
    min_position = autoproperty(0.0)
    max_position = autoproperty(5.0)
    position_maintain_min = autoproperty(0.0)
    position_maintain_max = autoproperty(5.0)

    def __init__(self):
        super().__init__(1.0, True, True, False, False, 2.0, 0.0)
        self._motor = rev.SparkMax(
            ports.CAN.pivot_motor, rev.SparkMax.MotorType.kBrushless
        )
        self._encoder = self._motor.getEncoder()
        self._switch_min = Switch(Switch.Type.NormallyOpen, ports.DIO.intake_switch_min)
        self._switch_max = Switch(Switch.Type.NormallyOpen, ports.DIO.intake_switch_max)

        if RobotBase.isSimulation():
            self._motor_sim = SparkMaxSim(self._motor, DCMotor.NEO(1))
            self._encoder_sim = self._motor_sim.getRelativeEncoderSim()

    def maintain(self):
        position = self.getPosition()

        if position >= self.position_maintain_min:
            self._motor.set(self.speed_maintain)

        if position <= self.position_maintain_max:
            self._motor.set(self.speed_maintain)
        else:
            self._motor.stopMotor()

    def stop(self):
        self._motor.stopMotor()

    def getMinPosition(self) -> float:
        return self.min_position

    def getMaxPosition(self) -> float:
        return self.max_position

    def isSwitchMinPressed(self) -> bool:
        return self._switch_min.isPressed()

    def isSwitchMaxPressed(self) -> bool:
        return self._switch_max.isPressed()

    def setSimSwitchMinPressed(self, pressed: bool) -> None:
        self._switch_min.setSimValue(pressed)

    def setSimSwitchMaxPressed(self, pressed: bool) -> None:
        self._switch_max.setSimValue(pressed)

    def getEncoderPosition(self) -> float:
        return self._encoder.getPosition()

    def setSimulationEncoderPosition(self, position: float) -> None:
        self._encoder_sim.setPosition(position)

    def getPositionConversionFactor(self) -> float:
        return 1.0

    def _setMotorOutput(self, speed: float) -> None:
        self._motor.set(speed)

    def getMotorOutput(self) -> float:
        return self._motor.get()
