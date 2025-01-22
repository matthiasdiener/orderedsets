__copyright__ = """
Copyright (C) 2025 University of Illinois Board of Trustees
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

from typing import Type, TypeVar, Union

import pytest

from orderedsets import FrozenIndexSet, IndexSet

T = TypeVar("T")

set_types = (IndexSet, FrozenIndexSet)
T_set = Union[Type[IndexSet[T]], Type[FrozenIndexSet[T]]]


@pytest.mark.parametrize("cls", set_types)
def test_indexset(cls: T_set[str]) -> None:
    input_list = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j"]
    iset = cls(input_list)

    assert iset[0] == "a" == input_list[0]
    assert iset[1] == "b" == input_list[1]
    assert iset[-1] == "j" == input_list[-1]
    assert iset[-2] == "i" == input_list[-2]

    # {{{ Check for correct int indexing

    assert iset[len(iset) - 1] == "j" == input_list[len(input_list) - 1]

    with pytest.raises(IndexError):
        iset[10]

    with pytest.raises(IndexError):
        iset[len(iset)]

    assert iset[-len(iset)] == "a" == input_list[-len(input_list)]

    with pytest.raises(IndexError):
        iset[-11]

    with pytest.raises(TypeError):
        iset["a"]  # type: ignore[index]

    # }}}

    # {{{ Check for correct slice indexing

    assert iset[0:2] == ["a", "b"] == input_list[0:2]
    assert iset[0:8:2] == ["a", "c", "e", "g"] == input_list[0:8:2]
    assert iset[0:8:3] == ["a", "d", "g"] == input_list[0:8:3]

    assert iset[-2:-8:-2] == ["i", "g", "e"] == input_list[-2:-8:-2]
    assert iset[-2:-8:-3] == ["i", "f"] == input_list[-2:-8:-3]

    # }}}
