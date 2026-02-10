from commands2 import Command

from subsystems.climber import Climber
from ultime.linear import manualmovelinear, resetlinear, movelinear
from ultime.autoproperty import autoproperty, FloatProperty
from ultime.linear.movelinear import MoveLinear

_ManualMoveClimber = manualmovelinear.createManualMoveClass(
    lambda: _manual__move_properties.speed_up,
    lambda: _manual__move_properties.speed_down
)

class ManualMoveClimber(_ManualMoveClimber):
    pass

_ResetClimber = resetlinear.createResetLinearClass(
    lambda: _reset_properties.speed_up,
    lambda: _reset_properties.speed_down
)

class ResetClimber(_ResetClimber):
    pass

class MoveClimber(MoveLinear):
    @classmethod
    def Climbed(cls, climber: Climber):
        cmd = cls(
            climber,
            lambda: _move_properties.position_open,
        )
        cmd.setName(cls.__name__ + ".Climbed")
        return cmd

    @classmethod
    def Ready(cls, climber: Climber):
        cmd = cls(
            climber,
            lambda: _move_properties.position_open,
        )
        cmd.setName(cls.__name__ + ".Ready")
        return cmd

    @classmethod
    def Retracted(cls, climber: Climber):
        cmd = cls(
            climber,
            lambda: _move_properties.position_open,
        )
        cmd.setName(cls.__name__ + ".Retracted")
        return cmd

    def __init__(self, climber: Climber, end_position: FloatProperty):
        super().__init__(
            climber,
            end_position,
            lambda: _move_properties.speed_min,
            lambda: _move_properties.speed_max,
            lambda: _move_properties.accel,
        )

class Hugger(Command):
    @classmethod
    def Hug(cls, climber: Climber):
        cmd = cls(
            climber,
            lambda: _move_properties.position_hug,
        )
        cmd.setName(cls.__name__ + ".Hug")
        return cmd

    @classmethod
    def Unhug(cls, climber: Climber):
        cmd = cls(
            climber,
            lambda: _move_properties.position_unhug_left,
            lambda: _move_properties.position_unhug_right,
        )
        cmd.setName(cls.__name__ + ".Unhug")
        return cmd



class _PropertiesManual:
    speed_up = autoproperty(0.25, subtable=ManualMoveClimber.__name__)
    speed_down = autoproperty(-0.25, subtable=ManualMoveClimber.__name__)

_manual__move_properties = _PropertiesManual()

class _PropertiesReset:
    speed_up = autoproperty(0.25, subtable=ResetClimber.__name__)
    speed_down = autoproperty(-0.25, subtable=ResetClimber.__name__)

_reset_properties = _PropertiesReset()

class _PropertiesMove:
    speed_up = autoproperty(0.25, subtable=MoveClimber.__name__)
    speed_down = autoproperty(-0.25, subtable=MoveClimber.__name__)
    accel = autoproperty(5.0, subtable=MoveClimber.__name__)

    position_climbed = autoproperty(0.295, subtable=MoveClimber.__name__)
    position_ready = autoproperty(0.295, subtable=MoveClimber.__name__)
    position_retracted = autoproperty(0.21, subtable=MoveClimber.__name__)
    position_hug_right = autoproperty(30.0, subtable=Hugger.__name__)
    position_hug_left = autoproperty(-30.0, subtable=Hugger.__name__)
    position_unhug_right = autoproperty(0.0, subtable=Hugger.__name__)
    position_unhug_left = autoproperty(0.0, subtable=Hugger.__name__)

_move_properties = _PropertiesMove()