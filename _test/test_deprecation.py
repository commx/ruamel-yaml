# coding: utf-8

from __future__ import print_function

import sys
import pytest  # NOQA


@pytest.mark.skipif(sys.version_info < (3, 7), reason="collections not available?")
def test_collections_deprecation():
    with pytest.warns(DeprecationWarning):
        from collections import Hashable  # NOQA
