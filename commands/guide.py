from subsystems.guide import Guide
from ultime.linear import manualmovelinear, resetlinear, movelinear
from ultime.autoproperty import autoproperty, FloatProperty
from ultime.linear.movelinear import MoveLinear


_ManualMoveGuide = manualmovelinear.createManualMoveClass(
    lambda: _manual_move_properties.speed_up,
    lambda: _manual_move_properties.speed_down,
)


class ManualMoveGuide(_ManualMoveGuide):
    pass


_ResetGuide = resetlinear.createResetLinearClass(
    lambda: _reset_properties.speed_up,
    lambda: _reset_properties.speed_down,
)


class ResetGuide(_ResetGuide):
    pass


class MoveGuide(MoveLinear):
    @classmethod
    def toOpen(cls, guide: Guide):
        cmd = cls(
            guide,
            lambda: _move_properties.position_open,
        )
        cmd.setName(cls.__name__ + ".toOpen")
        return cmd

    @classmethod
    def toClose(cls, guide: Guide):
        cmd = cls(
            guide,
            lambda: _move_properties.position_close,
        )
        cmd.setName(cls.__name__ + ".toClose")
        return cmd

    def __init__(self, guide: Guide, end_position: FloatProperty):
        super().__init__(
            guide,
            end_position,
            lambda: _move_properties.speed_min,
            lambda: _move_properties.speed_max,
            lambda: _move_properties.accel,
        )


class _PropertiesManual:
    speed_up = autoproperty(0.25, subtable=ManualMoveGuide.__name__)
    speed_down = autoproperty(-0.25, subtable=ManualMoveGuide.__name__)


_manual_move_properties = _PropertiesManual()


class _PropertiesReset:
    speed_up = autoproperty(0.25, subtable=ResetGuide.__name__)
    speed_down = autoproperty(-0.25, subtable=ResetGuide.__name__)


_reset_properties = _PropertiesReset()


class _PropertiesMove:
    speed_min = autoproperty(0.10, subtable=MoveGuide.__name__)
    speed_max = autoproperty(0.40, subtable=MoveGuide.__name__)
    accel = autoproperty(5.0, subtable=MoveGuide.__name__)

    position_open = autoproperty(10.0, subtable=MoveGuide.__name__)
    position_close = autoproperty(1.0, subtable=MoveGuide.__name__)


_move_properties = _PropertiesMove()
