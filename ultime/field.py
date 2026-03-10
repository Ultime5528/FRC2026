import wpilib
from pathplannerlib.path import PathPlannerPath
from pathplannerlib.util import FlippingUtil
from wpilib import DriverStation
from wpimath.geometry import Pose2d, Translation2d


def mirrorPose(pose: Pose2d) -> Pose2d:
    translation = Translation2d(pose.translation())
    new_translation = PathPlannerPath._mirrorTranslation(translation)
    return Pose2d(new_translation, pose.rotation())


def isRight(pose: Pose2d) -> bool:
    is_red = DriverStation.getAlliance() == DriverStation.Alliance.kRed

    if is_red:
        return pose.translation().y > (FlippingUtil.fieldSizeY / 2)
    else:
        return pose.translation().y < (FlippingUtil.fieldSizeY / 2)
