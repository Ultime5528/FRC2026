from subsystems.pivot import Pivot
from ultime.command import Command


class MaintainPivot(Command):
    def __init__(self, pivot: Pivot):
        super().__init__()
        self.pivot = pivot
        self.addRequirements(self.pivot)

    def execute(self):
        self.pivot.maintain()

    def isFinished(self) -> bool:
        return False

    def end(self, interrupted: bool):
        self.pivot.stop()
