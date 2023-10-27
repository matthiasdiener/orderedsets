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


def test_speed_init():
    s_time = timeit("set(range(1000))", number=10000)

    os_time = timeit("OrderedSet(range(1000))",
                     setup="from orderedsets import OrderedSet", number=10000)

    fos_time = timeit("FrozenOrderedSet(range(1000))",
                      setup="from orderedsets import FrozenOrderedSet", number=10000)

    print(s_time)
    print(os_time)
    print(fos_time)

    assert os_time < 2.1 * s_time
    assert fos_time < 2.6 * s_time


def test_speed_hash():
    fs_time = timeit("hash(s)", setup="s = frozenset(range(1000))", number=10000)

    fos_time = timeit("hash(s)",
                      setup="from orderedsets import FrozenOrderedSet;\
                             s = FrozenOrderedSet(range(1000))", number=10000)

    print(fs_time)
    print(fos_time)

    assert fos_time < 5 * fs_time


def test_speed_len():
    fs_time = timeit(
        "len(s)", setup="s = set(range(1000))", number=10000)

    fos_time = timeit(
        "len(s)", setup="from orderedsets import OrderedSet;\
                         s = OrderedSet(range(1000))", number=10000)

    print(fs_time)
    print(fos_time)

    assert fos_time < 5 * fs_time


def test_speed_union():
    fs_time = timeit(
        "set(range(1000)).union(set(range(1001)))", number=10000)

    fos_time = timeit(
        "OrderedSet(range(1000)).union(OrderedSet(range(1001)))",
        setup="from orderedsets import OrderedSet", number=10000)

    print(fs_time)
    print(fos_time)

    assert fos_time < 3 * fs_time
