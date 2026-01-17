from typing import Optional

import wpilib.deployinfo
from commands2 import CommandScheduler, Command
from wpilib import DataLogManager, DriverStation

from ultime.module import Module
from ultime.timethis import print_stats_every


def logInterrupt(interrupted: Command, interruptor: Optional[Command]):
    DataLogManager.log(
        f"Command {interrupted.getName()} interrupted by {interruptor.getName() if interruptor else 'None'}"
    )


class LoggingModule(Module):
    def __init__(self):
        super().__init__()
        DataLogManager.start()
        DriverStation.startDataLog(DataLogManager.getLog())
        CommandScheduler.getInstance().onCommandInitialize(
            lambda cmd: DataLogManager.log(f"Command {cmd.getName()} initialized")
        )
        CommandScheduler.getInstance().onCommandFinish(
            lambda cmd: DataLogManager.log(f"Command {cmd.getName()} finished")
        )
        CommandScheduler.getInstance().onCommandInterruptWithCause(logInterrupt)

    def robotPeriodic(self) -> None:
        print_stats_every(5.0, "ns")

    def initSendable(self, builder):
        # Deploy data
        data = wpilib.deployinfo.getDeployData()

        if data:
            for key, value in data.items():
                builder.publishConstString(key, value)
        else:
            DataLogManager.log("Could not find deploy data (not running on robot?)")
