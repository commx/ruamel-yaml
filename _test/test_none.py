# coding: utf-8


import pytest  # NOQA


class TestNone:
    def test_dump00(self):
        import ruamel.yaml  # NOQA

        data = None
        s = ruamel.yaml.round_trip_dump(data)
        assert s == 'null\n...\n'
        d = ruamel.yaml.round_trip_load(s)
        assert d == data

    def test_dump01(self):
        import ruamel.yaml  # NOQA

        data = None
        s = ruamel.yaml.round_trip_dump(data, explicit_end=True)
        assert s == 'null\n...\n'
        d = ruamel.yaml.round_trip_load(s)
        assert d == data

    def test_dump02(self):
        import ruamel.yaml  # NOQA

        data = None
        s = ruamel.yaml.round_trip_dump(data, explicit_end=False)
        assert s == 'null\n...\n'
        d = ruamel.yaml.round_trip_load(s)
        assert d == data

    def test_dump03(self):
        import ruamel.yaml  # NOQA

        data = None
        s = ruamel.yaml.round_trip_dump(data, explicit_start=True)
        assert s == '---\n...\n'
        d = ruamel.yaml.round_trip_load(s)
        assert d == data

    def test_dump04(self):
        import ruamel.yaml  # NOQA

        data = None
        s = ruamel.yaml.round_trip_dump(data, explicit_start=True, explicit_end=False)
        assert s == '---\n...\n'
        d = ruamel.yaml.round_trip_load(s)
        assert d == data
