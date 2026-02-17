from subsystems.climber import Climber
from ultime.autoproperty import autoproperty, FloatProperty
from ultime.linear import manualmovelinear, resetlinear
from ultime.linear.movelinear import MoveLinear

_ManualMoveClimber = manualmovelinear.createManualMoveClass(
    lambda: _manual_move_properties.speed_up, lambda: _manual_move_properties.speed_down
)


class ManualMoveClimber(_ManualMoveClimber):
    pass


_ResetClimber = resetlinear.createResetLinearClass(
    lambda: _reset_properties.speed_up, lambda: _reset_properties.speed_down
)


class ResetClimber(_ResetClimber):
    pass


class MoveClimber(MoveLinear):
    @classmethod
    def toClimbed(cls, climber: Climber):
        cmd = cls(
            climber,
            lambda: _move_properties.position_climbed,
        )
        cmd.setName(cls.__name__ + ".Climbed")
        return cmd

    @classmethod
    def toReady(cls, climber: Climber):
        cmd = cls(
            climber,
            lambda: _move_properties.position_ready,
        )
        cmd.setName(cls.__name__ + ".Ready")
        return cmd

    @classmethod
    def toRetracted(cls, climber: Climber):
        cmd = cls(
            climber,
            lambda: _move_properties.position_retracted,
        )
        cmd.setName(cls.__name__ + ".Retracted")
        return cmd

    def __init__(self, climber: Climber, end_position: FloatProperty):
        super().__init__(
            climber,
            end_position,
            lambda: _move_properties.speed_up,
            lambda: _move_properties.speed_down,
            lambda: _move_properties.accel,
        )


class _PropertiesManual:
    speed_up = autoproperty(0.25, subtable=ManualMoveClimber.__name__)
    speed_down = autoproperty(-0.25, subtable=ManualMoveClimber.__name__)


_manual_move_properties = _PropertiesManual()


class _PropertiesReset:
    speed_up = autoproperty(0.5, subtable=ResetClimber.__name__)
    speed_down = autoproperty(-0.5, subtable=ResetClimber.__name__)


_reset_properties = _PropertiesReset()


class _PropertiesMove:
    speed_up = autoproperty(0.1, subtable=MoveClimber.__name__)
    speed_down = autoproperty(1.0, subtable=MoveClimber.__name__)
    accel = autoproperty(0.5, subtable=MoveClimber.__name__)
    position_climbed = autoproperty(100.0, subtable=MoveClimber.__name__)
    position_ready = autoproperty(190.0, subtable=MoveClimber.__name__)
    position_retracted = autoproperty(0.0, subtable=MoveClimber.__name__)


_move_properties = _PropertiesMove()
