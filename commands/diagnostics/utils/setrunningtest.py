from typing import Union

from commands2 import Command

from ultime.command import ignore_requirements
from ultime.module import Module
from ultime.subsystem import Subsystem


@ignore_requirements(["component"])
class SetRunningTest(Command):
    def __init__(self, component: Union[Subsystem, Module], is_running_test: bool):
        super().__init__()
        self.component = component
        self.is_running_test = is_running_test

    def initialize(self):
        self.component.running_test.set(self.is_running_test)

    def isFinished(self) -> bool:
        return True
