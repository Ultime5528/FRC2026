import wpilib
from wpimath.geometry import Pose3d

from modules.questvision import QuestVisionModule
from modules.tagvision import TagVisionModule
from subsystems.drivetrain import Drivetrain
from subsystems.shooter import Shooter
from ultime.autoproperty import autoproperty
from ultime.module import Module


class PositionEstimator(Module):
    std_dev_position = autoproperty(0.1)
    std_dev_rotation = autoproperty(0.1)

    def __init__(
        self,
        drivetrain: Drivetrain,
        shooter: Shooter,
        quest_nav: QuestVisionModule,
        camera_front: TagVisionModule,
        camera_back: TagVisionModule,
        camera_second_back: TagVisionModule,
    ):
        super().__init__()
        self.drivetrain = drivetrain
        self.shooter = shooter
        self.quest_nav = quest_nav
        self.camera_front = camera_front
        self.camera_back = camera_back
        self.camera_second_back = camera_second_back

        self.is_quest_connected = self.createProperty(False)
        self.is_camera_front_connected = self.createProperty(False)
        self.is_camera_back_connected = self.createProperty(False)
        self.is_camera_second_back_connected = self.createProperty(False)

        self.is_tag_seen = self.createProperty(False)
        self.is_tag_seen_in_frame = self.createProperty(False)
        self.is_tag_accurate_in_frame = self.createProperty(False)

        self.is_initial_pose_reset_done = self.createProperty(False)

        self.rejection_threshold_z = self.createProperty(-0.1)
        self.good_estimated_pose = Pose3d()

        self.reset_pose_timer = wpilib.Timer()
        self.reset_pose_delay = self.createProperty(5.0)

        self._field = wpilib.Field2d()
        wpilib.SmartDashboard.putData("Field", self._field)

        self._quest_pose = self._field.getObject("Quest Pose")
        self._vision_pose = self._field.getObject("Vision Pose")
        self._odometry_pose = self._field.getObject("Odometry Pose")
        self._taget_pose = self._field.getObject("Target Pose")

    def robotInit(self) -> None:
        self.is_tag_seen = False
        self.is_tag_seen_in_frame = False
        self.is_tag_accurate_in_frame = False
        self.is_initial_pose_reset_done = False
        self.reset_pose_timer.restart()

    def robotPeriodic(self) -> None:
        self.is_tag_seen_in_frame = False
        self.is_tag_accurate_in_frame = False

        self.is_camera_front_connected = self.camera_front.isConnected()
        self.is_camera_back_connected = self.camera_back.isConnected()
        self.is_camera_second_back_connected = self.camera_second_back.isConnected()
        self.is_quest_connected = self.quest_nav.isConnected()

        if self.is_camera_front_connected:
            self._addCameraMeasurements(self.camera_front, True)

        is_shooting = self.shooter._flywheel.getAppliedOutput() > 0.0

        if self.is_camera_back_connected:
            self._addCameraMeasurements(self.camera_back, not is_shooting)

        if self.is_camera_second_back_connected:
            self._addCameraMeasurements(self.camera_second_back, not is_shooting)

        if (
            self.is_initial_pose_reset_done
            and self.is_tag_seen
            and self.is_quest_connected
        ):
            self._addQuestMeasurements()

        self.is_tag_seen = self.is_tag_seen or self.is_tag_seen_in_frame

        self._field.setRobotPose(self.drivetrain.getPose())
        self._odometry_pose.setPose(self.drivetrain.swerve_odometry.getPose())

        if self.is_tag_accurate_in_frame and self.reset_pose_timer.hasElapsed(
            self.reset_pose_delay
        ):
            if self.good_estimated_pose:
                if self.is_quest_connected:
                    self.quest_nav.resetToPose(self.good_estimated_pose)
                self.drivetrain.swerve_odometry.resetPose(
                    self.good_estimated_pose.toPose2d()
                )
                self.reset_pose_timer.restart()
                self.is_initial_pose_reset_done = True

    def _addQuestMeasurements(self):
        pose = self.quest_nav.getLastPoseTimeStampStdDevs()
        if pose:
            self.drivetrain.addPoseMeasurement(pose[0], pose[1], pose[2])
            self._quest_pose.setPose(pose[0])

    def _addCameraMeasurements(self, tag_vision_module: TagVisionModule, should_use):
        for (
            estimation,
            std_devs,
        ) in tag_vision_module.getAllUnreadEstimatedPosesWithStdDevs():

            if estimation and len(estimation.targetsUsed) >= 2 and should_use:
                pose = estimation.estimatedPose
                time = estimation.timestampSeconds

                if pose.translation().z > self.rejection_threshold_z:

                    self.is_tag_seen_in_frame = True

                    if (
                        std_devs[0] < self.std_dev_position
                        and std_devs[1] < self.std_dev_position
                        and std_devs[2] < self.std_dev_rotation
                    ):
                        self.is_tag_accurate_in_frame = True
                        self.good_estimated_pose = pose
                    else:
                        self.good_estimated_pose = None

                    pose2d = pose.toPose2d()

                    self.drivetrain.addPoseMeasurement(
                        pose2d,
                        time,
                        std_devs,
                    )

                    self._vision_pose.setPose(pose2d)
