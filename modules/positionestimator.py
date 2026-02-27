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

        self.best_pose: Pose3d = Pose3d()
        self.best_std = [1000, 1000, 1000]

    def robotPeriodic(self) -> None:
        self.quest_connected = self.quest_nav.isConnected()
        self.camera_front_connected = self.camera_front.isConnected()
        self.camera_back_connected = self.camera_back.isConnected()

        drivetrain_under_speed = self.drivetrain.isUnderSpeed(
            self.drivetrain_speed_threshold,
            self.drivetrain_speed_threshold,
            self.drivetrain_speed_rotation_threshold,
        )

        if self.quest_has_reset and self.quest_connected:
            if self.want_multiple_quest_reset and drivetrain_under_speed:
                dist = math.hypot(self.best_std[0], self.best_std[1])
                if dist < self.multiple_reset_distance_threshold:
                    self.quest_nav.resetToPose(self.best_pose)

            for (
                quest_data
            ) in self.quest_nav.getAllUnreadEstimatedPosesWithTimeStampAndStdDevs():
                quest_pose = quest_data[0]
                quest_time = quest_data[1]
                quest_std = quest_data[2]
                if quest_pose is not None:
                    self.drivetrain.addVisionMeasurement(
                        quest_pose, quest_time, quest_std
                    )

        self.best_pose = Pose3d()
        self.best_std = [1000, 1000, 1000]

        if self.camera_front_connected:
            for (
                camera_front_data
            ) in self.camera_front.getAllUnreadEstimatedPosesWithStdDevs():
                if camera_front_data[0] is not None:
                    camera_front_pose = camera_front_data[0].estimatedPose
                    camera_front_time = camera_front_data[0].timestampSeconds
                    camera_front_std = camera_front_data[1]

                    dist_estimated = math.hypot(
                        camera_front_std[0], camera_front_std[1]
                    )
                    dist_best = math.hypot(self.best_std[0], self.best_std[1])
                    if dist_estimated < dist_best:
                        self.best_pose = camera_front_pose
                        self.best_std = camera_front_std

                    if not self.quest_has_reset:
                        self.drivetrain.addVisionMeasurement(
                            camera_front_pose.toPose2d(),
                            camera_front_time,
                            camera_front_std,
                        )

        if self.camera_back_connected:
            for (
                camera_back_data
            ) in self.camera_back.getAllUnreadEstimatedPosesWithStdDevs():
                if camera_back_data[0] is not None:
                    camera_back_pose = camera_back_data[0].estimatedPose
                    camera_back_time = camera_back_data[0].timestampSeconds
                    camera_back_std = camera_back_data[1]

                    dist_estimated = math.hypot(camera_back_std[0], camera_back_std[1])
                    dist_best = math.hypot(self.best_std[0], self.best_std[1])
                    if dist_estimated < dist_best:
                        self.best_pose = camera_back_pose
                        self.best_std = camera_back_std

                    if not self.quest_has_reset:
                        self.drivetrain.addVisionMeasurement(
                            camera_back_pose.toPose2d(),
                            camera_back_time,
                            camera_back_std,
                        )

        if not self.quest_has_reset and drivetrain_under_speed:
            self.quest_nav.resetToPose(self.best_pose)
