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


from typing import AbstractSet, FrozenSet, Set, Type, TypeVar, Union

import pytest

from orderedsets import FrozenOrderedSet, OrderedSet

T = TypeVar("T")

set_types = (OrderedSet, FrozenOrderedSet, set, frozenset)
ordered_set_types = (OrderedSet, FrozenOrderedSet)
mutable_set_types = (OrderedSet, set)
immutable_set_types = (FrozenOrderedSet, frozenset)

T_set = Union[Type[OrderedSet[T]], Type[FrozenOrderedSet[T]],
              Type[Set[T]], Type[FrozenSet[T]]]
T_ordered_set = Union[Type[OrderedSet[T]], Type[FrozenOrderedSet[T]]]
T_mutable_set = Union[Type[OrderedSet[T]], Type[Set[T]]]
T_immutable_set = Union[Type[FrozenOrderedSet[T]], Type[FrozenSet[T]]]

all_set_types = pytest.mark.parametrize("_cls", set_types)
all_ordered_set_types = pytest.mark.parametrize("_cls", ordered_set_types)
all_mutable_set_types = pytest.mark.parametrize("_cls", mutable_set_types)
all_immutable_set_types = pytest.mark.parametrize("_cls", immutable_set_types)


def f(s: AbstractSet[T]) -> AbstractSet[T]:
    return s


@all_set_types
def test_call_abstractset(_cls: T_set[int]) -> None:
    f(_cls([4, 1, 4, 1]))


@all_ordered_set_types
def test_simple_ordered(_cls: T_ordered_set[int]) -> None:
    s = _cls([4, 1, 4, 1])
    assert list(s) == [4, 1]


@all_ordered_set_types
def test_str_repr(_cls: T_ordered_set[int]) -> None:
    s = _cls([4, 1, 4, 1])
    assert repr(s) == str(s) == f"{_cls.__name__}({{4, 1}})"

    s = _cls()
    assert repr(s) == str(s) == f"{_cls.__name__}()"


@all_set_types
def test_len(_cls: T_set[int]) -> None:
    s = _cls([4, 1, 4, 1])
    assert len(s) == 2


@all_set_types
def test_in(_cls: T_set[int]) -> None:
    s = _cls([4, 1, 4, 1])
    assert 4 in s
    assert 2 not in s


@all_set_types
def test_eq(_cls: T_set[int]) -> None:
    s1 = _cls([4, 1, 4, 1])
    s2 = _cls([4, 4, 1])
    s3 = set([4, 1, 4, 1])  # noqa: C405
    assert s1 == s2
    assert s1 == s3
    assert s2 == s1
    assert s3 == s1
    assert s2 == s3 == s1

    s4 = _cls([4])
    assert s1 != s4

    assert s1 != [4, 1]
    if _cls in ordered_set_types:
        assert [4, 1] == list(s1)

    if _cls in immutable_set_types:
        assert hash(s1) == hash(s2)
        assert hash(s1) != hash(s4)


@all_set_types
def test_isdisjoint(_cls: T_set[int]) -> None:
    s1 = _cls([3, 1, 2])
    s2 = _cls([1, 7])
    assert not s1.isdisjoint(s2)

    s_3 = _cls([10, 7])
    assert s1.isdisjoint(s_3)


@all_immutable_set_types
def test_remove_discard_immutable(_cls: T_immutable_set[int]) -> None:
    s = _cls([4, 1, 4, 1])

    with pytest.raises(AttributeError):
        s.remove(17)  # type: ignore[union-attr]
    with pytest.raises(AttributeError):
        s.discard(17)  # type: ignore[union-attr]


@all_mutable_set_types
def test_remove_discard_mutable(_cls: T_mutable_set[int]) -> None:
    s = _cls([4, 1, 4, 1])

    with pytest.raises(KeyError):
        s.remove(17)
    s.discard(17)

    assert s == _cls([4, 1])

    s.remove(4)

    assert s == {1}


@all_immutable_set_types
def test_clear_immutable(_cls: T_immutable_set[int]) -> None:
    s = _cls([4, 1, 4, 1])

    with pytest.raises(AttributeError):
        s.clear()  # type: ignore[union-attr]


