from ultime.timethis import timethis_enabled


def test_timethis_disabled():
    assert not timethis_enabled
