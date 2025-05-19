# coding: utf-8

from typing import Any
import pytest  # type: ignore  # NOQA

from roundtrip import round_trip, round_trip_load, round_trip_dump, dedent, YAML  # type: ignore  # NOQA


def rt(s: str) -> str:
    res = round_trip_dump(round_trip_load(s))
    assert res is not None
    return res.strip() + '\n'  # type: ignore


class TestIndent:
    def test_roundtrip_inline_list(self) -> None:
        s = 'a: [a, b, c]\n'
        output = rt(s)
        assert s == output

    def test_roundtrip_mapping_of_inline_lists(self) -> None:
        s = dedent("""\
        a: [a, b, c]
        j: [k, l, m]
        """)
        output = rt(s)
        assert s == output

    def test_roundtrip_mapping_of_inline_lists_comments(self) -> None:
        s = dedent("""\
        # comment A
        a: [a, b, c]
        # comment B
        j: [k, l, m]
        """)
        output = rt(s)
        assert s == output

    def test_roundtrip_mapping_of_inline_sequence_eol_comments(self) -> None:
        s = dedent("""\
        # comment A
        a: [a, b, c]  # comment B
        j: [k, l, m]  # comment C
        """)
        output = rt(s)
        assert s == output

    # first test by explicitly setting flow style
    def test_added_inline_list(self) -> None:
        s1 = dedent("""
        a:
        - b
        - c
        - d
        """)
        s = 'a: [b, c, d]\n'
        data = round_trip_load(s1)
        val = data['a']
        val.fa.set_flow_style()
        # print(type(val), '_yaml_format' in dir(val))
        output = round_trip_dump(data)
        assert s == output

    # ############ flow mappings

    def test_roundtrip_flow_mapping(self) -> None:
        s = dedent("""\
        - {a: 1, b: hallo}
        - {j: fka, k: 42}
        """)
        data = round_trip_load(s)
        output = round_trip_dump(data)
        assert s == output

    def test_roundtrip_sequence_of_inline_mappings_eol_comments(self) -> None:
        s = dedent("""\
        # comment A
        - {a: 1, b: hallo}  # comment B
        - {j: fka, k: 42}  # comment C
        """)
        output = rt(s)
        assert s == output

    def test_indent_top_level(self) -> None:
        inp = """
        -   a:
            -   b
        """
        round_trip(inp, indent=4)

    def test_set_indent_5_block_list_indent_1(self) -> None:
        inp = """
        a:
         -   b: c
         -   1
         -   d:
              -   2
        """
        round_trip(inp, indent=5, block_seq_indent=1)

    def test_set_indent_4_block_list_indent_2(self) -> None:
        inp = """
        a:
          - b: c
          - 1
          - d:
              - 2
        """
        round_trip(inp, indent=4, block_seq_indent=2)

    def test_set_indent_3_block_list_indent_0(self) -> None:
        inp = """
        a:
        -  b: c
        -  1
        -  d:
           -  2
        """
        round_trip(inp, indent=3, block_seq_indent=0)

    def Xtest_set_indent_3_block_list_indent_2(self) -> None:
        inp = """
        a:
          -
           b: c
          -
           1
          -
           d:
             -
              2
        """
        round_trip(inp, indent=3, block_seq_indent=2)

    def test_set_indent_3_block_list_indent_2(self) -> None:
        inp = """
        a:
          - b: c
          - 1
          - d:
             - 2
        """
        round_trip(inp, indent=3, block_seq_indent=2)

    def Xtest_set_indent_2_block_list_indent_2(self) -> None:
        inp = """
        a:
          -
           b: c
          -
           1
          -
           d:
             -
              2
        """
        round_trip(inp, indent=2, block_seq_indent=2)

    # this is how it should be: block_seq_indent stretches the indent
    def test_set_indent_2_block_list_indent_2(self) -> None:
        inp = """
        a:
          - b: c
          - 1
          - d:
            - 2
        """
        round_trip(inp, indent=2, block_seq_indent=2)

    # have to set indent!
    def test_roundtrip_four_space_indents(self) -> None:
        # fmt: off
        s = (
            'a:\n'
            '-   foo\n'
            '-   bar\n'
        )
        # fmt: on
        round_trip(s, indent=4)

    def test_roundtrip_four_space_indents_no_fail(self) -> None:
        inp = """
        a:
        -   foo
        -   bar
        """
        exp = """
        a:
        - foo
        - bar
        """
        assert round_trip_dump(round_trip_load(inp)) == dedent(exp)


