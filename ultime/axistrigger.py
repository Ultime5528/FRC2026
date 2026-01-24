from typing import Literal, Union

import commands2
import wpilib


class AxisTrigger(commands2.button.Trigger):
    def __init__(
        self,
        stick: Union[wpilib.Joystick, commands2.button.CommandJoystick],
        axis: int,
        direction: Literal["up", "down"],
    ):
        if direction != "up" and direction != "down":
            raise ValueError(f"direction must be 'up' or 'down': {direction}")
        super().__init__(
            lambda: (
                stick.getRawAxis(axis) < -0.5
                if direction == "down"
                else stick.getRawAxis(axis) > 0.5
            )
        )
