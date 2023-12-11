Welcome to orderedsets' documentation
=====================================

This site covers orderedsets' API documentation. For more information about orderedsets, see `the Github repository <https://github.com/matthiasdiener/orderedsets>`_.

Usage
-----

The :class:`.OrderedSet` class can be used as a drop-in replacement for :class:`set`.
To replace a :class:`frozenset`, you can use a :class:`.FrozenOrderedSet`. The
API is the same as :class:`.OrderedSet`, but without methods that mutate the
set.

.. literalinclude:: ../examples/demo.py
   :language: python

Some additional methods are provided, see the reference below.


API reference
-------------

.. toctree::
   :maxdepth: 1

   OrderedSets

   🚀 Github <https://github.com/matthiasdiener/orderedsets>
   💾 Download Releases <https://pypi.org/project/orderedsets>