class TestYpkgIndent:
    def test_00(self) -> None:
        inp = """
        name       : nano
        version    : 2.3.2
        release    : 1
        homepage   : http://www.nano-editor.org
        source     :
          - http://www.nano-editor.org/dist/v2.3/nano-2.3.2.tar.gz : ff30924807ea289f5b60106be8
        license    : GPL-2.0
        summary    : GNU nano is an easy-to-use text editor
        builddeps  :
          - ncurses-devel
        description: |
            GNU nano is an easy-to-use text editor originally designed
            as a replacement for Pico, the ncurses-based editor from the non-free mailer
            package Pine (itself now available under the Apache License as Alpine).
        """
        round_trip(
            inp, indent=4, block_seq_indent=2, top_level_colon_align=True, prefix_colon=' ',
        )


def guess(s: str) -> Any:
    from ruamel.yaml.util import load_yaml_guess_indent

    x, y, z = load_yaml_guess_indent(dedent(s))
    return y, z


class TestGuessIndent:
    def test_guess_20(self) -> None:
        inp = """\
        a:
        - 1
        """
        assert guess(inp) == (2, 0)

    def test_guess_42(self) -> None:
        inp = """\
        a:
          - 1
        """
        assert guess(inp) == (4, 2)

    def test_guess_42a(self) -> None:
        # block seq indent prevails over nested key indent level
        inp = """\
        b:
              a:
                - 1
        """
        assert guess(inp) == (4, 2)

    def test_guess_3None(self) -> None:
        inp = """\
        b:
           a: 1
        """
        assert guess(inp) == (3, None)

    def test_guess_with_preserve_quotes(self) -> None:
        from ruamel.yaml.util import load_yaml_guess_indent
        from ruamel.yaml.scalarstring import DoubleQuotedScalarString

        inp = """\
        b:
           a: "hello world"
        """
        yaml = YAML()
        yaml.preserve_quotes = True
        x, y, z = load_yaml_guess_indent(dedent(inp), yaml=yaml)
        assert y == 3
        assert z is None
        assert isinstance(x['b']['a'], DoubleQuotedScalarString)


class TestSeparateMapSeqIndents:
    # using uncommon 6 indent with 3 push in as 2 push in automatically
    # gets you 4 indent even if not set
    def test_00(self) -> None:
        # old style
        yaml = YAML()
        yaml.indent = 6
        yaml.block_seq_indent = 3
        inp = """
        a:
           -  1
           -  [1, 2]
        """
        yaml.round_trip(inp)

    def test_01(self) -> None:
        yaml = YAML()
        yaml.indent(sequence=6)
        yaml.indent(offset=3)
        inp = """
        a:
           -  1
           -  {b: 3}
        """
        yaml.round_trip(inp)

    def test_02(self) -> None:
        yaml = YAML()
        yaml.indent(mapping=5, sequence=6, offset=3)
        inp = """
        a:
             b:
                -  1
                -  [1, 2]
        """
        yaml.round_trip(inp)

    def test_03(self) -> None:
        inp = """
        a:
            b:
                c:
                -   1
                -   [1, 2]
        """
        round_trip(inp, indent=4)

    def test_04(self) -> None:
        yaml = YAML()
        yaml.indent(mapping=5, sequence=6)
        inp = """
        a:
             b:
             -     1
             -     [1, 2]
             -     {d: 3.14}
        """
        yaml.round_trip(inp)

    def test_issue_51(self) -> None:
        yaml = YAML()
        # yaml.map_indent = 2 # the default
        yaml.indent(sequence=4, offset=2)
        yaml.preserve_quotes = True
        yaml.round_trip("""
        role::startup::author::rsyslog_inputs:
          imfile:
            - ruleset: 'AEM-slinglog'
              File: '/opt/aem/author/crx-quickstart/logs/error.log'
              startmsg.regex: '^[-+T.:[:digit:]]*'
              tag: 'error'
            - ruleset: 'AEM-slinglog'
              File: '/opt/aem/author/crx-quickstart/logs/stdout.log'
              startmsg.regex: '^[-+T.:[:digit:]]*'
              tag: 'stdout'
        """)


# ############ indentation
