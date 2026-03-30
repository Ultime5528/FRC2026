from dataclasses import dataclass
from typing import Final, List, Optional

import ntcore
import wpilib
from ntcore import PubSubOptions, TimestampedRaw
from wpilib._wpilib import Timer
from wpimath.geometry import Pose3d, Translation3d, Quaternion, Rotation3d

from ultime.questnav.generated import commands_pb2, data_pb2, geometry3d_pb2


def rawValueToProtobuf(raw_data: bytes, protobuf_instance):
    try:
        if raw_data:
            protobuf_instance.ParseFromString(raw_data)
            return True
    except Exception as e:
        wpilib.reportError(f"[QuestNav] Error processing raw value: {e}", False)

    return False


@dataclass
class PoseFrame:
    """
    Represents a single frame of pose tracking data from the Quest headset.

    Mirrors the Java PoseFrame record from questnav-lib.

    Attributes:
        quest_pose_3d: The Quest's 3D pose in field coordinates
        data_timestamp: NetworkTables timestamp when data was received (use for pose estimator)
        app_timestamp: Quest app internal timestamp (for debugging only)
        frame_count: Sequential frame number from Quest
    """

    quest_pose_3d: Pose3d
    data_timestamp: float
    app_timestamp: float
    frame_count: int
    is_tracking: bool


