# coding: utf-8

from __future__ import absolute_import

_package_data = dict(
    full_package_name='ruamel.yaml',
    version_info=(0, 10, 7),
    author='Anthon van der Neut',
    author_email='a.van.der.neut@ruamel.eu',
    description="ruamel.yaml is a YAML parser/emitter that supports roundtrip preservation of comments, seq/map flow style, and map key order",  # NOQA
    entry_points=None,
    install_requires=['ruamel.base']
)

def _convert_version(tup):
    """create a PEP 386 pseudo-format conformant string from tuple tup"""
    ret_val = str(tup[0])  # first is always digit
    next_sep = "."  # separator for next extension, can be "" or "."
    for x in tup[1:]:
        if isinstance(x, int):
            ret_val += next_sep + str(x)
            next_sep = '.'
            continue
        first_letter = x[0].lower()
        next_sep = ''
        if first_letter in 'abcr':
            ret_val += 'rc' if first_letter == 'r' else first_letter
        elif first_letter in 'pd':
            ret_val += '.post' if first_letter == 'p' else '.dev'
    return ret_val


# <
version_info = _package_data['version_info']
__version__ = _convert_version(version_info)

del _convert_version

try:
    from .cyaml import *
    __with_libyaml__ = True
except ImportError:
    __with_libyaml__ = False

import sys

# body extracted to main.py
from .main import *

def main():
    # No direct import of yaml in order not to pollute namespace.
    # If other utility 'bodies' exist in this directory a module level
    # import here, would get you all of its initialisations/imports as well
    from ruamel.yaml import main as util_main
    util_main()
