from wpimath.geometry import Pose3d

from modules.questvision import QuestVisionModule
from modules.tagvision import TagVisionModule
from subsystems.drivetrain import Drivetrain
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

        self.quest_connected = self.createProperty(False)
        self.camera_front_connected = self.createProperty(False)
        self.camera_back_connected = self.createProperty(False)

        self.tag_seen = self.createProperty(False)
        self.tag_seen_in_frame = self.createProperty(False)

        self.rejection_treashold_z = self.createProperty(-0.1)

    def robotPeriodic(self) -> None:
        self.tag_seen_in_frame = False

        self.camera_front_connected = self.camera_front.isConnected()
        self.camera_back_connected = self.camera_back.isConnected()

        if self.tag_seen:
            self._addQuestMeasurements()

        if self.camera_front_connected:
            self._addCameraMeasurements(self.camera_front)

        if self.camera_back_connected:
            self._addCameraMeasurements(self.camera_back)

        self.tag_seen = self.tag_seen or self.tag_seen_in_frame

        if self.tag_seen_in_frame:
            estimated_pose = self.drivetrain.getPose()
            self.quest_nav.resetToPose(Pose3d(estimated_pose))

        self.quest_connected = self.quest_nav.isConnected()

    def _addQuestMeasurements(self):
        pose = self.quest_nav.getLastPoseTimeStampStdDevs()
        if pose:
            self.drivetrain.addVisionMeasurement(pose[0], pose[1], pose[2])

    def _addCameraMeasurements(self, tag_vision_module: TagVisionModule):
        for (
            estimation,
            std_devs,
        ) in tag_vision_module.getAllUnreadEstimatedPosesWithStdDevs():

            if estimation and len(estimation.targetsUsed) >= 2:
                pose = estimation.estimatedPose
                time = estimation.timestampSeconds

                if pose.translation().z > self.rejection_treashold_z:

                    self.tag_seen_in_frame = True

                    self.drivetrain.addVisionMeasurement(
                        pose.toPose2d(),
                        time,
                        std_devs,
                    )
