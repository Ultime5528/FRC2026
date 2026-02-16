from subsystems.pivot import Pivot
from ultime.autoproperty import autoproperty, FloatProperty
from ultime.linear import manualmovelinear, resetlinear
from ultime.linear.movelinear import MoveLinear

_ManualMovePivot = manualmovelinear.createManualMoveClass(
    lambda: manual_move_properties.speed_up,
    lambda: manual_move_properties.speed_down,
)


class ManualMovePivot(_ManualMovePivot):
    pass


_ResetPivot = resetlinear.createResetLinearClass(
    lambda: reset_properties.speed_up,
    lambda: reset_properties.speed_down,
)


class ResetPivot(_ResetPivot):
    pass


class MovePivot(MoveLinear):
    @classmethod
    def toUp(cls, pivot: Pivot):
        cmd = cls(
            pivot,
            lambda: move_properties.position_up,
        )
        cmd.setName(cls.__name__ + ".toUp")
        return cmd

    @classmethod
    def toDown(cls, pivot: Pivot):
        cmd = cls(
            pivot,
            lambda: move_properties.position_down,
        )
        cmd.setName(cls.__name__ + ".toDown")
        return cmd

    def __init__(self, pivot: Pivot, end_position: FloatProperty):
        super().__init__(
            pivot,
            end_position,
            lambda: move_properties.speed_min,
            lambda: move_properties.speed_max,
            lambda: move_properties.accel,
        )


class _PropertiesManual:
    speed_up = autoproperty(0.25, subtable=ManualMovePivot.__name__)
    speed_down = autoproperty(-0.25, subtable=ManualMovePivot.__name__)


manual_move_properties = _PropertiesManual()


class _PropertiesReset:
    speed_up = autoproperty(0.25, subtable=ResetPivot.__name__)
    speed_down = autoproperty(-0.25, subtable=ResetPivot.__name__)


reset_properties = _PropertiesReset()


class _PropertiesMove:
    speed_min = autoproperty(0.10, subtable=MovePivot.__name__)
    speed_max = autoproperty(0.40, subtable=MovePivot.__name__)
    accel = autoproperty(5.0, subtable=MovePivot.__name__)

    position_up = autoproperty(10.0, subtable=MovePivot.__name__)
    position_down = autoproperty(1.0, subtable=MovePivot.__name__)


move_properties = _PropertiesMove()
