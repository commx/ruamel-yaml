# coding: utf-8

"""
http://yaml.org/type/timestamp.html specifies the regexp to use
for datetime.date and datetime.datetime construction. Date is simple
but datetime can have 'T' or 't' as well as 'Z' or a timezone offset (in
hours and minutes). This information was originally used to create
a UTC datetime and then discarded

examples from the above:

canonical:        2001-12-15T02:59:43.1Z
valid iso8601:    2001-12-14t21:59:43.10-05:00
space separated:  2001-12-14 21:59:43.10 -5
no time zone (Z): 2001-12-15 2:59:43.10
date (00:00:00Z): 2002-12-14

Please note that a fraction can only be included if not equal to 0

"""

import sys
import copy
import pytest  # type: ignore  # NOQA
from datetime import datetime as DateTime, timezone as TimeZone, timedelta as TimeDelta

from roundtrip import round_trip, dedent, round_trip_load, round_trip_dump  # type: ignore # NOQA


class TestDateTime:
    def test_date_only(self) -> None:
        inp = """
        - 2011-10-02
        """
        exp = """
        - 2011-10-02
        """
        round_trip(inp, exp)

    def test_zero_fraction(self) -> None:
        inp = """
        - 2011-10-02 16:45:00.0
        """
        exp = """
        - 2011-10-02 16:45:00
        """
        round_trip(inp, exp)

    def test_long_fraction(self) -> None:
        inp = """
        - 2011-10-02 16:45:00.1234      # expand with zeros
        - 2011-10-02 16:45:00.123456
        - 2011-10-02 16:45:00.12345612  # round to microseconds
        - 2011-10-02 16:45:00.1234565   # round up
        - 2011-10-02 16:45:00.12345678  # round up
        """
        exp = """
        - 2011-10-02 16:45:00.123400    # expand with zeros
        - 2011-10-02 16:45:00.123456
        - 2011-10-02 16:45:00.123456    # round to microseconds
        - 2011-10-02 16:45:00.123457    # round up
        - 2011-10-02 16:45:00.123457    # round up
        """
        round_trip(inp, exp)

    def test_canonical(self) -> None:
        inp = """
        - 2011-10-02T16:45:00.1Z
        """
        exp = """
        - 2011-10-02T16:45:00.100000Z
        """
        round_trip(inp, exp)

    def test_spaced_timezone(self) -> None:
        inp = """
        - 2011-10-02T11:45:00 -5
        """
        exp = """
        - 2011-10-02T11:45:00-5
        """
        round_trip(inp, exp)

    def test_normal_timezone(self) -> None:
        round_trip("""
        - 2011-10-02T11:45:00-5
        - 2011-10-02 11:45:00-5
        - 2011-10-02T11:45:00-05:00
        - 2011-10-02 11:45:00-05:00
        """)

    def test_no_timezone(self) -> None:
        inp = """
        - 2011-10-02 6:45:00
        """
        exp = """
        - 2011-10-02 06:45:00
        """
        round_trip(inp, exp)

    def test_explicit_T(self) -> None:
        inp = """
        - 2011-10-02T16:45:00
        """
        exp = """
        - 2011-10-02T16:45:00
        """
        round_trip(inp, exp)

    def test_explicit_t(self) -> None:  # to upper
        inp = """
        - 2011-10-02t16:45:00
        """
        exp = """
        - 2011-10-02T16:45:00
        """
        round_trip(inp, exp)

    def test_no_T_multi_space(self) -> None:
        inp = """
        - 2011-10-02   16:45:00
        """
        exp = """
        - 2011-10-02 16:45:00
        """
        round_trip(inp, exp)

    def test_iso(self) -> None:
        round_trip("""
        - 2011-10-02T15:45:00+01:00
        """)

    def test_zero_tz(self) -> None:
        round_trip("""
        - 2011-10-02T15:45:00+0
        """)

    def test_issue_45(self) -> None:
        round_trip("""
        dt: 2016-08-19T22:45:47Z
        """)

    def test_issue_366(self) -> None:
        import ruamel.yaml
        import io

        round_trip("""
        [2021-02-01 22:34:48.696868-03:00]
        """)
        yaml = ruamel.yaml.YAML()
        dd = DateTime(2021, 2, 1, 22, 34, 48, 696868, TimeZone(TimeDelta(hours=-3), name=''))
        buf = io.StringIO()
        yaml.dump(dd, buf)
        assert buf.getvalue() == '2021-02-01 22:34:48.696868-03:00\n...\n'
        rd = yaml.load(buf.getvalue())
        assert rd == dd

    def test_deepcopy_datestring(self) -> None:
        # reported by Quuxplusone, http://stackoverflow.com/a/41577841/1307905
        x = dedent("""\
        foo: 2016-10-12T12:34:56
        """)
        data = copy.deepcopy(round_trip_load(x))
        assert round_trip_dump(data) == x

    def test_fraction_overflow(self) -> None:
        # reported (indirectly) by Luís Ferreira
        # https://sourceforge.net/p/ruamel-yaml/tickets/414/
        inp = dedent("""\
        - 2022-01-02T12:34:59.9999994
        - 2022-01-02T12:34:59.9999995
        """)
        exp = dedent("""\
        - 2022-01-02T12:34:59.999999
        - 2022-01-02T12:35:00
        """)
        round_trip(inp, exp)

    def Xtest_tzinfo(self) -> None:
        import ruamel.yaml

        yaml = ruamel.yaml.YAML()
        dts = '2011-10-02T16:45:00.930619+01:00'
        d = yaml.load(dts)
        print('d', repr(d), d._yaml)
        yaml.dump(dict(x=d), sys.stdout)
        print('----')
        # dx = DateTime.fromisoformat(dts)
        # print('dx', dx, repr(dx))
        dd = DateTime(2011, 10, 2, 16, 45, 00, 930619, TimeZone(TimeDelta(hours=1, minutes=0), name='+01:00'))  # NOQA
        yaml.dump([dd], sys.stdout)
        print('dd', dd, dd.tzinfo)
        raise AssertionError()
