import rev
import wpilib
import ports
from ultime.autoproperty import autoproperty
from ultime.linearsubsystem import LinearSubsystem
from ultime.switch import Switch


class Intake(LinearSubsystem):
    speed_intake = autoproperty(0.5)
    speed_pivot_ascend = autoproperty(0.5)
    speed_pivot_descend = autoproperty(-0.5)
    maintain = autoproperty(0.2)
    min_position = autoproperty(0)
    max_position = autoproperty(0)

    def __init__(self):
        super().__init__(0.0, True, True, True, True, 0.0, 9.81)
        self._motor_pivot = rev.SparkMax(
            ports.CAN.intake_motor_pivot, rev.SparkMax.MotorType.kBrushless
        )
        self._encoder_pivot = self._motor_pivot.getEncoder()
        self.motor_intake = rev.SparkMax(
            ports.CAN.intake_motor_intake, rev.SparkMax.MotorType.kBrushless
        )
        self._switch_min = Switch(
            Switch.Type.NormallyClosed, ports.DIO.intake_switch_min
        )
        self._switch_max = Switch(
            Switch.Type.NormallyClosed, ports.DIO.intake_switch_max
        )

    def roll_intake(self):
        self.motor_intake.set(self.speed_intake)

    def maintainer(self):
        self._motor_pivot.set(self.maintain)

    def stop_intake(self):
        self.motor_intake.stopMotor()

    def ascend_pivot(self):
        self._motor_pivot.set(self.speed_pivot_ascend)

    def descend_pivot(self):
        self._motor_pivot.set(self.speed_pivot_descend)

    def stop_pivot(self):
        self._motor_pivot.stopMotor()

    def initSimulationComponents(self):
        return self._motor_pivot

    def getMinPosition(self) -> float:
        return self.min_position

    def getMaxPosition(self) -> float:
        return self.max_position

    def isSwitchMinPressed(self) -> bool:
        return not self._switch_min.isPressed()

    def isSwitchMaxPressed(self) -> bool:
        return not self._switch_max.isPressed()

    def getEncoderPosition(self) -> float:
        return self._encoder_pivot.getPosition()

    def setSimulationEncoderPosition(self, position: float) -> None:
        self._encoder_pivot.setPosition(position)

    def getPositionConversionFactor(self) -> float:
        return 1.0

    def _setMotorOutput(self, speed: float) -> None:
        self._motor_pivot.set(speed)

    def getMotorOutput(self) -> float:
        return self._motor_pivot.get()
