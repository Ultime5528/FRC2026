from commands2 import SequentialCommandGroup
from commands2.cmd import sequence, deadline
from pathplannerlib.path import PathPlannerPath

from commands.autonomous.towerclimb import TowerClimb
from commands.drivetrain.auto.followpathprecise import FollowPathPrecise
from commands.feeder.grabfuel import GrabFuel
from commands.pivot.move import ManualMovePivot
from commands.resetall import ResetAll
from commands.shooter.prepareshoot import PrepareShoot
from commands.shootwithalign import ShootWithAlign
from modules.hardware import HardwareModule
from modules.shootercalcmodule import ShooterCalcModule


class RushToMiddle(SequentialCommandGroup):
    @classmethod
    def right(cls, hardware: HardwareModule, shooter_module: ShooterCalcModule):
        cmd = cls(
            PathPlannerPath.fromPathFile("RushToMiddleRight"),
            TowerClimb.right(hardware),
            hardware,
            shooter_module,
        )
        cmd.setName(RushToMiddle.__name__ + ".right")
        return cmd

    @classmethod
    def left(cls, hardware: HardwareModule, shooter_module: ShooterCalcModule):
        cmd = cls(
            PathPlannerPath.fromPathFile("RushToMiddleRight").mirrorPath(),
            TowerClimb.left(hardware),
            hardware,
            shooter_module,
        )
        cmd.setName(RushToMiddle.__name__ + ".left")
        return cmd

    def __init__(
        self,
        path: PathPlannerPath,
        climb_command: TowerClimb,
        hardware: HardwareModule,
        shooter_module: ShooterCalcModule,
    ):
        super().__init__()
        self.drivetrain = hardware.drivetrain
        self.climber = hardware.climber
        self.hugger = hardware.hugger
        self.guide = hardware.guide
        self.pivot = hardware.pivot
        self.feeder = hardware.feeder
        self.shooter = hardware.shooter
        self.controller = hardware.controller
        self.shooter_module = shooter_module
        self.path = path
        self.climb_command = climb_command

        self.addCommands(
            sequence(
                deadline(
                    FollowPathPrecise(self.drivetrain, self.path),
                    ManualMovePivot.down(self.pivot),
                    ResetAll(self.climber, self.hugger, self.guide),
                    sequence(
                        GrabFuel(self.feeder).withTimeout(4.0),
                        PrepareShoot(self.shooter, self.shooter_module),
                    ),
                ),
                ShootWithAlign(
                    self.shooter,
                    self.drivetrain,
                    self.pivot,
                    self.feeder,
                    self.controller,
                    self.shooter_module,
                ),
            ).withTimeout(13.0),
            self.climb_command,
        )
