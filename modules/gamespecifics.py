import math
from enum import Enum, auto

import wpilib
from wpilib import DriverStation

from ultime.autoproperty import autoproperty
from ultime.module import Module


class GameSpecifics(Module):
    class State(Enum):
        Shoot = auto()
        CannotShoot = auto()
        PrepareShoot = auto()
        EndGame = auto()
        Unknown = auto()

    prepare_shoot_delay = autoproperty(7.0)
    preshoot_delay = autoproperty(3)

    def __init__(self):
        super().__init__()
        self.game_time_sec = self.createProperty(0.0)
        self.shift_time_left = self.createProperty(0.0)
        self.our_shift = self.createProperty(False)
        self.can_shoot = self.createProperty(False)
        self.can_prepare_shoot = self.createProperty(False)
        self.alliance = DriverStation.Alliance.kRed
        self.game_specific_message = ""
        self.won_auto = False

        self.timer = wpilib.Timer()
        self.state = self.State.Unknown

        self.message = self.createProperty("🦀")

    def teleopInit(self) -> None:
        self.timer.restart()

    def whoWon(self) -> None:
        self.game_specific_message = DriverStation.getGameSpecificMessage()
        self.alliance = DriverStation.getAlliance()
        self.won_auto = (
            self.game_specific_message == "B"
            and self.alliance == DriverStation.Alliance.kBlue
            or self.game_specific_message == "R"
            and DriverStation.Alliance.kRed
        )

    def computeShiftTimeLeft(self):
        if self.game_time_sec > 130:
            self.shift_time_left = self.game_time_sec - 130
        elif self.game_time_sec > 30:
            self.shift_time_left = (self.game_time_sec - 30)%25
        else:
            self.shift_time_left = self.game_time_sec

        self.shift_time_left = math.floor(self.shift_time_left)

    def teleopPeriodic(self) -> None:
        self.game_time_sec = DriverStation.getMatchTime()

        self.computeShiftTimeLeft()

        if not self.timer.hasElapsed(5.0):
            self.whoWon()
        elif self.timer.isRunning():
            self.timer.stop()

        if self.won_auto:
            if self.game_time_sec > 130:
                self.state = self.State.Shoot
            elif (
                self.game_time_sec
                > 105 + self.prepare_shoot_delay + self.preshoot_delay
            ):
                self.state = self.State.CannotShoot
            elif self.game_time_sec > 105 + self.preshoot_delay:
                self.state = self.State.PrepareShoot
            elif self.game_time_sec > 80:
                self.state = self.State.Shoot
            elif (
                self.game_time_sec > 55 + self.prepare_shoot_delay + self.preshoot_delay
            ):
                self.state = self.State.CannotShoot
            elif self.game_time_sec > 55 + self.preshoot_delay:
                self.state = self.State.PrepareShoot
            elif self.game_time_sec > 15:
                self.state = self.State.Shoot
            elif self.game_time_sec == -1.0:
                self.state = self.State.Unknown
            else:
                self.state = self.State.EndGame
        else:
            if self.game_time_sec > 105:
                self.state = self.State.Shoot
            elif (
                self.game_time_sec > 80 + self.prepare_shoot_delay + self.preshoot_delay
            ):
                self.state = self.State.CannotShoot
            elif self.game_time_sec > 80 + self.preshoot_delay:
                self.state = self.State.PrepareShoot
            elif self.game_time_sec > 55:
                self.state = self.State.Shoot
            elif (
                self.game_time_sec > 30 + self.prepare_shoot_delay + self.preshoot_delay
            ):
                self.state = self.State.CannotShoot
            elif self.game_time_sec > 30 + self.preshoot_delay:
                self.state = self.State.PrepareShoot
            elif self.game_time_sec > 15:
                self.state = self.State.Shoot
            elif self.game_time_sec == -1.0:
                self.state = self.State.Unknown
            else:
                self.state = self.State.EndGame

        if self.game_time_sec > 130:
            self.message = "RETRACT CLIMBER 💥"
        elif self.state == self.State.Shoot:
            self.message = "SHOOT 👩‍🍳"
        elif self.state == self.State.PrepareShoot:
            self.message = "PREPARE 🍽"
        elif self.state == self.State.CannotShoot:
            self.message = "PICK UP BALLS 🧲"
        elif self.state == self.State.EndGame:
            self.message = "CLIMB ⛏⛰"
        elif self.state == self.State.Unknown:
            self.message = "🦀"

    def logValues(self):
        self.log("State", str(self.state))
