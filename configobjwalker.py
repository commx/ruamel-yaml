# coding: utf-8

import warnings

from ruamel.yaml.util import configobj_walker as new_configobj_walker

import sys
if sys.version_info >= (3, 5, 2):
    from typing import Any  # NOQA


def configobj_walker(cfg):
    # type: (Any) -> Any
    warnings.warn("configobj_walker has moved to ruamel.yaml.util, please update your code")
    return new_configobj_walker(cfg)
