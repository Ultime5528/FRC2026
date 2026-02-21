from commands2 import SequentialCommandGroup
from pathplannerlib.path import PathPlannerPath

from commands.drivetrain.auto.alignpreciseafterpath import AlignPreciseAfterPath
from subsystems.drivetrain import Drivetrain


class FollowPathPrecise(SequentialCommandGroup):
    def __init__(self, drivetrain: Drivetrain, path: PathPlannerPath):
        super().__init__()
        self.drivetrain = drivetrain
        self.addRequirements(drivetrain)
        self.path = path

        self.addCommands(
            self.drivetrain.getFollowCommand(self.path),
            AlignPreciseAfterPath(self.drivetrain, self.path),
        )
