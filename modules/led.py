import math
from typing import Union, Tuple, List, Callable

import numpy as np
from wpilib import AddressableLED, DriverStation, SmartDashboard, getTime

import ports
from modules.positionestimator import PositionEstimator
from ultime.autoproperty import autoproperty
from ultime.module import Module


def interpolate(t, color1, color2):
    assert 0 <= t <= 1
    return ((1 - t) * color1 + t * color2).astype(int)


def numpy_interpolation(t: np.ndarray, color1: np.ndarray, color2: np.ndarray):
    assert 0 <= t.min() and t.max() <= 1
    return ((1 - t)[:, np.newaxis] * color1 + t[:, np.newaxis] * color2).astype(int)


Color = Union[np.ndarray, Tuple[int, int, int], List[int]]


class LEDModule(Module):
    green_rgb = np.array([0, 255, 0])
    dark_green_rgb = np.array([3, 53, 0])
    red_rgb = np.array([255, 0, 0])
    orange_rgb = np.array([255, 69, 0])
    blue_rgb = np.array([0, 0, 255])
    yellow_rgb = np.array([253, 255, 0])
    cyan_rgb = np.array([0, 222, 255])
    black = np.array([0, 0, 0])
    white = np.array([255, 255, 255])
    purple = np.array([128, 0, 128])
    pink = np.array([255, 105, 180])

    led_number = autoproperty(100.0)

    brightness_value = autoproperty(100.0)

    def __init__(self, hardware, estimator: PositionEstimator):
        super().__init__()
        from modules.hardware import HardwareModule

        self.hardware: HardwareModule = hardware
        self.estimator = estimator

        self.led_strip = AddressableLED(ports.PWM.led_strip)
        self.buffer = [AddressableLED.LEDData() for _ in range(int(self.led_number))]
        self.led_strip.setLength(len(self.buffer))
        self.led_strip.start()

        self.time = self.createProperty(0.0)

    @property
    def brightness(self) -> float:
        return max(min(100, self.brightness_value), 0) / 100

    def setRGB(self, i: int, color: Color):
        self.buffer[i].setRGB(*color)

    def setAll(self, color_func: Callable[[int], Color]):
        a = np.arange(len(self.buffer))
        for i in np.nditer(a):
            self.setRGB(i, color_func(i))

    def getAllianceColor(self):
        alliance = DriverStation.getAlliance()
        if alliance == DriverStation.Alliance.kBlue:  # blue team
            color = self.blue_rgb
        elif alliance == DriverStation.Alliance.kRed:  # red team
            color = self.red_rgb
        else:
            color = self.black
        return color

    def e_stopped(self):
        interval = 10
        flash_time = 20
        state = round(self.time / flash_time) % 2

        red = (self.brightness * self.red_rgb).astype(int)

        def getColor(i: int):
            is_color = state - round(i / interval) % 2
            if is_color:
                return red
            else:
                return self.black

        self.setAll(getColor)

    def modeAuto(self):
        color = (self.brightness * self.getAllianceColor()).astype(int)
        white = (self.brightness * self.white).astype(int)
        i_values = np.arange(self.led_number)
        y_values = 0.5 * np.sin(2 * math.pi**2 * (i_values - 3 * self.time) / 200) + 0.5

        pixel_value = numpy_interpolation(y_values, color, white)
        for i, y in enumerate(pixel_value):
            self.buffer[i].setRGB(*y)

    def modeTeleop(self):
        self.commonTeleop(self.getAllianceColor(), self.white, 0.5)

    def modeEndgame(self):
        self.commonTeleop(self.pink, self.white, 1.5)

    def commonTeleop(self, color1, color2, speed):
        color1 = (self.brightness * color1).astype(int)
        color2 = (self.brightness * color2).astype(int)

        a = 3
        i_values = np.arange(self.led_number)
        y_values = np.maximum(
            0, (a + 1) * np.cos((i_values - speed * self.time) / 5) - a
        )

        pixel_value = numpy_interpolation(y_values, color1, color2)
        for i, y in enumerate(pixel_value):
            self.buffer[i].setRGB(*y)

    def modeConnected(self):
        pixel_value = round(
            abs(255 * self.brightness * (math.cos(self.time / (12 * math.pi))))
        )

        if DriverStation.getAlliance() == DriverStation.Alliance.kRed:
            for i in range(int(self.led_number)):
                self.buffer[i].setRGB(pixel_value, 0, 0)
        else:
            for i in range(int(self.led_number)):
                self.buffer[i].setRGB(0, 0, pixel_value)

    def modeConnectedLowBattery(self):
        interval = 10
        flash_time = 20
        state = round(self.time / flash_time) % 2

        yellow = (self.brightness * self.yellow_rgb).astype(int)
        cyan = (self.brightness * self.cyan_rgb).astype(int)

        def getColor(i: int):
            is_color = state - round(i / interval) % 2
            if is_color:
                return yellow
            else:
                return cyan

        self.setAll(getColor)

    def modeNotConnected(self):
        pixel_value = round(
            255 * self.brightness * math.cos(self.time / (18 * math.pi))
        )

        if pixel_value >= 0:
            r = pixel_value
            g = 0
            b = 0
        else:
            r = 0
            g = 0
            b = abs(pixel_value)

        for i in range(int(self.led_number)):
            self.buffer[i].setRGB(r, g, b)

    def rainbow(self):
        for i in range(int(self.led_number)):
            hue = (int(self.time) + int(i * 180 / self.led_number)) % 180
            self.buffer[i].setHSV(
                hue,
                255,
                round(255 * self.brightness),
            )

    def canShoot(self):
        self.commonTeleop(self.green_rgb, self.white, 0.5)

    def cannotShoot(self):
        self.commonTeleop(self.getAllianceColor(), self.white, 0.5)

    def prepareShoot(self):
        self.commonTeleop(self.yellow_rgb, self.white, 0.5)

    def seesTags(self):
        for i in range(len(self.buffer)):
            self.buffer[i].setRGB(255, 255, 255)

    def robotPeriodic(self) -> None:
        start_time = getTime()
        self.time += 1

        if DriverStation.isEStopped():
            self.e_stopped()
        elif DriverStation.isAutonomousEnabled():  # auto
            self.modeAuto()
        elif DriverStation.isTeleopEnabled():  # teleop
            game_data = DriverStation.getGameSpecificMessage()
            alliance = DriverStation.getAlliance()
            match_time = DriverStation.getMatchTime()

            won = (
                game_data == "B"
                and alliance == DriverStation.Alliance.kBlue
                or game_data == "R"
                and DriverStation.Alliance.kRed
            )

            prepare_shoot_delay = 7
            preshoot_delay = 3

            if won:
                if match_time > 130:
                    self.canShoot()
                elif match_time > 105 + prepare_shoot_delay + preshoot_delay:
                    self.cannotShoot()
                elif match_time > 105 + preshoot_delay:
                    self.prepareShoot()
                elif match_time > 80:
                    self.canShoot()
                elif match_time > 55 + prepare_shoot_delay + preshoot_delay:
                    self.cannotShoot()
                elif match_time > 55 + preshoot_delay:
                    self.prepareShoot()
                elif match_time > 15:
                    self.canShoot()
                elif match_time == -1.0:
                    self.rainbow()
                else:
                    self.modeEndgame()
            else:
                if match_time > 105:
                    self.canShoot()
                elif match_time > 80 + prepare_shoot_delay + preshoot_delay:
                    self.cannotShoot()
                elif match_time > 80 + preshoot_delay:
                    self.prepareShoot()
                elif match_time > 55:
                    self.canShoot()
                elif match_time > 30 + prepare_shoot_delay + preshoot_delay:
                    self.cannotShoot()
                elif match_time > 30 + preshoot_delay:
                    self.prepareShoot()
                elif match_time > 15:
                    self.canShoot()
                elif match_time == -1.0:
                    self.rainbow()
                else:
                    self.modeEndgame()

            # if DriverStation.getMatchTime() > 30:
            #     # TODO Les différents mode teleop / alliance shifts
            #     self.modeTeleop()
            # elif DriverStation.getMatchTime() == -1.0:
            #     self.rainbow()
            # else:
            #     self.modeEndgame()

        elif DriverStation.isDSAttached():
            if DriverStation.getBatteryVoltage() > 12:
                if self.estimator.tag_seen_in_frame:
                    self.seesTags()
                else:
                    self.modeConnected()  # connected to driver station
            else:
                self.modeConnectedLowBattery()  # has low voltage

        else:  # not connected to driver station
            self.modeNotConnected()

        self.led_strip.setData(self.buffer)
        SmartDashboard.putNumber("led_time", getTime() - start_time)
