import math
from typing import List

from wpimath.filter import LinearFilter
from wpimath.geometry import Pose3d, Rotation3d, Pose2d

from modules.questvision import QuestVisionModule
from modules.tagvision import TagVisionModule
from subsystems.drivetrain import Drivetrain
from ultime.autoproperty import autoproperty
from ultime.module import Module


class PositionEstimator(Module):
    drivetrain_speed_threshold = autoproperty(0.2)
    drivetrain_speed_rotation_threshold = autoproperty(5.0)
    want_multiple_quest_reset = autoproperty(False)
    multiple_reset_distance_threshold = autoproperty(0.03)

    drivetrain_starting_pose_x = autoproperty(1.0)
    drivetrain_starting_pose_y = autoproperty(1.0)
    drivetrain_starting_pose_angle = autoproperty(0.0)

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

        self.is_drivetrain_under_speed = self.createProperty(True)
        self.has_sean_at_least_one_tag = self.createProperty(False)

        # Find a good stating point based on alliance
        self.drivetrain.resetToPose(
            Pose2d(
                self.drivetrain_starting_pose_x,
                self.drivetrain_starting_pose_y,
                self.drivetrain_starting_pose_angle,
            )
        )

    def robotPeriodic(self) -> None:

        self.quest_connected = self.quest_nav.isConnected()
        self.camera_front_connected = self.camera_front.isConnected()
        self.camera_back_connected = self.camera_back.isConnected()

        self.is_drivetrain_under_speed = self.drivetrain.isUnderSpeed(
            self.drivetrain_speed_threshold,
            self.drivetrain_speed_threshold,
            self.drivetrain_speed_rotation_threshold,
        )

        is_at_least_one_camera_connnected = self.camera_front_connected or self.camera_back_connected

        if self.quest_connected:

            if not is_at_least_one_camera_connnected:
                self.quest_has_reset = True
                self._addQuestMeasurementsOnly()

            else:

                if self.want_multiple_quest_reset:
                    self._addQuestMeasurementsWithResetsFromCameras()
                else:
                    self._addQuestMeasurementsOnly()

        elif is_at_least_one_camera_connnected:
            self._addCameraMeasurementsOnly()

    def _addQuestMeasurementsWithResetsFromCameras(self):

        if self.quest_has_reset:

            self._addVisionMeasuremenstFromQuestVisionModule(self.quest_nav)

            if self.is_drivetrain_under_speed:
                self._addCameraMeasurementsOnly()
                estimated_pose = self.drivetrain.swerve_estimator.getEstimatedPosition()

                dist = math.hypot(self.estimated_pose[0], self.estimated_pose[1])
                if dist < self.multiple_reset_distance_threshold:
                    self.quest_nav.resetToPose(estimated_pose)

        else:
            self._addCameraMeasurementsOnly()

        if self.has_sean_at_least_one_tag:
            estimated_pose = self.drivetrain.swerve_estimator.getEstimatedPosition()
            self.quest_nav.resetToPose(estimated_pose)
            self.quest_has_reset = True


    def _addQuestMeasurementsOnly(self):

        if self.quest_has_reset:
            self._addVisionMeasuremenstFromQuestVisionModule(self.quest_nav)
        else:
            self._addCameraMeasurementsOnly()

        if self.has_sean_at_least_one_tag:
            estimated_pose = self.drivetrain.swerve_estimator.getEstimatedPosition()
            self.quest_nav.resetToPose(estimated_pose)
            self.quest_has_reset = True

    def _addCameraMeasurementsOnly(self):

        if self.camera_front_connected:
            self._addVisionMeasuremenstFromTagVisionModule(self.camera_front)

        if self.camera_back_connected:
            self._addVisionMeasuremenstFromTagVisionModule(self.camera_back)

    def _addVisionMeasuremenstFromQuestVisionModule(
        self, quest_vision_module: QuestVisionModule
    ):
        for (
            quest_data
        ) in self.quest_nav.getAllUnreadEstimatedPosesWithTimeStampAndStdDevs():
            pose = quest_data[0]
            time = quest_data[1]
            std_devs = quest_data[2]
            if pose is not None:
                self.drivetrain.addVisionMeasurement(pose, time, std_devs)

    def _addVisionMeasuremenstFromTagVisionModule(
        self, tag_vision_module: TagVisionModule
    ):
        poses_with_std_devs = tag_vision_module.getAllUnreadEstimatedPosesWithStdDevs()

        self.has_sean_at_least_one_tag = (
            self.has_sean_at_least_one_tag or len(poses_with_std_devs) > 0
        )

        for tag_vision_data in poses_with_std_devs:
            if tag_vision_data[0] is not None:
                pose = tag_vision_data[0].estimatedPose
                time = tag_vision_data[0].timestampSeconds
                std_devs = tag_vision_data[1]

                self.drivetrain.addVisionMeasurement(
                    pose.toPose2d(),
                    time,
                    std_devs,
                )
