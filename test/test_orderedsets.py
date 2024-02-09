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


from typing import (AbstractSet, Any, FrozenSet, Generator, Set, Type, TypeVar,
                    Union)

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


# Note: this file uses strings as test inputs for the most part, since
# strings exhibit the most non-determinism when using sets, as long as
# the PYTHONHASHSEED environment variable is not set.


def _char_range() -> Generator[str, None, None]:
    import string
    for c in string.ascii_lowercase + string.ascii_uppercase:
        yield c


def f(s: AbstractSet[T]) -> AbstractSet[T]:
    return s


def test_no_PYTHONHASHSEED() -> None:  # noqa: N802
    import os
    if "PYTHONHASHSEED" in os.environ:
        val = os.environ["PYTHONHASHSEED"]
        assert val == "random", \
            "PYTHONHASHSEED must not be set (or set to 'random') for these tests"


@all_set_types
def test_init(_cls: T_set[str]) -> None:
    # Simple init
    s = _cls(["d", "a", "d", "a"])
    assert len(s) == 2
    assert s == {"d", "a"}

    # Empty init
    s = _cls()
    assert s == set()

    s = _cls([])
    assert s == set()
    s = _cls(())
    assert s == set()
    s = _cls({})
    assert s == set()

    # Invalid single-item init
    with pytest.raises(TypeError):
        s = _cls(None)  # type: ignore[arg-type,call-overload]

    with pytest.raises(TypeError):
        s = _cls(42)  # type: ignore[arg-type,call-overload]

    # String is iterable, so this should pass
    s = _cls("d")
    assert s == {"d"}

    # Invalid multi-item init
    with pytest.raises(TypeError):
        s = _cls("a", "b")  # type: ignore[call-overload,call-arg]

    with pytest.raises(TypeError):
        s = _cls([], [])  # type: ignore[call-overload,call-arg]


@all_set_types
def test_call_abstractset(_cls: T_set[str]) -> None:
    f(_cls(["d", "a", "d", "a"]))


@all_ordered_set_types
def test_simple_ordered(_cls: T_ordered_set[str]) -> None:
    s = _cls(["d", "a", "d", "a"])
    assert list(s) == ["d", "a"]


@all_set_types
def test_str_repr(_cls: T_set[Any]) -> None:
    cls_name = "" if _cls == set else _cls.__name__ + "("
    end = "" if _cls == set else ")"

    s = _cls([1])
    print(repr(s), str(s), cls_name + "{'d'}" + end)
    assert repr(s) == str(s) == cls_name + "{1}" + end

    s = _cls(["d"])
    assert repr(s) == str(s) == cls_name + "{'d'}" + end

    s = _cls()
    assert repr(s) == str(s) \
        == "set()" if _cls == set else f"{cls_name}" + end

    if _cls in ordered_set_types:
        s = _cls([1, 4, 1, 4])
        assert repr(s) == str(s) == cls_name + "{1, 4}" + end

        s = _cls(["d", "a", "d", "a"])
        assert repr(s) == str(s) == cls_name + "{'d', 'a'}" + end

        s = _cls(["a", "d", "a", "d", "a"])
        assert repr(s) == str(s) == cls_name + "{'a', 'd'}" + end

        s = _cls()
        assert repr(s) == str(s) == f"{cls_name}" + end


@all_set_types
def test_len(_cls: T_set[str]) -> None:
    s = _cls(["d", "a", "d", "a"])
    assert len(s) == 2


@all_set_types
def test_in(_cls: T_set[str]) -> None:
    s = _cls(["d", "a", "d", "a"])
    assert "d" in s
    assert "b" not in s


