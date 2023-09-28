# coding: utf-8

"""
helper routines for testing round trip of commented YAML data
"""
import sys
import textwrap
import io
from pathlib import Path

from typing import Any, Optional, Union

unset = object()


def dedent(data: str) -> str:
    try:
        position_of_first_newline = data.index('\n')
        for idx in range(position_of_first_newline):
            if not data[idx].isspace():
                raise ValueError
    except ValueError:
        pass
    else:
        data = data[position_of_first_newline + 1 :]
    return textwrap.dedent(data)


def round_trip_load(
    inp: Any, preserve_quotes: Optional[bool] = None, version: Optional[Any] = None,
) -> Any:
    import ruamel.yaml  # NOQA

    dinp = dedent(inp)
    yaml = ruamel.yaml.YAML()
    yaml.preserve_quotes = preserve_quotes
    yaml.version = version
    return yaml.load(dinp)


def round_trip_load_all(
    inp: Any, preserve_quotes: Optional[bool] = None, version: Optional[Any] = None,
) -> Any:
    import ruamel.yaml  # NOQA

    dinp = dedent(inp)
    yaml = ruamel.yaml.YAML()
    yaml.preserve_quotes = preserve_quotes
    yaml.version = version
    return yaml.load_all(dinp)


def round_trip_dump(
    data: Any,
    stream: Any = None,  # *,
    indent: Optional[int] = None,
    block_seq_indent: Optional[int] = None,
    default_flow_style: Any = unset,
    top_level_colon_align: Any = None,
    prefix_colon: Any = None,
    explicit_start: Optional[bool] = None,
    explicit_end: Optional[bool] = None,
    version: Optional[Any] = None,
    allow_unicode: bool = True,
) -> Union[str, None]:
    import ruamel.yaml  # NOQA

    yaml = ruamel.yaml.YAML()
    yaml.indent(mapping=indent, sequence=indent, offset=block_seq_indent)
    if default_flow_style is not unset:
        yaml.default_flow_style = default_flow_style
    yaml.top_level_colon_align = top_level_colon_align
    yaml.prefix_colon = prefix_colon
    yaml.explicit_start = explicit_start
    yaml.explicit_end = explicit_end
    yaml.version = version
    yaml.allow_unicode = allow_unicode
    if stream is not None:
        yaml.dump(data, stream=stream)
        return None
    buf = io.StringIO()
    yaml.dump(data, stream=buf)
    return buf.getvalue()


def round_trip_dump_all(
    data: Any,
    stream: Any = None,  # *,
    indent: Optional[int] = None,
    block_seq_indent: Optional[int] = None,
    default_flow_style: Any = unset,
    top_level_colon_align: Any = None,
    prefix_colon: Any = None,
    explicit_start: Optional[bool] = None,
    explicit_end: Optional[bool] = None,
    version: Optional[Any] = None,
    allow_unicode: bool = True,
) -> Union[str, None]:
    import ruamel.yaml  # NOQA

    yaml = ruamel.yaml.YAML()
    yaml.indent(mapping=indent, sequence=indent, offset=block_seq_indent)
    if default_flow_style is not unset:
        yaml.default_flow_style = default_flow_style
    yaml.top_level_colon_align = top_level_colon_align
    yaml.prefix_colon = prefix_colon
    yaml.explicit_start = explicit_start
    yaml.explicit_end = explicit_end
    yaml.version = version
    yaml.allow_unicode = allow_unicode
    if stream is not None:
        yaml.dump(data, stream=stream)
        return None
    buf = io.StringIO()
    yaml.dump_all(data, stream=buf)
    return buf.getvalue()


def diff(inp: str, outp: str, file_name: str = 'stdin') -> None:
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


def round_trip(
    inp: str,
    outp: Optional[str] = None,
    extra: Optional[str] = None,
    intermediate: Any = None,
    indent: Optional[int] = None,
    block_seq_indent: Optional[int] = None,
    default_flow_style: Any = unset,
    top_level_colon_align: Any = None,
    prefix_colon: Any = None,
    preserve_quotes: Any = None,
    explicit_start: Optional[bool] = None,
    explicit_end: Optional[bool] = None,
    version: Optional[Any] = None,
    dump_data: Any = None,
) -> Any:
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
    if dump_data:
        print('data', data)
    if intermediate is not None:
        if isinstance(intermediate, dict):
            for k, v in intermediate.items():
                if data[k] != v:
                    print('{0!r} <> {1!r}'.format(data[k], v))
                    raise ValueError
    res = round_trip_dump(
        data,
        indent=indent,
        block_seq_indent=block_seq_indent,
        top_level_colon_align=top_level_colon_align,
        prefix_colon=prefix_colon,
        explicit_start=explicit_start,
        explicit_end=explicit_end,
        version=version,
    )
    assert isinstance(res, str)
    if res != doutp:
        diff(doutp, res, 'input string')
    print('\nroundtrip data:\n', res, sep="")
    assert res == doutp
    res = round_trip_dump(
        data,
        indent=indent,
        block_seq_indent=block_seq_indent,
        top_level_colon_align=top_level_colon_align,
        prefix_colon=prefix_colon,
        explicit_start=explicit_start,
        explicit_end=explicit_end,
        version=version,
    )
    print('roundtrip second round data:\n', res, sep="")
    assert res == doutp
    return data


