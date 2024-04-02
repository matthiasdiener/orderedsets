# Simple speed test for various set implementations

from timeit import timeit

import ordered_set
import orderedset
# https://github.com/idanmiara/ordered-set (pip install stableset), v5.2.1:
from ordered_set import OrderedSet as ordered_set2  # noqa: F401, N813
# https://github.com/simonpercivall/orderedset (pip install orderedset), v2.0.3:
from orderedset import OrderedSet as cython_ordered_set  # noqa: F401, N813

import orderedsets
from orderedsets import FrozenOrderedSet, OrderedSet  # noqa: F401

print(f"Versions:\norderedsets={orderedsets.__version__},\n"
      f"orderedset={orderedset.__version__},\n"
      f"ordered_set={ordered_set.__version__}")


for base_set in [{1}, set(range(1000))]:
    print("\nbase_set length:", len(base_set), "\n=====================")

    for set_impl in ("set", "frozenset", "OrderedSet", "FrozenOrderedSet",
                     "cython_ordered_set", "ordered_set2"):

        print(set_impl)

        print("  creation\t", timeit(f"{set_impl}({base_set})",
                                     number=10000, globals=globals()))

        try:
            print("  hash\t\t", timeit(f"hash({set_impl}({base_set}))",
                                       number=10000, globals=globals()))
        except (AttributeError, TypeError):
            print("  hash MISSING")

        try:
            print("  hash2\t\t", timeit("for i in range(1000): hash(x)",
                                        setup=f"x={set_impl}({base_set})",
                                        number=10000, globals=globals()))
        except (AttributeError, TypeError):
            print("  hash2 MISSING")

        print("  elem_access\t", timeit("next(iter(x))",
                                        setup=f"x={set_impl}({base_set})",
                                        number=10000, globals=globals()))

        print("  list(keys)\t", timeit(f"list({set_impl}({base_set}))",
                                       number=10000, globals=globals()))

        print("  union\t\t", timeit("x.union(y)",
                                    setup=f"x={set_impl}({base_set});"
                                          f"y={set_impl}({base_set})",
                                    number=10000, globals=globals()))

        print("  intersection\t", timeit("x.intersection(y)",
                                         setup=f"x={set_impl}({base_set});"
                                               f"y={set_impl}({base_set})",
                                         number=10000, globals=globals()))

        try:
            print("  add\t\t", timeit("x.add(y)",
                                      setup=f"x={set_impl}({base_set});"
                                            f"y={next(iter(base_set))}",
                                      number=10000, globals=globals()))
        except AttributeError:
            print("  add MISSING")
