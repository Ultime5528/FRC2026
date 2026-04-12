import sys
from enum import Enum, auto
from typing import List, Generator
from typing import Optional

from photonlibpy import PhotonPoseEstimator, EstimatedRobotPose
from photonlibpy.photonCamera import PhotonCamera
from photonlibpy.targeting import PhotonTrackedTarget, PhotonPipelineResult
from robotpy_apriltag import AprilTagFieldLayout, AprilTagField
from wpimath.geometry import Transform3d

from ultime.alert import AlertType
from ultime.module import Module

april_tag_field_layout = AprilTagFieldLayout.loadField(AprilTagField.k2026RebuiltWelded)


class VisionMode(Enum):
    Relative = auto()
    Absolute = auto()


class Vision(Module):
    def __init__(self, camera_name: str):
        super().__init__()
        self.camera_name = camera_name
        self._cam = PhotonCamera(self.camera_name)
        self.mode = VisionMode.Relative

        self.alert_vision_offline = self.createAlert(
            "Vision camera is having connection issues, check for connections?",
            AlertType.Error,
        )

    def robotPeriodic(self) -> None:
        self.alert_vision_offline.set(not self._cam.isConnected())

    def isConnected(self) -> bool:
        return self._cam.isConnected()

    def getName(self) -> str:
        return super().getName() + "_" + self.camera_name


class RelativeVision(Vision):
    def __init__(self, camera_name: str):
        super().__init__(camera_name=camera_name)
        self._targets: List[PhotonTrackedTarget] = []

    def robotPeriodic(self) -> None:
        super().robotPeriodic()

        if self.mode == VisionMode.Relative:
            if self._cam.isConnected():
                self._targets = self._cam.getLatestResult().getTargets()
            else:
                self._targets = []

    def getTargetWithID(self, _id: int) -> Optional[PhotonTrackedTarget]:
        for target in self._targets:
            if target.getFiducialId() == _id:
                return target
        return None


class AbsoluteVision(Vision):
    def __init__(self, camera_name: str, camera_offset: Transform3d):
        super().__init__(camera_name=camera_name)
        self.camera_pose_estimator = PhotonPoseEstimator(
            april_tag_field_layout,
            camera_offset,
        )
        self.estimated_pose: EstimatedRobotPose = None

    def getEstimatedPose(
        self, frame: PhotonPipelineResult
    ) -> EstimatedRobotPose | None:
        self.estimated_pose = self.camera_pose_estimator.estimateCoprocMultiTagPose(
            frame
        )
        if self.estimated_pose is None:
            self.estimated_pose = (
                self.camera_pose_estimator.estimateLowestAmbiguityPose(frame)
            )

        return self.estimated_pose

    def getAllUnreadEstimatedPosesWithStdDevs(
        self,
    ) -> Generator[tuple[EstimatedRobotPose, tuple[float, float, float]]]:

        # Should we use only the last value?
        # Are we losing the information that estimated_pose are not all in the same frame?
        for frame in self._cam.getAllUnreadResults():
            estimated_pose = self.getEstimatedPose(frame)
            std_devs = self.getEstimationStdDevs(
                self.estimated_pose, frame.getTargets()
            )
            yield estimated_pose, std_devs

    def getEstimationStdDevs(
        self, estimated_pose: EstimatedRobotPose, targets: List[PhotonTrackedTarget]
    ) -> tuple[float, float, float]:

        std_devs = (sys.float_info.max, sys.float_info.max, sys.float_info.max)

        if estimated_pose is None:
            return std_devs

        num_tags = 0
        max_distance = 0.0

        for target in targets:
            tag_pose = self.camera_pose_estimator.fieldTags.getTagPose(
                target.getFiducialId()
            )
            if tag_pose is None:
                continue
            else:
                num_tags += 1
                distance = tag_pose.translation().distance(
                    estimated_pose.estimatedPose.translation()
                )
                max_distance = max(max_distance, distance)

        max_accurate_distance = 4.0

        if num_tags > 0 and max_distance < max_accurate_distance:

            min_accurate_distance = 1.0
            min_std_devs = (0.01, 0.01, 0.02)
            max_std_devs = (0.05, 0.05, 0.1)

            if max_distance < min_accurate_distance:
                std_devs = min_std_devs
            else:
                lerp_factor = (max_distance - min_accurate_distance) / (
                    max_accurate_distance - min_accurate_distance
                )
                std_devs = [
                    min_std_devs[i] + lerp_factor * (max_std_devs[i] - min_std_devs[i])
                    for i in range(0, 3)
                ]

        return std_devs

    def getUsedTagIDs(self) -> list[int]:
        if self.estimated_pose:
            return [target.fiducialId for target in self.estimated_pose.targetsUsed]
        else:
            return []

    def logValues(self):
        self.log("used_tags_IDs", self.getUsedTagIDs())
