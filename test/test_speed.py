__copyright__ = """
Copyright (C) 2023 University of Illinois Board of Trustees
"""


__license__ = """
Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""


from timeit import timeit

import pytest


@pytest.mark.parametrize(
    "statement, setup, max_slowdown_factor, skip_mutable, skip_immutable",
    [
        ("set(range(1000))", "", 3, False, False),  # init
        ("hash(s)", "s = set(range(1000))", 13, True, False),  # hash
        ("len(s)", "s = set(range(1000))", 13, False, False),  # len
        ("set(range(1000)).union(set(range(1001)))", "", 12, False, False),  # union
        ("for e in s: pass", "s = set(range(1000))", 1.5, False, False),  # iter
        ("for i in range(1000): i in s", "s = set(range(500))", 15, False, False),  # contains  # noqa: E501
        ("for i in range(1000): s.discard(10011)", "s = set(range(500))", 12, False, True),  # discard  # noqa: E501
    ],
)
def test_speed(statement: str, setup: str, max_slowdown_factor: float,
               skip_mutable: bool, skip_immutable: bool) -> None:

    import platform
    if platform.python_implementation() == "PyPy":
        pytest.skip("Testing this against PyPy is not meaningful at the moment.")

    if not skip_mutable:
        s_time = timeit(statement, setup=setup, number=10000)
        os_time = timeit(statement,
                         setup="from orderedsets import OrderedSet as set;" + setup,
                         number=10000)
        print(f"{statement} {s_time} {os_time}")

        assert os_time < max_slowdown_factor * s_time

    if not skip_immutable:
        fs_time = timeit(statement, setup="set=frozenset;" + setup, number=10000)

        fos_time = timeit(statement,
                          setup="from orderedsets import FrozenOrderedSet as set;"
                          + setup,
                          number=10000)

        print(f"{statement} {fs_time} {fos_time}")

        assert fos_time < max_slowdown_factor * fs_time
