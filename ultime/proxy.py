__all__ = ["proxy"]

import weakref
from typing import TypeVar

Type = TypeVar("Type")


class WeakMethodProxy:
    def __init__(self, weak: weakref.WeakMethod):
        self.weak = weak

    def __call__(self, *args, **kwargs):
        ref = self.weak()
        if ref:
            return ref(*args, **kwargs)
        raise ReferenceError(
            "ReferenceError: weakly-referenced object no longer exists"
        )


def proxy(weak: Type) -> Type:
    try:
        # Checking if bound method
        obj = weak.__self__
        func = weak.__func__
        return WeakMethodProxy(weakref.WeakMethod(weak))

    except AttributeError:
        # Not a bound method, usual proxy
        return weakref.proxy(weak)
