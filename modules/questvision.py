from typing import Generator, List, Tuple

import wpimath
from wpimath.geometry import Pose3d, Pose2d

from subsystems.drivetrain import Drivetrain
from ultime.autoproperty import autoproperty
from ultime.module import Module
from ultime.questnav import questnav

### Offset of the camera relative to the middle of the robot. In robot Coordinate system
robot_to_quest_offset = wpimath.geometry.Transform3d(
    wpimath.geometry.Translation3d(-0.257, -0.245, 0.460),
    wpimath.geometry.Rotation3d.fromDegrees(0.0, 0.0, 0.0),
)


class QuestVisionModule(Module):
    std_translation: float = autoproperty(0.03)
    std_rotation: float = autoproperty(0.1)

    def __init__(self, drivetrain: Drivetrain):
        super().__init__()
        self.drivetrain = drivetrain
        self.quest_nav = questnav.QuestNav()
        self.estimated_pose = Pose3d()

    def getAllUnreadEstimatedPosesWithTimeStampAndStdDevs(
        self,
    ) -> Generator[tuple[Pose2d, float, Tuple[float, float, float]]]:
        for poseFrame in self.quest_nav.getAllUnreadPoseFrames():
            self.estimated_pose = poseFrame.quest_pose_3d
            self.estimated_pose = self.estimated_pose.transformBy(
                robot_to_quest_offset.inverse()
            )
            self.estimated_pose = self.estimated_pose.toPose2d()
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
        self.quest_nav.setPose(pose)

    def isConnected(self) -> bool:
        return self.quest_nav.isConnected()

    def logValues(self):
        self.log("x", self.estimated_pose.x)
        self.log("y", self.estimated_pose.y)
        self.log("z", self.estimated_pose.z)
        self.log("roll", self.estimated_pose.rotation().x)
        self.log("pitch", self.estimated_pose.rotation().y)
        self.log("yaw", self.estimated_pose.rotation().z)
