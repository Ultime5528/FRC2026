from subsystems.feeder import Feeder
from ultime.command import Command


class EjectFuel(Command):
    def __init__(self, feeder: Feeder):
        super().__init__()
        self.feeder = feeder
        self.addRequirements(feeder)

    def execute(self):
        self.feeder.eject()

    def isFinished(self) -> bool:
        return False

    def end(self, interrupted: bool):
        self.feeder.stop()
