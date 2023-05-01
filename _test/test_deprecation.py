# coding: utf-8

import sys
import pytest  # type:ignore  # NOQA


@pytest.mark.skipif(sys.version_info < (3, 7) or sys.version_info >= (3, 9),  # type: ignore
                    reason='collections not available?')
def test_collections_deprecation() -> None:
    with pytest.warns(DeprecationWarning):
        from collections import Hashable  # type: ignore  # NOQA
