__all__ = ["timethis_enabled", "timethis", "tt", "print_stats", "print_stats_every"]

import functools
import inspect
import statistics
from collections import defaultdict
from typing import Literal

import wpilib

timethis_enabled = False
register: dict[str, list[float]] = defaultdict(list)
timer = wpilib.Timer()


def timethis(f, key: str = None):
    if not timethis_enabled:
        return f

    if not key:
        curframe = inspect.currentframe()
        calframes = inspect.getouterframes(curframe, 1)
        calframe = calframes[1]
        self = calframe.frame.f_locals["self"]
        full_class_name = self.__module__ + "." + self.__class__.__name__

        called_code = calframe.code_context[0][
            calframe.positions.col_offset : calframe.positions.end_col_offset
        ]
        assert "(" in called_code
        assert called_code.endswith(")")
        called_code = called_code[called_code.index("(") + 1 : -1]

        key = full_class_name + " " + called_code

    times = register[key]

    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        start = wpilib.Timer.getFPGATimestamp()
        ret = f(*args, **kwargs)
        times.append(wpilib.Timer.getFPGATimestamp() - start)
        return ret

    return wrapper


tt = timethis


class Stats:
    def __init__(self, times: list[float]):
        self.mean = statistics.fmean(times)
        self.std = statistics.stdev(times)
        self.min = min(times)
        self.max = max(times)
        self.med = statistics.median(times)


def print_stats(unit: Literal["s", "ms", "ns"] = "ms"):
    if not timethis_enabled:
        return

    msg = f"--------------------------\n{timethis.__name__} report\n\n"

    if unit == "s":
        conv = 1.0
    elif unit == "ms":
        conv = 1000.0
    elif unit == "ns":
        conv = 1000000.0
    else:
        raise ValueError(f"Unit {unit} not supported")

    max_length = max(len(key) for key in register.keys())
    all_stats = {key: Stats(times) for key, times in register.items()}
    mean_total = sum(stats.mean for stats in all_stats.values())

    for key, stats in all_stats.items():
        # Prevent division by zero
        proportion = stats.mean / mean_total if mean_total else 0.0

        msg += (
            f"{key: <{max_length}}"
            + " | "
            + f"{proportion * 100:5.2f} % | "
            + f"{stats.mean * conv:.3f} ± {stats.std * conv:.3f} {unit} "
            + f"(min={stats.min * conv:.3f} med={stats.med * conv:.3f} max={stats.max * conv:.3f})\n"
        )

    msg += f"\nMean total: {mean_total * conv:.3f} {unit}\n"

    print(msg)


def print_stats_every(seconds: float, unit: Literal["s", "ms", "ns"] = "ms"):
    timer.start()

    if timer.advanceIfElapsed(seconds):
        print_stats(unit)
