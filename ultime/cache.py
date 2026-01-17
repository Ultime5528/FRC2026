__all__ = ["cache_every_loop", "clear_loop_cache"]

import functools
from collections import defaultdict

cache_enabled = True


class CachedValue:
    def __init__(self, reset_interval: int):
        self.has_value = False
        self.value = None
        self.iterations_until_reset = None

        if reset_interval <= 0:
            raise ValueError(f"Reset interval must be a positive int: {reset_interval}")

        self.reset_interval = reset_interval


cached_values: dict[int, list[CachedValue]] = defaultdict(list)


def cache_every_loop(f_or_num):
    num = f_or_num if isinstance(f_or_num, int) else 1

    def wrapper(f):
        if not cache_enabled:
            return f

        cached_value = CachedValue(num)
        cached_values_group = cached_values[num]
        cached_value.iterations_until_reset = (len(cached_values_group) % num) + 1
        cached_values_group.append(cached_value)

        @functools.wraps(f)
        def wrapped(*args, **kwargs):
            if cached_value.has_value:
                return cached_value.value

            ret = f(*args, **kwargs)

            cached_value.has_value = True
            cached_value.value = ret

            return ret

        return wrapped

    return wrapper(f_or_num) if callable(f_or_num) else wrapper


def clear_loop_cache():
    for reset_interval, cvs in cached_values.items():
        for cached_value in cvs:
            cached_value.iterations_until_reset -= 1
            if cached_value.iterations_until_reset == 0:
                cached_value.has_value = False
                cached_value.value = None
                cached_value.iterations_until_reset = reset_interval