@all_set_types
def test_eq(_cls: T_set[str]) -> None:
    s1 = _cls(["d", "a", "d", "a"])
    s2 = _cls(["d", "d", "a"])
    s3 = set(["d", "a", "d", "a"])  # noqa: C405
    assert s1 == s2
    assert s1 == s3
    assert s2 == s1
    assert s3 == s1
    assert s2 == s3 == s1

    s4 = _cls(["d"])
    assert s1 != s4

    assert s1 != ["d"]
    if _cls in ordered_set_types:
        assert ["d", "a"] == list(s1)

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
def test_remove_discard_immutable(_cls: T_immutable_set[str]) -> None:
    s = _cls(["d", "a", "d", "a"])

    with pytest.raises(AttributeError):
        s.remove(17)  # type: ignore[union-attr]
    with pytest.raises(AttributeError):
        s.discard(17)  # type: ignore[union-attr]


@all_mutable_set_types
def test_remove_discard_mutable(_cls: T_mutable_set[str]) -> None:
    s = _cls(["d", "a", "d", "a"])

    with pytest.raises(KeyError):
        s.remove("Y")
    s.discard("Y")

    assert s == _cls(["d", "a"])

    s.remove("d")

    assert s == {"a"}


@all_immutable_set_types
def test_clear_immutable(_cls: T_immutable_set[str]) -> None:
    s = _cls(["d", "a", "d", "a"])

    with pytest.raises(AttributeError):
        s.clear()  # type: ignore[union-attr]


@all_mutable_set_types
def test_clear_mutable(_cls: T_mutable_set[str]) -> None:
    s = _cls(["d", "a", "d", "a"])

    s.clear()

    assert len(s) == 0
    assert s == _cls()


@all_set_types
def test_convert_to_set(_cls: T_set[int]) -> None:
    assert {1, 2, 3} == set(_cls([3, 1, 2]))
    assert {1, 2, 3} == frozenset(_cls([3, 1, 2]))


@all_ordered_set_types
def test_tolist(_cls: T_ordered_set[str]) -> None:
    assert ["c", "a", "b"] == list(_cls(["c", "a", "b"]))


@all_set_types
def test_hash(_cls: T_set[Any]) -> None:
    s1 = _cls(["d", "a", "d", "a"])

    if _cls in mutable_set_types:
        with pytest.raises(TypeError):
            hash(s1)
    else:
        assert hash(s1)
        assert hash(s1) == hash(s1)

        s2 = _cls(["d", "a", "d", "a"])
        assert s1 == s2
        assert hash(s1) == hash(s2)

        s3 = _cls([4, 1, 4, 1, 5])
        assert s1 != s3
        assert hash(s1) != hash(s3)


def test_hash_value() -> None:
    fos: FrozenOrderedSet[int] = FrozenOrderedSet([1, 2, 3])
    fs = frozenset([1, 2, 3])

    assert fs == fos
    assert hash(fs) == hash(fos)

    fos2: FrozenOrderedSet[str] = FrozenOrderedSet(["a", "b", "c"])
    fs2 = frozenset(["a", "b", "c"])

    assert fs2 == fos2
    assert hash(fs2) == hash(fos2)


@all_immutable_set_types
def test_update_immutable(_cls: T_immutable_set[int]) -> None:
    s = _cls([1, 6, 8])

    with pytest.raises(AttributeError):
        s.update([6])  # type: ignore[union-attr]


@all_mutable_set_types
def test_update_mutable(_cls: T_mutable_set[Any]) -> None:
    s = _cls(["a", "f", "h"])

    if _cls in ordered_set_types:
        assert list(s) == ["a", "f", "h"]

    s.update(range(10, 100000))
    for v in range(10, 100000):
        s.remove(v)

    if _cls in ordered_set_types:
        assert list(s) == ["a", "f", "h"]

    assert len(s) == 3
    assert s == {"a", "f", "h"}


@all_set_types
def test_intersection(_cls: T_set[str]) -> None:
    s1 = _cls(["c", "a", "b"])
    s2 = _cls(["a", "g"])
    assert _cls(["a"]) == s1.intersection(s2)
    assert s1 == s1.intersection(s1)
    assert _cls(["a", "b"]) == s1.intersection(["a", "b"])

    if _cls in ordered_set_types:
        assert list(s1.intersection(["a", "b", "c"])) == ["c", "a", "b"]
        assert list(s1.intersection(["b", "a"])) == ["a", "b"]

    assert s1.intersection() == s1
    assert s1.intersection([]) == _cls()


