from commands2 import ParallelCommandGroup

from commands.climber.move import ResetClimber
from commands.guide.move import ResetGuide
from commands.hugger.unhug import Unhug
from subsystems.climber import Climber
from subsystems.guide import Guide
from subsystems.hugger import Hugger


class ResetAll(ParallelCommandGroup):
    def __init__(self, climber: Climber, hugger: Hugger, guide: Guide):
        super().__init__(
            ResetClimber.down(climber),
            Unhug(hugger),
            ResetGuide.down(guide),
        )
