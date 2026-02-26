import wpimath
from wpimath.geometry import Pose3d

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
    std_translation = autoproperty(0.03)
    std_rotation = autoproperty(0.1)

    def __init__(self, drivetrain: Drivetrain):
        super().__init__()
        self.drivetrain = drivetrain
        self.questnav = questnav.QuestNav()
        self.estimated_pose = Pose3d()

    def robotPeriodic(self) -> None:
        super().robotPeriodic()
        poseFrames = self.questnav.getAllUnreadPoseFrames()

        for poseFrame in poseFrames:
            self.estimated_pose = poseFrame.quest_pose_3d
            self.estimated_pose = self.estimated_pose.transformBy(
                robot_to_quest_offset.inverse()
            )
            time_stamp = poseFrame.data_timestamp
            self.drivetrain.addVisionMeasurement(
                self.estimated_pose.toPose2d(),
                time_stamp,
                [self.std_translation, self.std_translation, self.std_rotation],
            )

    def getEstimatedPose(self):
        return self.estimated_pose

    def reset(self, pose: Pose3d):
        self.questnav.setPose(pose)

    def logValues(self):
        self.log("x", self.getEstimatedPose().x)
        self.log("y", self.getEstimatedPose().y)
        self.log("z", self.getEstimatedPose().z)
        self.log("roll", self.getEstimatedPose().rotation().x)
        self.log("pitch", self.getEstimatedPose().rotation().y)
        self.log("yaw", self.getEstimatedPose().rotation().z)
