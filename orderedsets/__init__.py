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

import sys

try:
    import importlib.metadata as importlib_metadata
except ModuleNotFoundError:  # pragma: no cover
    # Python 3.7
    import importlib_metadata  # type: ignore[no-redef]

__version__ = importlib_metadata.version(__package__ or __name__)

import sys
from collections.abc import Iterator
from typing import Any, Dict, Iterable, Optional, TypeVar

if sys.version_info >= (3, 9):
    from collections.abc import MutableSet, Set
else:  # pragma: no cover
    from typing import MutableSet, Set

from immutabledict import immutabledict

T = TypeVar("T")


class OrderedSet(MutableSet[T]):
    def __init__(self, items: Optional[Iterable[T]] = None) -> None:
        if not items:
            self._dict: Dict[T, None] = {}
        elif isinstance(items, dict):
            self._dict = items
        else:
            self._dict = dict.fromkeys(items)

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Set):
            return set(self) == set(other)
        return False

    def __repr__(self) -> str:
        if len(self) == 0:
            return "OrderedSet()"
        return "OrderedSet({" + ", ".join(list(map(str, self._dict))) + "})"

    def add(self, element: T) -> None:
        self._dict = {**self._dict, **{element: None}}

    def clear(self) -> None:
        self._dict.clear()

    def copy(self) -> OrderedSet[T]:
        return OrderedSet(self._dict.copy())

    def difference(self, s: Iterable[Any]) -> OrderedSet[T]:
        return OrderedSet({e: None for e in self._dict if e not in s})

    def difference_update(self, s: Iterable[Any]) -> None:
        self._dict = {e: None for e in self._dict if e not in s}

    def discard(self, element: T) -> None:
        if element in self._dict:
            del self._dict[element]

    def intersection(self, s: Iterable[Any]) -> OrderedSet[T]:
        return OrderedSet({e: None for e in self._dict if e in s})

    def intersection_update(self, s: Iterable[Any]) -> None:
        self._dict = {e: None for e in self._dict if e in s}

    def isdisjoint(self, s: Iterable[Any]) -> bool:
        return self._dict.keys().isdisjoint(s)

    def issubset(self, s: Iterable[Any]) -> bool:
        return set(self).issubset(set(s))

    def issuperset(self, s: Iterable[Any]) -> bool:
        return set(self).issuperset(set(s))

    def pop(self) -> T:
        items = list(self._dict)
        result = items.pop()
        self._dict = dict.fromkeys(items)
        return result

    def remove(self, element: T) -> None:
        del self._dict[element]

    def symmetric_difference(self, s: Iterable[T]) -> OrderedSet[T]:
        return OrderedSet(
            dict.fromkeys([e for e in self._dict if e not in s]
                          + [e for e in s if e not in self._dict]))

    def symmetric_difference_update(self, s: Iterable[T]) -> None:
        self._dict = self.symmetric_difference(s)._dict

    def union(self, s: Iterable[T]) -> OrderedSet[T]:
        return OrderedSet({**self._dict, **dict.fromkeys(s)})

    def update(self, s: Iterable[T]) -> None:
        self._dict = self.union(s)._dict

    def __len__(self) -> int:
        return len(self._dict)

    def __contains__(self, o: object) -> bool:
        return o in self._dict

    def __iter__(self) -> Iterator[T]:
        return iter(self._dict)

    def __and__(self, s: Set[T]) -> OrderedSet[T]:
        return self.intersection(s)

    def __iand__(self, s: Set[T]) -> OrderedSet[T]:
        result = self.intersection(s)
        self._dict = result._dict
        return result

    def __or__(self, s: Set[Any]) -> OrderedSet[T]:
        return self.union(s)

    def __ior__(self, s: Set[Any]) -> OrderedSet[T]:
        result = self.union(s)
        self._dict = result._dict
        return result

    def __sub__(self, s: Set[T]) -> OrderedSet[T]:
        return self.difference(s)

    def __isub__(self, s: Set[T]) -> OrderedSet[T]:
        result = self.difference(s)
        self._dict = result._dict
        return result

    def __xor__(self, s: Set[Any]) -> OrderedSet[T]:
        return self.symmetric_difference(s)

    def __ixor__(self, s: Set[Any]) -> OrderedSet[T]:
        result = self.symmetric_difference(s)
        self._dict = result._dict
        return result

    def __le__(self, s: Set[T]) -> bool:
        return self.issubset(s)

    def __lt__(self, s: Set[T]) -> bool:
        return self.issubset(s) and len(self) < len(s)

    def __ge__(self, s: Set[T]) -> bool:
        return set(self) >= set(s)

    def __gt__(self, s: Set[T]) -> bool:
        return set(self) > set(s)


class FrozenOrderedSet(Set[T]):
    def __init__(self, base: Optional[Iterable[T]] = None) -> None:
        if not base:
            self._dict: immutabledict[T, None] = immutabledict()
        elif isinstance(base, dict):
            self._dict = immutabledict(base)
        else:
            self._dict = \
                immutabledict.fromkeys(base)

    if sys.version_info >= (3, 9):  # pragma: no cover
        # See
        # https://github.com/python/cpython/blob/4a1026077af65b308c98cdfe181b5f94c46fb48a/Lib/_collections_abc.py#L665
        # for why we are using this hash implementation.
        __hash__ = Set._hash
    else:  # pragma: no cover
        def __hash__(self) -> int:
            return hash(frozenset(self._dict))

    def __repr__(self) -> str:
        if len(self) == 0:
            return "FrozenOrderedSet()"
        return "FrozenOrderedSet({" + ", ".join(list(map(str, self._dict))) + "})"

    def __len__(self) -> int:
        return len(self._dict)

    def __contains__(self, o: object) -> bool:
        return o in self._dict

    def __iter__(self) -> Iterator:  # type: ignore[type-arg]
        return iter(self._dict)

    def copy(self) -> FrozenOrderedSet[T]:
        return FrozenOrderedSet(self._dict)

    def difference(self, s: Iterable[Any]) -> FrozenOrderedSet[T]:
        return FrozenOrderedSet(
            {e: None for e in self._dict if e not in s})

    def intersection(self, s: Iterable[Any]) -> FrozenOrderedSet[T]:
        return FrozenOrderedSet({e: None for e in self._dict if e in s})

    def symmetric_difference(self, s: Iterable[T]) -> FrozenOrderedSet[T]:
        return FrozenOrderedSet(
            dict.fromkeys([e for e in self._dict if e not in s]
                          + [e for e in s if e not in self._dict]))

    def isdisjoint(self, s: Iterable[Any]) -> bool:
        return self._dict.keys().isdisjoint(s)

    def issubset(self, s: Iterable[Any]) -> bool:
        return all(i in s for i in self)

    def issuperset(self, s: Iterable[Any]) -> bool:
        return set(self).issuperset(set(s))

    def union(self, s: Iterable[T]) -> FrozenOrderedSet[T]:
        return FrozenOrderedSet({**self._dict, **dict.fromkeys(s)})

    def __and__(self, s: Set[T]) -> FrozenOrderedSet[T]:
        return self.intersection(s)

    def __or__(self, s: Set[Any]) -> FrozenOrderedSet[T]:
        return self.union(s)

    def __sub__(self, s: Set[T]) -> FrozenOrderedSet[T]:
        return self.difference(s)

    def __xor__(self, s: Set[Any]) -> FrozenOrderedSet[T]:
        return self.symmetric_difference(s)
