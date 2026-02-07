from subsystems.guide import Guide
from ultime.linear import manualmovelinear, resetlinear, movelinear
from ultime.autoproperty import autoproperty


class ManualMoveGuide:
    pass


ManualMoveGuide = manualmovelinear.createManualMoveClass(
    ManualMoveGuide.__name__,
    lambda: manual_move_properties.speed_up,
    lambda: manual_move_properties.speed_down,
)


class ResetGuide:
    pass


ResetGuide = resetlinear.createResetLinearClass(
    ResetGuide.__name__,
    lambda: reset_properties.speed_up,
    lambda: reset_properties.speed_down,
)


class MoveGuide:
    @staticmethod
    def toOpen(guide: Guide):
        cmd = movelinear.MoveLinear(
            guide,
            move_properties.position_open,
            move_properties.speed_min,
            move_properties.speed_max,
            move_properties.accel,
        )
        cmd.setName(MoveGuide.__name__ + ".toOpen")
        return cmd

    @staticmethod
    def toClose(guide: Guide):
        cmd = movelinear.MoveLinear(
            guide,
            move_properties.position_close,
            move_properties.speed_min,
            move_properties.speed_max,
            move_properties.accel,
        )
        cmd.setName(MoveGuide.__name__ + ".toOpen")
        return cmd


class _PropertiesManual:
    speed_up = autoproperty(0.25, subtable=ManualMoveGuide.__name__)
    speed_down = autoproperty(-0.25, subtable=ManualMoveGuide.__name__)


manual_move_properties = _PropertiesManual()


class _PropertiesReset:
    speed_up = autoproperty(0.25, subtable=ResetGuide.__name__)
    speed_down = autoproperty(-0.25, subtable=ResetGuide.__name__)


reset_properties = _PropertiesReset()


class _PropertiesMove:
    speed_min = autoproperty(0.10, subtable=MoveGuide.__name__)
    speed_max = autoproperty(0.40, subtable=MoveGuide.__name__)
    accel = autoproperty(5.0, subtable=MoveGuide.__name__)

    position_open = autoproperty(10.0, subtable=MoveGuide.__name__)
    position_close = autoproperty(1.0, subtable=MoveGuide.__name__)


move_properties = _PropertiesMove()
