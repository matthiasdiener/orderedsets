[![PyPI version](https://badge.fury.io/py/orderedsets.svg)](https://badge.fury.io/py/orderedsets)
![License](https://img.shields.io/pypi/l/orderedsets)
![PyPI - Downloads](https://img.shields.io/pypi/dm/orderedsets)


# orderedsets

An implementation of mutable and immutable ordered sets as thin wrappers around
Python's `dict` class for the `OrderedSet` class, and
[immutabledict](https://github.com/corenting/immutabledict) for the `FrozenOrderedSet` class.
These classes are meant as drop-in replacements for Python's builtin `set` and
`frozenset` classes.

In contrast to Python's builtin `set` and `frozenset` classes, the order of
items is kept (generally, insertion order), such that iterating over items in
the set as well as mutating operations are deterministic.

This package requires the [immutabledict](https://github.com/corenting/immutabledict)
package for the immutable set class, but has no other external dependencies.


## Usage

```
$ pip install orderedsets
```

```python
from orderedsets import OrderedSet, FrozenOrderedSet
os = OrderedSet([1, 2, 4])
os.add(0)
assert list(os) == [1, 2, 4, 0]

fos = FrozenOrderedSet([1, 2, 4])
# a.add(0)  # raises AttributeError: 'FrozenOrderedSet' object has no attribute 'add'
assert list(fos) == [1, 2, 4]
```

## Inspirations

### Packages

- https://github.com/rindPHI/proxyorderedset/ (not 100% compatible with set)
- https://pypi.org/project/ordered-set/ (no frozen/immutable class)
- https://pypi.org/project/stableset/ (no frozen/immutable class)
- https://pypi.org/project/orderedset/ (Cython, no frozen/immutable class)
- https://pypi.org/project/Ordered-set-37/ (no frozen/immutable class)

### Discussions

- https://discuss.python.org/t/add-orderedset-to-stdlib/12730


## TODOs