@all_set_types
def test_intersection_multiple_args(_cls: T_set[str]) -> None:
    s1 = _cls(["c", "a", "b"])
    s2 = _cls(["a", "g"])
    assert _cls(["a"]) == s1.intersection(s2, s2)
    assert s1 == s1.intersection(s1, s1)

    if _cls in ordered_set_types:
        assert list(s1.intersection(["a", "b", "c"], ["a", "b", "c"], s1)) \
            == ["c", "a", "b"]


@all_immutable_set_types
def test_intersection_update_immutable(_cls: T_immutable_set[int]) -> None:
    s1 = _cls([3, 1, 2])
    s2 = _cls([1, 7])

    with pytest.raises(AttributeError):
        s1.intersection_update(s2)  # type: ignore[union-attr]


@all_mutable_set_types
def test_intersection_update_mutable(_cls: T_mutable_set[str]) -> None:
    s1 = _cls(["c", "a", "b"])
    s2 = _cls(["a", "g"])

    s1.intersection_update(s2)
    assert _cls(["a"]) == s1

    s1.intersection_update()
    assert _cls(["a"]) == s1

    s1.intersection_update([])
    assert _cls() == s1

    if _cls in ordered_set_types:
        s3 = _cls(["c", "a", "b"])
        s3.intersection_update(["b", "a"])
        s3.intersection_update({"b", "a"})
        assert list(s3) == ["a", "b"]


@all_immutable_set_types
def test_add_immutable(_cls: T_immutable_set[int]) -> None:
    s = _cls([3, 1, 2])

    with pytest.raises(AttributeError):
        s.add(0)  # type: ignore[union-attr]


@all_mutable_set_types
def test_add_mutable(_cls: T_mutable_set[str]) -> None:
    s = _cls(["c", "a", "b"])

    s.add("z")
    assert _cls(["c", "a", "b", "z"]) == s
    if _cls in ordered_set_types:
        assert list(s) == ["c", "a", "b", "z"]


@all_set_types
def test_copy(_cls: T_set[str]) -> None:
    s1 = _cls(["c", "a", "b"])
    s2 = s1.copy()
    assert s1 == s2

    if not isinstance(s1, frozenset):
        assert s1 is not s2

    if _cls in ordered_set_types:
        assert list(s1) == list(s2) == ["c", "a", "b"]


@all_set_types
def test_difference(_cls: T_set[str]) -> None:
    s1 = _cls(["c", "a", "b"])
    s2 = _cls(["a", "g"])
    assert _cls(["c", "b"]) == s1.difference(s2)
    assert s1.difference(s1) == _cls()
    assert s1.difference() == s1
    assert s1.difference(["a", "b", "c"]) == _cls()
    assert s1.difference(["b"], ["c"]) == _cls(["a"])

    if _cls in ordered_set_types:
        s3 = _cls(_char_range())
        s3 = s3.difference(["a"])
        s3_res = list(_char_range())
        s3_res.remove("a")
        assert list(s3) == s3_res

        s3 = _cls(_char_range())
        s3 = s3.difference(["b"], ["Y"])
        s3_res = list(_char_range())
        s3_res.remove("b")
        s3_res.remove("Y")
        assert list(s3) == s3_res


@all_set_types
def test_difference_multiple_args(_cls: T_set[str]) -> None:
    s1 = _cls(["c", "a", "b"])
    s2 = _cls(["a", "g"])
    assert _cls(["c", "b"]) == s1.difference(s2, s2)
    assert s1.difference(s1, s1) == _cls()

    if _cls in ordered_set_types:
        s3 = _cls(_char_range())
        s3 = s3.difference(["a"], ["b", "c"], ["Z", "Y"])
        s3_res = list(_char_range())
        s3_res.remove("a")
        s3_res.remove("b")
        s3_res.remove("c")
        s3_res.remove("Y")
        s3_res.remove("Z")
        assert list(s3) == s3_res


