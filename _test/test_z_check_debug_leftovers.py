# coding: utf-8

import sys
from typing import Any
import pytest  # type: ignore # NOQA

from roundtrip import round_trip_load, round_trip_dump, dedent  # type: ignore


class TestLeftOverDebug:
    # idea here is to capture round_trip_output via pytest stdout capture
    # if there is are any leftover debug statements they should show up
    def test_00(self, capsys: Any) -> None:
        s = dedent("""
        a: 1
        b: []
        c: [a, 1]
        d: {f: 3.14, g: 42}
        """)
        d = round_trip_load(s)
        round_trip_dump(d, sys.stdout)
        out, err = capsys.readouterr()
        assert out == s

    def test_01(self, capsys: Any) -> None:
        s = dedent("""
        - 1
        - []
        - [a, 1]
        - {f: 3.14, g: 42}
        - - 123
        """)
        d = round_trip_load(s)
        round_trip_dump(d, sys.stdout)
        out, err = capsys.readouterr()
        assert out == s
