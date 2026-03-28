import wpilib
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

        self.is_quest_connected = self.createProperty(False)
        self.is_camera_front_connected = self.createProperty(False)
        self.is_camera_back_connected = self.createProperty(False)

        self.is_tag_seen = self.createProperty(False)
        self.is_tag_seen_in_frame = self.createProperty(False)
        self.is_tag_accurate_in_frame = self.createProperty(False)
        
        self.rejection_threshold_z = self.createProperty(-0.1)

        self.reset_pose_timer = wpilib.Timer()
        self.reset_pose_delay = self.createProperty(5.0)

        self._field = wpilib.Field2d()
        wpilib.SmartDashboard.putData("Field", self._field)

        self._quest_pose = self._field.getObject("Quest Pose")
        self._vision_pose = self._field.getObject("Vision Pose")
        self._odometry_pose = self._field.getObject("Odometry Pose")

    def robotPeriodic(self) -> None:
        self.is_tag_seen_in_frame = False
        self.is_tag_accurate_in_frame = False

        self.is_camera_front_connected = self.camera_front.isConnected()
        self.is_camera_back_connected = self.camera_back.isConnected()
        self.is_quest_connected = self.quest_nav.isConnected()

        if self.is_tag_seen and self.is_quest_connected:
            self._addQuestMeasurements()

        if self.is_camera_front_connected:
            self._addCameraMeasurements(self.camera_front)

        if self.is_camera_back_connected:
            self._addCameraMeasurements(self.camera_back)

        self.is_tag_seen = self.is_tag_seen or self.is_tag_seen_in_frame

        self._field.setRobotPose(self.drivetrain.getPose())
        self._odometry_pose.setPose(self.drivetrain.swerve_odometry.getPose())

        if self.is_tag_accurate_in_frame and self.reset_pose_timer.hasElapsed(
            self.reset_pose_delay
        ):
            estimated_pose = self.drivetrain.getPose()
            if self.is_quest_connected:
                self.quest_nav.resetToPose(Pose3d(estimated_pose))
            self.drivetrain.resetToPose(estimated_pose)
            self.reset_pose_timer.restart()

    def _addQuestMeasurements(self):
        poses_and_stddevs = list(self.quest_nav.getAllUnreadPosesTimestampsStdDevs())
        if poses_and_stddevs:
            pose_and_stddevs = poses_and_stddevs[-1]
            self.drivetrain.addPoseMeasurement(
                pose_and_stddevs[0], pose_and_stddevs[1], pose_and_stddevs[2]
            )
            self._quest_pose.setPose(pose_and_stddevs[0])

    def _addCameraMeasurements(self, tag_vision_module: TagVisionModule):
        for (
            estimation,
            std_devs,
        ) in tag_vision_module.getAllUnreadEstimatedPosesWithStdDevs():

            if estimation and len(estimation.targetsUsed) >= 2:
                pose = estimation.estimatedPose
                time = estimation.timestampSeconds

                if pose.translation().z > self.rejection_threshold_z:

                    self.is_tag_seen_in_frame = True

                    if std_devs[0] < 0.02 and std_devs[1] < 0.02 and std_devs[2] < 0.04:
                        self.is_tag_accurate_in_frame = True

                    pose2d = pose.toPose2d()

                    self.drivetrain.addPoseMeasurement(
                        pose2d,
                        time,
                        std_devs,
                    )

                    self._vision_pose.setPose(pose2d)
