[![PyPI version](https://badge.fury.io/py/orderedsets.svg)](https://badge.fury.io/py/orderedsets)
[![Doc Status](https://img.shields.io/github/actions/workflow/status/matthiasdiener/orderedsets/doc.yaml?label=docs)](https://matthiasdiener.github.io/orderedsets)
[![License](https://img.shields.io/pypi/l/orderedsets)](https://github.com/matthiasdiener/orderedsets/blob/main/LICENSE)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/orderedsets)](https://badge.fury.io/py/orderedsets)

# orderedsets

An implementation of mutable and immutable ordered sets as thin wrappers around
Python's `dict` class.
These classes are meant as drop-in replacements for Python's builtin `set` and
`frozenset` classes. Care has been taken to provide the same functionality as the Python classes,
without API additions or removals, to allow easy switching between set implementations.

In contrast to Python's builtin `set` and `frozenset` classes, the order of
items is kept (generally, insertion order), such that iterating over items in
the set as well as mutating operations are deterministic.

This package has no external dependencies.


## Usage

Install this package with:
```
$ pip install orderedsets
```

Usage example:
```python
from orderedsets import OrderedSet, FrozenOrderedSet

os = OrderedSet([1, 2, 4])
os.add(0)
assert list(os) == [1, 2, 4, 0]
os.remove(0)

fos = FrozenOrderedSet([1, 2, 4])
# a.add(0)  # raises AttributeError: 'FrozenOrderedSet' object has no attribute 'add'
assert list(fos) == [1, 2, 4]

# sets with the same elements compare equal
assert os == fos == set([1, 2, 4]) == frozenset([1, 2, 4])

# only immutable sets can be hashed
assert hash(fos) == hash(frozenset([1, 2, 4]))
```

Please also see the [documentation](https://matthiasdiener.github.io/orderedsets).


## References

### Other packages

- https://github.com/rindPHI/proxyorderedset/ (not 100% compatible with set)
- https://pypi.org/project/ordered-set/ (no frozen/immutable class)
- https://pypi.org/project/stableset/ (no frozen/immutable class)
- https://pypi.org/project/orderedset/ (Cython, no frozen/immutable class)
- https://pypi.org/project/Ordered-set-37/ (no frozen/immutable class)

### Discussions

- https://discuss.python.org/t/add-orderedset-to-stdlib/12730

### Python implementations

- https://github.com/python/cpython/blob/main/Objects/setobject.c
- https://github.com/python/cpython/blob/main/Objects/dictobject.c
