# coding: utf-8

from __future__ import print_function, absolute_import, division, unicode_literals

import pytest  # NOQA

from roundtrip import round_trip, dedent, round_trip_load, round_trip_dump


class TestBinHexOct:
    # @pytest.mark.xfail(strict=True)
    def test_round_trip_hex_oct(self):
        round_trip("""\
        - 42
        - 0b101010
        - 0x2a
        - 0x2A
        - 0o52
        """)

    def test_calculate(self):
        s = dedent("""\
        - 42
        - 0b101010
        - 0x2a
        - 0x2A
        - 0o52
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
