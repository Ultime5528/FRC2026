import math


def feedforward(speed, kS, kF):
    volts = kS + kF * abs(speed)
    volts = math.copysign(volts, speed)
    return volts


def pf(current, target, kS, kF, kP):
    error = target - current
    volts = feedforward(target, kS, kF) + kP * error
    return volts


def clamp(value, min, max):
    if value < min:
        return min
    elif value > max:
        return max
    else:
        return value
