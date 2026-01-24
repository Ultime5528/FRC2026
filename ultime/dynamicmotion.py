import math
from typing import Optional

__all__ = ["DynamicMotion"]

import wpilib


def ensure_positive(value: float, name: str):
    if value <= 0:
        raise ValueError(f"{name} must be positive: {value}")
    return value


class DynamicMotion:
    """
    Proof
    -----
    Let
    ds = displacement (s - s0)
    v = current speed (m/s)
    vi = initial speed (m/s)
    vf = final speed (m/s)
    a = acceleration (m/s²)
    as = "acceleration" by distance (change of speed per unit of distance traveled) (m/s / m)

    Hence, by definition:
    (1.1) as = (vf - vi) / ds (constant)
    (1.2) => ds = (vf - vi) / as

    Cinematic equations:
    (2.1) v = vi + a * t
    (2.2) => t = (v - vi) / a
    # (2.3) => a = (v - vi) / t

    With cinematic equation:
    (3) ds = vi * t + ½ * a * t²

    Replace t by (2.2) in (3)
    => ds = vi * (v - vi) / a + ½ * ((v - vi)/a)²
    => ds = (v² - vi²) / 2a
    => 2 a ds = v² - vi²
    (4) => v = sqrt( vi² + 2 a ds )

    In cases where we know as, but not a.
    We want to express v in respect of ds: v(ds) = ?

    We know that v(0) = vi. This is already the case: v(0) = sqrt( vi² + 2 a * 0 ) = vi.
    By eq. (1.2), we also know that the ds to reach vf is (vf - vi) / as.

    Hence,
    v((vf - vi) / as) = vf.

    Let's replace ds by (vf - vi) / as in eq. (4) and solve for a:
    vf = sqrt( vi² + 2 a (vf - vi) / as )
    vf² = vi² + 2 a (vf - vi) / as
    a = (vf² - vi²) / 2 ((vf - vi)/as)

    Hence,
    (5) v = sqrt( vi² + ds / ((vf - vi)/as) * (vf² - vi²) )

    The previous equation is more intuitive, but it can be simplified:
    (6) v = sqrt( vi² + as ds (vi + vf) )

    """

    def __init__(
        self,
        goal: float,
        max_speed: float,
        end_speed: float,
        accel: float,
        decel: Optional[float] = None,
    ):
        self._goal = goal
        self._max_speed = ensure_positive(max_speed, "max_speed")
        self._end_speed = ensure_positive(end_speed, "end_speed")
        if self._max_speed < self._end_speed:
            raise ValueError(
                f"max_speed cannot be lower than than end_speed: {self._max_speed} < {self._end_speed}"
            )
        self._accel = ensure_positive(accel, "accel")
        self._decel = ensure_positive(decel, "decel") if decel is not None else accel
        self._last_time = None
        self._speed = None
        self._remaining_distance = None
        self._stopping_distance = None
        self._crossed_goal = False

    def _calculate_stopping_distance(self, current_speed: float):
        """
        Calculate the distance needed to decelerate from current speed to end speed.

        Args:
            current_speed (float): Current speed (m/s)

        Returns:
            float: Distance required to reach end_speed (m)
        """
        # Use v² = v₀² + 2a·x formula (solving for x)
        # We're decelerating, so a is negative
        return max(0.0, (current_speed**2 - self._end_speed**2) / (2 * self._decel))

    def update(self, position: float, current_speed: Optional[float] = None) -> float:
        remaining_distance = self._goal - position

        if (
            self._remaining_distance
            and self._remaining_distance * remaining_distance < 0
        ):
            self._crossed_goal = True

        self._remaining_distance = remaining_distance

        if current_speed is None:
            current_speed = self._speed if self._speed is not None else 0.0

        current_time = wpilib.Timer.getFPGATimestamp()
        delta = current_time - self._last_time if self._last_time is not None else 0
        self._last_time = current_time

        # Not moving in the right direction
        remaining_distance_abs = abs(self._remaining_distance)
        current_speed_abs = abs(current_speed)

        # Calculate stopping distance based on current speed
        self._stopping_distance = self._calculate_stopping_distance(current_speed_abs)

        target_speed = self._max_speed

        if self._remaining_distance * current_speed < 0:
            target_speed = current_speed - math.copysign(
                self._accel * delta, current_speed
            )

        # Check if we need to start decelerating
        else:
            if remaining_distance_abs <= self._stopping_distance:
                # We need to decelerate now
                # Formula: v² = v₀² + 2a·x (solving for v)
                # target_speed = (self.end_speed**2 + 2 * self.decel * remaining_distance)**0.5
                # Ensure we don't exceed current speed when decelerating
                # target_speed = min(target_speed, current_speed_abs)
                target_speed = max(
                    current_speed_abs - self._decel * delta, self._end_speed
                )

            # If we're not at max speed yet, accelerate
            elif current_speed_abs < self._max_speed:
                target_speed = min(
                    current_speed_abs + self._accel * delta, self._max_speed
                )

            target_speed = math.copysign(target_speed, self._remaining_distance)

        self._speed = target_speed

        return self._speed

    def getSpeed(self) -> float:
        return self._speed

    def getRemainingDistance(self) -> float:
        """
        Get the remaining distance to the goal.
        Can be negative.
        :return:
        """
        return self._remaining_distance

    def reachedGoal(self, tolerance):
        return abs(self._remaining_distance) <= tolerance

    def crossedGoal(self):
        return self._crossed_goal
