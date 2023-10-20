from typing import Any

import pytest

from orderedsets import FrozenOrderedSet, OrderedSet

set_types = (OrderedSet, FrozenOrderedSet, set, frozenset)
ordered_set_types = (OrderedSet, FrozenOrderedSet)
mutable_set_types = (OrderedSet, set)
immutable_set_types = (FrozenOrderedSet, frozenset)

all_set_types = pytest.mark.parametrize("_cls", set_types)
all_ordered_set_types = pytest.mark.parametrize("_cls", ordered_set_types)
all_mutable_set_types = pytest.mark.parametrize("_cls", mutable_set_types)
all_immutable_set_types = pytest.mark.parametrize("_cls", immutable_set_types)


@all_ordered_set_types
def test_simple(_cls: type[set[Any]]) -> None:
    s = _cls([4, 1, 4, 1])
    assert list(s) == [4, 1]


@all_ordered_set_types
def test_str_repr(_cls: type[set[Any]]) -> None:
    s = _cls([4, 1, 4, 1])
    assert repr(s) == str(s) == f"{_cls.__name__}({{4, 1}})"

    s = _cls()
    assert repr(s) == str(s) == f"{_cls.__name__}()"


@all_set_types
def test_len(_cls: type[set[Any]]) -> None:
    s = _cls([4, 1, 4, 1])
    assert len(s) == 2


@all_set_types
def test_in(_cls: type[set[Any]]) -> None:
    s = _cls([4, 1, 4, 1])
    assert 4 in s
    assert 2 not in s


@all_set_types
def test_eq(_cls: type[set[Any]]) -> None:
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

    assert s1 != [4, 1]  # type: ignore[comparison-overlap]
    if _cls in ordered_set_types:
        assert [4, 1] == list(s1)


@all_set_types
def test_isdisjoint(_cls: type[set[Any]]) -> None:
    s1 = _cls([3, 1, 2])
    s2 = _cls([1, 7])
    assert not s1.isdisjoint(s2)

    s_3 = _cls([10, 7])
    assert s1.isdisjoint(s_3)


@all_set_types
def test_remove_discard(_cls: type[set[Any]]) -> None:
    s = _cls([4, 1, 4, 1])

    if _cls in immutable_set_types:
        with pytest.raises(AttributeError):
            s.remove(17)
        with pytest.raises(AttributeError):
            s.discard(17)
        return

    with pytest.raises(KeyError):
        s.remove(17)
    s.discard(17)

    assert s == _cls([4, 1])

    s.remove(4)

    assert s == {1}


@all_set_types
def test_clear(_cls: type[set[Any]]) -> None:
    s = _cls([4, 1, 4, 1])

    if _cls in immutable_set_types:
        with pytest.raises(AttributeError):
            s.clear()
        return

    s.clear()

    assert len(s) == 0
    assert s == _cls()


@all_set_types
def test_toset(_cls: type[set[Any]]) -> None:
    assert {1, 2, 3} == set(_cls([3, 1, 2]))


@all_ordered_set_types
def test_tolist(_cls: type[set[Any]]) -> None:
    assert [3, 1, 2] == list(_cls([3, 1, 2]))


@all_set_types
def test_hash(_cls: type[set[Any]]) -> None:
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


@all_set_types
def test_update(_cls: type[set[Any]]) -> None:
    s = _cls([1, 6, 8])

    if _cls in immutable_set_types:
        with pytest.raises(AttributeError):
            s.update([6])
        return

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
def test_intersection(_cls: type[set[Any]]) -> None:
    s1 = _cls([3, 1, 2])
    s2 = _cls([1, 7])
    assert _cls([1]) == s1.intersection(s2)
    assert s1 == s1.intersection(s1)


@all_set_types
def test_intersection_update(_cls: type[set[Any]]) -> None:
    s1 = _cls([3, 1, 2])
    s2 = _cls([1, 7])

    if _cls in immutable_set_types:
        with pytest.raises(AttributeError):
            s1.intersection_update(s2)
    else:
        s1.intersection_update(s2)
        assert _cls([1]) == s1


@all_set_types
def test_add(_cls: type[set[Any]]) -> None:
    s = _cls([3, 1, 2])
    if _cls in immutable_set_types:
        with pytest.raises(AttributeError):
            s.add(0)
    else:
        s.add(0)
        assert _cls([3, 1, 2, 0]) == s


@all_set_types
def test_copy(_cls: type[set[Any]]) -> None:
    s1 = _cls([3, 1, 2])
    s2 = s1.copy()
    assert s1 == s2

    if not isinstance(s1, frozenset):
        assert s1 is not s2


@all_set_types
def test_difference(_cls: type[set[Any]]) -> None:
    s1 = _cls([3, 1, 2])
    s2 = _cls([1, 7])
    assert _cls([3, 2]) == s1.difference(s2)
    assert s1.difference(s1) == _cls()


@all_set_types
def test_difference_update(_cls: type[set[Any]]) -> None:
    s1 = _cls([3, 1, 2])
    s2 = _cls([1, 7])
    if _cls in immutable_set_types:
        with pytest.raises(AttributeError):
            s1.difference_update(s2)
    else:
        s1.difference_update(s2)
        assert _cls([3, 2]) == s1


