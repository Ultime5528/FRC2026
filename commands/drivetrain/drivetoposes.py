import math
from typing import List, Callable, Optional

from commands2 import Command
from pathplannerlib.util import FlippingUtil
from wpilib import DriverStation, DataLogManager
from wpimath.geometry import Pose2d, Translation2d, Transform2d

from subsystems.drivetrain import Drivetrain
from ultime.auto import eitherRedBlue
from ultime.autoproperty import autoproperty, FloatProperty, asCallable
from ultime.command import DeferredCommand
from ultime.dynamicmotion import DynamicMotion
from ultime.trapezoidalmotion import TrapezoidalMotion


class DriveToPosesAutoFlip(DeferredCommand):
    def __init__(self, blue_poses: list[Pose2d], drivetrain: Drivetrain):
        super().__init__()
        self.drivetrain = drivetrain
        self.blue_poses = blue_poses
        self.red_poses = [FlippingUtil.flipFieldPose(p) for p in blue_poses]
        self.addRequirements(drivetrain)

    def createCommand(self) -> Command:
        return DriveToPoses(self.drivetrain, self.getPoses())

    def getPoses(self) -> list[Pose2d]:
        alliance = DriverStation.getAlliance()

        if alliance is None:
            DataLogManager.log(
                "DriveToPosesAutoFlip used blue_poses but was not connected to DS"
            )

        is_red = alliance == DriverStation.Alliance.kRed

        return self.red_poses if is_red else self.blue_poses


class DriveToPoses(Command):
    @classmethod
    def back(cls, drivetrain: Drivetrain, distance: FloatProperty):
        get_distance = asCallable(distance)

        def get_poses():
            current_pose = drivetrain.getPose()
            needed_pose = current_pose.transformBy(
                Transform2d(-get_distance(), 0.0, 0.0)
            )
            return [needed_pose]

        cmd = cls(drivetrain, get_poses)
        cmd.setName(cmd.getName() + ".back")
        return cmd

    xy_accel = autoproperty(10.0)
    xy_decel = autoproperty(1.4)
    xy_speed_end = autoproperty(0.5)
    xy_tol_pos = autoproperty(0.3)
    xy_tol_pos_last = autoproperty(0.03)
    xy_speed_max = autoproperty(3.0)

    xy_dist_slow = autoproperty(0.25)

    rot_accel = autoproperty(180.0)
    rot_decel = autoproperty(90.0)
    rot_speed_end = autoproperty(0.5)
    rot_tol_pos_last = autoproperty(3.0)
    rot_speed_max = autoproperty(120.0)

    def __init__(
        self,
        drivetrain: Drivetrain,
        goals: List[Pose2d] | Callable[[], List[Pose2d]],
        speed_constraint: Optional[float] = None,
        end_speed_constraint: Optional[float] = None,
        rotation_speed_constraint: Optional[float] = None,
        rotation_end_speed_constraint: Optional[float] = None,
    ):
        super().__init__()
        self.addRequirements(drivetrain)
        self.drivetrain = drivetrain
        self.get_goals = goals if callable(goals) else lambda: goals
        self.goals: List[Pose2d] = None
        self.last_goal: Pose2d = None
        self.speed_constraint = speed_constraint
        self.end_speed_constraint = end_speed_constraint
        self.rotation_speed_constraint = rotation_speed_constraint
        self.rotation_end_speed_constraint = rotation_end_speed_constraint
        self.remaining_distance = float("inf")

    @staticmethod
    def fromRedBluePoints(
        drivetrain: Drivetrain, red_poses: List[Pose2d], blue_poses: List[Pose2d]
    ) -> Command:
        return eitherRedBlue(
            DriveToPoses(drivetrain, red_poses),
            DriveToPoses(drivetrain, blue_poses),
        )

    def initialize(self):
        if self.speed_constraint is None:
            self.speed_constraint = self.xy_speed_max

        if self.end_speed_constraint is None:
            self.end_speed_constraint = self.xy_speed_end

        if self.rotation_speed_constraint is None:
            self.rotation_speed_constraint = self.rot_speed_max

        if self.rotation_end_speed_constraint is None:
            self.rotation_end_speed_constraint = self.rot_speed_end

        self.goals = self.get_goals()
        self.last_goal = self.goals[-1]
        self.currGoal = 0

        self.motion_xy = TrapezoidalMotion(
            start_position=self.drivetrain.getPose()
            .translation()
            .distance(self.last_goal.translation()),
            end_position=self.xy_dist_slow,
            start_speed=self.speed_constraint / 2,
            max_speed=self.speed_constraint,
            end_speed=self.end_speed_constraint,
            accel=self.xy_accel,
            decel=self.xy_decel,
        )
        self.motion_rot = DynamicMotion(
            goal=0.0,
            max_speed=self.rotation_speed_constraint,
            end_speed=self.rotation_end_speed_constraint,
            accel=self.rot_accel,
            decel=self.rot_decel,
        )

    def execute(self):
        current_pose = self.drivetrain.getPose()

        translation_error = (
            self.goals[self.currGoal].translation() - current_pose.translation()
        )

        self.remaining_distance = self.last_goal.translation().distance(
            current_pose.translation()
        )
        if self.remaining_distance <= self.xy_dist_slow:
            xy_mag = self.end_speed_constraint
        else:
            self.motion_xy.setPosition(self.remaining_distance)

            xy_mag = abs(self.motion_xy.getSpeed())
        translation_error_norm = translation_error.norm()

        # Prevent division by zero
        if translation_error_norm < 0.01:
            vel_xy = Translation2d()
        else:
            vel_xy: Translation2d = translation_error * xy_mag / translation_error_norm

        vel_rot = -self.motion_rot.update(
            (self.last_goal.rotation() - current_pose.rotation()).degrees(),
            # current_chassis_speed.omega
        )

        if self.motion_rot.reachedGoal(self.rot_tol_pos_last):
            vel_rot = 0.0

        self.drivetrain.driveRaw(
            vel_xy.X(),
            vel_xy.Y(),
            math.radians(vel_rot),
            True,
        )

        if (
            self.currGoal < len(self.goals) - 1
            and self.isWithinTolerances()
            or self.currGoal == len(self.goals) - 1
            and self.isWithinLastTolerances()
        ):
            self.currGoal += 1

    def end(self, interrupted):
        self.drivetrain.stop()

    def isFinished(self):
        return self.currGoal == len(self.goals)

    def isWithinLastTolerances(self) -> bool:
        return (
            self.remaining_distance <= self.xy_tol_pos_last
            and self.motion_rot.reachedGoal(self.rot_tol_pos_last)
        )

    def isWithinTolerances(self) -> bool:
        return (
            self.goals[self.currGoal]
            .translation()
            .distance(self.drivetrain.getPose().translation())
            <= self.xy_tol_pos
        )
