Welcome to orderedsets' documentation
=====================================

This site covers orderedsets' API documentation. For more information about orderedsets, see `the Github repository <https://github.com/matthiasdiener/orderedsets>`_.

Usage
-----

The :class:`.OrderedSet`  class can be used as a drop-in replacement for :class:`set`.

For replacing a :class:`frozenset`, you can use a :class:`.FrozenOrderedSet`. The API is the same as :class:`.OrderedSet`, but it uses an :class:`immutabledict.immutabledict` under the hood.

.. code-block:: python

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

Some additional methods are provided, see the reference below.


API reference
-------------

.. toctree::
   :maxdepth: 1

   OrderedSets

   🚀 Github <https://github.com/matthiasdiener/orderedsets>
   💾 Download Releases <https://pypi.org/project/orderedsets>
