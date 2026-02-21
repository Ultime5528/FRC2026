import wpilib
from rev import SparkMax, SparkMaxSim
from wpilib import RobotBase
from wpimath._controls._controls.plant import DCMotor
from wpiutil import SendableBuilder

import ports
from ultime.autoproperty import autoproperty
from ultime.linear.linearsubsystem import LinearSubsystem
from ultime.switch import Switch


class Climber(LinearSubsystem):
    position_hug_left = autoproperty(-45.0)
    position_unhug_left = autoproperty(0.0)
    position_hug_right = autoproperty(0.0)
    position_unhug_right = autoproperty(45.0)
    delay_hug = autoproperty(2.0)

    position_conversion_factor = autoproperty(0.2)
    height_max = autoproperty(0.295)

    def __init__(self):
        super().__init__(
            sim_initial_position=self.height_max,
            should_reset_min=True,
            should_reset_max=False,
            should_block_min_position=False,
            should_block_max_position=True,
            sim_motor_to_distance_factor=1.0,
            sim_gravity=0.0,
        )

        self._climber_motor = SparkMax(
            ports.CAN.climber_motor, SparkMax.MotorType.kBrushless
        )
        self._hugger_motor_left = wpilib.Servo(ports.PWM.climber_servo_left)
        self._hugger_motor_right = wpilib.Servo(ports.PWM.climber_servo_right)
        self._climber_encoder = self._climber_motor.getEncoder()
        self._switch = Switch(Switch.Type.NormallyClosed, ports.DIO.climber_switch)

        if RobotBase.isSimulation():
            self._climber_sim_motor = SparkMaxSim(self._climber_motor, DCMotor.NEO(1))
            self._climber_sim_encoder = self._climber_sim_motor.getRelativeEncoderSim()

    def getMinPosition(self) -> float:
        return 0.0

    def getMaxPosition(self) -> float:
        return self.height_max

    def isSwitchMinPressed(self) -> bool:
        return self._switch.isPressed()

    def isSwitchMaxPressed(self) -> bool:
        return False

    def getEncoderPosition(self) -> float:
        return self._climber_encoder.getPosition()

    def setSimulationEncoderPosition(self, position: float) -> None:
        self._climber_sim_encoder.setPosition(position)

    def getPositionConversionFactor(self) -> float:
        return self.position_conversion_factor

    def _setMotorOutput(self, speed: float) -> None:
        self._climber_motor.set(speed)

    def getMotorOutput(self) -> float:
        return self._climber_motor.get()

    def setSimSwitchMinPressed(self, pressed: bool) -> None:
        self._switch.setSimValue(pressed)

    def setSimSwitchMaxPressed(self, pressed: bool) -> None:
        pass

    def hug(self):
        self._hugger_motor_left.setAngle(self.position_hug_left)
        self._hugger_motor_right.setAngle(self.position_hug_right)

    def unhug(self):
        self._hugger_motor_left.setAngle(self.position_unhug_left)
        self._hugger_motor_right.setAngle(self.position_unhug_right)

    def initSendable(self, builder: SendableBuilder) -> None:
        super().initSendable(builder)

        def noop(_):
            pass

        builder.addBooleanProperty(
            "ClimberSwitch", (lambda: self._switch.isPressed()), noop
        )
        builder.addFloatProperty(
            "ClimberMotor", (lambda: self._climber_motor.get()), noop
        )
