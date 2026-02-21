import commands2.sysid
import wpilib
from commands2.cmd import sequence

from commands.drivetrain.forwardposition import ForwardPosition
from subsystems.drivetrain import Drivetrain
from ultime.module import Module


class SysID(Module):
    def __init__(self, drivetrain: Drivetrain):
        super().__init__()
        self.drivetrain = drivetrain

        self.sys_id_routine = commands2.sysid.SysIdRoutine(
            commands2.sysid.SysIdRoutine.Config(),
            commands2.sysid.SysIdRoutine.Mechanism(
                lambda voltage: (
                    self.drivetrain.swerve_module_fl.runCharacterization(voltage),
                    self.drivetrain.swerve_module_fr.runCharacterization(voltage),
                    self.drivetrain.swerve_module_bl.runCharacterization(voltage),
                    self.drivetrain.swerve_module_br.runCharacterization(voltage),
                ),
                lambda log: (
                    log.motor("Front Left Swerve").voltage(
                        self.drivetrain.swerve_module_fl.getDrivingMotorAppliedVoltage()
                    ),
                    log.motor("Front Left Swerve").angularPosition(
                        self.drivetrain.swerve_module_fl.getEncoderPosition()
                    ),
                    log.motor("Front Left Swerve").angularVelocity(
                        self.drivetrain.swerve_module_fl.getVelocity()
                    ),
                    log.motor("Front Right Swerve").voltage(
                        self.drivetrain.swerve_module_fr.getDrivingMotorAppliedVoltage()
                    ),
                    log.motor("Front Right Swerve").angularPosition(
                        self.drivetrain.swerve_module_fr.getEncoderPosition()
                    ),
                    log.motor("Front Right Swerve").angularVelocity(
                        self.drivetrain.swerve_module_fr.getVelocity()
                    ),
                    log.motor("Back Left Swerve").voltage(
                        self.drivetrain.swerve_module_bl.getDrivingMotorAppliedVoltage()
                    ),
                    log.motor("Back Left Swerve").angularPosition(
                        self.drivetrain.swerve_module_bl.getEncoderPosition()
                    ),
                    log.motor("Back Left Swerve").angularVelocity(
                        self.drivetrain.swerve_module_bl.getVelocity()
                    ),
                    log.motor("Back Right Swerve").voltage(
                        self.drivetrain.swerve_module_br.getDrivingMotorAppliedVoltage()
                    ),
                    log.motor("Back Right Swerve").angularPosition(
                        self.drivetrain.swerve_module_br.getEncoderPosition()
                    ),
                    log.motor("Back Right Swerve").angularVelocity(
                        self.drivetrain.swerve_module_br.getVelocity()
                    ),
                ),
                self.drivetrain,
            ),
        )

        wpilib.SmartDashboard.putData(
            "SysID/ForwardPosition", ForwardPosition(self.drivetrain)
        )

        wpilib.SmartDashboard.putData(
            "SysID/QuasistaticForward",
            sequence(
                ForwardPosition(self.drivetrain),
                self.sys_id_routine.quasistatic(
                commands2.sysid.SysIdRoutine.Direction.kForward
                ),
            )
        )

        wpilib.SmartDashboard.putData(
            "SysID/QuasistaticReverse",
            sequence(
                ForwardPosition(self.drivetrain),
                self.sys_id_routine.quasistatic(
                    commands2.sysid.SysIdRoutine.Direction.kReverse
                ),
            )
        )

        wpilib.SmartDashboard.putData(
            "SysID/DynamicForward",
            sequence(
                ForwardPosition(self.drivetrain),
                self.sys_id_routine.dynamic(
                    commands2.sysid.SysIdRoutine.Direction.kForward
                ),
            )
        )

        wpilib.SmartDashboard.putData(
            "SysID/DynamicReverse",
            sequence(
                ForwardPosition(self.drivetrain),
                self.sys_id_routine.dynamic(
                    commands2.sysid.SysIdRoutine.Direction.kReverse
                ),
            )
        )
