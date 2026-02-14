from abc import abstractmethod

import wpilib
from wpiutil import SendableBuilder

from ultime.subsystem import Subsystem


class LinearSubsystem(Subsystem):
    def __init__(
        self,
        sim_initial_position: float,
        should_reset_min: bool,
        should_reset_max: bool,
        should_block_min_position: bool,
        should_block_max_position: bool,
        sim_motor_to_distance_factor: float = 1.0,
        sim_gravity: float = 0.0,
    ):
        super().__init__()
        self._offset = self.createProperty(0.0)
        self._has_reset = self.createProperty(False)
        self._prev_is_at_min = self.createProperty(False)
        self._prev_is_at_max = self.createProperty(False)
        self._should_reset_min = should_reset_min
        self._should_reset_max = should_reset_max
        self._should_block_min_position = should_block_min_position
        self._should_block_max_position = should_block_max_position

        self._sim_initial_position = sim_initial_position
        self._sim_position = sim_initial_position
        self._sim_prev_time = wpilib.Timer.getFPGATimestamp()
        self._sim_motor_to_distance_factor = sim_motor_to_distance_factor
        self._sim_gravity = sim_gravity

    def logValues(self):
        self.log("position", self.getPosition())
        self.log("encoder_position", self.getEncoderPosition())
        self.log("min_switch_pressed", self.isSwitchMinPressed())
        self.log("max_switch_pressed", self.isSwitchMaxPressed())

    @abstractmethod
    def getMinPosition(self) -> float:
        raise NotImplementedError()

    @abstractmethod
    def getMaxPosition(self) -> float:
        raise NotImplementedError()

    @abstractmethod
    def isSwitchMinPressed(self) -> bool:
        raise NotImplementedError()

    @abstractmethod
    def isSwitchMaxPressed(self) -> bool:
        raise NotImplementedError()

    @abstractmethod
    def getEncoderPosition(self) -> float:
        raise NotImplementedError()

    @abstractmethod
    def setSimulationEncoderPosition(self, position: float) -> None:
        raise NotImplementedError()

    def hasReset(self) -> bool:
        return self._has_reset

    @abstractmethod
    def getPositionConversionFactor(self) -> float:
        raise NotImplementedError()

    def getPosition(self) -> float:
        return self.getPositionConversionFactor() * (
            self.getEncoderPosition() + self._offset
        )

    @abstractmethod
    def _setMotorOutput(self, speed: float) -> None:
        raise NotImplementedError()

    @abstractmethod
    def getMotorOutput(self) -> float:
        raise NotImplementedError()

    @abstractmethod
    def setSimSwitchMinPressed(self, pressed: bool) -> None:
        raise NotImplementedError()

    @abstractmethod
    def setSimSwitchMaxPressed(self, pressed: bool) -> None:
        raise NotImplementedError()

    def setSpeed(self, speed: float) -> None:
        if speed < 0.0 and (
            self.isSwitchMinPressed()
            or (
                self._should_block_min_position
                and self.hasReset()
                and self.getPosition() < self.getMinPosition()
            )
        ):
            speed = 0.0
        elif speed > 0.0 and (
            self.isSwitchMaxPressed()
            or (
                self._should_block_max_position
                and self.hasReset()
                and self.getPosition() > self.getMaxPosition()
            )
        ):
            speed = 0.0

        self._setMotorOutput(speed)

    def periodic(self) -> None:
        if self._should_reset_min:
            if self._prev_is_at_min and not self.isSwitchMinPressed():
                self._offset = self.getMinPosition() - self.getEncoderPosition()
                self._has_reset = True
            self._prev_is_at_min = self.isSwitchMinPressed()

        if self._should_reset_max:
            if self._prev_is_at_max and not self.isSwitchMaxPressed():
                self._offset = self.getMaxPosition() - self.getEncoderPosition()
                self._has_reset = True
            self._prev_is_at_max = self.isSwitchMaxPressed()

    def simulationPeriodic(self) -> None:
        current_time = wpilib.Timer.getFPGATimestamp()
        dt = current_time - self._sim_prev_time
        self._sim_prev_time = current_time

        delta = (
            (self.getMotorOutput() - self._sim_gravity)
            * self._sim_motor_to_distance_factor
            * dt
        )
        self._sim_position += delta

        self.setSimulationEncoderPosition(
            (self._sim_position - self._sim_initial_position)
            / self.getPositionConversionFactor()
        )

        if self._sim_position <= self.getMinPosition():
            self.setSimSwitchMinPressed(True)
        else:
            self.setSimSwitchMinPressed(False)

        if self._sim_position >= self.getMaxPosition():
            self.setSimSwitchMaxPressed(True)
        else:
            self.setSimSwitchMaxPressed(False)

    def initSendable(self, builder: SendableBuilder) -> None:
        def setHasReset(value: bool) -> None:
            self._has_reset = value

        builder.addBooleanProperty(
            "switch_min_pressed", self.isSwitchMinPressed, lambda _: None
        )
        builder.addBooleanProperty(
            "switch_max_pressed", self.isSwitchMaxPressed, lambda _: None
        )
        builder.addDoubleProperty("position", self.getPosition, lambda _: None)
        builder.addBooleanProperty("has_reset", self.hasReset, setHasReset)
