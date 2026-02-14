from subsystems.intake import Intake
from ultime.autoproperty import autoproperty, FloatProperty
from ultime.linear import manualmovelinear, resetlinear
from ultime.linear.movelinear import MoveLinear

_ManualMoveIntake = manualmovelinear.createManualMoveClass(
    lambda: manual_move_properties.speed_up,
    lambda: manual_move_properties.speed_down,
)


class ManualMoveIntake(_ManualMoveIntake):
    pass


_ResetIntake = resetlinear.createResetLinearClass(
    lambda: reset_properties.speed_up,
    lambda: reset_properties.speed_down,
)


class ResetIntake(_ResetIntake):
    pass


class MoveIntake(MoveLinear):
    @classmethod
    def toUp(cls, intake: Intake):
        cmd = cls(
            intake,
            lambda: move_properties.position_up,
        )
        cmd.setName(cls.__name__ + ".toUp")
        return cmd

    @classmethod
    def toDown(cls, intake: Intake):
        cmd = cls(
            intake,
            lambda: move_properties.position_down,
        )
        cmd.setName(cls.__name__ + ".toDown")
        return cmd

    def __init__(self, intake: Intake, end_position: FloatProperty):
        super().__init__(
            intake,
            end_position,
            lambda: move_properties.speed_min,
            lambda: move_properties.speed_max,
            lambda: move_properties.accel,
        )


class _PropertiesManual:
    speed_up = autoproperty(0.25, subtable=ManualMoveIntake.__name__)
    speed_down = autoproperty(-0.25, subtable=ManualMoveIntake.__name__)


manual_move_properties = _PropertiesManual()


class _PropertiesReset:
    speed_up = autoproperty(0.25, subtable=ResetIntake.__name__)
    speed_down = autoproperty(-0.25, subtable=ResetIntake.__name__)


reset_properties = _PropertiesReset()


class _PropertiesMove:
    speed_min = autoproperty(0.10, subtable=MoveIntake.__name__)
    speed_max = autoproperty(0.40, subtable=MoveIntake.__name__)
    accel = autoproperty(5.0, subtable=MoveIntake.__name__)

    position_up = autoproperty(10.0, subtable=MoveIntake.__name__)
    position_down = autoproperty(1.0, subtable=MoveIntake.__name__)


move_properties = _PropertiesMove()
