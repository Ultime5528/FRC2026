import wpilib
from wpilib import RobotBase
from wpilib.simulation import EncoderSim

import ports
from subsystems.guideio import GuideIO
from ultime.autoproperty import autoproperty
from ultime.linear.linearsubsystem import LinearSubsystem
from ultime.modulerobot import is_simulation


class Guide(LinearSubsystem):
    position_min = autoproperty(0.0)
    position_max = autoproperty(90.0)

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

        self._io = GuideIO()
        self._inputs = self._io.inputs
        self._outputs = self._io.outputs

        if is_simulation:
            encoder = self._io._encoder
            self._sim_encoder = EncoderSim(encoder)

    def getMinPosition(self) -> float:
        return self.position_min

    def getMaxPosition(self) -> float:
        return self.position_max

    def setSimSwitchMinPressed(self, pressed: bool) -> None:
        self._io._min_switch.setSimValue(pressed)

    def setSimSwitchMaxPressed(self, pressed: bool) -> None:
        pass

    def isSwitchMinPressed(self) -> bool:
        return self._inputs.switch_pressed

    def isSwitchMaxPressed(self) -> bool:
        return False

    def getEncoderPosition(self) -> float:
        return self._inputs.encoder_position

    def getPositionConversionFactor(self):
        return self.position_conversion_factor

    def setSimulationEncoderPosition(self, position: float) -> None:
        self._sim_encoder.setCount(int(position))

    def _setMotorOutput(self, speed: float) -> None:
        self._outputs.motor_output = speed

    def getMotorOutput(self) -> float:
        return self._inputs.motor_output
