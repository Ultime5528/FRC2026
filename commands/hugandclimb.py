from commands2 import SequentialCommandGroup

from commands.climber.move import MoveClimber
from commands.hugger.hug import Hug

from subsystems.climber import Climber
from subsystems.hugger import Hugger
from ultime.command import ignore_requirements


@ignore_requirements(["shooter", "hugger"])
class HugAndClimb(SequentialCommandGroup):
    def __init__(
        self,
        climber: Climber,
        hugger: Hugger,
    ):
        super().__init__(
            Hug(hugger),
            MoveClimber.toClimbed(climber),
        )
