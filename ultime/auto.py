from commands2 import Command
from commands2.cmd import either
from wpilib import DriverStation


def eitherRedBlue(red: Command, blue: Command) -> Command:
    return either(
        red,
        blue,
        lambda: DriverStation.getAlliance() == DriverStation.Alliance.kRed,
    )
