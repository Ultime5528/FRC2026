import math

from wpiutil import Sendable


def input_modulus(input: float, minimum_input: float, maximum_input: float) -> float:
    modulus = maximum_input - minimum_input

    # Wrap input if it's above the maximum input
    num_max = int((input - minimum_input) / modulus)
    input -= num_max * modulus

    # Wrap input if it's below the minimum input
    num_min = int((input - maximum_input) / modulus)
    input -= num_min * modulus

    return input


class AffineController(Sendable):
    def __init__(self, p: float, b: float, period: float = 0.02):
        super().__init__()
        self._p = p
        self._b = b
        self._period = period
        self._maximum_output = float("inf")

        self._measurement = 0.0
        self._has_measurement = False
        self._setpoint = 0.0
        self._has_setpoint = False

        self._position_error = 0.0
        self._prev_error = 0.0
        self._velocity_error = 0.0

        self._position_tolerance = 0.05
        self._velocity_tolerance = float("inf")

        self._continuous = False
        self._minimum_input = 0.0
        self._maximum_input = 0.0

    def setP(self, p: float) -> None:
        self._p = p

    def getP(self) -> float:
        return self._p

    def setB(self, b: float) -> None:
        self._b = b

    def getB(self) -> float:
        return self._b

    def getPositionError(self) -> float:
        return self._position_error

    def getVelocityError(self) -> float:
        return self._velocity_error

    def setTolerance(
        self, position_tolerance: float, velocity_tolerance=float("inf")
    ) -> None:
        self._position_tolerance = position_tolerance
        self._velocity_tolerance = velocity_tolerance

    def getPositionTolerance(self) -> float:
        return self._position_tolerance

    def getVelocityTolerance(self) -> float:
        return self._velocity_tolerance

    def setMaximumOutput(self, maximum_output: float) -> None:
        self._maximum_output = maximum_output

    def getMaximumOutput(self) -> float:
        return self._maximum_output

    def setSetpoint(self, setpoint) -> None:
        self._setpoint = setpoint
        self._has_setpoint = True

    def getSetpoint(self) -> float:
        return self._setpoint

    def enableContinuousInput(self, minimum_input: float, maximum_input: float) -> None:
        self._continuous = True
        self._minimum_input = minimum_input
        self._maximum_input = maximum_input

    def disableContinuousInput(self) -> None:
        self._continuous = False

    def calculate(self, measurement: float) -> float:
        self._measurement = measurement
        self._has_measurement = True
        self._prev_error = self._position_error

        if self._continuous:
            error_bound = (self._maximum_input - self._minimum_input) / 2
            self._position_error = input_modulus(
                self._setpoint - self._measurement, -error_bound, error_bound
            )
        else:
            self._position_error = self._setpoint - self._measurement

        self._velocity_error = (self._position_error - self._prev_error) / self._period

        # if abs(self._position_error) < self._position_tolerance:
        #     output = 0.0
        # else:
        abs_output = (
            self._p * (abs(self._position_error) - self._position_tolerance) + self._b
        )
        abs_output = min(abs_output, self._maximum_output)
        output = math.copysign(abs_output, self._position_error)

        return output

    def atSetpoint(self) -> bool:
        return (
            self._has_measurement
            and self._has_setpoint
            and abs(self._position_error) < self._position_tolerance
            and abs(self._velocity_error) < self._velocity_tolerance
        )
