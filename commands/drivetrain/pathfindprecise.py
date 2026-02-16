from commands2 import SequentialCommandGroup
from wpimath.geometry import Pose2d

from commands.drivetrain.alignpreciseafterpath import AlignPreciseAfterPath
from subsystems.drivetrain import Drivetrain


class FollowPathPrecise(SequentialCommandGroup):
    def __init__(self, drivetrain: Drivetrain, pose: Pose2d):
        super().__init__()
        self.drivetrain = drivetrain
        self.addRequirements(drivetrain)
        self.pose = pose

        self.addCommands(
            self.drivetrain.getFollowCommand(self.path),
            AlignPreciseAfterPath(self.drivetrain, self.pose),
        )
