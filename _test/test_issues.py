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

    def test_issue_102(self):
        yaml_str = dedent("""
        var1: #empty
        var2: something #notempty
        var3: {} #empty object
        var4: {a: 1} #filled object
        var5: [] #empty array
        """)
        x = round_trip(yaml_str, preserve_quotes=True)  # NOQA

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

    def test_issue_161(self):
        yaml_str = dedent("""\
        mapping-A:
          key-A:{}
        mapping-B:
        """)
        for comment in ['', ' # no-newline', '  # some comment\n', '\n']:
            s = yaml_str.format(comment)
            res = round_trip(s)  # NOQA

    def test_issue_161a(self):
        yaml_str = dedent("""\
        mapping-A:
          key-A:{}
        mapping-B:
        """)
        for comment in ['\n# between']:
            s = yaml_str.format(comment)
            res = round_trip(s)  # NOQA

    def test_issue_163(self):
        s = dedent("""\
        some-list:
        # List comment
        - {}
        """)
        x = round_trip(s, preserve_quotes=True)  # NOQA

    json_str = (
        '{"sshKeys":[{"name":"AETROS\/google-k80-1","uses":0,"getLastUse":0,'
        '"fingerprint":"MD5:19:dd:41:93:a1:a3:f5:91:4a:8e:9b:d0:ae:ce:66:4c",'
        '"created":1509497961}]}'
    )

    json_str2 = '{"abc":[{"a":"1", "uses":0}]}'

    def test_issue_172(self):
        x = round_trip_load(TestIssues.json_str2)  # NOQA
        x = round_trip_load(TestIssues.json_str)   # NOQA
