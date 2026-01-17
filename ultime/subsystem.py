from abc import abstractmethod

import commands2
from wpiutil import SendableBuilder

from ultime.alert import AlertCreator
from ultime.timethis import tt


class Subsystem(AlertCreator, commands2.Subsystem):
    @abstractmethod
    def getCurrentDrawAmps(self) -> float:
        raise NotImplementedError(
            f"Subsystem {self.getName()} does not implement getCurrentDrawAmps"
        )

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
