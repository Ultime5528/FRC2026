import wpimath

from subsystems.drivetrain import Drivetrain
from ultime.autoproperty import autoproperty
from ultime.timethis import tt
from ultime.vision import AbsoluteVision, VisionMode

### Offset of the camera relative to the middle of the robot. In robot Coordinate system
robot_to_camera_offset = wpimath.geometry.Transform3d(
    wpimath.geometry.Translation3d(0.35, -0.098, 0.236),
    wpimath.geometry.Rotation3d.fromDegrees(0.0, -15.0, 0.0),
)


class TagVisionModule(AbsoluteVision):
    ambiguity_threshold = autoproperty(0.05)

    def __init__(self, drivetrain: Drivetrain):
        super().__init__(
            camera_name="PositionEstimator", camera_offset=robot_to_camera_offset
        )
        self.mode = VisionMode.Absolute
        self.drivetrain = drivetrain

    def robotPeriodic(self) -> None:
        super().robotPeriodic()
        for frame in self._cam.getAllUnreadResults():
            estimated_pose = self.getEstimatedPose(frame)
            if estimated_pose:
                time_stamp = self.getEstimatedPoseTimeStamp()
                std_devs = self.getEstimationStdDevs()
                self.drivetrain.addVisionMeasurement(
                    estimated_pose.estimatedPose.toPose2d(), time_stamp, std_devs
                )

    def getNumberTagsUsed(self) -> int:
        return len(self.getUsedTags())

    def getFirstTagAmbiguity(self) -> float:
        """
        Get the ambiguity of the first tag used, -1.0 if no tag is seen.
        """
        used_tags = self.getUsedTags()

        if used_tags:
            return used_tags[0].getPoseAmbiguity()

        return -1.0

    def initSendable(self, builder):
        super().initSendable(builder)

        def noop(x):
            pass

        builder.addIntegerProperty("number_tags_used", tt(self.getNumberTagsUsed), noop)
        builder.addDoubleProperty(
            "first_tag_ambiguity", tt(self.getFirstTagAmbiguity), noop
        )
        builder.addFloatArrayProperty("std_devs", tt(self.getEstimationStdDevs), noop)
