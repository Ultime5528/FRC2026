import rev
import wpilib

from ultime.autoproperty import autoproperty
from ultime.subsystem import Subsystem


class Intake(Subsystem):
    speed_flywheel = autoproperty()
    angle_up = autoproperty()
    angle_down = autoproperty()
    maintien = autoproperty()

    def __init__(self):
        super().__init__()
        self.moteur_pivot = rev.SparkMax(
        ports.moteur_pivot, rev.SparkMax.MotorType.kBrushless
        )
        self.moteur_intake = rev.SparkMax(
        ports.moteur_intake, rev.SparkMax.MotorType.kBrushless
        )


    def move_up(self):
        self.moteur_pivot.setAngle(self.angle_up)

    def move_down(self):
        self.moteur_pivot.setAngle(self.angle_down)

    def roll(self):
        self.moteur_intake.set(self.speed_flywheel)

    def maintien(self):
        self.moteur_pivot.set(self.maintien)

    def stop(self):
        self.moteur_pivot.stopMotor()
        self.moteur_intake.stopMotor()