from __future__ import annotations
from collections.abc import Iterator, MutableSet, Set
from typing import AbstractSet, Any, Dict, Hashable, Iterable, Optional, TypeVar

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
        return (isinstance(other, Set)
                and len(self) == other
                and all(i in other for i in self))

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
        return all(i in s for i in self)

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

    def __and__(self, s: AbstractSet[T]) -> OrderedSet[T]:
        return self.intersection(s)

    def __iand__(self, s: AbstractSet[T]) -> OrderedSet[T]:
        result = self.intersection(s)
        self._dict = result._dict
        return result

    def __or__(self, s: AbstractSet[T]) -> OrderedSet[T]:
        return self.union(s)

    def __ior__(self, s: AbstractSet[T]) -> OrderedSet[T]:
        result = self.union(s)
        self._dict = result._dict
        return result

    def __sub__(self, s: AbstractSet[T]) -> OrderedSet[T]:
        return self.difference(s)

    def __isub__(self, s: AbstractSet[T]) -> OrderedSet[T]:
        result = self.difference(s)
        self._dict = result._dict
        return result

    def __xor__(self, s: AbstractSet[T]) -> OrderedSet[T]:
        return self.symmetric_difference(s)

    def __ixor__(self, s: AbstractSet[T]) -> OrderedSet[T]:
        result = self.symmetric_difference(s)
        self._dict = result._dict
        return result

    def __le__(self, s: AbstractSet[T]) -> bool:
        return self.issubset(s)

    def __lt__(self, s: AbstractSet[T]) -> bool:
        return len(self) < len(s) and self.issubset(s)

    def __ge__(self, s: AbstractSet[T]) -> bool:
        return set(self) >= set(s)

    def __gt__(self, s: AbstractSet[T]) -> bool:
        return len(self) > len(s) and set(self) > set(s)


class FrozenOrderedSet(AbstractSet[T]):
    def __init__(self, base: Optional[Iterable[T]] = None) -> None:
        if not base:
            self._dict: immutabledict[
                T, None] = immutabledict()
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

    def union(self, s: Iterable[T]) -> FrozenOrderedSet[T]:
        return FrozenOrderedSet({**self._dict, **dict.fromkeys(s)})

    def __and__(self, s: AbstractSet[T]) -> FrozenOrderedSet[T]:
        return self.intersection(s)

    def __or__(self, s: AbstractSet[T]) -> FrozenOrderedSet[T]:
        return self.union(s)

    def __sub__(self, s: AbstractSet[T]) -> FrozenOrderedSet[T]:
        return self.difference(s)

    def __xor__(self, s: AbstractSet[T]) -> FrozenOrderedSet[T]:
        return self.symmetric_difference(s)
