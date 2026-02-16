from subsystems.feeder import Feeder
from ultime.command import Command


class GrabFuel(Command):
    def __init__(self, feeder: Feeder):
        super().__init__()
        self.feeder = feeder
        self.addRequirements(feeder)

    def execute(self):
        self.feeder.grab()

    def isFinished(self) -> bool:
        return False

    def end(self, interrupted: bool):
        self.feeder.stop()