def na_round_trip(
    inp: str,
    outp: Optional[str] = None,
    extra: Optional[str] = None,
    intermediate: Any = None,
    indent: Optional[int] = None,
    top_level_colon_align: Any = None,
    prefix_colon: Any = None,
    preserve_quotes: Any = None,
    explicit_start: Optional[bool] = None,
    explicit_end: Optional[bool] = None,
    version: Optional[Any] = None,
    dump_data: Any = None,
) -> Any:
    """
    inp:    input string to parse
    outp:   expected output (equals input if not specified)
    """
    inp = dedent(inp)
    if outp is None:
        outp = inp
    if version is not None:
        version = version
    doutp = dedent(outp)
    if extra is not None:
        doutp += extra
    yaml = YAML()
    yaml.preserve_quotes = preserve_quotes
    yaml.scalar_after_indicator = False  # newline after every directives end
    data = yaml.load(inp)
    if dump_data:
        print('data', data)
    if intermediate is not None:
        if isinstance(intermediate, dict):
            for k, v in intermediate.items():
                if data[k] != v:
                    print('{0!r} <> {1!r}'.format(data[k], v))
                    raise ValueError
    yaml.indent = indent
    yaml.top_level_colon_align = top_level_colon_align
    yaml.prefix_colon = prefix_colon
    yaml.explicit_start = explicit_start
    yaml.explicit_end = explicit_end
    res = yaml.dump(data, compare=doutp)
    return res


def YAML(**kw: Any) -> Any:
    import ruamel.yaml  # NOQA

    class MyYAML(ruamel.yaml.YAML):
        """auto dedent string parameters on load"""

        def load(self, stream: Any) -> Any:
            if isinstance(stream, str):
                if stream and stream[0] == '\n':
                    stream = stream[1:]
                stream = textwrap.dedent(stream)
            return ruamel.yaml.YAML.load(self, stream)

        def load_all(self, stream: Any) -> Any:
            if isinstance(stream, str):
                if stream and stream[0] == '\n':
                    stream = stream[1:]
                stream = textwrap.dedent(stream)
            for d in ruamel.yaml.YAML.load_all(self, stream):
                yield d

        def dump(self, data: Any, **kw: Any) -> Any:  # type: ignore
            from ruamel.yaml.compat import StringIO, BytesIO  # NOQA

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
                res = sorted(res.splitlines())  # type: ignore
                expected = sorted(expected.splitlines())  # type: ignore
            assert res == expected

        def round_trip(self, stream: Any, **kw: Any) -> None:
            from ruamel.yaml.compat import StringIO, BytesIO  # NOQA

            assert isinstance(stream, str)
            lkw = kw.copy()
            if stream and stream[0] == '\n':
                stream = stream[1:]
            stream = textwrap.dedent(stream)
            data = ruamel.yaml.YAML.load(self, stream)
            outp = lkw.pop('outp', stream)
            lkw['stream'] = st = StringIO()
            ruamel.yaml.YAML.dump(self, data, **lkw)
            res = st.getvalue()
            if res != outp:
                diff(outp, res, 'input string')
            assert res == outp

        def round_trip_all(self, stream: Any, **kw: Any) -> None:
            from ruamel.yaml.compat import StringIO, BytesIO  # NOQA

            assert isinstance(stream, str)
            lkw = kw.copy()
            if stream and stream[0] == '\n':
                stream = stream[1:]
            stream = textwrap.dedent(stream)
            data = list(ruamel.yaml.YAML.load_all(self, stream))
            outp = lkw.pop('outp', stream)
            lkw['stream'] = st = StringIO()
            ruamel.yaml.YAML.dump_all(self, data, **lkw)
            res = st.getvalue()
            if res != outp:
                diff(outp, res, 'input string')
            assert res == outp

    return MyYAML(**kw)


def save_and_run(
    program: str,
    base_dir: Optional[Any] = None,
    output: Optional[Any] = None,
    file_name: Optional[Any] = None,
    optimized: bool = False,
) -> int:
    """
    safe and run a python program, thereby circumventing any restrictions on module level
    imports
    """
    from subprocess import check_output, STDOUT, CalledProcessError

    if not hasattr(base_dir, 'hash'):
        base_dir = Path(str(base_dir))
    if file_name is None:
        file_name = 'safe_and_run_tmp.py'
    file_name = base_dir / file_name  # type: ignore
    file_name.write_text(dedent(program))

    try:
        cmd = [sys.executable, '-Wd']
        if optimized:
            cmd.append('-O')
        cmd.append(str(file_name))
        print('running:', *cmd)
        # 3.5 needs strings
        res = check_output(cmd, stderr=STDOUT, universal_newlines=True, cwd=str(base_dir))
        if output is not None:
            if '__pypy__' in sys.builtin_module_names:
                res1 = res.splitlines(True)
                res2 = [line for line in res1 if 'no version info' not in line]
                res = ''.join(res2)
            print('result:  ', res, end='')
            print('expected:', output, end='')
            assert res == output
    except CalledProcessError as exception:
        print("##### Running '{} {}' FAILED #####".format(sys.executable, file_name))
        print(exception.output)
        return exception.returncode
    return 0
