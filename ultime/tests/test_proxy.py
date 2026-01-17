import pytest

from ultime.proxy import proxy


class A:
    def b(self):
        return "b"


def test_proxy_object():
    a = A()
    weak = proxy(a)

    assert weak.b() == "b"

    del a
    with pytest.raises(ReferenceError):
        weak.b()


def test_proxy_function():
    def func():
        return "func"

    weak = proxy(func)
    assert weak() == "func"

    del func

    with pytest.raises(ReferenceError):
        weak()


def test_proxy_method():
    a = A()
    weak = proxy(a.b)
    assert weak() == "b"

    del a
    with pytest.raises(ReferenceError):
        weak()
