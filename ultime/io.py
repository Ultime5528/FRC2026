from abc import ABC, abstractmethod

from ultime.modulerobot import ModuleRobot


class Io(ABC):
    def __init__(self):
        ModuleRobot.ios.add(self)

    @abstractmethod
    def updateInputs(self):
        pass

    @abstractmethod
    def sendOutputs(self):
        pass
