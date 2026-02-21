import rev
from rev import SparkMaxSim
from wpilib import RobotBase
from wpimath._controls._controls.plant import DCMotor

import ports
from ultime.autoproperty import autoproperty
from ultime.linear.linearsubsystem import LinearSubsystem
from ultime.switch import Switch


class Pivot(LinearSubsystem):
    speed_maintain = autoproperty(0.0)
    min_position = autoproperty(0.0)
    max_position = autoproperty(6.35)
    position_maintain_min = autoproperty(0.5)
    position_maintain_max = autoproperty(6.5)

    position_conversion_factor = autoproperty(1.0)

    def __init__(self):
        super().__init__(
            sim_initial_position=1.0,
            should_reset_min=False,
            should_reset_max=True,
            should_block_min_position=True,
            should_block_max_position=False,
            should_block_min_switch=True,
            should_block_max_switch=True,
            sim_motor_to_distance_factor=2.0,
            sim_gravity=0.0,
        )
        self._encoder_position: float = 0.0
        self._switch_max_pressed: bool = False
        self._switch_min_pressed: bool = False

        self._motor = rev.SparkMax(
            ports.CAN.pivot_motor, rev.SparkMax.MotorType.kBrushless
        )
        self._encoder = self._motor.getEncoder()
        self._switch_min = Switch(
            Switch.Type.AlwaysUnpressed, ports.DIO.pivot_switch_min
        )
        self._switch_max = Switch(Switch.Type.NormallyOpen, ports.DIO.pivot_switch_max)

        if RobotBase.isSimulation():
            self._motor_sim = SparkMaxSim(self._motor, DCMotor.NEO(1))
            self._encoder_sim = self._motor_sim.getRelativeEncoderSim()

    def readInputs(self):
        self._encoder_position = self._encoder.getPosition()
        self._switch_max_pressed = self._switch_max.isPressed()
        self._switch_min_pressed = self._switch_min.isPressed()

    def maintain(self):
        position = self.getPosition()

        if self.position_maintain_min <= position <= self.position_maintain_max:
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
        return self._switch_min_pressed

    def isSwitchMaxPressed(self) -> bool:
        return self._switch_max_pressed

    def setSimSwitchMinPressed(self, pressed: bool) -> None:
        self._switch_min.setSimValue(pressed)

    def setSimSwitchMaxPressed(self, pressed: bool) -> None:
        self._switch_max.setSimValue(pressed)

    def getEncoderPosition(self) -> float:
        return self._encoder_position

    def setSimulationEncoderPosition(self, position: float) -> None:
        self._encoder_sim.setPosition(position)

    def getPositionConversionFactor(self) -> float:
        return self.position_conversion_factor

    def _setMotorOutput(self, speed: float) -> None:
        self._motor.set(speed)

    def getMotorOutput(self) -> float:
        return self._motor.get()
