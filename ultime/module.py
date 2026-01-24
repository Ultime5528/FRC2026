import inspect
from functools import wraps

from wpiutil import Sendable

from ultime.alert import AlertCreator


class Module(AlertCreator, Sendable):
    def __init__(self):
        super().__init__()
        self.redefines_init_sendable = False

    def getName(self) -> str:
        return self.__class__.__name__

    def initSendable(self, builder):
        pass

    def robotInit(self) -> None:
        pass

    def robotPeriodic(self) -> None:
        pass

    def simulationInit(self) -> None:
        pass

    def simulationPeriodic(self) -> None:
        pass

    def disabledInit(self) -> None:
        pass

    def disabledPeriodic(self) -> None:
        pass

    def disabledExit(self) -> None:
        pass

    def autonomousInit(self) -> None:
        pass

    def autonomousPeriodic(self) -> None:
        pass

    def autonomousExit(self) -> None:
        pass

    def teleopInit(self) -> None:
        pass

    def teleopPeriodic(self) -> None:
        pass

    def teleopExit(self) -> None:
        pass

    def testInit(self) -> None:
        pass

    def testPeriodic(self) -> None:
        pass

    def testExit(self) -> None:
        pass

    def driverStationConnected(self) -> None:
        pass


def createWrappedFunction(wrapped_func: callable, methods: list[callable]) -> callable:
    @wraps(wrapped_func)
    def call():
        for method in methods:
            method()

    return call


class ModuleList(Module):
    def __init__(self, *modules: Module):
        super().__init__()
        self.modules = list(modules)
        self._setup()

    def getName(self) -> str:
        return "ModuleList"

    def addModules(self, *modules):
        self.modules = self.modules + list(modules)
        self._setup()

    def _setup(self):
        for module in self.modules:
            if not isinstance(module, Module):
                raise TypeError(
                    "Every module must be an instance of a Module subclass :", module
                )

        self._methods: dict[str, list[callable]] = {
            name: []
            for name, attr in Module.__dict__.items()
            if inspect.isfunction(attr)
        }

        for name, methods in self._methods.items():
            for module in self.modules:
                for module_parent in module.__class__.mro():
                    if module_parent is Module:
                        break

                    if name in module_parent.__dict__:
                        module_method = getattr(module, name)
                        methods.append(module_method)

                        if name == "initSendable":
                            module.redefines_init_sendable = True

            if len(methods) > 0:
                original_func = getattr(self, name)
                new_func = createWrappedFunction(original_func, methods)
                setattr(self, name, new_func)
