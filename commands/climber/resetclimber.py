from commands2 import Command


class ResetClimber(Command):
    def __init__(self, climber: Climber):
        super().__init__()
        self.climber = climber
        self.addRequirements(climber)
        self.touched_switch = False

    def initialize(self):
        self.touched_switch = False
        self.climber.state = self.climber.State.Moving

    def execute(self):
        pass

    def isFinished(self) -> bool:
        return self.touched_switch and self.climber.getPosition() <= 0.0