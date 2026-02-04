from commands2 import Command

from subsystems.climber import Climber


class ResetClimber(Command):
    def __init__(self, climber: Climber):
        super().__init__()
        self.climber = climber
        self.addRequirements(climber)

    def initialize(self):
        self.climber.state = self.climber.State.Unknown

    def execute(self):
        if not self.climber.isDown():
            self.climber.moveDown()
        else:
            self.climber.stop()
            self.climber.setOffset()
            self.climber.state = self.climber.State.Ready


    def isFinished(self) -> bool:
        return self.climber.isDown()