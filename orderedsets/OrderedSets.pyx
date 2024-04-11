

from collections.abc import Iterator, Set
from typing import AbstractSet, Any, Iterable, Optional, Type, TypeVar, Union

T = TypeVar("T")


class _NotProvided:
    pass


cdef class OrderedSet:
    """A set class that preserves insertion order.

    It can be used as a drop-in replacement for :class:`set` where ordering is
    desired.
    """
    cdef dict _dict

    def __cinit__(self):
        self._dict = {}

    def __init__(self, items: Union[Iterable[T], Type[_NotProvided]] = _NotProvided)\
            -> None:
        """Create a new :class:`OrderedSet`, optionally initialized with *items*."""
        if items is not _NotProvided:
            self._dict = dict.fromkeys(items)

    def __eq__(self, other: object) -> bool:
        """Return whether this set is equal to *other*."""
        # return NotImplemented
        return (isinstance(other,
                            (Set, OrderedSet, FrozenOrderedSet))
                and len(self) == len(other)
                and all(i in other for i in self))

    def __repr__(self) -> str:
        """Return a string representation of this set."""
        if len(self) == 0:
            return "OrderedSet()"
        return "OrderedSet({" + ", ".join([repr(k) for k in self._dict]) + "})"

    cpdef add(self, element: T):
        """Add *element* to this set."""
        self._dict[element] = None

    def clear(self) -> None:
        """Remove all elements from this set."""
        self._dict.clear()

    def copy(self) -> "OrderedSet[T]":
        """Return a shallow copy of this set."""
        return OrderedSet(self._dict.copy())

    def difference(self, *others: Iterable[T]) -> "OrderedSet[T]":
        """Return all elements that are in this set but not in *others*."""
        if not others:
            return OrderedSet(self._dict)
        other_elems = set.union(*map(set, others))
        items = [item for item in self._dict if item not in other_elems]
        return OrderedSet(items)

    def difference_update(self, *others: Iterable[T]) -> None:
        """Update this set to remove all items that are in *others*."""
        for other in others:
            for e in other:
                self.discard(e)

    def discard(self, element: T) -> None:
        """Remove *element* from this set if it is present."""
        # try/except and self._dict.pop(element, None) seem to be slower than this,
        # independent of whether 'element' is present or not.
        if element in self._dict:
            del self._dict[element]

    def intersection(self, *others: Iterable[T]) -> "OrderedSet[T]":
        """Return a new set with elements common to this set and all *others*."""
        if not others:
            return OrderedSet(self._dict)

        oth = set(self).intersection(*others)
        result_elements = [element for element in self._dict if element in oth]

        return OrderedSet(result_elements)

    def intersection_update(self, *others: Iterable[T]) -> None:
        """Update this set to be the intersection of itself and *others*."""
        if not others:
            return

        common_keys = list(self._dict.keys())
        for other in others:
            common_keys = [key for key in common_keys if key in set(other)]

        self._dict = dict.fromkeys(common_keys)

    def isdisjoint(self, s: Iterable[T]) -> bool:
        """Return whether this set is disjoint with *s*."""
        return self._dict.keys().isdisjoint(s)

    def issubset(self, s: Iterable[T]) -> bool:
        """Return whether this set is a subset of *s*."""
        return all(i in s for i in self)

    def issuperset(self, s: Iterable[T]) -> bool:
        """Return whether this set is a superset of *s*."""
        return set(self).issuperset(set(s))

    def pop(self) -> T:
        """Remove and return the most recently added element from this set."""
        return self._dict.popitem()[0]

    def remove(self, element: T) -> None:
        """Remove *element* from this set, raising :exc:`KeyError` if not present."""
        del self._dict[element]

    def symmetric_difference(self, s: Iterable[T]) -> "OrderedSet[T]":
        """Return the symmetric difference of this set and *s*."""
        return OrderedSet(
            dict.fromkeys([e for e in self._dict if e not in s]
                          + [e for e in s if e not in self._dict]))

    def symmetric_difference_update(self, s: Iterable[T]) -> None:
        """Update this set to be the symmetric difference of itself and *s*."""
        self._dict = self.symmetric_difference(s)._dict

    def union(self, *others: Iterable[T]) -> "OrderedSet[T]":
        """Return a new set with elements from this set and *others*."""
        return OrderedSet(list(self._dict)
                          + [e for other in others for e in other])

    def update(self, *others: Iterable[T]) -> None:
        """Update this set to be the union of itself and *others*."""
        # cdef dict _dict
        self._dict.update(*others)

    def __len__(self) -> int:
        """Return the number of elements in this set."""
        return len(self._dict)

    def __contains__(self, o: object) -> bool:
        """Return whether *o* is in this set."""
        return o in self._dict

    def __iter__(self) -> Iterator[T]:
        """Return an iterator over the elements of this set."""
        return iter(self._dict)

    def __and__(self, s: Set[T]) -> "OrderedSet[T]":
        """Return the intersection of this set and *s*."""
        return self.intersection(s)

    def __iand__(self, s: Set[T]) -> "OrderedSet[T]":
        """Update this set to be the intersection of itself and *s*."""
        result = self.intersection(s)
        self._dict = result._dict
        return result

    def __or__(self, s: Set[Any]) -> "OrderedSet[T]":
        """Return the union of this set and *s*."""
        return self.union(s)

    def __ior__(self, s: Set[Any]) -> "OrderedSet[T]":
        """Update this set to be the union of itself and *s*."""
        result = self.union(s)
        self._dict = result._dict
        return result

    def __sub__(self, s: Set[T]) -> "OrderedSet[T]":
        """Return the difference of this set and *s*."""
        return self.difference(s)

    def __isub__(self, s: Set[T]) -> "OrderedSet[T]":
        """Update this set to be the difference of itself and *s*."""
        result = self.difference(s)
        self._dict = result._dict
        return result

    def __xor__(self, s: Set[Any]) -> "OrderedSet[T]":
        """Return the symmetric difference of this set and *s*."""
        return self.symmetric_difference(s)

    def __ixor__(self, s: Set[Any]) -> "OrderedSet[T]":
        """Update this set to be the symmetric difference of itself and *s*."""
        result = self.symmetric_difference(s)
        self._dict = result._dict
        return result

    def __le__(self, s: Set[T]) -> bool:
        """Return whether this set is a subset of *s*."""
        return self.issubset(s)

    def __lt__(self, s: Set[T]) -> bool:
        """Return whether this set is a proper subset of *s*."""
        return len(self) < len(s) and self.issubset(s)

    def __ge__(self, s: Set[T]) -> bool:
        """Return whether this set is a superset of *s*."""
        return set(self) >= set(s)

    def __gt__(self, s: Set[T]) -> bool:
        """Return whether this set is a proper superset of *s*."""
        return len(self) > len(s) and set(self) > set(s)


