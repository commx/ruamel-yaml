# coding: utf-8

import pytest                        # NOQA

import ruamel.yaml
from roundtrip import dedent


def load(s, version=None):
    return ruamel.yaml.round_trip_load(dedent(s), version)


class TestVersions:
    def test_explicit_1_2(self):
        l = load("""\
        %YAML 1.2
        ---
        - 12:34:56
        - 012
        - 012345678
        - 0o12
        - on
        - off
        - yes
        - no
        - true
        """)
        assert l[0] == '12:34:56'
        assert l[1] == 12
        assert l[2] == '012345678'
        assert l[3] == 10
        assert l[4] == 'on'
        assert l[5] == 'off'
        assert l[6] == 'yes'
        assert l[7] == 'no'
        assert l[8] is True

    def test_explicit_1_1(self):
        l = load("""\
        %YAML 1.1
        ---
        - 12:34:56
        - 012
        - 012345678
        - 0o12
        - on
        - off
        - yes
        - no
        - true
        """)
        assert l[0] == 45296
        assert l[1] == 10
        assert l[2] == '012345678'
        assert l[3] == 10
        assert l[4] is True
        assert l[5] is False
        assert l[6] is True
        assert l[7] is False
        assert l[8] is True

    def test_implicit_1_2(self):
        l = load("""\
        - 12:34:56
        - 012
        - 012345678
        - 0o12
        - on
        - off
        - yes
        - no
        - true
        """)
        assert l[0] == '12:34:56'
        assert l[1] == 12
        assert l[2] == '012345678'
        assert l[3] == 10
        assert l[4] == 'on'
        assert l[5] == 'off'
        assert l[6] == 'yes'
        assert l[7] == 'no'
        assert l[8] is True

    def test_load_version_1_1(self):
        l = load("""\
        - 12:34:56
        - 012
        - 012345678
        - 0o12
        - on
        - off
        - yes
        - no
        - true
        """, version="1.1")
        assert l[0] == 45296
        assert l[1] == 10
        assert l[2] == '012345678'
        assert l[3] == 10
        assert l[4] is True
        assert l[5] is False
        assert l[6] is True
        assert l[7] is False
        assert l[8] is True
