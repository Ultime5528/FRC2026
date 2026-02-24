import wpimath
from wpimath.geometry import Transform3d

from subsystems.drivetrain import Drivetrain
from ultime.autoproperty import autoproperty
from ultime.vision import AbsoluteVision, VisionMode

### Offset of the camera relative to the middle of the robot. In robot Coordinate system
robot_to_camera_front_offset = wpimath.geometry.Transform3d(
    wpimath.geometry.Translation3d(0.35, -0.098, 0.236),
    wpimath.geometry.Rotation3d.fromDegrees(0.0, -15.0, 0.0),
)
robot_to_camera_back_offset = wpimath.geometry.Transform3d(
    wpimath.geometry.Translation3d(0.35, -0.098, 0.236),
    wpimath.geometry.Rotation3d.fromDegrees(0.0, -15.0, 0.0),
)

camera_front_name = "FrontCamera"
camera_back_name = "BackCamera"


class TagVisionModule(AbsoluteVision):
    ambiguity_threshold = autoproperty(0.05)

    @classmethod
    def front(cls, drivetrain: Drivetrain):
        return cls(camera_front_name, robot_to_camera_front_offset, drivetrain)

    @classmethod
    def back(cls, drivetrain: Drivetrain):
        return cls(camera_back_name, robot_to_camera_back_offset, drivetrain)

    def __init__(self, name: str, transform: Transform3d, drivetrain: Drivetrain):
        super().__init__(camera_name=name, camera_offset=transform)
        self.name = name
        self.mode = VisionMode.Absolute
        self.drivetrain = drivetrain

    def getName(self) -> str:
        return super().getName() + "_" + self.name

    def robotPeriodic(self) -> None:
        super().robotPeriodic()
        for estimated_pose in self.getAllUnreadEstimatedPoses():
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

    def logValues(self):
        super().logValues()
        self.log("number_tag_used", self.getNumberTagsUsed())
        self.log("first_tag_ambiguity", self.getFirstTagAmbiguity())
