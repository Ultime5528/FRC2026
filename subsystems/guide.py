import wpilib
from wpilib import RobotBase
from wpilib.simulation import EncoderSim

import ports
from ultime.autoproperty import autoproperty
from ultime.linear.linearsubsystem import LinearSubsystem
from ultime.switch import Switch


class Guide(LinearSubsystem):
    position_min = autoproperty(0.0)
    position_max = autoproperty(90.0)

    position_unuse = autoproperty(0.0)
    position_use = autoproperty(90.0)

    position_conversion_factor = autoproperty(1.0)

    def __init__(self):
        super().__init__(
            sim_initial_position=1.0,
            should_reset_min=True,
            should_reset_max=False,
            should_block_min_position=False,
            should_block_max_position=True,
            sim_motor_to_distance_factor=100.0,
        )
        self._motor_output: float = 0.0
        self._encoder_position: float = 0.0
        self._switch_pressed: bool = False

        self._motor = wpilib.VictorSP(ports.PWM.guide_servo)
        self._motor.setInverted(False)
        self._encoder = wpilib.Encoder(
            ports.DIO.guide_encoder_a, ports.DIO.guide_encoder_b
        )
        self._min_switch = Switch(Switch.Type.NormallyOpen, ports.DIO.guide_switch)

        if RobotBase.isSimulation():
            self._sim_encoder = EncoderSim(self._encoder)

    def readInputs(self):
        self._encoder_position = self._encoder.get()
        self._switch_pressed = self._min_switch.isPressed()

    def getMinPosition(self) -> float:
        return self.position_min

    def getMaxPosition(self) -> float:
        return self.position_max

    def setSimSwitchMinPressed(self, pressed: bool) -> None:
        self._min_switch.setSimValue(pressed)

    def setSimSwitchMaxPressed(self, pressed: bool) -> None:
        pass

    def isSwitchMinPressed(self) -> bool:
        return self._switch_pressed

    def isSwitchMaxPressed(self) -> bool:
        return False

    def getEncoderPosition(self) -> float:
        return self._encoder_position

    def getPositionConversionFactor(self):
        return self.position_conversion_factor

    def setSimulationEncoderPosition(self, position: float) -> None:
        self._sim_encoder.setCount(int(position))

    def _setMotorOutput(self, speed: float) -> None:
        self._motor.set(speed)

    def getMotorOutput(self) -> float:
        return self._motor.get()
