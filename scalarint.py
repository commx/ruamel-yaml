# coding: utf-8

from __future__ import print_function, absolute_import, division, unicode_literals

import sys

if sys.version_info >= (3, 5, 2):
    from typing import Text, Any, Dict, List  # NOQA

__all__ = ["ScalarInt", "BinaryInt", "OctalInt", "HexInt", "HexCapsInt"]


class ScalarInt(int):
    __slots__ = ()

    def __new__(cls, *args, **kw):
        # type: (Any, Any) -> Any
        return int.__new__(cls, *args, **kw)  # type: ignore

    def __iadd__(self, a):  # type: ignore
        # type: (Any) -> Any
        return type(self)(self + a)

    def __ifloordiv__(self, a):  # type: ignore
        # type: (Any) -> Any
        return type(self)(self // a)

    def __imul__(self, a):  # type: ignore
        # type: (Any) -> Any
        return type(self)(self * a)

    def __ipow__(self, a):  # type: ignore
        # type: (Any) -> Any
        return type(self)(self ** a)

    def __isub__(self, a):  # type: ignore
        # type: (Any) -> Any
        return type(self)(self - a)


class BinaryInt(ScalarInt):
    __slots__ = ()

    def __new__(cls, value):
        # type: (Text) -> Any
        return ScalarInt.__new__(cls, value)


class OctalInt(ScalarInt):
    __slots__ = ()

    def __new__(cls, value):
        # type: (Text) -> Any
        return ScalarInt.__new__(cls, value)


# mixed casing of A-F is not supported, when loading the first non digit
# determines the case

class HexInt(ScalarInt):
    """uses lower case (a-f)"""
    __slots__ = ()

    def __new__(cls, value):
        # type: (Text) -> Any
        return ScalarInt.__new__(cls, value)


class HexCapsInt(ScalarInt):
    """uses upper case (A-F)"""
    __slots__ = ()

    def __new__(cls, value):
        # type: (Text) -> Any
        return ScalarInt.__new__(cls, value)
