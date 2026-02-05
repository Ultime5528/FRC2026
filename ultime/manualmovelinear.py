from ultime.autoproperty import FloatProperty, asCallable
from ultime.command import Command
from ultime.linearsubsystem import LinearSubsystem


def createManualMoveClass(class_name, speed_up: FloatProperty, speed_down: FloatProperty):
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
            self.speed = asCallable(speed)

        def execute(self):
            self.subsystem.setSpeed(self.speed())

        def isFinish(self):
            return self.speed() < 0.0 and self.subsystem.isSwitchMinPressed() or self.speed() > 0.0 and self.subsystem.isSwitchMaxPressed()

        def end(self, interrupted: bool):
            self.subsystem.setSpeed(0.0)

    ManualMoveLinear.__name__ = class_name
    ManualMoveLinear.__qualname__ = class_name

    return ManualMoveLinear