@all_set_types
def test_symmetric_difference(_cls: type[set[Any]]) -> None:
    s1 = _cls([3, 1, 2])
    s2 = _cls([1, 7])
    assert _cls([3, 2, 7]) == s1.symmetric_difference(s2)


@all_set_types
def test_symmetric_difference_update(_cls: type[set[Any]]) -> None:
    s1 = _cls([3, 1, 2])
    s2 = _cls([1, 7])
    if _cls in immutable_set_types:
        with pytest.raises(AttributeError):
            s1.symmetric_difference_update(s2)
    else:
        s1.symmetric_difference_update(s2)
        assert _cls([3, 2, 7]) == s1


@all_set_types
def test_op_and(_cls: type[set[Any]]) -> None:
    s1 = _cls([3, 1, 2])
    s2 = _cls([1, 7])
    s3 = _cls([42])
    assert _cls([1]) == s1 & s2
    assert _cls() == s1 & s3


@all_set_types
def test_op_iand(_cls: type[set[Any]]) -> None:
    s1 = _cls([3, 1, 2])
    s2 = _cls([1, 7])
    s3 = _cls([42])
    s1 &= s2
    assert _cls([1]) == s1
    s1 &= s3
    assert _cls() == s1


@all_set_types
def test_op_or(_cls: type[set[Any]]) -> None:
    s1 = _cls([3, 1, 2])
    s2 = _cls([1, 7])
    s3 = _cls([42])
    assert _cls([1, 3, 2, 7]) == s1 | s2
    assert _cls([1, 3, 2, 42]) == s1 | s3


@all_set_types
def test_op_ior(_cls: type[set[Any]]) -> None:
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
def test_op_sub(_cls: type[set[Any]]) -> None:
    s1 = _cls([3, 1, 2])
    s2 = _cls([1, 7])
    s3 = _cls([42])
    assert _cls([3, 2]) == s1 - s2
    assert _cls([3, 1, 2]) == s1 - s3


@all_set_types
def test_op_isub(_cls: type[set[Any]]) -> None:
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
def test_op_xor(_cls: type[set[Any]]) -> None:
    s1 = _cls([3, 1, 2])
    s2 = _cls([1, 7])
    s3 = _cls([42])
    assert _cls([3, 2, 7]) == s1 ^ s2
    assert _cls([3, 1, 2, 42]) == s1 ^ s3


@all_set_types
def test_op_ixor(_cls: type[set[Any]]) -> None:
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
def test_issubset(_cls: type[set[Any]]) -> None:
    s1 = _cls([3, 1, 2])
    s2 = _cls([1, 7])
    assert not s2.issubset(s1)
    assert _cls().issubset(s1)

    if _cls in mutable_set_types:
        s2.discard(7)
        assert s2.issubset(s1)


@all_set_types
def test_issuperset(_cls: type[set[Any]]) -> None:
    s1 = _cls([3, 1, 2])
    s2 = _cls([1, 7])
    assert not s1.issuperset(s2)

    if _cls in mutable_set_types:
        s2.discard(7)
        assert s1.issuperset(s2)
        assert _cls(s1).issuperset(s2)


@all_set_types
def test_pop(_cls: type[set[Any]]) -> None:
    s1 = _cls([3, 1, 2])
    if _cls in immutable_set_types:
        with pytest.raises(AttributeError):
            s1.pop()
    else:
        p = s1.pop()
        assert len(s1) == 2

        if _cls in ordered_set_types:
            assert p == 2
            assert _cls([3, 1]) == s1


@all_set_types
def test_op_le(_cls: type[set[Any]]) -> None:
    s1 = _cls([3, 1, 2])
    s2 = _cls([1, 7])
    assert not (s2 <= s1)
    s3 = _cls([1, 2])
    assert s3 <= s1
    assert not s2.issubset(s1)


@all_set_types
def test_op_lt(_cls: type[set[Any]]) -> None:
    s1 = _cls([3, 1, 2])
    s2 = _cls([1, 7])
    assert not (s2 < s1)
    s3 = _cls([1, 2])
    assert s3 < s1
    assert not s2.issubset(s1)


@all_set_types
def test_op_ge(_cls: type[set[Any]]) -> None:
    s1 = _cls([3, 1, 2])
    s2 = _cls([1, 7])
    assert not (s2 >= s1)
    s3 = _cls([1, 2])
    assert s1 >= s3
    assert not s2.issubset(s1)


@all_set_types
def test_op_gt(_cls: type[set[Any]]) -> None:
    s1 = _cls([3, 1, 2])
    s2 = _cls([1, 7])
    assert not (s2 > s1)
    s3 = _cls([1, 2])
    assert s1 > s3
    assert not s2.issubset(s1)


@all_set_types
def test_bool(_cls: type[set[Any]]) -> None:
    assert not _cls()
    assert _cls([1])
    assert not bool(_cls())
    assert bool(_cls([1]))
