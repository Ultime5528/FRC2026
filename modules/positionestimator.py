import math

from wpimath.geometry import Pose2d, Pose3d

from modules.questvision import QuestVisionModule
from modules.tagvision import TagVisionModule
from subsystems.drivetrain import Drivetrain
from ultime.autoproperty import autoproperty
from ultime.module import Module


class PositionEstimator(Module):
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

        self.tag_seen = self.createProperty(False)
        self.tag_seen_in_frame = self.createProperty(False)

    def robotPeriodic(self) -> None:
        self.tag_seen_in_frame = False

        self.quest_connected = self.quest_nav.isConnected()
        self.camera_front_connected = self.camera_front.isConnected()
        self.camera_back_connected = self.camera_back.isConnected()

        if self.quest_connected and self.tag_seen:
            self._addQuestMeasurements()

        if self.camera_front_connected:
            self._addCameraMeasurements(self.camera_front)

        if self.camera_back_connected:
            self._addCameraMeasurements(self.camera_back)

        self.tag_seen = self.tag_seen or self.tag_seen_in_frame

        if self.tag_seen_in_frame:
            estimated_pose = self.drivetrain.getPose()
            self.quest_nav.resetToPose(Pose3d(estimated_pose))

    def _addQuestMeasurements(self):
        for (
            quest_data
        ) in self.quest_nav.getAllUnreadEstimatedPosesWithTimeStampAndStdDevs():
            pose = quest_data[0]
            time = quest_data[1]
            std_devs = quest_data[2]
            if pose is not None:
                self.drivetrain.addVisionMeasurement(pose, time, std_devs)

    def _addCameraMeasurements(self, tag_vision_module: TagVisionModule):
        for (
            estimation,
            std_devs,
        ) in tag_vision_module.getAllUnreadEstimatedPosesWithStdDevs():

            if estimation and len(estimation.targetsUsed) >= 2:
                pose = estimation.estimatedPose
                time = estimation.timestampSeconds

                self.tag_seen_in_frame = True

                self.drivetrain.addVisionMeasurement(
                    pose.toPose2d(),
                    time,
                    std_devs,
                )
