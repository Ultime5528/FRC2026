from commands2 import SequentialCommandGroup
from commands2.cmd import parallel, sequence

from commands.alignshoot import AlignShoot
from commands.autonomous.towerclimb import TowerClimb
from commands.climber.move import MoveClimber
from commands.resetall import ResetAll
from modules.hardware import HardwareModule
from modules.shootercalcmodule import ShooterCalcModule


class ShootAndClimb(SequentialCommandGroup):
    @classmethod
    def right(cls, hardware: HardwareModule, shooter_module: ShooterCalcModule):
        cmd = cls(TowerClimb.right(hardware), hardware, shooter_module)
        cmd.setName(ShootAndClimb.__name__ + ".right")
        return cmd

    @classmethod
    def left(cls, hardware: HardwareModule, shooter_module: ShooterCalcModule):
        cmd = cls(TowerClimb.left(hardware), hardware, shooter_module)
        cmd.setName(ShootAndClimb.__name__ + ".left")
        return cmd

    def __init__(
        self,
        climb_command: TowerClimb,
        hardware: HardwareModule,
        shooter_module: ShooterCalcModule,
    ):
        super().__init__()
        self.climb_command = climb_command
        self.shooter = hardware.shooter
        self.drivetrain = hardware.drivetrain
        self.climber = hardware.climber
        self.hugger = hardware.hugger
        self.pivot = hardware.pivot
        self.feeder = hardware.feeder
        self.shooter = hardware.shooter
        self.controller = hardware.controller
        self.shooter_module = shooter_module

        self.addCommands(
            parallel(
                AlignShoot(
                    self.shooter,
                    self.drivetrain,
                    self.pivot,
                    self.feeder,
                    self.controller,
                    self.shooter_module,
                ).withTimeout(10.0),
                sequence(
                    ResetAll(self.climber, self.hugger),
                    MoveClimber.toReady(self.climber),
                ),
            ),
            self.climb_command,
        )
