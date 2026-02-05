from ultime import manualmovelinear
from ultime.autoproperty import autoproperty


class ManualMoveGuide:
    pass


class _Properties:
    speed_up = autoproperty(0.25, subtable=ManualMoveGuide.__name__)
    speed_down = autoproperty(-0.25, subtable=ManualMoveGuide.__name__)

manual_move_properties = _Properties()

ManualMoveGuide = manualmovelinear.createManualMoveClass(
    ManualMoveGuide.__name__,
    lambda: manual_move_properties.speed_up,
    lambda: manual_move_properties.speed_down,
)
