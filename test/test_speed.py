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
from orderedsets import FrozenOrderedSet, OrderedSet


def test_speed_init():
    fz_time = timeit("frozenset(range(1000))", setup="s = ", number=10000)

    fos_time = timeit("FrozenOrderedSet(range(1000))", setup="from orderedsets import FrozenOrderedSet; s = ", number=10000)

    print(fz_time)
    print(fos_time)


def test_speed_hash():
    # setup =

    fz_time = timeit("hash(s)", setup="s = frozenset(range(1000))", number=10000)

    fos_time = timeit("hash(s)", setup="from orderedsets import FrozenOrderedSet; s = FrozenOrderedSet(range(1000))", number=10000)



    print(fz_time)
    print(fos_time)
