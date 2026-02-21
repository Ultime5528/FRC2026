from commands2 import Command

from subsystems.climber import Climber


class MaintainClimber(Command):

    def __init__(self, climber: Climber):
        super().__init__()
        self.climber = climber
        self.addRequirements(climber)

    def execute(self):
        self.climber.maintain()