@all_mutable_set_types
def test_clear_mutable(_cls: T_mutable_set[int]) -> None:
    s = _cls([4, 1, 4, 1])

    s.clear()

    assert len(s) == 0
    assert s == _cls()


@all_set_types
def test_convert_to_set(_cls: T_set[int]) -> None:
    assert {1, 2, 3} == set(_cls([3, 1, 2]))


@all_ordered_set_types
def test_tolist(_cls: T_ordered_set[int]) -> None:
    assert [3, 1, 2] == list(_cls([3, 1, 2]))


@all_set_types
def test_hash(_cls: T_set[int]) -> None:
    s1 = _cls([4, 1, 4, 1])

    if _cls in mutable_set_types:
        with pytest.raises(TypeError):
            hash(s1)
    else:
        assert hash(s1)
        assert hash(s1) == hash(s1)

        s2 = _cls([4, 1, 4, 1])
        assert s1 == s2
        assert hash(s1) == hash(s2)

        s3 = _cls([4, 1, 4, 1, 5])
        assert s1 != s3
        assert hash(s1) != hash(s3)


def test_hash_value() -> None:
    fos = FrozenOrderedSet([1, 2, 3])
    fs = frozenset([1, 2, 3])

    assert fs == fos
    assert hash(fs) == hash(fos)

    fos2 = FrozenOrderedSet(["a", "b", "c"])
    fs2 = frozenset(["a", "b", "c"])

    assert fs2 == fos2
    assert hash(fs2) == hash(fos2)


@all_immutable_set_types
def test_update_immutable(_cls: T_immutable_set[int]) -> None:
    s = _cls([1, 6, 8])

    with pytest.raises(AttributeError):
        s.update([6])  # type: ignore[union-attr]


@all_mutable_set_types
def test_update_mutable(_cls: T_mutable_set[int]) -> None:
    s = _cls([1, 6, 8])

    if _cls in ordered_set_types:
        assert list(s) == [1, 6, 8]

    s.update(range(10, 100000))
    for v in range(10, 100000):
        s.remove(v)

    if _cls in ordered_set_types:
        assert list(s) == [1, 6, 8]

    assert len(s) == 3
    assert s == {1, 6, 8}


@all_set_types
def test_intersection(_cls: T_set[int]) -> None:
    s1 = _cls([3, 1, 2])
    s2 = _cls([1, 7])
    assert _cls([1]) == s1.intersection(s2)
    assert s1 == s1.intersection(s1)


@all_immutable_set_types
def test_intersection_update_immutable(_cls: T_immutable_set[int]) -> None:
    s1 = _cls([3, 1, 2])
    s2 = _cls([1, 7])

    with pytest.raises(AttributeError):
        s1.intersection_update(s2)  # type: ignore[union-attr]


@all_mutable_set_types
def test_intersection_update_mutable(_cls: T_mutable_set[int]) -> None:
    s1 = _cls([3, 1, 2])
    s2 = _cls([1, 7])

    s1.intersection_update(s2)
    assert _cls([1]) == s1


@all_immutable_set_types
def test_add_immutable(_cls: T_immutable_set[int]) -> None:
    s = _cls([3, 1, 2])

    with pytest.raises(AttributeError):
        s.add(0)  # type: ignore[union-attr]


@all_mutable_set_types
def test_add_mutable(_cls: T_mutable_set[int]) -> None:
    s = _cls([3, 1, 2])

    s.add(0)
    assert _cls([3, 1, 2, 0]) == s


@all_set_types
def test_copy(_cls: T_set[int]) -> None:
    s1 = _cls([3, 1, 2])
    s2 = s1.copy()
    assert s1 == s2

    if not isinstance(s1, frozenset):
        assert s1 is not s2


@all_set_types
def test_difference(_cls: T_set[int]) -> None:
    s1 = _cls([3, 1, 2])
    s2 = _cls([1, 7])
    assert _cls([3, 2]) == s1.difference(s2)
    assert s1.difference(s1) == _cls()


@all_immutable_set_types
def test_difference_update_immutable(_cls: T_immutable_set[int]) -> None:
    s1 = _cls([3, 1, 2])
    s2 = _cls([1, 7])

    with pytest.raises(AttributeError):
        s1.difference_update(s2)  # type: ignore[union-attr]


