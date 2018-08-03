# coding: utf-8

from test_mark import *  # NOQA
from test_reader import *  # NOQA
from test_canonical import *  # NOQA
from test_tokens import *  # NOQA
from test_structure import *  # NOQA
from test_errors import *  # NOQA
from test_resolver import *  # NOQA
from test_constructor import *  # NOQA
from test_emitter import *  # NOQA
from test_representer import *  # NOQA
from test_recursive import *  # NOQA
from test_input_output import *  # NOQA

if __name__ == '__main__':
    import sys
    import test_appliance

    sys.exit(test_appliance.run(globals()))
