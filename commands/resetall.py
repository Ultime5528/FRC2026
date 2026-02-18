from commands2 import ParallelCommandGroup

from commands.climber.move import ResetClimber
from commands.guide import ResetGuide
from commands.pivot.move import ResetPivot
from subsystems.climber import Climber
from subsystems.guide import Guide
from subsystems.pivot import Pivot
from ultime.command import ignore_requirements


@ignore_requirements(["climber", "pivot", "guide"])
class ResetAll(ParallelCommandGroup):
    def __init__(self, climber: Climber, pivot: Pivot, guide: Guide):
        super().__init__(
            ResetClimber.down(climber),
            climber.unhug(),
            ResetPivot.up(pivot),
            ResetGuide.down(guide),
        )
