import commands2
from wpiutil import SendableBuilder

from ultime.alert import AlertCreator
from ultime.log import Loggable
from ultime.timethis import tt


class Subsystem(Loggable, AlertCreator, commands2.Subsystem):
    def getSubtable(self) -> str:
        return super().getSubtable() + self.getName() + "/"

    def readInputs(self):
        pass

    def initSendable(self, builder: SendableBuilder) -> None:
        super().initSendable(builder)

        def currentCommandName():
            cmd = self.getCurrentCommand()
            if cmd:
                return cmd.getName()
            else:
                return "None"

        def defaultCommandName():
            cmd = self.getDefaultCommand()
            if cmd:
                return cmd.getName()
            else:
                return "None"

        def noop(_):
            pass

        builder.setSmartDashboardType("List")
        builder.addStringProperty("Current command", tt(currentCommandName), noop)
        builder.addStringProperty("Default command", tt(defaultCommandName), noop)
