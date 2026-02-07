import pytest

from ultime.switch import Switch


# port 30 is max we can put so it doesn't interfere with robot
def test_normallyOpened():
    switch = Switch(Switch.Type.NormallyOpen, 30)
    switch.setSimValue(True)
    assert switch.isPressed()
    assert switch._input.get()
    switch.setSimValue(False)
    assert not switch.isPressed()
    assert not switch._input.get()


def test_normallyClosed():
    switch = Switch(Switch.Type.NormallyClosed, 30)
    switch.setSimValue(True)
    assert switch.isPressed()
    assert not switch._input.get()
    switch.setSimValue(False)
    assert not switch.isPressed()
    assert switch._input.get()


def test_alwaysPressed():
    switch = Switch(Switch.Type.AlwaysPressed)
    switch.setSimValue(True)
    assert switch.isPressed()
    switch.setSimValue(False)
    assert not switch.isPressed()


def test_alwaysUnPressed():
    switch = Switch(Switch.Type.AlwaysUnpressed)
    switch.setSimValue(True)
    assert switch.isPressed()
    switch.setSimValue(False)
    assert not switch.isPressed()


def test_TypeError():
    with pytest.raises(TypeError):
        Switch(1, 3)
