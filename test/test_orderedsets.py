from orderedsets import OrderedSet
import pytest


def test_simple():
    s = OrderedSet([4, 1, 4, 1])
    assert list(s) == [4, 1]


def test_str_repr():
    s = OrderedSet([4, 1, 4, 1])
    assert repr(s) == str(s) == "{4, 1}"

    s = OrderedSet()
    assert repr(s) == str(s) == "OrderedSet()"


def test_len():
    s = OrderedSet([4, 1, 4, 1])
    assert len(s) == 2


def test_in():
    s = OrderedSet([4, 1, 4, 1])
    assert 4 in s
    assert 2 not in s


def test_eq():
    s = OrderedSet([4, 1, 4, 1])
    s2 = OrderedSet([4, 4, 1])
    s3 = set([4, 1, 4, 1])
    assert s == s2
    assert s == s3
    assert s2 == s
    assert s3 == s
    assert s2 == s3 == s


def test_isdisjoint():
    s_1 = OrderedSet([3, 1, 2])
    s_2 = OrderedSet([1, 7])
    assert not s_1.isdisjoint(s_2)

    s_3 = OrderedSet([10, 7])
    assert s_1.isdisjoint(s_3)


def test_remove_discard():
    s = OrderedSet([4, 1, 4, 1])
    with pytest.raises(KeyError):
        s.remove(17)
    s.discard(17)

    assert s == OrderedSet([4, 1])

    s.remove(4)

    assert s == {1}


def test_clear():
    s = OrderedSet([4, 1, 4, 1])
    s.clear()

    assert len(s) == 0
    assert s == OrderedSet()


def test_toset():
    assert {1, 2, 3} == set(OrderedSet([3, 1, 2]))


def test_tolist():
    assert [3, 1, 2] == list(OrderedSet([3, 1, 2]))


def test_hash():
    s = OrderedSet([4, 1, 4, 1])
    with pytest.raises(TypeError):
        hash(s)


def test_update():
    s = OrderedSet([1, 6, 8])

    assert list(s) == [1, 6, 8]

    s.update(range(10, 100000))
    for v in range(10, 100000):
        s.remove(v)

    assert list(s) == [1, 6, 8]
