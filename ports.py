from ultime.immutable import Immutable

"""
Respect the naming convention : "subsystem" _ "component type" _ "precision"

Put port variables into the right category: CAN - PWM - DIO

Order port numbers, ex:
    shooter_motor = 0
    drivetrain_motor_fr = 1
    drivetrain_motor_rr = 2
"""


class CAN(Immutable):
    drivetrain_motor_turning_br = 6
    drivetrain_motor_driving_br = 5

    drivetrain_motor_turning_bl = 1
    drivetrain_motor_driving_bl = 2

    drivetrain_motor_turning_fl = 3
    drivetrain_motor_driving_fl = 4

    drivetrain_motor_turning_fr = 7
    drivetrain_motor_driving_fr = 8

    climber_motor = 9

    feeder_motor = 11

    pivot_motor = 12

    shooter_flywheel = 14
    shooter_feeder = 13
    shooter_indexer = 12


class PWM(Immutable):
    guide_servo = 0
    climber_servo_left = 1
    climber_servo_right = 2


class DIO(Immutable):
    guide_switch = 7
    guide_encoder_a = 8
    guide_encoder_b = 9
    climber_switch = 6
    pivot_switch_min = -1
    pivot_switch_max = 5


class PDP(Immutable):
    pass
