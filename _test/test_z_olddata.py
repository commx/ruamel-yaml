# coding: utf-8

import sys
import os
import pytest  # type: ignore  # NOQA

sys.path.insert(0, os.path.dirname(__file__) + '/lib')

import warnings  # NOQA

from typing import List, Any  # NOQA

args: List[Any] = []


def test_data() -> None:
    import test_appliance  # type: ignore  # NOQA

    warnings.simplefilter('ignore', PendingDeprecationWarning)
    collections = []
    import test_yaml  # type: ignore

    collections.append(test_yaml)
    test_appliance.run(collections, args)


# @pytest.mark.skipif(not ruamel.yaml.__with_libyaml__,
#                     reason="no libyaml")


def test_data_ext() -> None:
    collections = []
    import ruamel.yaml  # NOQA
    import test_appliance  # NOQA

    warnings.simplefilter('ignore', ruamel.yaml.error.UnsafeLoaderWarning)
    warnings.simplefilter('ignore', PendingDeprecationWarning)
    if ruamel.yaml.__with_libyaml__:
        import test_yaml_ext  # type: ignore

        collections.append(test_yaml_ext)
        test_appliance.run(collections, args)
