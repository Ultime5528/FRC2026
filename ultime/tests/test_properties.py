from ultime.autoproperty import mode, PropertyMode


def test_local_mode():
    assert mode == PropertyMode.Local
