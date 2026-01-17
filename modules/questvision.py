import wpimath
from wpimath.geometry import Transform3d, Pose3d

from subsystems.drivetrain import Drivetrain
from ultime.module import Module
from ultime.questnav import questnav
from ultime.timethis import tt

### Offset of the camera relative to the middle of the robot. In robot Coordinate system
robot_to_quest_offset = wpimath.geometry.Transform3d(
    wpimath.geometry.Translation3d(0.20, 0.01, 1.03),
    wpimath.geometry.Rotation3d.fromDegrees(0.0, 0.0, 0.0),
)


class QuestVisionModule(Module):

    def __init__(self, drivetrain: Drivetrain):
        super().__init__()
        self.drivetrain = drivetrain
        self.questnav = questnav.QuestNav()
        self.estimated_pose = Pose3d()

    def robotPeriodic(self) -> None:
        super().robotPeriodic()
        poseFrames = self.questnav.get_all_unread_pose_frames()

        # Documentation of get_all_unread_pose_frames uses all poseFrames
        # Here we choose to use only the last one.... should we???
        for poseFrame in poseFrames:
            self.estimated_pose = poseFrame.quest_pose_3d
            self.estimated_pose = self.estimated_pose.transformBy(
                robot_to_quest_offset.inverse()
            )
            time_stamp = poseFrame.data_timestamp
            self.drivetrain.addVisionMeasurement(
                self.estimated_pose.toPose2d(), time_stamp, [0.03, 0.03, 0.1]
            )

    def X(self):
        return self.estimated_pose.x

    def Y(self):
        return self.estimated_pose.y

    def Z(self):
        return self.estimated_pose.z

    def Roll(self):
        return self.estimated_pose.rotation().x

    def Pitch(self):
        return self.estimated_pose.rotation().y

    def Yaw(self):
        return self.estimated_pose.rotation().z

    def reset(self, pose: Pose3d):
        self.questnav.set_pose(pose)

    def initSendable(self, builder):
        super().initSendable(builder)

        def noop(x):
            pass

        builder.addFloatProperty("X", tt(self.X), noop)
        builder.addFloatProperty("Y", tt(self.Y), noop)
        builder.addFloatProperty("Z", tt(self.Z), noop)
        builder.addFloatProperty("roll", tt(self.Roll), noop)
        builder.addFloatProperty("pitch", tt(self.Pitch), noop)
        builder.addFloatProperty("yaw", tt(self.Yaw), noop)
