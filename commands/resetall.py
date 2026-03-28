from commands2 import ParallelCommandGroup

from commands.climber.move import ResetClimber
from commands.drivetrain.resetodometryandquest import ResetOdometryAndQuest
from commands.hugger.unhug import Unhug
from subsystems.climber import Climber
from subsystems.drivetrain import Drivetrain
from subsystems.hugger import Hugger
from ultime.questnav.questnav import QuestNav


class ResetAll(ParallelCommandGroup):
    def __init__(self, climber: Climber, hugger: Hugger):
        super().__init__(
            ResetClimber.down(climber),
            Unhug(hugger),
        )
