import wpimath
from wpimath.geometry import Transform3d, Pose3d

from subsystems.drivetrain import Drivetrain
from ultime.autoproperty import autoproperty
from ultime.module import Module
from ultime.questnav import questnav
from ultime.timethis import tt

### Offset of the camera relative to the middle of the robot. In robot Coordinate system
robot_to_quest_offset = wpimath.geometry.Transform3d(
    wpimath.geometry.Translation3d(0.20, 0.01, 1.03),
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

    def initSendable(self, builder):
        super().initSendable(builder)

        def noop(x):
            pass

        builder.addFloatProperty("X", tt(lambda: self.getEstimatedPose().x), noop)
        builder.addFloatProperty("Y", tt(lambda: self.getEstimatedPose().y), noop)
        builder.addFloatProperty("Z", tt(lambda: self.getEstimatedPose().z), noop)
        builder.addFloatProperty(
            "roll", tt(lambda: self.getEstimatedPose().rotation().x), noop
        )
        builder.addFloatProperty(
            "pitch", tt(lambda: self.getEstimatedPose().rotation().y), noop
        )
        builder.addFloatProperty(
            "yaw", tt(lambda: self.getEstimatedPose().rotation().z), noop
        )
