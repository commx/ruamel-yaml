from __future__ import absolute_import

__all__ = ['BaseLoader', 'SafeLoader', 'Loader', 'RoundTripLoader']

try:
    from .reader import *
    from .scanner import *
    from .parser_ import *
    from .composer import *
    from .constructor import *
    from .resolver import *
except (ImportError, ValueError):  # for Jython
    from ruamel.yaml.reader import *
    from ruamel.yaml.scanner import *
    from ruamel.yaml.parser_ import *
    from ruamel.yaml.composer import *
    from ruamel.yaml.constructor import *
    from ruamel.yaml.resolver import *



class BaseLoader(Reader, Scanner, Parser, Composer, BaseConstructor,
                 BaseResolver):
    def __init__(self, stream):
        Reader.__init__(self, stream)
        Scanner.__init__(self)
        Parser.__init__(self)
        Composer.__init__(self)
        BaseConstructor.__init__(self)
        BaseResolver.__init__(self)


class SafeLoader(Reader, Scanner, Parser, Composer, SafeConstructor, Resolver):
    def __init__(self, stream):
        Reader.__init__(self, stream)
        Scanner.__init__(self)
        Parser.__init__(self)
        Composer.__init__(self)
        SafeConstructor.__init__(self)
        Resolver.__init__(self)


class Loader(Reader, Scanner, Parser, Composer, Constructor, Resolver):

    def __init__(self, stream):
        Reader.__init__(self, stream)
        Scanner.__init__(self)
        Parser.__init__(self)
        Composer.__init__(self)
        Constructor.__init__(self)
        Resolver.__init__(self)


class RoundTripLoader(Reader, RoundTripScanner, Parser,
                      Composer, RoundTripConstructor, Resolver):
    def __init__(self, stream):
        Reader.__init__(self, stream)
        RoundTripScanner.__init__(self)
        Parser.__init__(self)
        Composer.__init__(self)
        RoundTripConstructor.__init__(self)
        Resolver.__init__(self)
