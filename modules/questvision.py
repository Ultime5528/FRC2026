from typing import Generator, Tuple, Optional

import wpimath
from wpimath.geometry import Pose3d, Pose2d

from subsystems.drivetrain import Drivetrain
from ultime.autoproperty import autoproperty
from ultime.module import Module
from ultime.questnav import questnav, quickquestnav

### Offset of the camera relative to the middle of the robot. In robot Coordinate system
robot_to_quest_offset = wpimath.geometry.Transform3d(
    wpimath.geometry.Translation3d(-0.257, -0.28, 0.47),
    wpimath.geometry.Rotation3d.fromDegrees(0.0, 0.0, 180.0),
)


class QuestVisionModule(Module):
    std_translation = autoproperty(0.03)
    std_rotation = autoproperty(0.1)

    def __init__(self, drivetrain: Drivetrain):
        super().__init__()
        self.drivetrain = drivetrain
        self.quest_nav = quickquestnav.QuestNav()
        self.estimated_pose = Pose2d()

    def robotPeriodic(self) -> None:
        self.quest_nav.periodic()

    def getLastPoseTimeStampStdDevs(
        self,
    ) -> Optional[tuple[Pose2d, float, Tuple[float, float, float]]]:
        poseFrame = self.quest_nav.getLastPoseFrame()[0]
        if poseFrame.is_tracking:
            pose = poseFrame.quest_pose_3d
            pose = pose.transformBy(robot_to_quest_offset.inverse())
            self.estimated_pose = pose.toPose2d()
            time_stamp = poseFrame.data_timestamp
            return (
                self.estimated_pose,
                time_stamp,
                (
                    self.std_translation,
                    self.std_translation,
                    self.std_rotation,
                ),
            )

    def getAllUnreadPosesTimestampsStdDevs(
        self,
    ) -> Generator[tuple[Pose2d, float, Tuple[float, float, float]]]:
        for poseFrame in self.quest_nav.getAllUnreadPoseFrames():
            if poseFrame.is_tracking:
                pose = poseFrame.quest_pose_3d
                pose = pose.transformBy(robot_to_quest_offset.inverse())
                self.estimated_pose = pose.toPose2d()
                time_stamp = poseFrame.data_timestamp
                yield (
                    self.estimated_pose,
                    time_stamp,
                    (
                        self.std_translation,
                        self.std_translation,
                        self.std_rotation,
                    ),
                )

    def resetToPose(self, pose: Pose3d):
        self.quest_nav.setPose(pose.transformBy(robot_to_quest_offset))

    def isConnected(self) -> bool:
        return self.quest_nav.isConnected() and self.quest_nav.isTracking()

    def logValues(self):
        self.log("x", self.estimated_pose.x)
        self.log("y", self.estimated_pose.y)
        self.log("yaw", self.estimated_pose.rotation().degrees())
        self.log("isTracking", self.quest_nav.isTracking())
        self.log("battery", self.quest_nav.getBatteryPercent())