@all_mutable_set_types
def test_difference_update_mutable(_cls: T_mutable_set[int]) -> None:
    s1 = _cls([3, 1, 2])
    s2 = _cls([1, 7])

    s1.difference_update(s2)
    assert _cls([3, 2]) == s1


@all_set_types
def test_symmetric_difference(_cls: T_set[int]) -> None:
    s1 = _cls([3, 1, 2])
    s2 = _cls([1, 7])
    assert _cls([3, 2, 7]) == s1.symmetric_difference(s2)


@all_immutable_set_types
def test_symmetric_difference_update_immutable(_cls: T_immutable_set[int]) -> None:
    s1 = _cls([3, 1, 2])
    s2 = _cls([1, 7])

    with pytest.raises(AttributeError):
        s1.symmetric_difference_update(s2)  # type: ignore[union-attr]


@all_mutable_set_types
def test_symmetric_difference_update(_cls: T_mutable_set[int]) -> None:
    s1 = _cls([3, 1, 2])
    s2 = _cls([1, 7])

    s1.symmetric_difference_update(s2)
    assert _cls([3, 2, 7]) == s1


@all_set_types
def test_union(_cls: T_set[int]) -> None:
    s1 = _cls([3, 1, 2])
    s2 = _cls([1, 7])
    s3 = _cls([42])
    assert _cls([1, 3, 2, 7]) == s1.union(s2)
    assert _cls([1, 3, 2, 42]) == s1.union(s3)


@all_set_types
def test_op_and(_cls: T_set[int]) -> None:
    s1 = _cls([3, 1, 2])
    s2 = _cls([1, 7])
    s3 = _cls([42])
    assert _cls([1]) == s1 & s2
    assert _cls() == s1 & s3


@all_set_types
def test_op_iand(_cls: T_set[int]) -> None:
    s1 = _cls([3, 1, 2])
    s2 = _cls([1, 7])
    s3 = _cls([42])
    s1 &= s2
    assert _cls([1]) == s1
    s1 &= s3
    assert _cls() == s1


@all_set_types
def test_op_or(_cls: T_set[int]) -> None:
    s1 = _cls([3, 1, 2])
    s2 = _cls([1, 7])
    s3 = _cls([42])
    assert _cls([1, 3, 2, 7]) == s1 | s2
    assert _cls([1, 3, 2, 42]) == s1 | s3


@all_set_types
def test_op_ior(_cls: T_set[int]) -> None:
    s1 = _cls([3, 1, 2])
    s2 = _cls([1, 7])
    s3 = _cls([42])
    s1 |= s2
    assert _cls([1, 3, 2, 7]) == s1
    if _cls in ordered_set_types:
        assert [3, 1, 2, 7] == list(s1)
    s1 |= s3
    assert _cls([1, 3, 2, 7, 42]) == s1


@all_set_types
def test_op_sub(_cls: T_set[int]) -> None:
    s1 = _cls([3, 1, 2])
    s2 = _cls([1, 7])
    s3 = _cls([42])
    assert _cls([3, 2]) == s1 - s2
    assert _cls([3, 1, 2]) == s1 - s3


@all_set_types
def test_op_isub(_cls: T_set[int]) -> None:
    s1 = _cls([3, 1, 2])
    s2 = _cls([1, 7])
    s3 = _cls([42])
    s1 -= s2
    assert _cls([3, 2]) == s1
    if _cls in ordered_set_types:
        assert [3, 2] == list(s1)
    s1 -= s3
    assert _cls([3, 2]) == s1


@all_set_types
def test_op_xor(_cls: T_set[int]) -> None:
    s1 = _cls([3, 1, 2])
    s2 = _cls([1, 7])
    s3 = _cls([42])
    assert _cls([3, 2, 7]) == s1 ^ s2
    assert _cls([3, 1, 2, 42]) == s1 ^ s3


@all_set_types
def test_op_ixor(_cls: T_set[int]) -> None:
    s1 = _cls([3, 1, 2])
    s2 = _cls([1, 7])
    s3 = _cls([42])
    s1 ^= s2
    assert _cls([3, 2, 7]) == s1
    if _cls in ordered_set_types:
        assert [3, 2, 7] == list(s1)
    s1 ^= s3
    assert _cls([3, 2, 7, 42]) == s1


