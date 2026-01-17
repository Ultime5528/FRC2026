import wpilib
from ntcore import NetworkTableInstance
from wpilib import DriverStation, Timer, RobotBase

from properties import loop_delay, entry_name_check_time, entry_name_check_mirror
from ultime.autoproperty import mode, PropertyMode
from ultime.module import Module


class PropertySaveCheckerModule(Module):
    def __init__(self):
        super().__init__()
        inst = NetworkTableInstance.getDefault()
        self.entry_check_time = inst.getEntry(entry_name_check_time)
        self.entry_check_mirror = inst.getEntry(entry_name_check_mirror)
        self.timer_check = Timer()

        self._enabled = False

        if RobotBase.isSimulation():
            print("Disabling PropertySaveCheckerModule : Robot is in simulation")
        elif mode == PropertyMode.Local:
            print("Disabling PropertySaveCheckerModule : PropertyMode is Local")
        else:
            print(f"Enabling PropertySaveCheckerModule : {mode}")
            self._enabled = True

    def robotPeriodic(self) -> None:
        if self._enabled:
            # TODO add wpilib.Alert in module (add Modules to Diagnostics ?)
            if DriverStation.isFMSAttached():
                self.timer_check.start()
                if self.timer_check.advanceIfElapsed(10.0):
                    wpilib.reportWarning(
                        f"FMS is connected, but PropertyMode is not Local: {mode}"
                    )

            elif DriverStation.isDSAttached():
                self.timer_check.start()
                current_time = wpilib.getTime()
                self.entry_check_time.setDouble(current_time)
                if self.timer_check.advanceIfElapsed(loop_delay * 2):
                    mirror_time = self.entry_check_mirror.getDouble(0.0)
                    if current_time - mirror_time < loop_delay:
                        print("Save loop running")
                    else:
                        raise RuntimeError(
                            f"Save loop is not running ({current_time=:.2f}, {mirror_time=:.2f})"
                        )