@all_immutable_set_types
def test_difference_update_immutable(_cls: T_immutable_set[int]) -> None:
    s1 = _cls([3, 1, 2])
    s2 = _cls([1, 7])

    with pytest.raises(AttributeError):
        s1.difference_update(s2)  # type: ignore[union-attr]


@all_mutable_set_types
def test_difference_update_mutable(_cls: T_mutable_set[str]) -> None:
    s1 = _cls(["c", "a", "b"])
    s2 = _cls(["a", "g"])

    s1.difference_update(s2)
    assert _cls(["c", "b"]) == s1

    if _cls in ordered_set_types:
        assert list(s1) == ["c", "b"]


@all_set_types
def test_symmetric_difference(_cls: T_set[str]) -> None:
    s1 = _cls(["c", "a", "b"])
    s2 = _cls(["a", "g"])
    assert _cls(["c", "b", "g"]) == s1.symmetric_difference(s2)

    if _cls in ordered_set_types:
        assert list(s1.symmetric_difference(s2)) == ["c", "b", "g"]


@all_immutable_set_types
def test_symmetric_difference_update_immutable(_cls: T_immutable_set[int]) -> None:
    s1 = _cls([3, 1, 2])
    s2 = _cls([1, 7])

    with pytest.raises(AttributeError):
        s1.symmetric_difference_update(s2)  # type: ignore[union-attr]


@all_mutable_set_types
def test_symmetric_difference_update(_cls: T_mutable_set[str]) -> None:
    s1 = _cls(["c", "a", "b"])
    s2 = _cls(["a", "g"])

    s1.symmetric_difference_update(s2)
    assert _cls(["c", "b", "g"]) == s1

    if _cls in ordered_set_types:
        assert list(s1) == ["c", "b", "g"]


@all_set_types
def test_union(_cls: T_set[str]) -> None:
    s1 = _cls(["c", "a", "b"])
    s2 = _cls(["a", "g"])
    s3 = _cls(["Z"])
    assert _cls(["c", "a", "b", "g"]) == s1.union(s2)
    assert _cls(["c", "a", "b", "Z"]) == s1.union(s3)

    if _cls in ordered_set_types:
        assert list(s1.union(s2)) == ["c", "a", "b", "g"]
        assert list(s1.union(s3)) == ["c", "a", "b", "Z"]


@all_set_types
def test_union_multiple_args(_cls: T_set[str]) -> None:
    s1 = _cls(["c", "a", "b"])
    s2 = _cls(["a", "g"])
    s3 = _cls(["Z"])
    assert _cls(["c", "a", "b", "g", "Z"]) == s1.union(s2, s3)

    if _cls in ordered_set_types:
        assert list(s1.union(s2, s3)) == ["c", "a", "b", "g", "Z"]


@all_set_types
def test_op_and(_cls: T_set[str]) -> None:
    s1 = _cls(["c", "a", "b"])
    s2 = _cls(["a", "g", "b"])
    s3 = _cls(["Z", "b", "c"])
    assert _cls(["a", "b"]) == s1 & s2
    assert _cls(["c", "b"]) == s1 & s3

    assert s1 & s1 == s1
    assert s1 & _cls(["Z"]) == _cls([])

    if _cls in ordered_set_types:
        assert list(s1 & s2) == ["a", "b"]
        assert list(s1 & s3) == ["c", "b"]


@all_set_types
def test_op_iand(_cls: T_set[str]) -> None:
    s1 = _cls(["c", "a", "b"])
    s2 = _cls(["a", "g", "b"])
    s3 = _cls(["Z", "b", "c"])

    s1 &= s2
    assert _cls(["a", "b"]) == s1

    if _cls in ordered_set_types:
        assert list(s1) == ["a", "b"]

    s1 &= s3
    assert _cls(["b"]) == s1


