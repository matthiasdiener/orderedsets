from typing import Generic, Optional, Iterable, Hashable, Any, Dict
from collections.abc import Set, Iterator
from frozendict import frozendict


class OrderedSet(Set[Hashable]):
    def __init__(self, items: Optional[Iterable[Hashable]] = None) -> None:
        self._dict: Dict[Hashable, None]
        if not items:
            self._dict = {}
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

    def copy(self) -> 'OrderedSet':
        return OrderedSet(self._dict.copy())

    def difference(self, s: Iterable[Any]) -> 'OrderedSet':
        return OrderedSet({e: None for e in self._dict if e not in s})

    def difference_update(self, s: Iterable[Any]) -> None:
        self._dict = {e: None for e in self._dict if e not in s}

    def discard(self, element: Hashable) -> None:
        if element in self._dict:
            del self._dict[element]

    def intersection(self, s: Iterable[Any]) -> 'OrderedSet':
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

    def symmetric_difference(self, s: Iterable[Hashable]) -> 'OrderedSet':
        return OrderedSet(
            dict.fromkeys([e for e in self._dict if e not in s] +
                          [e for e in s if e not in self._dict]))

    def symmetric_difference_update(self, s: Iterable[Hashable]) -> None:
        self._dict = self.symmetric_difference(s)._dict

    def union(self, s: Iterable[Hashable]) -> 'OrderedSet':
        return OrderedSet({**self._dict, **dict.fromkeys(s)})

    def update(self, s: Iterable[Hashable]) -> None:
        self._dict = self.union(s)._dict

    def __len__(self) -> int:
        return len(self._dict)

    def __contains__(self, o: object) -> bool:
        return o in self._dict

    def __iter__(self) -> Iterator[Hashable]:
        return iter(self._dict)

    def __and__(self, s: Set[Hashable]) -> 'OrderedSet':
        return self.intersection(s)

    def __iand__(self, s: Set[Hashable]) -> 'OrderedSet':
        result = self.intersection(s)
        self._dict = result._dict
        return result

    def __or__(self, s: Set[Hashable]) -> 'OrderedSet':
        return self.union(s)

    def __ior__(self, s: Set[Hashable]) -> 'OrderedSet':
        result = self.union(s)
        self._dict = result._dict
        return result

    def __sub__(self, s: Set[Hashable]) -> 'OrderedSet':
        return self.difference(s)

    def __isub__(self, s: Set[Hashable]) -> 'OrderedSet':
        result = self.difference(s)
        self._dict = result._dict
        return result

    def __xor__(self, s: Set[Hashable]) -> 'OrderedSet':
        return self.symmetric_difference(s)

    def __ixor__(self, s: Set[Hashable]) -> 'OrderedSet':
        result = self.symmetric_difference(s)
        self._dict = result._dict
        return result

    def __le__(self, s: Set[Hashable]) -> bool:
        return self.issubset(s)

    def __lt__(self, s: Set[Hashable]) -> bool:
        return self.issubset(s) and len(self) < len(s)

    def __ge__(self, s: Set[Hashable]) -> bool:
        return set(self) >= set(s)

    def __gt__(self, s: Set[Hashable]) -> bool:
        return set(self) > set(s)


class FrozenOrderedSet(OrderedSet):
    def __init__(self, base: Optional[Iterable[Hashable]] = None) -> None:
        super().__init__()
        self._dict: frozendict[Hashable, None]
        if not base:
            self._dict = frozendict({})
        elif isinstance(base, frozendict):
            self._dict = base
        else:
            self._dict = frozendict.fromkeys(base)

    def __hash__(self) -> int:
        return type(self) ^ hash(self._dict)

    def __repr__(self) -> str:
        if len(self) == 0:
            return "FrozenOrderedSet()"
        return "FrozenOrderedSet({" + ", ".join(list(map(str, self._dict))) + "})"

    def add(self, element: Hashable) -> None:
        raise NotImplementedError('Cannot add to FrozenOrderedSet')

    def clear(self) -> None:
        raise NotImplementedError('Cannot clear FrozenOrderedSet')

    def copy(self) -> 'FrozenOrderedSet':
        return FrozenOrderedSet(self._dict)

    def difference(self, s: Iterable[Any]) -> 'FrozenOrderedSet':
        return FrozenOrderedSet(frozendict({e: None for e in self._dict if e not in s}))

    def difference_update(self, s: Iterable[Any]) -> None:
        self._dict = frozendict(
            {e: None for e in self._dict if e not in s})

    def discard(self, element: Hashable) -> None:
        raise NotImplementedError('Cannot discard from FrozenOrderedSet')

    def intersection(self, s: Iterable[Any]) -> 'FrozenOrderedSet':
        return FrozenOrderedSet(frozendict({e: None for e in self._dict if e in s}))

    def intersection_update(self, s: Iterable[Any]) -> None:
        self._dict = FrozenOrderedSet(frozendict(
            {e: None for e in self._dict if e in s}))

    def pop(self) -> Hashable:
        raise NotImplementedError('Cannot pop from FrozenOrderedSet')

    def remove(self, element: Hashable) -> None:
        raise NotImplementedError('Cannot remove from FrozenOrderedSet')

    def symmetric_difference(self, s: Iterable[Hashable]) -> 'FrozenOrderedSet[T]':
        return FrozenOrderedSet(
            frozendict.fromkeys([e for e in self._dict if e not in s] +
                                [e for e in s if e not in self._dict]))

    def symmetric_difference_update(self, s: Iterable[Hashable]) -> None:
        raise NotImplementedError('Cannot update FrozenOrderedSet')

    def union(self, s: Iterable[Hashable]) -> 'FrozenOrderedSet[T]':
        return FrozenOrderedSet(frozendict({**self._dict, **dict.fromkeys(s)}))

    def update(self, s: Iterable[Hashable]) -> None:
        raise NotImplementedError('Cannot update FrozenOrderedSet')

    def __and__(self, s: Set[Hashable]) -> 'FrozenOrderedSet[T]':
        return self.intersection(s)

    def __iand__(self, s: Set[Hashable]) -> 'FrozenOrderedSet[T]':
        raise NotImplementedError('Cannot update FrozenOrderedSet')

    def __or__(self, s: Set[Hashable]) -> 'FrozenOrderedSet[Union[T, S]]':
        return self.union(s)

    def __ior__(self, s: Set[Hashable]) -> 'FrozenOrderedSet[Union[T, S]]':
        raise NotImplementedError('Cannot update FrozenOrderedSet')

    def __sub__(self, s: Set[Hashable]) -> 'FrozenOrderedSet[T]':
        return self.difference(s)

    def __isub__(self, s: Set[Hashable]) -> 'FrozenOrderedSet[T]':
        raise NotImplementedError('Cannot update FrozenOrderedSet')

    def __xor__(self, s: Set[Hashable]) -> 'FrozenOrderedSet[Union[T, S]]':
        return self.symmetric_difference(s)

    def __ixor__(self, s: Set[Hashable]) -> 'FrozenOrderedSet[Union[T, S]]':
        raise NotImplementedError('Cannot update FrozenOrderedSet')
