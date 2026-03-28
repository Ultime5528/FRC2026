from wpimath.geometry import Pose2d

from modules.positionestimator import PositionEstimator
from modules.questvision import QuestVisionModule
from subsystems.drivetrain import Drivetrain
from ultime.command import Command


class ResetOdometryAndQuest(Command):
    def __init__(self, drivetrain: Drivetrain, quest_nav: QuestVisionModule, positionEstimator: PositionEstimator):
        super().__init__()
        self.drivetrain = drivetrain
        self.quest_nav = quest_nav
        self.positionEstimator = positionEstimator
        self.addRequirements(drivetrain)

    def initialize(self):
        pose = self.drivetrain.getPose()
        self.drivetrain.resetToPose(pose)
        self.quest_nav.resetToPose(pose)
        self.positionEstimator.is_initial_pose_reset_done = True

    def isFinished(self) -> bool:
        return True
