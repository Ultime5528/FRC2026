from commands2 import SequentialCommandGroup
from commands2.cmd import parallel, deadline
from pathplannerlib.path import PathPlannerPath
from wpimath.geometry import Translation2d

from commands.autonomous import autopath
from commands.climber.move import MoveClimber
from commands.drivetrain.aligntotower import AlignToTower
from commands.drivetrain.auto.pathfindfollowpath import PathFindFollowPath
from commands.drivetrain.driverelative import DriveRelative
from commands.hugandclimb import HugAndClimb
from modules.hardware import HardwareModule
from ultime.autoproperty import autoproperty


class TowerClimb(SequentialCommandGroup):
    speed = autoproperty(0.2)

    @classmethod
    def left(cls, hardware: HardwareModule):
        cmd = cls(hardware, autopath.to_tower_ready_left_path)
        cmd.setName(TowerClimb.__name__ + ".left")
        return cmd

    @classmethod
    def right(cls, hardware: HardwareModule):
        cmd = cls(hardware, autopath.to_tower_ready_right_path)
        cmd.setName(TowerClimb.__name__ + ".right")
        return cmd

    def __init__(self, hardware: HardwareModule, path: PathPlannerPath):
        super().__init__()
        self.drivetrain = hardware.drivetrain
        self.climber = hardware.climber
        self.hugger = hardware.hugger
        self.path = path

        self.addCommands(
            parallel(
                PathFindFollowPath(self.drivetrain, self.path),
                MoveClimber.toReady(self.climber),
            ),
            AlignToTower(self.drivetrain),
            deadline(
                HugAndClimb(self.climber, self.hugger),
                DriveRelative(self.drivetrain, lambda: Translation2d(-self.speed, 0.0)),
            ),
        )
