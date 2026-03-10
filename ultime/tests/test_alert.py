from ntcore import NetworkTableInstance
from wpilib import SmartDashboard

from ultime.alert import AlertType, Alert
from ultime.tests.utils import RobotTestController


def test_alert(robot_controller: RobotTestController):
    topic = (
        NetworkTableInstance.getDefault()
        .getStringArrayTopic("/SmartDashboard/Alerts/errors")
        .subscribe(["default"])
    )
    alert = Alert("Test", AlertType.Error)

    SmartDashboard.updateValues()

    assert topic.get() == []

    alert.set(True)
    SmartDashboard.updateValues()

    assert topic.get() == ["Test"]

    alert.setText("Test2")
    SmartDashboard.updateValues()

    assert topic.get() == ["Test2"]

    alert.set(False)
    SmartDashboard.updateValues()

    assert topic.get() == []

    alert.setText("Test3")
    SmartDashboard.updateValues()

    assert topic.get() == []

    alert.set(True)
    SmartDashboard.updateValues()

    assert topic.get() == ["Test3"]


def test_alert_sort(robot_controller: RobotTestController):
    """
    Alerts should be sorted from the most recent to the oldest shown.
    """

    topic = (
        NetworkTableInstance.getDefault()
        .getStringArrayTopic("/SmartDashboard/AlertGroup/warnings")
        .subscribe(["default"])
    )

    SmartDashboard.updateValues()
    recent = Alert("Recent", AlertType.Warning, "AlertGroup", prefix="[P] ")
    oldest = Alert("Oldest", AlertType.Warning, "AlertGroup", prefix="[P] ")

    SmartDashboard.updateValues()
    assert topic.get() == []

    oldest.set(True)
    SmartDashboard.updateValues()
    assert topic.get() == ["[P] Oldest"]

    recent.set(True)
    SmartDashboard.updateValues()
    assert topic.get() == ["[P] Recent", "[P] Oldest"]

    oldest.setText("Oldest modified")
    SmartDashboard.updateValues()
    assert topic.get() == ["[P] Oldest modified", "[P] Recent"]
