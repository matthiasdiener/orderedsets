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

import os
import sys
from typing import Any, Callable, Dict, Optional

import pytest

from orderedsets import FrozenOrderedSet

# {{{ test infrastructure


def run_test_with_new_python_invocation(f: Callable[..., Any], *args: Any,
                                        extra_env_vars:
                                        Optional[Dict[str, Any]] = None) -> None:
    if extra_env_vars is None:
        extra_env_vars = {}

    from base64 import b64encode
    from pickle import dumps
    from subprocess import check_call

    env_vars = {
        "INVOCATION_INFO": b64encode(dumps((f, args))).decode(),
    }
    env_vars.update(extra_env_vars)

    my_env = os.environ.copy()
    my_env.update(env_vars)

    check_call([sys.executable, __file__], env=my_env)


def run_test_with_new_python_invocation_inner() -> None:
    from base64 import b64decode
    from pickle import loads
    f, args = loads(b64decode(os.environ["INVOCATION_INFO"].encode()))

    f(*args)

# }}}


# {{{ test that pickling a FrozenOrderedSet recomputes the hash on unpickling

_set_data = ["a", "b", "c"]


@pytest.mark.xfail(reason="needs fix for caching hash value issue")
def test_pickle_hash() -> None:
    from pickle import dumps

    f1 = FrozenOrderedSet(_set_data)
    print(hash(f1))  # Force creating a cached hash value

    assert f1._my_hash
    run_test_with_new_python_invocation(_test_pickle_hash_stage2, dumps(f1),
                                        hash(f1))


def _test_pickle_hash_stage2(pickle_dumps: bytes, old_hash: int) -> None:
    from pickle import loads
    f1 = FrozenOrderedSet(_set_data)  # same set as above

    f2 = loads(pickle_dumps)
    assert f1 == f2
    print(hash(f1), hash(f2), old_hash)

    # If the hash value is restored from the pickle file, then the hash values
    # would not be equal, because the hash changes on each Python execution.
    assert hash(f1) == hash(f2)

    # Make sure the hash value has changed after unpickling.
    assert hash(f2) != old_hash

# }}}


if __name__ == "__main__":
    if "INVOCATION_INFO" in os.environ:
        run_test_with_new_python_invocation_inner()
    elif len(sys.argv) > 1:
        exec(sys.argv[1])
    else:
        from pytest import main
        main([__file__])