@all_set_types
def test_issubset(_cls: T_set[int]) -> None:
    s1 = _cls([3, 1, 2])
    s2 = _cls([1, 7])
    assert not s2.issubset(s1)
    assert _cls().issubset(s1)

    if _cls in mutable_set_types:
        s2.discard(7)  # type: ignore[union-attr]
        assert s2.issubset(s1)


@all_set_types
def test_issuperset(_cls: T_set[int]) -> None:
    s1 = _cls([3, 1, 2])
    s2 = _cls([1, 7])
    assert not s1.issuperset(s2)

    if _cls in mutable_set_types:
        s2.discard(7)  # type: ignore[union-attr]
        assert s1.issuperset(s2)
        assert _cls(s1).issuperset(s2)


@all_immutable_set_types
def test_pop_immutable(_cls: T_immutable_set[int]) -> None:
    s1 = _cls([3, 1, 2])

    with pytest.raises(AttributeError):
        s1.pop()  # type: ignore[union-attr]


@all_mutable_set_types
def test_pop_mutable(_cls: T_mutable_set[int]) -> None:
    s1 = _cls([3, 1, 2])

    p = s1.pop()
    assert len(s1) == 2

    if _cls in ordered_set_types:
        assert p == 2
        assert _cls([3, 1]) == s1


@all_set_types
def test_op_le(_cls: T_set[int]) -> None:
    s1 = _cls([3, 1, 2])
    s2 = _cls([1, 7])
    assert not (s2 <= s1)
    s3 = _cls([1, 2])
    assert s3 <= s1
    assert not s2.issubset(s1)


@all_set_types
def test_op_lt(_cls: T_set[int]) -> None:
    s1 = _cls([3, 1, 2])
    s2 = _cls([1, 7])
    assert not (s2 < s1)
    s3 = _cls([1, 2])
    assert s3 < s1
    assert not s2.issubset(s1)


@all_set_types
def test_op_ge(_cls: T_set[int]) -> None:
    s1 = _cls([3, 1, 2])
    s2 = _cls([1, 7])
    assert not (s2 >= s1)
    s3 = _cls([1, 2])
    assert s1 >= s3
    assert not s2.issubset(s1)


@all_set_types
def test_op_gt(_cls: T_set[int]) -> None:
    s1 = _cls([3, 1, 2])
    s2 = _cls([1, 7])
    assert not (s2 > s1)
    s3 = _cls([1, 2])
    assert s1 > s3
    assert not s2.issubset(s1)


@all_set_types
def test_bool(_cls: T_set[int]) -> None:
    assert not _cls()
    assert _cls([1])
    assert not bool(_cls())
    assert bool(_cls([1]))


@all_set_types
def test_ordering(_cls: T_set[int]) -> None:
    # Based on https://github.com/simonpercivall/orderedset/pull/22
    lst = list(range(10))

    oset1 = _cls(lst)
    oset2 = _cls(lst)

    assert oset2 <= oset1
    assert oset2 <= set(oset1)
    # assert oset2 <= list(oset1)
    assert oset1 >= oset2
    assert oset1 >= set(oset2)
    # assert oset1 >= list(oset2)

    oset3 = _cls(lst[:-1])

    assert oset3 < oset1
    assert oset3 < set(oset1)
    # assert oset3 < list(oset1)

    assert oset1 > oset3
    assert oset1 > set(oset3)
    # assert oset1 > list(oset3)

    oset4 = _cls(lst[1:])

    assert not (oset3 < oset4)
    assert not (oset3 < set(oset4))
    # assert not (oset3 < list(oset4))
    assert not (oset3 >= oset4)
    assert not (oset3 >= set(oset4))
    # assert not (oset3 >= list(oset4))
    assert not (oset3 < oset4)
    assert not (oset3 < set(oset4))
    # assert not (oset3 < list(oset4))
    assert not (oset3 >= oset4)
    assert not (oset3 >= set(oset4))
    # assert not (oset3 >= list(oset4))
