from commands2 import Command

from commands.autonomous.towerclimb import TowerClimb
from modules.hardware import HardwareModule
from ultime.command import DeferredCommand
from ultime.field import isRight


class ChooseSideTowerClimb(DeferredCommand):
    def __init__(self, hardware: HardwareModule):
        super().__init__()
        self.hardware = hardware
        self.drivetrain = hardware.drivetrain

    def createCommand(self) -> Command:
        current_pose = self.drivetrain.getPose()
        if isRight(current_pose):
            return TowerClimb.right(self.hardware)
        else:
            return TowerClimb.left(self.hardware)
