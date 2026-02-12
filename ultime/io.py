from abc import ABC, abstractmethod

from ultime.modulerobot import ModuleRobot


class IO(ABC):
    def __init__(self):
        ModuleRobot.ios.add(self)

    @abstractmethod
    def updateInputs(self):
        raise NotImplementedError()

    @abstractmethod
    def sendOutputs(self):
        raise NotImplementedError()
