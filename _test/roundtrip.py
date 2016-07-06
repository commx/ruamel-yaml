
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


def round_trip_load(inp, preserve_quotes=None):
    dinp = dedent(inp)
    return ruamel.yaml.load(dinp, ruamel.yaml.RoundTripLoader, preserve_quotes=preserve_quotes)


def round_trip_dump(data, indent=None, block_seq_indent=None, top_level_colon_align=None,
                    prefix_colon=None):
    return ruamel.yaml.round_trip_dump(data,
                                       indent=indent, block_seq_indent=block_seq_indent,
                                       top_level_colon_align=top_level_colon_align,
                                       prefix_colon=prefix_colon)


def round_trip(inp, outp=None, extra=None, intermediate=None, indent=None,
               block_seq_indent=None, top_level_colon_align=None, prefix_colon=None,
               preserve_quotes=None):
    if outp is None:
        outp = inp
    doutp = dedent(outp)
    if extra is not None:
        doutp += extra
    data = round_trip_load(inp, preserve_quotes=preserve_quotes)
    if intermediate is not None:
        if isinstance(intermediate, dict):
            for k, v in intermediate.items():
                if data[k] != v:
                    print('{0!r} <> {1!r}'.format(data[k], v))
                    raise ValueError
    res = round_trip_dump(data, indent=indent, block_seq_indent=block_seq_indent,
                          top_level_colon_align=top_level_colon_align,
                          prefix_colon=prefix_colon)
    print('roundtrip data:\n', res, sep='')
    assert res == doutp
    res = round_trip_dump(data, indent=indent, block_seq_indent=block_seq_indent,
                          top_level_colon_align=top_level_colon_align,
                          prefix_colon=prefix_colon)
    print('roundtrip second round data:\n', res, sep='')
    assert res == doutp
