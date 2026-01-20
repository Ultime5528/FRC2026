import inspect

from commands2 import Subsystem

import ultime
from ultime.subsystem import Subsystem
from ultime.tests import import_submodules


def get_subsystems() -> list[Subsystem or None]:
    import subsystems

    results = import_submodules(subsystems)
    subs = []

    for mod in results.values():
        for _, cls in inspect.getmembers(mod, inspect.isclass):
            if issubclass(cls, Subsystem) and cls.__name__ != "Subsystem":
                subs.append(cls)

    return subs


def test_inheritance():
    for obj in get_subsystems():
        assert issubclass(
            obj, ultime.subsystem.Subsystem
        ), f"{obj.__name__} is not a subclass of ultime.subsystem.Subsystem"
