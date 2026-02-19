import wpilib

from ultime.autoproperty import FloatProperty, asCallable
from ultime.command import Command
from ultime.linear.linearsubsystem import LinearSubsystem
from ultime.trapezoidalmotion import TrapezoidalMotion


class MoveLinear(Command):
    def __init__(
        self,
        subsystem: LinearSubsystem,
        end_position: FloatProperty,
        speed_min: FloatProperty,
        speed_max: FloatProperty,
        accel: FloatProperty,
    ):
        super().__init__()
        self.subsystem = subsystem
        self.addRequirements(subsystem)
        self.end_position = asCallable(end_position)
        self.speed_min = asCallable(speed_min)
        self.speed_max = asCallable(speed_max)
        self.accel = asCallable(accel)

    def initialize(self):
        self.motion = TrapezoidalMotion(
            start_position=self.subsystem.getPosition(),
            end_position=self.end_position(),
            start_speed=max(self.speed_min(), self.subsystem.getMotorOutput()),
            end_speed=self.speed_min(),
            max_speed=self.speed_max(),
            accel=self.accel(),
        )

    def execute(self):
        position = self.subsystem.getPosition()
        self.motion.setPosition(position)
        self.subsystem.setSpeed(self.motion.getSpeed())

    def isFinished(self):
        if self.subsystem.hasReset():
            return True
        elif self.motion.getSpeed() > 0.0 and self.subsystem.shouldBlockUp():
            return True
        elif self.motion.getSpeed() < 0.0 and self.subsystem.shouldBlockDown():
            return True

        return self.motion.isFinished()

    def end(self, interrupted: bool):
        if not self.subsystem.hasReset():
            wpilib.reportError(
                f"{self.subsystem.getName()} has not reset: cannot {self.getName()}"
            )

        self.subsystem.setSpeed(0.0)