@all_set_types
def test_op_or(_cls: T_set[str]) -> None:
    s1 = _cls(["c", "a", "b"])
    s2 = _cls(["a", "g"])
    s3 = _cls(["Z"])

    assert _cls(["c", "a", "b", "g"]) == s1 | s2
    assert _cls(["c", "a", "b", "Z"]) == s1 | s3

    if _cls in ordered_set_types:
        assert list(s1 | s2) == ["c", "a", "b", "g"]
        assert list(s1 | s3) == ["c", "a", "b", "Z"]

    assert s1 | s1 == s1


@all_set_types
def test_op_ior(_cls: T_set[str]) -> None:
    s1 = _cls(["c", "a", "b"])
    s2 = _cls(["a", "g"])
    s3 = _cls(["Z"])

    s1 |= s2
    assert _cls(["c", "a", "b", "g"]) == s1

    if _cls in ordered_set_types:
        assert ["c", "a", "b", "g"] == list(s1)

    s1 |= s3
    assert _cls(["c", "a", "b", "g", "Z"]) == s1

    if _cls in ordered_set_types:
        assert ["c", "a", "b", "g", "Z"] == list(s1)


@all_set_types
def test_op_sub(_cls: T_set[str]) -> None:
    s1 = _cls(["c", "a", "b"])
    s2 = _cls(["a", "g"])
    s3 = _cls(["Z"])

    assert _cls(["c", "b"]) == s1 - s2
    assert _cls(["c", "a", "b"]) == s1 - s3

    if _cls in ordered_set_types:
        assert list(s1 - s2) == ["c", "b"]
        assert list(s1 - s3) == ["c", "a", "b"]


@all_set_types
def test_op_isub(_cls: T_set[str]) -> None:
    s1 = _cls(["c", "a", "b"])
    s2 = _cls(["a", "g"])
    s3 = _cls(["Z"])

    s1 -= s2
    assert _cls(["c", "b"]) == s1

    if _cls in ordered_set_types:
        assert ["c", "b"] == list(s1)
    s1 -= s3
    assert _cls(["c", "b"]) == s1


@all_set_types
def test_op_xor(_cls: T_set[str]) -> None:
    s1 = _cls(["c", "a", "b"])
    s2 = _cls(["a", "g"])
    s3 = _cls(["Z"])

    assert _cls(["c", "b", "g"]) == s1 ^ s2
    assert _cls(["c", "a", "b", "Z"]) == s1 ^ s3

    if _cls in ordered_set_types:
        assert list(s1 ^ s2) == ["c", "b", "g"]
        assert list(s1 ^ s3) == ["c", "a", "b", "Z"]


@all_set_types
def test_op_ixor(_cls: T_set[str]) -> None:
    s1 = _cls(["c", "a", "b"])
    s2 = _cls(["a", "g"])
    s3 = _cls(["Z"])
    s1 ^= s2

    assert _cls(["c", "b", "g"]) == s1
    if _cls in ordered_set_types:
        assert list(s1) == ["c", "b", "g"]
    s1 ^= s3
    assert _cls(["c", "b", "Z", "g"]) == s1


@all_set_types
def test_issubset(_cls: T_set[int]) -> None:
    s1 = _cls([3, 1, 2])
    s2 = _cls([1, 7])
    assert not s2.issubset(s1)
    assert _cls().issubset(s1)

    if _cls in mutable_set_types:
        s2.discard(7)  # type: ignore[union-attr]
        assert s2.issubset(s1)


@all_ordered_set_types
def test_issuperset(_cls: T_set[int]) -> None:
    s1 = _cls([3, 1, 2])
    s2 = _cls([1, 7])
    assert not s1.issuperset(s2)

    s3 = _cls([1, 2])
    assert s1.issuperset(s3)

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
def test_pop_mutable(_cls: T_mutable_set[str]) -> None:
    s1 = _cls(["c", "a", "b"])

    p = s1.pop()
    assert len(s1) == 2

    if _cls in ordered_set_types:
        assert p == "b"
        assert list(s1) == ["c", "a"]


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