class FrozenOrderedSet(AbstractSet[T]):
    """A frozen set class that preserves insertion order.

    It can be used as a drop-in replacement for :class:`frozenset` where
    ordering is desired.
    """

    def __init__(self, items: Union[Iterable[T], Type[_NotProvided]] = _NotProvided)\
            -> None:
        """Create a new :class:`FrozenOrderedSet`, optionally initialized \
            with *items*."""
        if items is _NotProvided:
            self._dict = {}
        else:
            # type-ignore-reason:
            # mypy thinks 'items' can still be Type[_NotProvided] here.
            self._dict = dict.fromkeys(items)  # type: ignore[arg-type]

        self._my_hash: Optional[int] = None

    def __reduce__(self) -> tuple[Any, ...]:
        """Return pickling information for this set."""
        # The hash must be recomputed on unpickling, because it may
        # change across Python invocations (e.g. due to hash randomization of
        # strings stored in the FrozenOrderedSet), so make sure it is not saved
        # here.
        return (self.__class__, (self._dict,))

    def __hash__(self) -> int:
        """Return a hash of this set."""
        if self._my_hash is not None:
            return self._my_hash

        self._my_hash = hash(frozenset(self))
        return self._my_hash

    def __eq__(self, other: object) -> bool:
        """Return whether this set is equal to *other*."""
        return (isinstance(other, Set)
                and len(self) == len(other)
                and all(i in other for i in self))

    def __repr__(self) -> str:
        """Return a string representation of this set."""
        if len(self) == 0:
            return "FrozenOrderedSet()"
        return "FrozenOrderedSet({" + ", ".join([repr(k) for k in self._dict]) + "})"

    def __len__(self) -> int:
        """Return the number of elements in this set."""
        return len(self._dict)

    def __contains__(self, o: object) -> bool:
        """Return whether *o* is in this set."""
        return o in self._dict

    def __iter__(self) -> Iterator[T]:
        """Return an iterator over the elements of this set."""
        return iter(self._dict)

    def copy(self) -> "FrozenOrderedSet[T]":
        """Return a shallow copy of this set."""
        return FrozenOrderedSet(self._dict)

    def difference(self, *others: Iterable[T]) -> "FrozenOrderedSet[T]":
        """Return the difference of this set and *others*."""
        if not others:
            return FrozenOrderedSet(self._dict)
        other_elems = set.union(*map(set, others))
        items = [item for item in self._dict if item not in other_elems]
        return FrozenOrderedSet(items)

    def intersection(self, *others: Iterable[T]) -> "FrozenOrderedSet[T]":
        """Return the intersection of this set and *others*."""
        if not others:
            return FrozenOrderedSet(self._dict)

        oth = set(self).intersection(*others)
        result_elements = [element for element in self._dict if element in oth]

        return FrozenOrderedSet(result_elements)

    def symmetric_difference(self, s: Iterable[T]) -> "FrozenOrderedSet[T]":
        """Return the symmetric difference of this set and *s*."""
        return FrozenOrderedSet(
            dict.fromkeys([e for e in self._dict if e not in s]
                          + [e for e in s if e not in self._dict]))

    def isdisjoint(self, s: Iterable[T]) -> bool:
        """Return whether this set is disjoint with *s*."""
        return self._dict.keys().isdisjoint(s)  # pylint: disable=no-member

    def issubset(self, s: Iterable[T]) -> bool:
        """Return whether this set is a subset of *s*."""
        return all(i in s for i in self)

    def issuperset(self, s: Iterable[T]) -> bool:
        """Return whether this set is a superset of *s*."""
        return set(self).issuperset(set(s))

    def union(self, *others: Iterable[T]) -> "FrozenOrderedSet[T]":
        """Return the union of this set and *others*."""
        return FrozenOrderedSet(list(self._dict)
                                + [e for other in others for e in other])

    def __and__(self, s: Set[T]) -> "FrozenOrderedSet[T]":
        """Return the intersection of this set and *s*."""
        return self.intersection(s)

    def __or__(self, s: Set[Any]) -> "FrozenOrderedSet[T]":
        """Return the union of this set and *s*."""
        return self.union(s)

    def __sub__(self, s: Set[T]) -> "FrozenOrderedSet[T]":
        """Return the difference of this set and *s*."""
        return self.difference(s)

    def __xor__(self, s: Set[Any]) -> "FrozenOrderedSet[T]":
        """Return the symmetric difference of this set and *s*."""
        return self.symmetric_difference(s)
