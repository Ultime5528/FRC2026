from subsystems.intake import Intake
from ultime.autoproperty import autoproperty, FloatProperty, asCallable
from ultime.command import Command


class ManualMoveIntake(Command):
    @classmethod
    def up(cls, intake: Intake):
        cmd = cls(intake, lambda: manual_move_properties.speed)
        cmd.setName(cmd.getName() + ".up")
        return cmd

    @classmethod
    def down(cls, intake: Intake):
        cmd = cls(intake, lambda: -manual_move_properties.speed)
        cmd.setName(cmd.getName() + ".down")
        return cmd

    def __init__(self, intake: Intake, speed: FloatProperty):
        super().__init__()
        self.intake = intake
        self.addRequirements(self.intake)
        self.get_speed = asCallable(speed)

    def execute(self):
        self.intake.setSpeed(self.get_speed())

    def isFinished(self) -> bool:
        return False

    def end(self, interrupted: bool):
        self.intake.stop_pivot()

class _ClassProperties:
        speed = autoproperty(0.15, subtable=ManualMoveIntake.__name__)

manual_move_properties = _ClassProperties()
