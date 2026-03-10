from commands2 import SequentialCommandGroup

from commands.climber.move import MoveClimber
from commands.hugger.unhug import Unhug
from subsystems.climber import Climber
from subsystems.hugger import Hugger


class RetractAndUnhug(SequentialCommandGroup):
    def __init__(
        self,
        climber: Climber,
        hugger: Hugger,
    ):
        super().__init__(
            MoveClimber.toReady(climber),
            Unhug(hugger),
        )
