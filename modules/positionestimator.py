from wpimath.geometry import Pose2d, Pose3d, Rotation3d

from modules.questvision import QuestVisionModule
from modules.tagvision import TagVisionModule
from subsystems.drivetrain import Drivetrain
from ultime.autoproperty import autoproperty
from ultime.module import Module


class PositionEstimator(Module):
    drivetrain_speed_threshold = autoproperty(0.2)
    drivetrain_speed_rotation_threshold = autoproperty(5.0)

    def __init__(
        self,
        drivetrain: Drivetrain,
        quest_nav: QuestVisionModule,
        camera_front: TagVisionModule,
        camera_back: TagVisionModule,
    ):
        super().__init__()
        self.drivetrain = drivetrain
        self.quest_nav = quest_nav
        self.camera_front = camera_front
        self.camera_back = camera_back

        self.quest_has_reset = self.createProperty(False, subscribe=True)
        self.quest_connected = self.createProperty(False)
        self.camera_front_connected = self.createProperty(False)
        self.camera_back_connected = self.createProperty(False)

    def robotPeriodic(self) -> None:
        self.quest_connected = self.quest_nav.isConnected()
        self.camera_front_connected = self.camera_front.isConnected()
        self.camera_back_connected = self.camera_back.isConnected()

        for quest_data, camera_front_data, camera_back_data in zip(
            self.quest_nav.getAllUnreadEstimatedPosesWithTimeStampAndStdDevs(),
            self.camera_front.getAllUnreadEstimatedPosesWithStdDevs(),
            self.camera_back.getAllUnreadEstimatedPosesWithStdDevs(),
        ):
            quest_pose = quest_data[0]
            quest_time = quest_data[1]
            quest_std = quest_data[2]

            camera_front_pose = camera_front_data[0].estimatedPose
            camera_front_time = camera_front_data[0].timestampSeconds
            camera_front_std = camera_front_data[1]
            camera_front_number_of_tags_used = len(camera_front_data[0].targetsUsed)

            camera_back_pose = camera_back_data[0].estimatedPose
            camera_back_time = camera_back_data[0].timestampSeconds
            camera_back_std = camera_back_data[1]
            camera_back_number_of_tags_used = len(camera_back_data[0].targetsUsed)

            drivetrain_under_speed = self.drivetrain.isUnderSpeed(self.drivetrain_speed_threshold, self.drivetrain_speed_threshold, self.drivetrain_speed_rotation_threshold)

            if self.quest_has_reset and self.quest_connected:
                self.drivetrain.addVisionMeasurement(
                    quest_pose, quest_time, quest_std
                )
            else:
                if camera_front_number_of_tags_used > camera_back_number_of_tags_used and self.camera_front_connected:
                    if drivetrain_under_speed:
                        self.quest_nav.resetToPose(camera_front_pose)
                    else:
                        self.drivetrain.addVisionMeasurement(
                            camera_front_pose.toPose2d(),
                            camera_front_time,
                            camera_front_std
                        )
                elif camera_back_number_of_tags_used > camera_front_number_of_tags_used and self.camera_back_connected:
                    if drivetrain_under_speed:
                        self.quest_nav.resetToPose(camera_back_pose)
                    else:
                        self.drivetrain.addVisionMeasurement(
                            camera_back_pose.toPose2d(),
                            camera_back_time,
                            camera_back_std
                        )
                else:
                    if drivetrain_under_speed and self.camera_front_connected and self.camera_back_connected:
                        x = (camera_front_pose.x + camera_back_pose.x) / 2
                        y = (camera_front_pose.y + camera_back_pose.y) / 2
                        z = (camera_front_pose.z + camera_back_pose.z) / 2
                        rot_x = (camera_front_pose.rotation().x + camera_back_pose.rotation().x) / 2
                        rot_y = (camera_front_pose.rotation().y + camera_back_pose.rotation().y) / 2
                        rot_z = (camera_front_pose.rotation().z + camera_back_pose.rotation().z) / 2
                        pose = Pose3d(x, y, z, Rotation3d(rot_x, rot_y, rot_z))

                        self.quest_nav.resetToPose(pose)
                    else:
                        if self.camera_front_connected:
                            self.drivetrain.addVisionMeasurement(
                                camera_front_pose.toPose2d(),
                                camera_front_time,
                                camera_front_std
                            )
                        if self.camera_back_connected:
                            self.drivetrain.addVisionMeasurement(
                                camera_back_pose.toPose2d(),
                                camera_back_time,
                                camera_back_std
                            )

