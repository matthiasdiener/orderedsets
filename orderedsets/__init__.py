"""Set classes that preserve insertion order."""

from __future__ import annotations

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

try:
    import importlib.metadata as importlib_metadata
except ModuleNotFoundError:  # pragma: no cover
    # Python 3.7
    import importlib_metadata  # type: ignore[no-redef]

__version__ = importlib_metadata.version(__package__ or __name__)

import sys
from collections.abc import Iterable, Iterator
from typing import Any, Hashable, TypeVar

if sys.version_info < (3, 9):  # pragma: no cover
    from typing import AbstractSet as MutableSet
    from typing import AbstractSet as Set
else:
    from collections.abc import MutableSet, Set


T = TypeVar("T", bound=Hashable)
T_cov = TypeVar("T_cov", covariant=True, bound=Hashable)


class _NotProvided:
    pass


class OrderedSet(MutableSet[T]):
    """A set class that preserves insertion order.

    It implements the same API as :class:`set` and can be used as a drop-in
    replacement for that class when ordering is desired.
    """

    def __init__(self, items: Iterable[T] | type[_NotProvided] = _NotProvided)\
            -> None:
        """Create a new :class:`OrderedSet`, optionally initialized with *items*."""
        if items is _NotProvided:
            self._dict = {}
        else:
            # type-ignore-reason:
            # mypy thinks 'items' can still be Type[_NotProvided] here.
            self._dict = dict.fromkeys(items)  # type: ignore[arg-type]

    def __repr__(self) -> str:
        """Return a string representation of this set."""
        cls_name = self.__class__.__name__
        if len(self) == 0:
            return f"{cls_name}()"
        return f"{cls_name}({{" + ", ".join([repr(k) for k in self._dict]) + "})"

    def add(self, element: T) -> None:
        """Add *element* to this set."""
        self._dict[element] = None

    def clear(self) -> None:
        """Remove all elements from this set."""
        self._dict.clear()

    def copy(self) -> OrderedSet[T]:
        """Return a shallow copy of this set."""
        return self.__class__(self._dict.copy())

    def difference(self, *others: Iterable[T]) -> OrderedSet[T]:
        """Return all elements that are in this set but not in *others*."""
        if not others:
            return self.__class__(self._dict)
        other_elems = set.union(*map(set, others))
        items = [item for item in self._dict if item not in other_elems]
        return self.__class__(items)

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

    def intersection(self, *others: Iterable[T]) -> OrderedSet[T]:
        """Return a new set with elements common to this set and all *others*."""
        if not others:
            return self.__class__(self._dict)

        oth = set(self).intersection(*others)
        result_elements = [element for element in self._dict if element in oth]

        return self.__class__(result_elements)

    def intersection_update(self, *others: Iterable[T]) -> None:
        """Update this set to be the intersection of itself and *others*."""
        if not others:
            return

        common_keys = list(self._dict.keys())
        for other in others:
            common_keys = [key for key in common_keys if key in set(other)]

        self._dict = dict.fromkeys(common_keys)

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

    def symmetric_difference(self, s: Iterable[T]) -> OrderedSet[T]:
        """Return the symmetric difference of this set and *s*."""
        return self.__class__(
            dict.fromkeys([e for e in self._dict if e not in s]
                          + [e for e in s if e not in self._dict]))

    def symmetric_difference_update(self, s: Iterable[T]) -> None:
        """Update this set to be the symmetric difference of itself and *s*."""
        self._dict = self.symmetric_difference(s)._dict

    def union(self, *others: Iterable[T]) -> OrderedSet[T]:
        """Return a new set with elements from this set and *others*."""
        return self.__class__(list(self._dict)
                          + [e for other in others for e in other])

    def update(self, *others: Iterable[T]) -> None:
        """Update this set to be the union of itself and *others*."""
        self._dict = self.union(*others)._dict

    def __len__(self) -> int:
        """Return the number of elements in this set."""
        return len(self._dict)

    def __contains__(self, o: object) -> bool:
        """Return whether *o* is in this set."""
        return o in self._dict

    def __iter__(self) -> Iterator[T]:
        """Return an iterator over the elements of this set."""
        return iter(self._dict)

    def __and__(self, s: Set[T]) -> OrderedSet[T]:
        """Return the intersection of this set and *s*."""
        return self.intersection(s)

    def __iand__(self, s: Set[T]) -> OrderedSet[T]:
        """Update this set to be the intersection of itself and *s*."""
        result = self.intersection(s)
        self._dict = result._dict
        return result

    def __or__(self, s: Set[Any]) -> OrderedSet[T]:
        """Return the union of this set and *s*."""
        return self.union(s)

    def __ior__(self, s: Set[Any]) -> OrderedSet[T]:
        """Update this set to be the union of itself and *s*."""
        result = self.union(s)
        self._dict = result._dict
        return result

    def __sub__(self, s: Set[T]) -> OrderedSet[T]:
        """Return the difference of this set and *s*."""
        return self.difference(s)

    def __isub__(self, s: Set[T]) -> OrderedSet[T]:
        """Update this set to be the difference of itself and *s*."""
        result = self.difference(s)
        self._dict = result._dict
        return result

    def __xor__(self, s: Set[Any]) -> OrderedSet[T]:
        """Return the symmetric difference of this set and *s*."""
        return self.symmetric_difference(s)

    def __ixor__(self, s: Set[Any]) -> OrderedSet[T]:
        """Update this set to be the symmetric difference of itself and *s*."""
        result = self.symmetric_difference(s)
        self._dict = result._dict
        return result


class FrozenOrderedSet(Set[T_cov]):
    """A frozen set class that preserves insertion order.

    It implements the same API as :class:`frozenset` and can be used as a
    drop-in replacement for that class when ordering is desired.
    """

    _dict: dict[T_cov, None]
    _my_hash: int | None = None

    __init__ = OrderedSet.__init__

    def __reduce__(self) -> tuple[Any, ...]:
        """Return pickling information for this set."""
        # The hash must be recomputed on unpickling, because it may
        # change across Python invocations (e.g. due to hash randomization of
        # strings stored in the FrozenOrderedSet), so make sure it is not saved
        # here.
        return (self.__class__, (self._dict,))

    def __hash__(self) -> int:
        """Return a hash of this set.

        The hash has the same value as a :class:`frozenset` with the same
        elements, and it is cached after the first call.
        """
        if self._my_hash is not None:
            return self._my_hash

        # This needs to use the same hashing algorithm as frozenset.
        # Converting to a frozenset is the safest and fastest way to do that.
        self._my_hash = hash(frozenset(self))
        return self._my_hash

    __repr__ = OrderedSet.__repr__
    __len__ = OrderedSet.__len__
    __contains__ = OrderedSet.__contains__
    __iter__ = OrderedSet.__iter__

    if sys.version_info >= (3, 9):
        __eq__ = Set.__eq__  # needed for mypy

    copy = OrderedSet.copy

    difference = OrderedSet.difference
    intersection = OrderedSet.intersection
    symmetric_difference = OrderedSet.symmetric_difference

    issubset = OrderedSet.issubset
    issuperset = OrderedSet.issuperset
    union = OrderedSet.union

    __and__ = OrderedSet.__and__
    __or__ = OrderedSet.__or__
    __sub__ = OrderedSet.__sub__
    __xor__ = OrderedSet.__xor__
