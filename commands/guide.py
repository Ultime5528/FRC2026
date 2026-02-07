from ultime.linear import manualmovelinear, resetlinear
from ultime.autoproperty import autoproperty


class ManualMoveGuide:
    pass


class _PropertiesManual:
    speed_up = autoproperty(0.25, subtable=ManualMoveGuide.__name__)
    speed_down = autoproperty(-0.25, subtable=ManualMoveGuide.__name__)


manual_move_properties = _PropertiesManual()

ManualMoveGuide = manualmovelinear.createManualMoveClass(
    ManualMoveGuide.__name__,
    lambda: manual_move_properties.speed_up,
    lambda: manual_move_properties.speed_down,
)

class ResetGuide:
    pass

class _PropertiesReset:
    speed_up = autoproperty(0.25, subtable=ResetGuide.__name__)
    speed_down = autoproperty(-0.25, subtable=ResetGuide.__name__)

reset_properties = _PropertiesReset()

ResetGuide = resetlinear.createResetLinearClasses(
    ResetGuide.__name__,
    lambda: reset_properties.speed_up,
    lambda: reset_properties.speed_down,
)
