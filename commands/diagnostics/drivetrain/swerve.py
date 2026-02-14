import wpilib
from commands2 import SequentialCommandGroup, Command
from commands2.cmd import runOnce, run, waitSeconds, deadline
from wpilib import DataLogManager
from wpimath.geometry import Rotation2d
from wpimath.kinematics import SwerveModuleState

from ultime.alert import Alert
from ultime.autoproperty import autoproperty
from ultime.proxy import proxy
from ultime.swerve.swerve import SwerveModule


class DiagnoseSwerveModuleTurnEncoder(Command):
    angle_tolerance = autoproperty(5.0)
    delay = autoproperty(1.0)

    def __init__(
        self, location: str, swerve: SwerveModule, alert: Alert, degrees: float
    ):
        super().__init__()
        self.location = location
        self.swerve = swerve
        self.alert = alert
        self.rotation = Rotation2d.fromDegrees(degrees)
        self.opposite_rotation = self.rotation + Rotation2d.fromDegrees(180)
        self.timer = wpilib.Timer()
        self.diff = None
        self.opposite_diff = None

    def initialize(self):
        self.timer.restart()

    def execute(self):
        self.swerve.setDesiredState(SwerveModuleState(0, self.rotation))

    def isWithinTolerance(self):
        current_angle = self.swerve.getPosition().angle
        self.diff = abs((current_angle - self.rotation).degrees())
        self.opposite_diff = abs((current_angle - self.opposite_rotation).degrees())
        return min(self.diff, self.opposite_diff) < self.angle_tolerance

    def isFinished(self) -> bool:
        return self.isWithinTolerance() or self.timer.hasElapsed(self.delay)

    def end(self, interrupted: bool):
        if not self.isWithinTolerance():
            DataLogManager.log(
                f"Drivetrain diagnostics: {self.location} swerve turn encoder diff: "
                + f"{self.diff:.3f} or {self.opposite_diff:.3f}"
            )
            self.alert.set(True)


class DiagnoseSwerveModule(SequentialCommandGroup):
    min_velocity = autoproperty(0.5)

    def __init__(
        self,
        location: str,
        swerve: SwerveModule,
        alert_encoders: Alert,
        alert_turning_motor: Alert,
    ):
        super().__init__(
            deadline(  # for driving motor
                waitSeconds(1.0),
                run(proxy(self.test_encoder)),
            ),
            runOnce(proxy(self.after_encoder_test)),
            *(
                DiagnoseSwerveModuleTurnEncoder(location, swerve, alert_encoders, angle)
                for angle in range(0, 390, 30)  # 0 to 360 deg, with step of 30 deg
            ),
        )
        self.swerve = proxy(swerve)
        self.max_velocity = 0
        self.alert_encoders = alert_encoders
        self.alert_turning_motor = alert_turning_motor

    def test_encoder(self):
        self.swerve._driving_motor.set(0.2)
        self.max_velocity = max(self.swerve.getVelocity(), self.max_velocity)

    def after_encoder_test(self):
        self.swerve._driving_motor.set(0.0)
        if self.max_velocity < self.min_velocity:
            self.alert_encoders.set(True)
