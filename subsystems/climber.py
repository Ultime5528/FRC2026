import wpilib
from rev import SparkMax, SparkMaxSim
from wpilib import RobotBase
from wpimath._controls._controls.plant import DCMotor

import ports
from ultime.autoproperty import autoproperty
from ultime.linear.linearsubsystem import LinearSubsystem
from ultime.switch import Switch


class Climber(LinearSubsystem):
    position_conversion_factor = autoproperty(1.0)
    speed_maintain = autoproperty(0.04)
    position_min = autoproperty(0.0)
    position_max = autoproperty(190.0)

    def __init__(self):

        super().__init__(
            sim_initial_position=self.position_max * 0.5,
            should_reset_min=True,
            should_reset_max=False,
            should_block_min_position=False,
            should_block_max_position=True,
            should_block_min_switch=True,
            should_block_max_switch=True,
            sim_motor_to_distance_factor=80.0,
            sim_gravity=0.0,
        )

        self._motor = SparkMax(ports.CAN.climber_motor, SparkMax.MotorType.kBrushless)
        self._motor.setInverted(False)
        self._encoder = self._motor.getEncoder()
        self._switch = Switch(Switch.Type.NormallyClosed, ports.DIO.climber_switch)

        self.maintain_position_tolerance = self.position_max * 0.01

        if RobotBase.isSimulation():
            self._sim_motor = SparkMaxSim(self._motor, DCMotor.NEO(1))
            self._sim_encoder = self._sim_motor.getRelativeEncoderSim()

    def getMinPosition(self) -> float:
        return 0.0

    def getMaxPosition(self) -> float:
        return self.position_max

    def isSwitchMinPressed(self) -> bool:
        return self._switch.isPressed()

    def isSwitchMaxPressed(self) -> bool:
        return False

    def getEncoderPosition(self) -> float:
        return self._encoder.getPosition()

    def setSimulationEncoderPosition(self, position: float) -> None:
        self._sim_encoder.setPosition(position)

    def getPositionConversionFactor(self) -> float:
        return self.position_conversion_factor

    def _setMotorOutput(self, speed: float) -> None:
        self._motor.set(speed)

    def getMotorOutput(self) -> float:
        return self._motor.get()

    def setSimSwitchMinPressed(self, pressed: bool) -> None:
        self._switch.setSimValue(pressed)

    def setSimSwitchMaxPressed(self, pressed: bool) -> None:
        pass

    def maintain(self):
        position = self.getPosition()
        if (
            self.hasReset()
            and position >= (self.position_min - self.maintain_position_tolerance)
            and position <= (self.position_max + self.maintain_position_tolerance)
        ):
            self._motor.set(self.speed_maintain)
