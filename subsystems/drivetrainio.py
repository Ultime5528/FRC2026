import ports
from ultime.swerve.swervemoduleio import SwerveModuleIo, SwerveModuleIoSim


class DrivetrainIo:
    def __init__(self):
        self.swerve_io_fl = SwerveModuleIo(
            ports.CAN.drivetrain_motor_driving_fl,
            ports.CAN.drivetrain_motor_turning_fl,
        )
        self.swerve_io_fr = SwerveModuleIo(
            ports.CAN.drivetrain_motor_driving_fr,
            ports.CAN.drivetrain_motor_turning_fr,
        )

        self.swerve_io_bl = SwerveModuleIo(
            ports.CAN.drivetrain_motor_driving_bl,
            ports.CAN.drivetrain_motor_turning_bl,
        )
        self.swerve_io_br = SwerveModuleIo(
            ports.CAN.drivetrain_motor_driving_br,
            ports.CAN.drivetrain_motor_turning_br,
        )


class DrivetrainIoSim:
    def __init__(self):
        self.swerve_io_fl = SwerveModuleIoSim(
            ports.CAN.drivetrain_motor_driving_fl,
            ports.CAN.drivetrain_motor_turning_fl,
        )
        self.swerve_io_fr = SwerveModuleIoSim(
            ports.CAN.drivetrain_motor_driving_fr,
            ports.CAN.drivetrain_motor_turning_fr,
        )

        self.swerve_io_bl = SwerveModuleIoSim(
            ports.CAN.drivetrain_motor_driving_bl,
            ports.CAN.drivetrain_motor_turning_bl,
        )
        self.swerve_io_br = SwerveModuleIoSim(
            ports.CAN.drivetrain_motor_driving_br,
            ports.CAN.drivetrain_motor_turning_br,
        )
