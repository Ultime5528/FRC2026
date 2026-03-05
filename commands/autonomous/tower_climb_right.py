from commands2 import SequentialCommandGroup
from commands2.cmd import parallel
from wpimath.geometry import Translation2d

from commands.climber.move import MoveClimber
from commands.drivetrain.driverelative import DriveRelative
from commands.hugandclimb import HugAndClimb
from modules.hardware import HardwareModule
from commands.drivetrain.auto.pathfindfollowpath import PathFindFollowPath
from ultime import autopath
from ultime.autoproperty import autoproperty


class TowerClimbRight(SequentialCommandGroup):
    forward_timeout = autoproperty(0.2)
    speed = autoproperty(0.1)

    def __init__(self, hardware: HardwareModule):
        super().__init__()
        self.drivetrain = hardware.drivetrain
        self.climber = hardware.climber
        self.hugger = hardware.hugger
        self.path = autopath.to_tower_ready_right_path

        self.addCommands(
            parallel(
                PathFindFollowPath(self.drivetrain, self.path),
                MoveClimber.toReady(self.climber),
            ),
            DriveRelative(self.drivetrain, lambda: Translation2d(-self.speed, 0.0)).withTimeout(self.forward_timeout),
            HugAndClimb(self.climber, self.hugger),
        )
