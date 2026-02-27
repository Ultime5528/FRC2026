import wpimath
from wpimath.geometry import Transform3d

from subsystems.drivetrain import Drivetrain
from ultime.autoproperty import autoproperty
from ultime.vision import AbsoluteVision, VisionMode

### Offset of the camera relative to the middle of the robot. In robot Coordinate system
robot_to_camera_front_offset = wpimath.geometry.Transform3d(
    wpimath.geometry.Translation3d(0.053, 0.005, 0.535),
    wpimath.geometry.Rotation3d.fromDegrees(0.0, 18.5, 0.0),
)
robot_to_camera_back_offset = wpimath.geometry.Transform3d(
    wpimath.geometry.Translation3d(-0.298, -0.350, 0.453),
    wpimath.geometry.Rotation3d.fromDegrees(0.0, 17.5, 135.0),
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
        self.mode = VisionMode.Absolute
        self.drivetrain = drivetrain
