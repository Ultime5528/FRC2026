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
        self.std_devs = [4, 4, 8]

    def getEstimatedPose(self, frame: PhotonPipelineResult) -> EstimatedRobotPose:
        self.estimated_pose = None
        self.estimated_pose = self.camera_pose_estimator.estimateCoprocMultiTagPose(
            frame
        )
        if self.estimated_pose is None:
            self.estimated_pose = (
                self.camera_pose_estimator.estimateLowestAmbiguityPose(frame)
            )
        return self.estimated_pose

    def getAllUnreadEstimatedPosesWithStdDevs(self) -> Generator[tuple[EstimatedRobotPose, List[float]]]:
        for frame in self._cam.getAllUnreadResults():
            estimated_pose = self.getEstimatedPose(frame)
            std_devs = self.getEstimationStdDevs(self.estimated_pose, frame.getTargets())
            yield estimated_pose, std_devs

    def getEstimationStdDevs(
        self, estimated_pose: EstimatedRobotPose, targets: List[PhotonTrackedTarget]
    ) -> list[float]:
        if estimated_pose is None:
            self.std_devs = [4, 4, 8]
        else:
            self.std_devs = [4, 4, 8]
            num_tags = 0
            av_dist = 0

            for target in targets:
                tag_pose = self.camera_pose_estimator.fieldTags.getTagPose(
                    target.getFiducialId()
                )
                if tag_pose is None:
                    continue
                else:
                    num_tags += 1
                    av_dist += (
                        tag_pose.toPose2d()
                        .translation()
                        .distance(estimated_pose.estimatedPose.toPose2d().translation())
                    )

            if num_tags == 0:
                self.std_devs = [4, 4, 8]
            else:
                av_dist /= num_tags

                if num_tags > 1:
                    self.std_devs = [0.5, 0.5, 1]

                if num_tags == 1 and av_dist > 4:
                    self.std_devs = [
                        sys.float_info.max,
                        sys.float_info.max,
                        sys.float_info.max,
                    ]
                else:
                    self.std_devs = [
                        val * (1 + (av_dist * av_dist / 30)) for val in self.std_devs
                    ]
        return self.std_devs

    def getUsedTagIDs(self) -> list[int]:
        if self.estimated_pose:
            return [target.fiducialId for target in self.estimated_pose.targetsUsed]
        else:
            return []

    def getUsedTags(self) -> list[PhotonTrackedTarget]:
        if self.estimated_pose:
            return self.estimated_pose.targetsUsed
        else:
            return []

    def logValues(self):
        self.log("used_tags_IDs", self.getUsedTagIDs())
        self.log("estimated_pose", self.estimated_pose)
        self.log("estimation_std_devs", self.getEstimationStdDevs())
