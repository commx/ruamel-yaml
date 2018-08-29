# coding: utf-8

from __future__ import print_function, absolute_import, division, unicode_literals

import pytest  # NOQA

from roundtrip import round_trip, dedent, round_trip_load, round_trip_dump

# http://yaml.org/type/int.html is where underscores in integers are defined


class TestBinHexOct:
    def test_round_trip_hex_oct(self):
        round_trip("""\
        - 42
        - 0b101010
        - 0x2a
        - 0x2A
        - 0o52
        """)

    def test_calculate(self):
        # make sure type, leading zero(s) and underscore are preserved
        s = dedent("""\
        - 42
        - 0b101010
        - 0x_2a
        - 0x2A
        - 0o00_52
        """)
        x = round_trip_load(s)
        for idx, elem in enumerate(x):
            # x[idx] = type(elem)(elem - 21)
            elem -= 21
            x[idx] = elem
        for idx, elem in enumerate(x):
            # x[idx] = type(elem)(2 * elem)
            elem *= 2
            x[idx] = elem
        for idx, elem in enumerate(x):
            t = elem
            elem **= 2
            elem //= t
            x[idx] = elem
        assert round_trip_dump(x) == s

    # if a scalar int has one or more leading zeros, it is assumed that the width
    # of the int is significant, as padding with a zero doesn't make much sense
    # please note that none of this should work on YAML 1.1 as it collides with
    # the old octal representation.

    def test_leading_zero_hex_oct_bin(self):
        round_trip("""\
        - 0b0101010
        - 0b00101010
        - 0x02a
        - 0x002a
        - 0x02A
        - 0x002A
        - 0o052
        - 0o0052
        """)

    def test_leading_zero_int(self):
        round_trip("""\
        - 042
        - 0042
        """)

    def test_leading_zero_YAML_1_1(self):
        d = round_trip_load("""\
        %YAML 1.1
        ---
        - 042
        - 0o42
        """)
        assert d[0] == 0o42
        assert d[1] == '0o42'

    def test_underscore(self):
        round_trip("""\
        - 0b10000_10010010
        - 0b0_0000_1001_0010
        - 0x2_87_57_b2_
        - 0x0287_57B2
        - 0x_0_2_8_7_5_7_B_2
        - 0o2416_53662
        - 42_42_
        """)

    def test_leading_underscore(self):
        d = round_trip_load("""\
        - 0x_2_8_7_5_7_B_2
        - _42_42_
        - 42_42_
        """)
        assert d[0] == 42424242
        assert d[1] == '_42_42_'
        assert d[2] == 4242

    def test_big(self):
        # bitbucket issue 144 reported by ccatterina
        d = round_trip_load("""\
        - 2_147_483_647
        - 9_223_372_036_854_775_808
        """)
        assert d[0] == 2147483647
        assert d[1] == 9223372036854775808


class TestIntIssues:
    def test_issue_218_single_plus_sign_is_not_int(self):
        d = round_trip_load("""\
        +: 1
        """)
        assert d == {'+': 1}
