import bisect
from enum import Enum, auto
from weakref import WeakSet

from wpilib import SmartDashboard, RobotController
from wpiutil import Sendable, SendableBuilder

from ultime.timethis import tt


class AlertType(Enum):
    Error = auto()
    Warning = auto()
    Info = auto()


class PublishedAlert:
    def __init__(self, timestamp: int, text: str):
        self.timestamp = timestamp
        self.text = text

    # Sorts from the most recent to the oldest
    def __lt__(self, other):
        return self.timestamp >= other.timestamp

    def __eq__(self, other):
        return self.timestamp == other.timestamp and self.text == other.text


class AlertGroup(Sendable):
    def __init__(self, name: str):
        super().__init__()
        self.name = name
        self.alerts: dict[AlertType, list[PublishedAlert]] = {}

    def getActiveAlertStorage(self, alert_type: AlertType) -> list[PublishedAlert]:
        return self.alerts.setdefault(alert_type, [])

    def getStrings(self, alert_type: AlertType) -> list[str]:
        return [alert.text for alert in self.getActiveAlertStorage(alert_type)]

    def initSendable(self, builder: SendableBuilder) -> None:
        def noop(_):
            pass

        builder.setSmartDashboardType("Alerts")
        builder.addStringArrayProperty(
            "errors", tt(lambda: self.getStrings(AlertType.Error)), noop
        )
        builder.addStringArrayProperty(
            "warnings", tt(lambda: self.getStrings(AlertType.Warning)), noop
        )
        builder.addStringArrayProperty(
            "infos", tt(lambda: self.getStrings(AlertType.Info)), noop
        )


class Alert:
    _groups: WeakSet[AlertGroup] = WeakSet()

    def __init__(self, text: str, alert_type: AlertType, group: str = "Alerts"):
        self._text = text
        self._alert_type = alert_type
        self._active = False
        self._published_alert = None
        # Important to keep ref to group to prevent it from being gc
        self._group = self._get_or_create_group(group)
        self._active_alerts = self._group.getActiveAlertStorage(alert_type)

    def set(self, active: bool) -> None:
        if active == self._active:
            return

        if active:
            self._published_alert = PublishedAlert(
                RobotController.getTime(), self._text
            )
            bisect.insort(self._active_alerts, self._published_alert)
        else:
            self._active_alerts.remove(self._published_alert)

        self._active = active

    def get(self) -> bool:
        return self._active

    def setText(self, text: str) -> None:
        if self._text == text:
            return

        self._text = text

        if self._active:
            timestamp = self._published_alert.timestamp
            self._active_alerts.remove(self._published_alert)
            self._published_alert = PublishedAlert(timestamp, text)
            bisect.insort(self._active_alerts, self._published_alert)

    def getText(self) -> str:
        return self._text

    def getType(self) -> AlertType:
        return self._alert_type

    @classmethod
    def _get_or_create_group(cls, group_name: str) -> AlertGroup:
        for group in cls._groups:
            if group.name == group_name:
                return group
        new_group = AlertGroup(group_name)
        cls._groups.add(new_group)
        SmartDashboard.putData(group_name, new_group)
        return new_group


class AlertCreator:
    """
    A mixin for modules and subsystems that allows them to create alerts.
    Classes using this mixin must have a method getName() that returns a string.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.registered_alerts = []
        self.running_test = self.createAlert("Diagnosing component...", AlertType.Info)

    def createAlert(self, text: str, alert_type: AlertType) -> Alert:
        alert = Alert(text, alert_type, self.getName() + "/Alerts")
        self.registered_alerts.append(alert)
        return alert

    def clearAlerts(self) -> None:
        for alert in self.registered_alerts:
            alert.set(False)

    def getName(self) -> str:
        return super().getName()
