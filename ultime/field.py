from pathplannerlib.path import PathPlannerPath
from wpimath.geometry import Pose2d, Translation2d


def mirrorPose(pose: Pose2d) -> Pose2d:
    translation = Translation2d(pose.translation())
    new_translation = PathPlannerPath._mirrorTranslation(translation)
    return Pose2d(new_translation, pose.rotation())