@all_set_types
def test_isinstance(_cls: T_set[int]) -> None:
    # Note that some tests appear multiple times, this is intentional.

    from collections.abc import MutableSet as abc_MutableSet
    from collections.abc import Set as abc_Set

    # All of the following imports from 'typing' are deprecated as of Python 3.9
    from typing import AbstractSet as tp_AbstractSet
    from typing import FrozenSet as tp_FrozenSet
    from typing import MutableSet as tp_MutableSet
    from typing import Set as tp_Set

    # set
    if _cls == set:
        assert isinstance(set(), tp_AbstractSet)
        assert isinstance(set(), tp_Set)
        assert isinstance(set(), tp_MutableSet)
        assert not isinstance(set(), tp_FrozenSet)
        assert isinstance(set(), abc_Set)
        assert isinstance(set(), abc_MutableSet)

        assert isinstance(_cls(), set)
        assert not isinstance(_cls(), frozenset)

        assert not isinstance(_cls(), OrderedSet)
        assert not isinstance(_cls(), FrozenOrderedSet)

    # OrderedSet
    if _cls == OrderedSet:
        assert isinstance(OrderedSet(), tp_AbstractSet)
        # assert isinstance(OrderedSet(), tp_Set)
        assert isinstance(OrderedSet(), tp_MutableSet)
        assert not isinstance(OrderedSet(), tp_FrozenSet)
        assert isinstance(OrderedSet(), abc_Set)
        assert isinstance(OrderedSet(), abc_MutableSet)

        # assert isinstance(_cls(), set)
        assert not isinstance(_cls(), frozenset)

        assert isinstance(_cls(), OrderedSet)
        # assert not isinstance(_cls(), FrozenOrderedSet)

    # frozenset
    if _cls == frozenset:
        assert isinstance(frozenset(), tp_AbstractSet)
        assert not isinstance(frozenset(), tp_Set)
        assert not isinstance(frozenset(), tp_MutableSet)
        assert isinstance(frozenset(), tp_FrozenSet)
        assert isinstance(frozenset(), abc_Set)
        assert not isinstance(frozenset(), abc_MutableSet)

        assert not isinstance(_cls(), set)
        assert isinstance(_cls(), frozenset)

        assert not isinstance(_cls(), OrderedSet)
        assert not isinstance(_cls(), FrozenOrderedSet)

    # FrozenOrderedSet
    if _cls == FrozenOrderedSet:
        assert isinstance(FrozenOrderedSet(), tp_AbstractSet)
        assert not isinstance(FrozenOrderedSet(), tp_Set)
        assert not isinstance(FrozenOrderedSet(), tp_MutableSet)
        # assert isinstance(FrozenOrderedSet(), tp_FrozenSet)
        assert isinstance(FrozenOrderedSet(), abc_Set)
        assert not isinstance(FrozenOrderedSet(), abc_MutableSet)

        assert not isinstance(_cls(), set)
        # assert isinstance(_cls(), frozenset)

        assert not isinstance(_cls(), OrderedSet)
        assert isinstance(_cls(), FrozenOrderedSet)

    assert isinstance(_cls(), tp_AbstractSet)
    assert isinstance(_cls(), abc_Set)
    assert isinstance(_cls(), AbstractSet)

    if _cls in mutable_set_types:
        # assert isinstance(_cls(), Set)
        # assert isinstance(_cls(), set)
        assert not isinstance(_cls(), frozenset)
        if _cls in ordered_set_types:
            assert isinstance(_cls(), OrderedSet)
            # assert not isinstance(_cls(), FrozenOrderedSet)
    else:
        assert not isinstance(_cls(), Set)
        assert not isinstance(_cls(), set)
        # assert isinstance(_cls(), frozenset)
        if _cls in ordered_set_types:
            assert not isinstance(_cls(), OrderedSet)
            assert isinstance(_cls(), FrozenOrderedSet)
