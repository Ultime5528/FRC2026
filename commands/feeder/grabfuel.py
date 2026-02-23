from subsystems.feeder import Feeder
from subsystems.shooter import Shooter
from ultime.command import Command


class GrabFuel(Command):
    def __init__(self, feeder: Feeder, shooter: Shooter):
        super().__init__()
        self.feeder = feeder
        self.shooter = shooter
        self.addRequirements(feeder)

    def execute(self):
        self.feeder.grab()
        self.shooter.mix()

    def isFinished(self) -> bool:
        return False

    def end(self, interrupted: bool):
        self.feeder.stop()
        self.shooter.stop()
