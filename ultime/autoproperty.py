import contextlib
import inspect
import os
from dataclasses import dataclass
from enum import Enum, auto
from typing import Optional, Union, Callable

from ntcore.util import ntproperty as _old_ntproperty


class PropertyMode(Enum):
    Dashboard = auto()
    Local = auto()


@dataclass
class AutopropertyCall:
    key: str
    filename: str
    lineno: int
    col_offset: int


mode = PropertyMode.Dashboard

registry: list[AutopropertyCall] = []

FloatProperty = Union[float, Callable[[], float]]
_DEFAULT_CLASS_NAME = object()


def asCallable(val: FloatProperty) -> Callable[[], float]:
    if callable(val):
        return val
    return lambda: val


def defaultSetter(value):
    pass


def autoproperty(
    default_value,
    key: Optional[str] = None,
    table: Optional[str] = None,
    subtable: Optional[str] = _DEFAULT_CLASS_NAME,
    full_key: Optional[str] = None,
):
    if mode == PropertyMode.Local:
        return property(lambda _: default_value)

    assert full_key is None or (key is None and table is None and subtable is None)

    curframe = inspect.currentframe()
    calframes = inspect.getouterframes(curframe, 1)
    calframe = calframes[1]

    if full_key is None:
        if table is None:
            table = "Properties"

        if not table.startswith("/"):
            table = "/" + table

        if not table.endswith("/"):
            table += "/"

        if subtable is _DEFAULT_CLASS_NAME:
            subtable = calframe.function

        if subtable is not None:
            table += subtable + "/"

        if key is None:
            code_line = calframe.code_context[0]
            key = code_line.split("=")[0].strip()

        full_key = table + key

    registry.append(
        AutopropertyCall(
            full_key,
            calframe.filename,
            calframe.positions.lineno,
            calframe.positions.col_offset,
        )
    )

    if isinstance(default_value, int):
        print(f"{full_key} was converted to double")
        default_value = float(default_value)

    with open(os.devnull, "w") as devnull:
        with contextlib.redirect_stdout(devnull):
            prop = _old_ntproperty(
                full_key, default_value, writeDefault=False, persistent=False
            )

    def fget(_):
        val = prop.fget(_)
        if val is None:
            return default_value
        return val

    return property(fget, fset=prop.fset)