class QuestNav:
    version_check_interval: Final = 5.0
    """
    Python implementation of the Java QuestNav class.

    Provides interface for communicating with a Meta Quest VR headset for
    robot localization in FRC robotics applications.

    This class handles:
    - Real-time pose tracking data from Quest
    - Device status monitoring (battery, tracking state)
    - Command sending (pose reset)
    - Connection monitoring

    Usage:
        # Create instance
        questnav = QuestNav()

        # Set initial pose
        from wpimath.geometry import Pose2d, Rotation2d
        initial_pose = Pose2d(1.0, 2.0, Rotation2d.fromDegrees(90))
        questnav.setPose(Pose3d(initial_pose))

        # In robotPeriodic():
        questnav.command_periodic()

        frames = questnav.get_all_unread_pose_frames()
        for frame in frames:
            if questnav.isConnected() and questnav.isTracking():
                # Use frame.quest_pose_3d with pose estimator
                pass
    """

    def __init__(self):
        """
        Creates a new QuestNav instance.

        Initializes NetworkTables subscribers and publishers for communication
        with the Quest headset.
        """
        # Get NetworkTables instance (default instance used by robot)
        self.nt_instance = ntcore.NetworkTableInstance.getDefault()

        # Get QuestNav table
        self.quest_nav_table = self.nt_instance.getTable("QuestNav")

        self.response_sub = self.quest_nav_table.getRawTopic("response").subscribe(
            "proto:"
            + commands_pb2.ProtobufQuestNavCommandResponse.DESCRIPTOR.full_name,
            bytes(),
            PubSubOptions(periodic=0.05, sendAll=True, pollStorage=20),
        )

        self.frame_data_sub = self.quest_nav_table.getRawTopic("frameData").subscribe(
            "proto:" + data_pb2.ProtobufQuestNavFrameData.DESCRIPTOR.full_name,
            bytes(),
        )

        self.device_data_sub = self.quest_nav_table.getRawTopic("deviceData").subscribe(
            "proto:" + data_pb2.ProtobufQuestNavDeviceData.DESCRIPTOR.full_name, bytes()
        )

        self.version_sub = self.quest_nav_table.getStringTopic("version").subscribe(
            "unknown"
        )

        self.request_pub = self.quest_nav_table.getRawTopic("request").publish(
            "proto:" + commands_pb2.ProtobufQuestNavCommand.DESCRIPTOR.full_name
        )

        self.cached_command = commands_pb2.ProtobufQuestNavCommand()
        self.cached_pose_reset_payload = commands_pb2.ProtobufQuestNavPoseResetPayload()
        self.cached_pose = geometry3d_pb2.ProtobufPose3d()
        self.cached_device_data = data_pb2.ProtobufQuestNavDeviceData()
        self.cached_frame_data = data_pb2.ProtobufQuestNavFrameData()
        self.cached_response = commands_pb2.ProtobufQuestNavCommandResponse()
        self.frame_data_queue: list[TimestampedRaw] = []
        self.last_frame_data = data_pb2.ProtobufQuestNavFrameData()

        self.last_sent_request_id = 0
        self.version_check_enabled = True
        self.last_version_check_time = 0.0

    def checkVersionMatch(self) -> None:
        if not self.version_check_enabled or not self.isConnected():
            return

        current_time = Timer.getTimestamp()

        if current_time - self.last_version_check_time < self.version_check_interval:
            return

        self.last_version_check_time = current_time

        lib_version = "2026-2.1.0"
        quest_nav_version = self.getQuestNavVersion()

        if quest_nav_version != lib_version:
            wpilib.reportWarning(
                f"[QUESTNAV] Version on your robot {lib_version} does not match QuestNav app version {quest_nav_version}."
            )

    def getQuestNavVersion(self) -> str:
        return self.version_sub.get()

    def getLastPoseFrame(self) -> List[PoseFrame]:
        self._updateFrameData()

        frame = []
        if not self.frame_data_queue:
            return frame
        timestamped_raw = self.frame_data_queue[-1]
        raw = timestamped_raw.value
        if rawValueToProtobuf(raw, self.cached_frame_data):
            pose_proto = self.cached_frame_data.pose3d
            translation = pose_proto.translation
            rot_quat = pose_proto.rotation.q

            translation3d = Translation3d(translation.x, translation.y, translation.z)
            quaternion = Quaternion(rot_quat.w, rot_quat.x, rot_quat.y, rot_quat.z)
            rotation = Rotation3d(quaternion)
            pose = Pose3d(translation3d, rotation)
            frame.append(
                PoseFrame(
                    pose,
                    timestamped_raw.serverTime / 1_000_000,
                    self.cached_frame_data.timestamp,
                    self.cached_frame_data.frame_count,
                    self.cached_frame_data.isTracking,
                )
            )

        self.frame_data_queue.clear()

        return frame

    def getAllUnreadPoseFrames(self) -> List[PoseFrame]:
        """
        Retrieves all new pose frames received since the last call.

        This is the primary method for integrating QuestNav with FRC pose
        estimation systems. Returns array of PoseFrame objects containing
        pose data and timestamps.

        Each frame contains:
        - Pose data: Quest position and orientation in field coordinates
        - NetworkTables timestamp: When data was received (use for pose estimation)
        - App timestamp: Quest internal timestamp (for debugging)
        - Frame count: Sequential frame number

        Returns:
            List of PoseFrame objects. Empty list if no new frames available.

        Example:
            frames = questnav.get_all_unread_pose_frames()
            for frame in frames:
                if questnav.is_tracking() and questnav.isConnected():
                    pose_estimator.add_vision_measurement(
                        frame.quest_pose_3d.toPose2d(),
                        frame.data_timestamp,
                        (0.1, 0.1, 0.05)  # Standard deviations
                    )
        """
        self.periodic()
        self._updateFrameData()
        frames = []

        for timestamped_raw in self.frame_data_queue:
            raw = timestamped_raw.value
            if rawValueToProtobuf(raw, self.cached_frame_data):
                pose_proto = self.cached_frame_data.pose3d
                translation = pose_proto.translation
                rot_quat = pose_proto.rotation.q

                translation3d = Translation3d(
                    translation.x, translation.y, translation.z
                )
                quaternion = Quaternion(rot_quat.w, rot_quat.x, rot_quat.y, rot_quat.z)
                rotation = Rotation3d(quaternion)
                pose = Pose3d(translation3d, rotation)
                frames.append(
                    PoseFrame(
                        pose,
                        timestamped_raw.serverTime / 1_000_000,
                        self.cached_frame_data.timestamp,
                        self.cached_frame_data.frame_count,
                        self.cached_frame_data.isTracking,
                    )
                )

        self.frame_data_queue.clear()

        return frames

    def setPose(self, pose: Pose3d):
        """
        Sets the field-relative pose of the Quest headset.

        Sends a pose reset command to the Quest, telling it where it is
        currently located on the field. Essential for establishing field-relative
        tracking.

        Call this:
        - At start of autonomous/teleop when Quest position is known
        - When robot is placed at a known location
        - After significant tracking drift

        Important: This should be the Quest's pose, not the robot's pose.
        If you know the robot's pose, apply the mounting offset to get Quest pose.

        Args:
            pose: The Quest's current field-relative pose in WPILib coordinates

        Example:
            # If you know Quest pose directly
            quest_pose = Pose3d(1.5, 5.5, 0.0, Rotation3d())
            questnav.setPose(quest_pose)

            # If you know robot pose, apply mounting offset
            robot_pose = pose_estimator.getEstimatedPosition()
            quest_pose = Pose3d(robot_pose).transformBy(mounting_offset)
            questnav.setPose(quest_pose)
        """
        self.last_sent_request_id += 1

        try:
            # Create command protobuf
            self.cached_command.type = commands_pb2.POSE_RESET
            self.cached_command.command_id = self.last_sent_request_id

            # Set target pose
            self.cached_pose.translation.x = pose.translation().X()
            self.cached_pose.translation.y = pose.translation().Y()
            self.cached_pose.translation.z = pose.translation().Z()

            quat = pose.rotation().getQuaternion()
            self.cached_pose.rotation.q.w = quat.W()
            self.cached_pose.rotation.q.x = quat.X()
            self.cached_pose.rotation.q.y = quat.Y()
            self.cached_pose.rotation.q.z = quat.Z()

            self.cached_pose_reset_payload.target_pose.CopyFrom(self.cached_pose)
            self.cached_command.pose_reset_payload.CopyFrom(
                self.cached_pose_reset_payload
            )

            # Publish command
            serialized = self.cached_command.SerializeToString()
            self.request_pub.set(serialized)

        except Exception as e:
            print(f"QuestNav error sending pose reset: {e}")

    def _updateDeviceData(self):
        changes = self.device_data_sub.readQueue()

        if changes:
            raw = changes[-1].value
            rawValueToProtobuf(raw, self.cached_device_data)

    def _updateFrameData(self):
        new_frame_data = self.frame_data_sub.readQueue()

        if new_frame_data:
            self.frame_data_queue += new_frame_data
            raw = new_frame_data[-1].value
            rawValueToProtobuf(raw, self.last_frame_data)

    def getBatteryPercent(self) -> Optional[int]:
        """
        Returns the Quest headset's current battery level as a percentage.

        Returns:
            Battery percentage (0-100)
        """
        self._updateDeviceData()
        return self.cached_device_data.battery_percent

    def getFrameCount(self) -> int:
        self._updateFrameData()
        return self.last_frame_data.frame_count

    def getTrackingLostCounter(self):
        self._updateDeviceData()
        return self.cached_device_data.tracking_lost_counter

    def isTracking(self) -> bool:
        self._updateFrameData()
        return self.last_frame_data.isTracking

    def isConnected(self) -> bool:
        """
        Determines if the Quest headset is currently connected.

        Connection is determined by how recent the last frame data was received.

        Returns:
            True if Quest is connected and sending data, False otherwise
        """
        current = Timer.getTimestamp()
        last_change = self.frame_data_sub.getLastChange() / 1_000_000
        return (current - last_change) < 0.1  # 100ms timeout

    def getLatencyMs(self):
        current = Timer.getTimestamp()
        last_change = self.frame_data_sub.getLastChange() / 1_000_000
        return (current - last_change) * 1000

    def periodic(self):
        """
        Processes command responses from the Quest headset.

        Must be called regularly (typically in robotPeriodic()) to:
        - Process responses to commands sent via setPose()
        - Log command failures for debugging
        - Maintain proper command/response synchronization

        Call this every robot loop (20ms).

        Example:
            def robotPeriodic(self):
                self.questnav.command_periodic()
                # ... other code
        """
        self.checkVersionMatch()

        for timestamped_raw in self.response_sub.readQueue():
            if rawValueToProtobuf(timestamped_raw.value, self.cached_response):
                if not self.cached_response.success:
                    wpilib.reportError(
                        f"[QuestNav] Command failed: {self.cached_response.error_message}"
                    )
