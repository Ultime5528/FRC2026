from subsystems.intake import Intake
from ultime.command import Command


class Feed(Command):

    def __init__(self, intake: Intake):
        super().__init__()
        self.intake = intake

    def execute(self):
        self.intake.feed()

    def isFinished(self) -> bool:
        return False

    def end(self, interrupted: bool):
        self.intake.stop_feeder()
