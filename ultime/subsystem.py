import commands2
from commands2 import Command

from ultime.alert import AlertCreator
from ultime.log import Loggable


class Subsystem(Loggable, AlertCreator, commands2.Subsystem):
    def __init__(self):
        super().__init__()
        self.log("Default command", "None")

    def getSubtable(self) -> str:
        return super().getSubtable() + self.getName() + "/"

    def logValues(self):
        super().logValues()
        if self.getCurrentCommand() is None:
            self.log("Current command", "None")
        else:
            self.log("Current command", self.getCurrentCommand().getName())

    def setDefaultCommand(self, command: Command) -> None:
        super().setDefaultCommand(command)
        if command is None:
            self.log("Default command", "None")
        else:
            self.log("Default command", command.getName())

    def readInputs(self):
        pass
