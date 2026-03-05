from commands2 import SequentialCommandGroup
from commands2.cmd import parallel

from commands.climber.move import MoveClimber
from commands.hugandclimb import HugAndClimb
from modules.hardware import HardwareModule
from commands.drivetrain.auto.pathfindfollowpath import PathFindFollowPath
from ultime import autopath


class TowerClimbRight(SequentialCommandGroup):
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
            HugAndClimb(self.climber, self.hugger),
        )
