# coding: utf-8

from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals


from textwrap import dedent

import pytest  # NOQA

import ruamel.yaml
from ruamel.yaml.util import load_yaml_guess_indent

from roundtrip import round_trip


def rt(s):
    return ruamel.yaml.dump(
        ruamel.yaml.load(s, Loader=ruamel.yaml.RoundTripLoader),
        Dumper=ruamel.yaml.RoundTripDumper,
    ).strip() + '\n'


class TestIndent:
    def test_roundtrip_inline_list(self):
        s = 'a: [a, b, c]\n'
        output = rt(s)
        assert s == output

    def test_roundtrip_mapping_of_inline_lists(self):
        s = dedent("""\
        a: [a, b, c]
        j: [k, l, m]
        """)
        output = rt(s)
        assert s == output

    def test_roundtrip_mapping_of_inline_lists_comments(self):
        s = dedent("""\
        # comment A
        a: [a, b, c]
        # comment B
        j: [k, l, m]
        """)
        output = rt(s)
        assert s == output

    def test_roundtrip_mapping_of_inline_sequence_eol_comments(self):
        s = dedent("""\
        # comment A
        a: [a, b, c]  # comment B
        j: [k, l, m]  # comment C
        """)
        output = rt(s)
        assert s == output

    # first test by explicitly setting flow style
    def test_added_inline_list(self):
        s1 = dedent("""
        a:
        - b
        - c
        - d
        """)
        s = 'a: [b, c, d]\n'
        data = ruamel.yaml.load(s1, Loader=ruamel.yaml.RoundTripLoader)
        val = data['a']
        val.fa.set_flow_style()
        # print(type(val), '_yaml_format' in dir(val))
        output = ruamel.yaml.dump(data, Dumper=ruamel.yaml.RoundTripDumper)
        assert s == output

    # ############ flow mappings

    def test_roundtrip_flow_mapping(self):
        s = dedent("""\
        - {a: 1, b: hallo}
        - {j: fka, k: 42}
        """)
        data = ruamel.yaml.load(s, Loader=ruamel.yaml.RoundTripLoader)
        output = ruamel.yaml.dump(data, Dumper=ruamel.yaml.RoundTripDumper)
        assert s == output

    def test_roundtrip_sequence_of_inline_mappings_eol_comments(self):
        s = dedent("""\
        # comment A
        - {a: 1, b: hallo}  # comment B
        - {j: fka, k: 42}  # comment C
        """)
        output = rt(s)
        assert s == output

    def test_indent_top_level(self):
        round_trip("""
        -   a:
            -   b
        """, indent=4)

    def test_set_indent_5_block_list_indent_1(self):
        round_trip("""
        a:
         -   b: c
         -   1
         -   d:
              -   2
        """, indent=5, block_seq_indent=1)

    def test_set_indent_4_block_list_indent_2(self):
        round_trip("""
        a:
          - b: c
          - 1
          - d:
              - 2
        """, indent=4, block_seq_indent=2)

    def test_set_indent_3_block_list_indent_0(self):
        round_trip("""
        a:
        -  b: c
        -  1
        -  d:
           -  2
        """, indent=3, block_seq_indent=0)

    def test_set_indent_3_block_list_indent_2(self):
        round_trip("""
        a:
          -
           b: c
          -
           1
          -
           d:
             -
              2
        """, indent=3, block_seq_indent=2)

    def test_set_indent_2_block_list_indent_2(self):
        round_trip("""
        a:
          -
           b: c
          -
           1
          -
           d:
             -
              2
        """, indent=2, block_seq_indent=2)


def guess(s):
    x, y, z = load_yaml_guess_indent(dedent(s))
    return y, z


class TestGuessIndent:
    def test_guess_20(self):
        assert guess("""\
        a:
        - 1
        """) == (2, 0)

    def test_guess_42(self):
        assert guess("""\
        a:
          - 1
        """) == (4, 2)

    def test_guess_42a(self):
        assert guess("""\
        b:
            a:
              - 1
        """) == (4, 2)

    def test_guess_3None(self):
        assert guess("""\
        b:
           a: 1
        """) == (3, None)

# ############ indentation
