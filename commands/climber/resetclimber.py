from commands2 import Command

from subsystems.climber import Climber


class ResetClimber(Command):
    def __init__(self, climber: Climber):
        super().__init__()
        self.climber = climber
        self.addRequirements(climber)

    def initialize(self):
        self.climber.invalidateReset()

    def execute(self):
        if not self.climber.isSwitchMinPressed():
            self.climber.setSpeed(-self.climber.speed)
        else:
            self.climber.setSpeed(0.0)

    def isFinished(self) -> bool:
        return self.climber.isSwitchMinPressed()

    def end(self, interrupted: bool):
        self.climber.setSpeed(0.0)