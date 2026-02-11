from ultime.autoproperty import FloatProperty, asCallable
from ultime.command import Command
from ultime.linear.linearsubsystem import LinearSubsystem


def createManualMoveClass(speed_up: FloatProperty, speed_down: FloatProperty):
    class ManualMoveLinear(Command):
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

        def execute(self):
            self.subsystem.setSpeed(self.speed())

        def isFinished(self) -> bool:
            return (
                self.speed() < 0.0
                and self.subsystem.isSwitchMinPressed()
                or self.speed() > 0.0
                and self.subsystem.isSwitchMaxPressed()
            )

        def end(self, interrupted: bool):
            self.subsystem.setSpeed(0.0)

    return ManualMoveLinear
