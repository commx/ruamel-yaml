# coding: utf-8

from __future__ import absolute_import, print_function, unicode_literals


import pytest  # NOQA


from roundtrip import round_trip, round_trip_load, round_trip_dump, dedent  # NOQA


class TestIssue61:
    def test_issue_61(self):
        import ruamel.yaml

        s = dedent("""
        def1: &ANCHOR1
            key1: value1
        def: &ANCHOR
            <<: *ANCHOR1
            key: value
        comb:
            <<: *ANCHOR
        """)
        data = ruamel.yaml.round_trip_load(s)
        assert str(data['comb']) == str(data['def'])
        assert str(data['comb']) == "ordereddict([('key', 'value'), ('key1', 'value1')])"
