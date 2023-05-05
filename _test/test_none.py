# coding: utf-8

import pytest  # type: ignore  # NOQA
from roundtrip import round_trip_load, round_trip_dump  # type: ignore


class TestNone:
    def test_dump00(self) -> None:
        data = None
        s = round_trip_dump(data)
        assert s == 'null\n...\n'
        d = round_trip_load(s)
        assert d == data

    def test_dump01(self) -> None:
        data = None
        s = round_trip_dump(data, explicit_end=True)
        assert s == 'null\n...\n'
        d = round_trip_load(s)
        assert d == data

    def test_dump02(self) -> None:
        data = None
        s = round_trip_dump(data, explicit_end=False)
        assert s == 'null\n...\n'
        d = round_trip_load(s)
        assert d == data

    def test_dump03(self) -> None:
        data = None
        s = round_trip_dump(data, explicit_start=True)
        assert s == '---\n...\n'
        d = round_trip_load(s)
        assert d == data

    def test_dump04(self) -> None:
        data = None
        s = round_trip_dump(data, explicit_start=True, explicit_end=False)
        assert s == '---\n...\n'
        d = round_trip_load(s)
        assert d == data
