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
    drivetrain_motor_turning_br = 1
    drivetrain_motor_driving_br = 2

    drivetrain_motor_turning_bl = 3
    drivetrain_motor_driving_bl = 4

    drivetrain_motor_turning_fr = 6
    drivetrain_motor_driving_fr = 5

    drivetrain_motor_turning_fl = 7
    drivetrain_motor_driving_fl = 8

    climber_motor = 11

    feeder_motor = 10

    pivot_motor = 9

    shooter_flywheel = 14
    shooter_feeder = 13
    shooter_indexer = 12


class PWM(Immutable):
    guide_servo = 5
    hugger_servo_left = 9
    hugger_servo_right = 8


class DIO(Immutable):
    guide_switch = 7
    guide_encoder_a = 8
    guide_encoder_b = 9
    climber_switch = 6
    pivot_switch_min = -1
    pivot_switch_max = 5
    drivetrain_photocell_left = 4
    drivetrain_photocell_right = 3


class PDP(Immutable):
    pass
