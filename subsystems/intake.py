import rev
import wpilib

import ports
from ultime.autoproperty import autoproperty
from ultime.linearsubsystem import LinearSubsystem
from ultime.switch import Switch


class Intake(LinearSubsystem):
    speed_intake = autoproperty(0.5)
    maintain = autoproperty(0.2)
    min_position = autoproperty(0)
    max_position = autoproperty(0)

    def __init__(self):
        super().__init__()
        self._motor_pivot = rev.SparkMax(
            ports.CAN.intake_motor_pivot, rev.SparkMax.MotorType.kBrushless
        )
        self._encoder_pivot = self.motor_pivot.getEncoder()
        self.motor_intake = rev.SparkMax(
            ports.CAN.intake_motor_intake, rev.SparkMax.MotorType.kBrushless
        )
        self._switch_min = Switch(
            Switch.Type.NormallyClosed, ports.DIO.intake_switch_min
        )
        self._switch_max = Switch(
            Switch.Type.NormallyClosed, ports.DIO.intake_switch_max
        )

    def roll(self):
        self.moteur_intake.set(self.speed_intake)

    def maintainer(self):
        self.moteur_pivot.set(self.maintain)

    def stop_intake(self):
        self.moteur_intake.stopMotor()

    def stop_pivot(self):
        self.moteur_pivot.stopMotor()

    def initSimulationComponents(self):
        self._motor_pivot

    def getMinPosition(self) -> float:
        return self.min_position

    def getMaxPosition(self) -> float:
        return self.max_position

    def isSwitchMinPressed(self) -> bool:
        return self.switch_min.get()

    def isSwitchMaxPressed(self) -> bool:
        return self.switch_max.get()

    def getEncoderPosition(self) -> float:
        return self.encoder_pivot.getPosition()

    def setSimulationEncoderPosition(self, position: float) -> None:
        self._sim_encoder_pivot.setEncoderPosition(position)

    def getPositionConversionFactor(self) -> float:
        pass

    def _setMotorOutput(self, speed: float) -> None:
        self._motor_pivot.set(speed)

    def getMotorOutput(self) -> float:
        return self._motor_pivot.getOutputCurrent()
