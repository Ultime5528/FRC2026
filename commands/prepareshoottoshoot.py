from commands2 import SequentialCommandGroup

from commands.shooter.prepareshoot import PrepareShoot
from commands.shooter.shoot import Shoot
from subsystems.shooter import Shooter
from ultime.command import ignore_requirements


@ignore_requirements(["shooter"])
class PrepareShootToShoot(SequentialCommandGroup):
    def __init__(
        self,
        shooter: Shooter,
    ):
        super().__init__(
            PrepareShoot(shooter),
            Shoot(shooter),
        )
