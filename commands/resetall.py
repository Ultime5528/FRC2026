from commands2 import ParallelCommandGroup
from commands2.cmd import parallel

from commands.climber.move import ResetClimber
from commands.pivot.move import ResetPivot
from subsystems.climber import Climber
from subsystems.pivot import Pivot


class ResetAll(ParallelCommandGroup):
    def __init__(
        self,
        climber: Climber,
        pivot: Pivot,
    ):

        super().__init__(
            parallel(
                ResetClimber(climber).withTimeout(1.5),
                ResetPivot(pivot),
            )
        )
