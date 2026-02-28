from commands2 import ParallelCommandGroup

from commands.climber.move import ResetClimber
from commands.guide import ResetGuide
from commands.hugger.unhug import Unhug
from commands.pivot.move import ResetPivot
from subsystems.climber import Climber
from subsystems.guide import Guide
from subsystems.hugger import Hugger
from subsystems.pivot import Pivot


class ResetAll(ParallelCommandGroup):
    def __init__(self, climber: Climber, hugger: Hugger, pivot: Pivot, guide: Guide):
        super().__init__(
            ResetClimber.down(climber),
            Unhug(hugger),
            ResetPivot.down(pivot),
            ResetGuide.down(guide),
        )
