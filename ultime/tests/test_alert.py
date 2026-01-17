from ntcore import NetworkTableInstance

from ultime.alert import AlertType, Alert
from ultime.tests.utils import RobotTestController


def test_alert(robot_controller: RobotTestController):
    topic = (
        NetworkTableInstance.getDefault()
        .getStringArrayTopic("/SmartDashboard/Alerts/errors")
        .subscribe(["default"])
    )
    alert = Alert("Test", AlertType.Error)

    robot_controller.wait(0.1)

    assert topic.get() == []

    alert.set(True)
    robot_controller.wait(0.1)

    assert topic.get() == ["Test"]

    alert.setText("Test2")
    robot_controller.wait(0.1)

    assert topic.get() == ["Test2"]

    alert.set(False)
    robot_controller.wait(0.1)

    assert topic.get() == []

    alert.setText("Test3")
    robot_controller.wait(0.1)

    assert topic.get() == []

    alert.set(True)
    robot_controller.wait(0.1)

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

    robot_controller.wait(0.1)
    recent = Alert("Recent", AlertType.Warning, "AlertGroup")
    oldest = Alert("Oldest", AlertType.Warning, "AlertGroup")

    robot_controller.wait(0.1)
    assert topic.get() == []

    oldest.set(True)
    robot_controller.wait(0.1)
    assert topic.get() == ["Oldest"]

    recent.set(True)
    robot_controller.wait(0.1)
    assert topic.get() == ["Recent", "Oldest"]

    oldest.setText("Oldest modified")
    robot_controller.wait(0.1)
    assert topic.get() == ["Recent", "Oldest modified"]
