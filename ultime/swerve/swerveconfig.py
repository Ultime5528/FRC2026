import math

from rev import SparkMaxConfig, ClosedLoopConfig, SparkBaseConfig, FeedbackSensor

max_speed_per_second = 4
max_angular_speed = 2 * math.pi

odometry_frequency = 100.0  # Hz

# 45 teeth on the wheel's bevel gear, 22 teeth on the first-stage spur gear, 15 teeth on the bevel pinion
drive_motor_pinion_teeth = 13
drive_motor_gear_ratio = (45.0 * 22) / (drive_motor_pinion_teeth * 15)

wd_bl = 0.075757752911742
wd_fl = 0.074802823253191
wd_br = 0.075439443025558
wd_fr = 0.074802823253191

wheel_diameter = 0.0745  # meters
drive_encoder_position_conversion_factor = (
    math.pi * wheel_diameter / drive_motor_gear_ratio
)  # meters
drive_encoder_velocity_conversion_factor = (
    drive_encoder_position_conversion_factor / 60
)  # meters per second
drive_motor_free_rps = 5676 / 60  # Neo motor max free RPM into rotations per second
drive_wheel_free_rps = (
    drive_motor_free_rps * (math.pi * wheel_diameter) / drive_motor_gear_ratio
)

turning_encoder_position_conversion_factor = math.pi * 2  # radians
turning_encoder_velocity_conversion_factor = math.pi * 2 / 60  # radians per second

turning_encoder_position_PID_min_input = 0
turning_encoder_position_PID_max_input = turning_encoder_position_conversion_factor

driveKp = 0.45
driveKd = 0.0
driveKs = 0.151515
driveKv = 2.64445
driveKa = 0.5

turnKp = 0.4
turnKd = 0.0

driving_config = SparkMaxConfig()
turning_config = SparkMaxConfig()

# Constants
driving_factor = drive_encoder_position_conversion_factor
driving_velocity_factor = drive_encoder_velocity_conversion_factor

turning_factor = turning_encoder_position_conversion_factor
turning_velocity_factor = turning_encoder_velocity_conversion_factor

driving_velocity_feed_forward = 1 / drive_wheel_free_rps

# Set up driving config
driving_config.setIdleMode(SparkBaseConfig.IdleMode.kBrake)
driving_config.smartCurrentLimit(50)
driving_config.voltageCompensation(12.0)

# Set up driving encoder config
driving_config.encoder.positionConversionFactor(driving_factor)
driving_config.encoder.velocityConversionFactor(driving_velocity_factor)
driving_config.encoder.uvwMeasurementPeriod(10)
driving_config.encoder.uvwAverageDepth(2)

# Set up driving closed loop config
driving_config.closedLoop.setFeedbackSensor(FeedbackSensor.kPrimaryEncoder)
driving_config.closedLoop.pidf(driveKp, 0.0, driveKd, 0.0)

# Set up driving signals config
driving_config.signals.primaryEncoderPositionAlwaysOn(True)
driving_config.signals.primaryEncoderPositionPeriodMs(int(1000.0 / odometry_frequency))
driving_config.signals.primaryEncoderVelocityAlwaysOn(True)
driving_config.signals.primaryEncoderVelocityPeriodMs(20)
driving_config.signals.appliedOutputPeriodMs(20)
driving_config.signals.busVoltagePeriodMs(20)
# driving_config.signals.outputCurrentPeriodMs(20)

# Set up turning config
turning_config.inverted(False)
turning_config.setIdleMode(SparkBaseConfig.IdleMode.kBrake)
turning_config.smartCurrentLimit(20)
turning_config.voltageCompensation(12)

# Set up turning encoder config
turning_config.absoluteEncoder.inverted(True)
turning_config.absoluteEncoder.positionConversionFactor(turning_factor)
turning_config.absoluteEncoder.velocityConversionFactor(turning_velocity_factor)
turning_config.absoluteEncoder.averageDepth(2)

# Set up turning closed loop config
turning_config.closedLoop.setFeedbackSensor(FeedbackSensor.kAbsoluteEncoder)
turning_config.closedLoop.positionWrappingEnabled(True)
turning_config.closedLoop.positionWrappingInputRange(0, turning_factor)
turning_config.closedLoop.pidf(turnKp, 0.0, turnKd, 0.0)

# Set up driving signals config
turning_config.signals.absoluteEncoderPositionAlwaysOn(True)
turning_config.signals.absoluteEncoderPositionPeriodMs(int(1000.0 / odometry_frequency))
turning_config.signals.absoluteEncoderVelocityAlwaysOn(True)
turning_config.signals.absoluteEncoderVelocityPeriodMs(20)
turning_config.signals.appliedOutputPeriodMs(20)
turning_config.signals.busVoltagePeriodMs(20)
# turning_config.signals.outputCurrentPeriodMs(20)
