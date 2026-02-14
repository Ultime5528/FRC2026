import rev
from rev import SparkMaxSim
from wpilib._wpilib import RobotBase
from wpimath._controls._controls.plant import DCMotor

import ports
from ultime.autoproperty import autoproperty
from ultime.linear.linearsubsystem import LinearSubsystem
from ultime.switch import Switch


class Intake(LinearSubsystem):
    speed_feeder = autoproperty(0.5)
    maintain = autoproperty(0.2)
    min_position = autoproperty(0.0)
    max_position = autoproperty(5.0)

    def __init__(self):
        super().__init__(1.0, True, True, False, False, 2.0, 0.0)
        self._motor_pivot = rev.SparkMax(
            ports.CAN.intake_motor_pivot, rev.SparkMax.MotorType.kBrushless
        )
        self._encoder_pivot = self._motor_pivot.getEncoder()

        self.motor_feeder = rev.SparkMax(
            ports.CAN.intake_motor_intake, rev.SparkMax.MotorType.kBrushless
        )
        self._switch_min = Switch(Switch.Type.NormallyOpen, ports.DIO.intake_switch_min)
        self._switch_max = Switch(Switch.Type.NormallyOpen, ports.DIO.intake_switch_max)

        if RobotBase.isSimulation():
            self._motor_pivot_sim = SparkMaxSim(self._motor_pivot, DCMotor.NEO(1))
            self._encoder_sim = self._motor_pivot_sim.getRelativeEncoderSim()

    def feed(self):
        self.motor_feeder.set(self.speed_feeder)

    def maintainer(self):
        self._motor_pivot.set(self.maintain)

    def stop_feeder(self):
        self.motor_feeder.stopMotor()

    def stop_pivot(self):
        self._motor_pivot.stopMotor()

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
        return self._encoder_pivot.getPosition()

    def setSimulationEncoderPosition(self, position: float) -> None:
        self._encoder_sim.setPosition(position)

    def getPositionConversionFactor(self) -> float:
        return 1.0

    def _setMotorOutput(self, speed: float) -> None:
        self._motor_pivot.set(speed)

    def getMotorOutput(self) -> float:
        return self._motor_pivot.get()
