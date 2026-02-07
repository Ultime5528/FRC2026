from ultime.autoproperty import FloatProperty, asCallable
from ultime.command import Command
from ultime.linear.linearsubsystem import LinearSubsystem


def createResetLinearClass(speed_up: FloatProperty, speed_down: FloatProperty):
    class ResetLinear(Command):
        @classmethod
        def up(cls, subsystem: LinearSubsystem):
            cmd = cls(subsystem, speed_up)
            cmd.setName(cmd.getName() + ".up")
            return cmd

        @classmethod
        def down(cls, subsystem: LinearSubsystem):
            cmd = cls(subsystem, speed_down)
            cmd.setName(cmd.getName() + ".down")
            return cmd

        def __init__(self, subsystem: LinearSubsystem, speed: FloatProperty):
            super().__init__()
            self.subsystem = subsystem
            self.addRequirements(subsystem)
            self.speed = asCallable(speed)
            self.switch_pressed = False

        def initialize(self):
            self.switch_pressed = False

        def execute(self):
            if self.speed() > 0.0:
                if self.subsystem.isSwitchMaxPressed():
                    self.switch_pressed = True
                    self.subsystem.setSpeed(-self.speed())
                else:
                    self.subsystem.setSpeed(self.speed())
            elif self.speed() < 0.0:
                if self.subsystem.isSwitchMinPressed():
                    self.switch_pressed = True
                    self.subsystem.setSpeed(-self.speed())
                else:
                    self.subsystem.setSpeed(self.speed())

        def isFinished(self) -> bool:
            if self.speed() > 0.0:
                return not self.subsystem.isSwitchMaxPressed() and self.switch_pressed
            else:
                return not self.subsystem.isSwitchMinPressed() and self.switch_pressed

        def end(self, interrupted: bool):
            self.subsystem.setSpeed(0.0)

    return ResetLinear
