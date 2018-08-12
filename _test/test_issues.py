# coding: utf-8

from __future__ import absolute_import, print_function, unicode_literals


import pytest  # NOQA


from roundtrip import round_trip, round_trip_load, round_trip_dump, dedent  # NOQA


class TestIssues:
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

    def test_issue_160(self):
        s = dedent("""\
        root:
            # a comment
            - {some_key: "value"}
        
        foo: 32
        bar: 32
        """)
        x = round_trip(s, block_seq_indent=4, preserve_quotes=True)
        assert x['bar'] == 32
        
