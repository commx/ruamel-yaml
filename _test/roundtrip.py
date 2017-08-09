
from __future__ import print_function

"""
helper routines for testing round trip of commented YAML data
"""
import sys
import textwrap

import ruamel.yaml
from ruamel.yaml.compat import StringIO, BytesIO  # NOQA


def dedent(data):
    try:
        position_of_first_newline = data.index('\n')
        for idx in range(position_of_first_newline):
            if not data[idx].isspace():
                raise ValueError
    except ValueError:
        pass
    else:
        data = data[position_of_first_newline + 1:]
    return textwrap.dedent(data)


def round_trip_load(inp, preserve_quotes=None, version=None):
    dinp = dedent(inp)
    return ruamel.yaml.load(
        dinp,
        Loader=ruamel.yaml.RoundTripLoader,
        preserve_quotes=preserve_quotes,
        version=version,
    )


def round_trip_load_all(inp, preserve_quotes=None, version=None):
    dinp = dedent(inp)
    return ruamel.yaml.load_all(
        dinp,
        Loader=ruamel.yaml.RoundTripLoader,
        preserve_quotes=preserve_quotes,
        version=version,
    )


def round_trip_dump(data, indent=None, block_seq_indent=None, top_level_colon_align=None,
                    prefix_colon=None, explicit_start=None, explicit_end=None, version=None):
    return ruamel.yaml.round_trip_dump(data,
                                       indent=indent, block_seq_indent=block_seq_indent,
                                       top_level_colon_align=top_level_colon_align,
                                       prefix_colon=prefix_colon,
                                       explicit_start=explicit_start,
                                       explicit_end=explicit_end,
                                       version=version)


def diff(inp, outp, file_name='stdin'):
    import difflib
    inl = inp.splitlines(True)  # True for keepends
    outl = outp.splitlines(True)
    diff = difflib.unified_diff(inl, outl, file_name, 'round trip YAML')
    # 2.6 difflib has trailing space on filename lines %-)
    strip_trailing_space = sys.version_info < (2, 7)
    for line in diff:
        if strip_trailing_space and line[:4] in ['--- ', '+++ ']:
            line = line.rstrip() + '\n'
        sys.stdout.write(line)


def round_trip(inp, outp=None, extra=None, intermediate=None, indent=None,
               block_seq_indent=None, top_level_colon_align=None, prefix_colon=None,
               preserve_quotes=None,
               explicit_start=None, explicit_end=None,
               version=None):
    """
    inp:    input string to parse
    outp:   expected output (equals input if not specified)
    """
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
                          prefix_colon=prefix_colon,
                          explicit_start=explicit_start,
                          explicit_end=explicit_end,
                          version=version)
    if res != doutp:
        diff(doutp, res, "input string")
    print('\nroundtrip data:\n', res, sep='')
    assert res == doutp
    res = round_trip_dump(data, indent=indent, block_seq_indent=block_seq_indent,
                          top_level_colon_align=top_level_colon_align,
                          prefix_colon=prefix_colon,
                          explicit_start=explicit_start,
                          explicit_end=explicit_end,
                          version=version)
    print('roundtrip second round data:\n', res, sep='')
    assert res == doutp
    return data


class YAML(ruamel.yaml.YAML):
    """auto dedent string parameters on load"""
    def load(self, stream):
        if isinstance(stream, str):
            if stream and stream[0] == '\n':
                stream = stream[1:]
            stream = textwrap.dedent(stream)
        return ruamel.yaml.YAML.load(self, stream)

    def load_all(self, stream):
        if isinstance(stream, str):
            if stream and stream[0] == '\n':
                stream = stream[1:]
            stream = textwrap.dedent(stream)
        for d in ruamel.yaml.YAML.load_all(self, stream):
            yield d

    def dump(self, data, **kw):
        assert ('stream' in kw) ^ ('compare' in kw)
        if 'stream' in kw:
            return ruamel.yaml.YAML.dump(data, **kw)
        lkw = kw.copy()
        expected = textwrap.dedent(lkw.pop('compare'))
        unordered_lines = lkw.pop('unordered_lines', False)
        if expected and expected[0] == '\n':
            expected = expected[1:]
        lkw['stream'] = st = StringIO()
        ruamel.yaml.YAML.dump(self, data, **lkw)
        res = st.getvalue()
        print(res)
        if unordered_lines:
            res = sorted(res.splitlines())
            expected = sorted(expected.splitlines())
        assert res == expected
