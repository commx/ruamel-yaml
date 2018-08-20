# coding: utf-8

from __future__ import print_function, absolute_import, division, unicode_literals

from ruamel.yaml.compat import text_type

if False:  # MYPY
    from typing import Text, Any, Dict, List  # NOQA

__all__ = [
    'ScalarString',
    'PreservedScalarString',
    'SingleQuotedScalarString',
    'DoubleQuotedScalarString',
]


class ScalarString(text_type):
    __slots__ = ()

    def __new__(cls, *args, **kw):
        # type: (Any, Any) -> Any
        return text_type.__new__(cls, *args, **kw)  # type: ignore

    def replace(self, old, new, maxreplace=-1):
        # type: (Any, Any, int) -> Any
        return type(self)((text_type.replace(self, old, new, maxreplace)))


class PreservedScalarString(ScalarString):
    __slots__ = 'comment'  # the comment after the | on the first line

    style = '|'

    def __new__(cls, value):
        # type: (Text) -> Any
        return ScalarString.__new__(cls, value)


class SingleQuotedScalarString(ScalarString):
    __slots__ = ()

    style = "'"

    def __new__(cls, value):
        # type: (Text) -> Any
        return ScalarString.__new__(cls, value)


class DoubleQuotedScalarString(ScalarString):
    __slots__ = ()

    style = '"'

    def __new__(cls, value):
        # type: (Text) -> Any
        return ScalarString.__new__(cls, value)


def preserve_literal(s):
    # type: (Text) -> Text
    return PreservedScalarString(s.replace('\r\n', '\n').replace('\r', '\n'))


def walk_tree(base, map=None):
    # type: (Any) -> None
    """
    the routine here walks over a simple yaml tree (recursing in
    dict values and list items) and converts strings that
    have multiple lines to literal scalars

    You can also provide an explicit (ordered) mapping for multiple transforms
    (first of which is executed):
        map = ruamel.yaml.compat.ordereddict
        map['\n'] = preserve_literal
        map[':'] = SingleQuotedScalarString
        walk_tree(data, map=map)
    """
    from ruamel.yaml.compat import string_types, MutableMapping, MutableSequence

    if map is None:
        map = {'\n': preserve_literal}

    if isinstance(base, MutableMapping):
        for k in base:
            v = base[k]  # type: Text
            if isinstance(v, string_types):
                for ch in map:
                    if ch in v:
                        base[k] = map[ch](v)
                        break
            else:
                walk_tree(v)
    elif isinstance(base, MutableSequence):
        for idx, elem in enumerate(base):
            if isinstance(elem, string_types):
                for ch in map:
                    if ch in elem:
                        base[idx] = map[ch](elem)
                        break
            else:
                walk_tree(elem)
