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
