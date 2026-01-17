from collections import defaultdict

import ultime.cache as cache
from ultime.cache import cache_every_loop


def test_cache_every_loop():
    class Demo:
        def __init__(self):
            self.a_calls = 0
            self.a_return = "a1"
            self.b_calls = 0
            self.b_return = "b1"

        @cache_every_loop
        def a(self):
            self.a_calls += 1
            return self.a_return

        @cache_every_loop
        def b(self):
            self.b_calls += 1
            return self.b_return

    demo = Demo()

    assert demo.a() == "a1"
    assert demo.a_calls == 1

    demo.a_return = "a2"

    for _ in range(10):
        assert demo.a() == "a1"
        assert demo.a_calls == 1
        assert demo.b() == "b1"
        assert demo.b_calls == 1

    cache.clear_loop_cache()

    for _ in range(10):
        assert demo.a() == "a2"
        assert demo.a_calls == 2
        assert demo.b() == "b1"
        assert demo.b_calls == 2


def test_cache_different_intervals():
    # Reset cached value list for deterministic results
    # Robot is always created and adds values in the cache, if used
    cache.cached_values = defaultdict(list)

    class Demo:
        def __init__(self):
            self.loop_1_1_calls = 0
            self.loop_1_2_calls = 0
            self.loop_2_1_calls = 0
            self.loop_2_2_calls = 0
            self.loop_2_3_calls = 0
            self.loop_2_4_calls = 0
            self.loop_3_1_calls = 0
            self.loop_3_2_calls = 0
            self.loop_3_3_calls = 0
            self.loop_3_4_calls = 0
            self.loop_3_5_calls = 0
            self.loop_3_6_calls = 0
            self.loop_3_7_calls = 0
            self.return_value = 1

        @cache_every_loop
        def loop_1_1(self):
            self.loop_1_1_calls += 1
            return "loop_1_1=" + str(self.return_value)

        @cache_every_loop(1)
        def loop_1_2(self):
            self.loop_1_2_calls += 1
            return "loop_1_2=" + str(self.return_value)

        @cache_every_loop(2)
        def loop_2_1(self):
            self.loop_2_1_calls += 1
            return "loop_2_1=" + str(self.return_value)

        @cache_every_loop(2)
        def loop_2_2(self):
            self.loop_2_2_calls += 1
            return "loop_2_2=" + str(self.return_value)

        @cache_every_loop(2)
        def loop_2_3(self):
            self.loop_2_3_calls += 1
            return "loop_2_3=" + str(self.return_value)

        @cache_every_loop(2)
        def loop_2_4(self):
            self.loop_2_4_calls += 1
            return "loop_2_4=" + str(self.return_value)

        @cache_every_loop(3)
        def loop_3_1(self):
            self.loop_3_1_calls += 1
            return "loop_3_1=" + str(self.return_value)

        @cache_every_loop(3)
        def loop_3_2(self):
            self.loop_3_2_calls += 1
            return "loop_3_2=" + str(self.return_value)

        @cache_every_loop(3)
        def loop_3_3(self):
            self.loop_3_3_calls += 1
            return "loop_3_3=" + str(self.return_value)

        @cache_every_loop(3)
        def loop_3_4(self):
            self.loop_3_4_calls += 1
            return "loop_3_4=" + str(self.return_value)

        @cache_every_loop(3)
        def loop_3_5(self):
            self.loop_3_5_calls += 1
            return "loop_3_5=" + str(self.return_value)

        @cache_every_loop(3)
        def loop_3_6(self):
            self.loop_3_6_calls += 1
            return "loop_3_6=" + str(self.return_value)

        @cache_every_loop(3)
        def loop_3_7(self):
            self.loop_3_7_calls += 1
            return "loop_3_7=" + str(self.return_value)

        def get_calls(self):
            return [
                self.loop_1_1_calls,
                self.loop_1_2_calls,
                self.loop_2_1_calls,
                self.loop_2_2_calls,
                self.loop_2_3_calls,
                self.loop_2_4_calls,
                self.loop_3_1_calls,
                self.loop_3_2_calls,
                self.loop_3_3_calls,
                self.loop_3_4_calls,
                self.loop_3_5_calls,
                self.loop_3_6_calls,
                self.loop_3_7_calls,
            ]

    demo = Demo()

    for _ in range(10):
        assert demo.loop_1_1() == "loop_1_1=1"
        assert demo.loop_1_2() == "loop_1_2=1"
        assert demo.loop_2_1() == "loop_2_1=1"
        assert demo.loop_2_2() == "loop_2_2=1"
        assert demo.loop_2_3() == "loop_2_3=1"
        assert demo.loop_2_4() == "loop_2_4=1"
        assert demo.loop_3_1() == "loop_3_1=1"
        assert demo.loop_3_2() == "loop_3_2=1"
        assert demo.loop_3_3() == "loop_3_3=1"
        assert demo.loop_3_4() == "loop_3_4=1"
        assert demo.loop_3_5() == "loop_3_5=1"
        assert demo.loop_3_6() == "loop_3_6=1"
        assert demo.loop_3_7() == "loop_3_7=1"
        assert demo.get_calls() == [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]

    demo.return_value = 2
    cache.clear_loop_cache()

    for _ in range(10):
        assert demo.loop_1_1() == "loop_1_1=2"
        assert demo.loop_1_2() == "loop_1_2=2"
        assert demo.loop_2_1() == "loop_2_1=2"
        assert demo.loop_2_2() == "loop_2_2=1"
        assert demo.loop_2_3() == "loop_2_3=2"
        assert demo.loop_2_4() == "loop_2_4=1"
        assert demo.loop_3_1() == "loop_3_1=2"
        assert demo.loop_3_2() == "loop_3_2=1"
        assert demo.loop_3_3() == "loop_3_3=1"
        assert demo.loop_3_4() == "loop_3_4=2"
        assert demo.loop_3_5() == "loop_3_5=1"
        assert demo.loop_3_6() == "loop_3_6=1"
        assert demo.loop_3_7() == "loop_3_7=2"

        assert demo.get_calls() == [2, 2, 2, 1, 2, 1, 2, 1, 1, 2, 1, 1, 2]

    demo.return_value = 3
    cache.clear_loop_cache()

    for _ in range(10):
        assert demo.loop_1_1() == "loop_1_1=3"
        assert demo.loop_1_2() == "loop_1_2=3"
        assert demo.loop_2_1() == "loop_2_1=2"
        assert demo.loop_2_2() == "loop_2_2=3"
        assert demo.loop_2_3() == "loop_2_3=2"
        assert demo.loop_2_4() == "loop_2_4=3"
        assert demo.loop_3_1() == "loop_3_1=2"
        assert demo.loop_3_2() == "loop_3_2=3"
        assert demo.loop_3_3() == "loop_3_3=1"
        assert demo.loop_3_4() == "loop_3_4=2"
        assert demo.loop_3_5() == "loop_3_5=3"
        assert demo.loop_3_6() == "loop_3_6=1"
        assert demo.loop_3_7() == "loop_3_7=2"

        assert demo.get_calls() == [3, 3, 2, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2]

    demo.return_value = 4
    cache.clear_loop_cache()

    for _ in range(10):
        assert demo.loop_1_1() == "loop_1_1=4"
        assert demo.loop_1_2() == "loop_1_2=4"
        assert demo.loop_2_1() == "loop_2_1=4"
        assert demo.loop_2_2() == "loop_2_2=3"
        assert demo.loop_2_3() == "loop_2_3=4"
        assert demo.loop_2_4() == "loop_2_4=3"
        assert demo.loop_3_1() == "loop_3_1=2"
        assert demo.loop_3_2() == "loop_3_2=3"
        assert demo.loop_3_3() == "loop_3_3=4"
        assert demo.loop_3_4() == "loop_3_4=2"
        assert demo.loop_3_5() == "loop_3_5=3"
        assert demo.loop_3_6() == "loop_3_6=4"
        assert demo.loop_3_7() == "loop_3_7=2"

        assert demo.get_calls() == [4, 4, 3, 2, 3, 2, 2, 2, 2, 2, 2, 2, 2]

    demo.return_value = 5
    cache.clear_loop_cache()

    for _ in range(10):
        assert demo.loop_1_1() == "loop_1_1=5"
        assert demo.loop_1_2() == "loop_1_2=5"
        assert demo.loop_2_1() == "loop_2_1=4"
        assert demo.loop_2_2() == "loop_2_2=5"
        assert demo.loop_2_3() == "loop_2_3=4"
        assert demo.loop_2_4() == "loop_2_4=5"
        assert demo.loop_3_1() == "loop_3_1=5"
        assert demo.loop_3_2() == "loop_3_2=3"
        assert demo.loop_3_3() == "loop_3_3=4"
        assert demo.loop_3_4() == "loop_3_4=5"
        assert demo.loop_3_5() == "loop_3_5=3"
        assert demo.loop_3_6() == "loop_3_6=4"
        assert demo.loop_3_7() == "loop_3_7=5"

        assert demo.get_calls() == [5, 5, 3, 3, 3, 3, 3, 2, 2, 3, 2, 2, 3]
