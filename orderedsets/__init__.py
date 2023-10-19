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
except ModuleNotFoundError:
    import importlib_metadata  # type: ignore[no-redef]

__version__ = importlib_metadata.version(__package__ or __name__)

from collections.abc import Iterator, MutableSet, Set
from typing import Any, Dict, Hashable, Iterable, Optional

from immutabledict import immutabledict


class OrderedSet(MutableSet):  # type: ignore[type-arg]
    def __init__(self, items: Optional[Iterable[Hashable]] = None) -> None:
        if not items:
            self._dict: Dict[Hashable, None] = {}
        elif isinstance(items, dict):
            self._dict = items
        else:
            self._dict = dict.fromkeys(items)

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Set):
            return set(self) == set(other)
        return False

    def __ne__(self, other: object) -> bool:
        return not self.__eq__(other)

    def __repr__(self) -> str:
        if len(self) == 0:
            return "OrderedSet()"
        return "{" + ", ".join(list(map(str, self._dict))) + "}"

    def add(self, element: Hashable) -> None:
        self._dict = {**self._dict, **{element: None}}

    def clear(self) -> None:
        self._dict.clear()

    def copy(self) -> "OrderedSet":
        return OrderedSet(self._dict.copy())

    def difference(self, s: Iterable[Any]) -> "OrderedSet":
        return OrderedSet({e: None for e in self._dict if e not in s})

    def difference_update(self, s: Iterable[Any]) -> None:
        self._dict = {e: None for e in self._dict if e not in s}

    def discard(self, element: Hashable) -> None:
        if element in self._dict:
            del self._dict[element]

    def intersection(self, s: Iterable[Any]) -> "OrderedSet":
        return OrderedSet({e: None for e in self._dict if e in s})

    def intersection_update(self, s: Iterable[Any]) -> None:
        self._dict = {e: None for e in self._dict if e in s}

    def isdisjoint(self, s: Iterable[Any]) -> bool:
        return self._dict.keys().isdisjoint(s)

    def issubset(self, s: Iterable[Any]) -> bool:
        return set(self).issubset(set(s))

    def issuperset(self, s: Iterable[Any]) -> bool:
        return set(self).issuperset(set(s))

    def pop(self) -> Hashable:
        items = list(self._dict)
        result = items.pop()
        self._dict = dict.fromkeys(items)
        return result

    def remove(self, element: Hashable) -> None:
        del self._dict[element]

    def symmetric_difference(self, s: Iterable[Hashable]) -> "OrderedSet":
        return OrderedSet(
            dict.fromkeys([e for e in self._dict if e not in s]
                          + [e for e in s if e not in self._dict]))

    def symmetric_difference_update(self, s: Iterable[Hashable]) -> None:
        self._dict = self.symmetric_difference(s)._dict

    def union(self, s: Iterable[Hashable]) -> "OrderedSet":
        return OrderedSet({**self._dict, **dict.fromkeys(s)})

    def update(self, s: Iterable[Hashable]) -> None:
        self._dict = self.union(s)._dict

    def __len__(self) -> int:
        return len(self._dict)

    def __contains__(self, o: object) -> bool:
        return o in self._dict

    def __iter__(self) -> Iterator:  # type: ignore[type-arg]
        return iter(self._dict)

    def __and__(self, s: Set) -> "OrderedSet":  # type: ignore[type-arg]
        return self.intersection(s)

    def __iand__(self, s: Set) -> "OrderedSet":  # type: ignore[type-arg]
        result = self.intersection(s)
        self._dict = result._dict
        return result

    def __or__(self, s: Set) -> "OrderedSet":  # type: ignore[type-arg]
        return self.union(s)

    def __ior__(self, s: Set) -> "OrderedSet":  # type: ignore[type-arg]
        result = self.union(s)
        self._dict = result._dict
        return result

    def __sub__(self, s: Set) -> "OrderedSet":  # type: ignore[type-arg]
        return self.difference(s)

    def __isub__(self, s: Set) -> "OrderedSet":  # type: ignore[type-arg]
        result = self.difference(s)
        self._dict = result._dict
        return result

    def __xor__(self, s: Set) -> "OrderedSet":  # type: ignore[type-arg]
        return self.symmetric_difference(s)

    def __ixor__(self, s: Set) -> "OrderedSet":  # type: ignore[type-arg]
        result = self.symmetric_difference(s)
        self._dict = result._dict
        return result

    def __le__(self, s: Set) -> bool:  # type: ignore[type-arg]
        return self.issubset(s)

    def __lt__(self, s: Set) -> bool:  # type: ignore[type-arg]
        return self.issubset(s) and len(self) < len(s)

    def __ge__(self, s: Set) -> bool:  # type: ignore[type-arg]
        return set(self) >= set(s)

    def __gt__(self, s: Set) -> bool:  # type: ignore[type-arg]
        return set(self) > set(s)


class FrozenOrderedSet(Set):  # type: ignore[type-arg]
    def __init__(self, base: Optional[Iterable[Hashable]] = None) -> None:
        if not base:
            self._dict: immutabledict[
                Hashable, None] = immutabledict()
        elif isinstance(base, dict):
            self._dict = immutabledict(base)
        else:
            self._dict = \
                immutabledict.fromkeys(base)

    def __hash__(self) -> int:
        return hash(type(self)) ^ hash(self._dict)

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

    def copy(self) -> "FrozenOrderedSet":
        return FrozenOrderedSet(self._dict)

    def difference(self, s: Iterable[Any]) -> "FrozenOrderedSet":
        return FrozenOrderedSet(
            {e: None for e in self._dict if e not in s})

    def intersection(self, s: Iterable[Any]) -> "FrozenOrderedSet":
        return FrozenOrderedSet({e: None for e in self._dict if e in s})

    def symmetric_difference(self, s: Iterable[Hashable]) -> "FrozenOrderedSet":
        return FrozenOrderedSet(
            dict.fromkeys([e for e in self._dict if e not in s]
                          + [e for e in s if e not in self._dict]))

    def union(self, s: Iterable[Hashable]) -> "FrozenOrderedSet":
        return FrozenOrderedSet({**self._dict, **dict.fromkeys(s)})

    def __and__(self, s: Set) -> "FrozenOrderedSet":  # type: ignore[type-arg]
        return self.intersection(s)

    def __or__(self, s: Set) -> "FrozenOrderedSet":  # type: ignore[type-arg]
        return self.union(s)

    def __sub__(self, s: Set) -> "FrozenOrderedSet":  # type: ignore[type-arg]
        return self.difference(s)

    def __xor__(self, s: Set) -> "FrozenOrderedSet":  # type: ignore[type-arg]
        return self.symmetric_difference(s)
