import pytest

from orderedsets import FrozenOrderedSet, OrderedSet

all_set_types = pytest.mark.parametrize("_cls",
                                        [OrderedSet, FrozenOrderedSet, set,
                                         frozenset])

all_orderedset_types = pytest.mark.parametrize("_cls",
                                               [OrderedSet, FrozenOrderedSet])

all_mutableset_types = pytest.mark.parametrize("_cls",
                                               [OrderedSet, set])


@all_orderedset_types
def test_simple(_cls):
    if _cls in (set, frozenset):
        pytest.skip()
    s = _cls([4, 1, 4, 1])
    assert list(s) == [4, 1]


def test_str_repr():
    s = OrderedSet([4, 1, 4, 1])
    assert repr(s) == str(s) == "{4, 1}"

    s = OrderedSet()
    assert repr(s) == str(s) == "OrderedSet()"

    s = FrozenOrderedSet([4, 1, 4, 1])
    assert repr(s) == str(s) == "FrozenOrderedSet({4, 1})"

    s = FrozenOrderedSet()
    assert repr(s) == str(s) == "FrozenOrderedSet()"


@all_set_types
def test_len(_cls):
    s = _cls([4, 1, 4, 1])
    assert len(s) == 2


@all_set_types
def test_in(_cls):
    s = _cls([4, 1, 4, 1])
    assert 4 in s
    assert 2 not in s


@all_set_types
def test_eq(_cls):
    s = _cls([4, 1, 4, 1])
    s2 = _cls([4, 4, 1])
    s3 = set([4, 1, 4, 1])  # noqa: C405
    assert s == s2
    assert s == s3
    assert s2 == s
    assert s3 == s
    assert s2 == s3 == s


@all_set_types
def test_isdisjoint(_cls):
    s_1 = _cls([3, 1, 2])
    s_2 = _cls([1, 7])
    assert not s_1.isdisjoint(s_2)

    s_3 = _cls([10, 7])
    assert s_1.isdisjoint(s_3)


@all_mutableset_types
def test_remove_discard(_cls):
    s = _cls([4, 1, 4, 1])

    with pytest.raises(KeyError):
        s.remove(17)
    s.discard(17)

    assert s == _cls([4, 1])

    s.remove(4)

    assert s == {1}


@all_mutableset_types
def test_clear(_cls):
    s = OrderedSet([4, 1, 4, 1])
    s.clear()

    assert len(s) == 0
    assert s == OrderedSet()


@all_set_types
def test_toset(_cls):
    assert {1, 2, 3} == set(_cls([3, 1, 2]))


@all_orderedset_types
def test_tolist(_cls):
    assert [3, 1, 2] == list(_cls([3, 1, 2]))


def test_hash():
    s = OrderedSet([4, 1, 4, 1])
    with pytest.raises(TypeError):
        hash(s)

    s = FrozenOrderedSet([4, 1, 4, 1])
    s2 = FrozenOrderedSet([4, 1, 4, 1])
    assert hash(s)
    assert hash(s) == hash(s)
    assert s == s2
    assert hash(s) == hash(s2)


def test_update():
    s = OrderedSet([1, 6, 8])

    assert list(s) == [1, 6, 8]

    s.update(range(10, 100000))
    for v in range(10, 100000):
        s.remove(v)

    assert list(s) == [1, 6, 8]
