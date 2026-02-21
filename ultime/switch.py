from enum import Enum, auto
from typing import Optional

from wpilib import DigitalInput
from wpilib.simulation import DIOSim

from ultime.modulerobot import is_simulation, is_real


class Switch:
    class Type(Enum):
        NormallyOpen = auto()  # The switch is False when not pressed
        NormallyClosed = auto()  # The switch is True when not pressed
        AlwaysPressed = auto()  # The switch is always open
        AlwaysUnpressed = auto()  # The switch is always close

    def __init__(self, switch_type: "Switch.Type", port: Optional[int] = None):
        if not isinstance(switch_type, Switch.Type):
            raise TypeError(
                f"switch_type is not instance of Switch.Type : {switch_type}"
            )

        self._type = switch_type

        if (
            switch_type == Switch.Type.NormallyClosed
            or switch_type == Switch.Type.NormallyOpen
        ):
            self._input = DigitalInput(port)
        elif self._type == Switch.Type.AlwaysPressed:
            self._sim_switch_state = True
        elif self._type == Switch.Type.AlwaysUnpressed:
            self._sim_switch_state = False

        if is_simulation:
            if self._type == Switch.Type.NormallyOpen:
                self._sim_input = DIOSim(self._input)
                self._sim_input.setValue(False)
            elif self._type == Switch.Type.NormallyClosed:
                self._sim_input = DIOSim(self._input)
                self._sim_input.setValue(True)

    def isPressed(self) -> bool:
        if self._type == Switch.Type.NormallyOpen:
            return self._input.get()
        elif self._type == Switch.Type.NormallyClosed:
            return not self._input.get()
        elif self._type == Switch.Type.AlwaysPressed:
            return self._sim_switch_state
        elif self._type == Switch.Type.AlwaysUnpressed:
            return self._sim_switch_state
        else:
            raise TypeError(f"Type is not instance of Switch.Type: {type}")

    def setSimValue(self, pressed):
        if is_real:
            raise RuntimeError("setSimValue should only be called in simulation")
        if self._type == Switch.Type.NormallyOpen:
            self._sim_input.setValue(pressed)
        elif self._type == Switch.Type.NormallyClosed:
            self._sim_input.setValue(not pressed)
        elif self._type == Switch.Type.AlwaysPressed:
            self._sim_switch_state = pressed
        elif self._type == Switch.Type.AlwaysUnpressed:
            self._sim_switch_state = pressed
        else:
            raise TypeError(f"Type is not instance of Switch.Type: {type}")

    def getChannel(self):
        return self._input.getChannel()

    def getType(self):
        return self._type
