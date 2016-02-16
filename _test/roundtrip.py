
from __future__ import print_function

"""
helper routines for testing round trip of commented YAML data
"""
import textwrap

import ruamel.yaml


def dedent(data):
    try:
        position_of_first_newline = data.index('\n')
        for idx in range(position_of_first_newline):
            if not data[idx].isspace():
                raise ValueError
    except ValueError:
        pass
    else:
        data = data[position_of_first_newline+1:]
    return textwrap.dedent(data)


def round_trip_load(dinp):
    return ruamel.yaml.load(dinp, ruamel.yaml.RoundTripLoader)


def round_trip_dump(data, indent=None):
    dumper = ruamel.yaml.RoundTripDumper
    return ruamel.yaml.dump(data, default_flow_style=False, Dumper=dumper, indent=indent)


def round_trip(inp, outp=None, extra=None, intermediate=None):
    dinp = dedent(inp)
    if outp is not None:
        doutp = dedent(outp)
    else:
        doutp = dinp
    if extra is not None:
        doutp += extra
    data = round_trip_load(dinp)
    if intermediate is not None:
        if isinstance(intermediate, dict):
            for k, v in intermediate.items():
                if data[k] != v:
                    print('{0!r} <> {1!r}'.format(data[k], v))
                    raise ValueError
    res = round_trip_dump(data)
    print('roundtrip data:\n', res, sep='')
    assert res == doutp
    res = round_trip_dump(data)
    print('roundtrip second round data:\n', res, sep='')
    assert res == doutp
