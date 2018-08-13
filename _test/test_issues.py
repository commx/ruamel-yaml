# coding: utf-8

from __future__ import absolute_import, print_function, unicode_literals


import pytest  # NOQA


from roundtrip import (
    round_trip,
    round_trip_load,
    round_trip_dump,
    dedent,
    save_and_run,
)  # NOQA


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

    def test_issue_82(self, tmpdir):
        program_src = dedent('''\
        from __future__ import print_function

        from ruamel import yaml

        import re
        
        
        class SINumber(yaml.YAMLObject):
            PREFIXES = {'k': 1e3, 'M': 1e6, 'G': 1e9}
            yaml_loader = yaml.Loader
            yaml_dumper = yaml.Dumper
            yaml_tag = u'!si'
            yaml_implicit_pattern = re.compile(
                r'^(?P<value>[0-9]+(?:\.[0-9]+)?)(?P<prefix>[kMG])$')
        
            @classmethod
            def from_yaml(cls, loader, node):
                return cls(node.value)
        
            @classmethod
            def to_yaml(cls, dumper, data):
                return dumper.represent_scalar(cls.yaml_tag, str(data))
        
            def __init__(self, *args):
                m = self.yaml_implicit_pattern.match(args[0])
                self.value = float(m.groupdict()['value'])
                self.prefix = m.groupdict()['prefix']
        
            def __str__(self):
                return str(self.value)+self.prefix
        
            def __int__(self):
                return int(self.value*self.PREFIXES[self.prefix])
        
        # This fails:
        yaml.add_implicit_resolver(SINumber.yaml_tag, SINumber.yaml_implicit_pattern)
        
        ret = yaml.load("""
        [1,2,3, !si 10k, 100G]
        """, Loader=yaml.Loader)
        for idx, l in enumerate([1, 2, 3, 10000, 100000000000]):
            assert int(ret[idx]) == l
        ''')
        assert save_and_run(program_src, tmpdir) == 0

    def test_issue_82rt(self, tmpdir):
        yaml_str = "[1, 2, 3, !si 10k, 100G]\n"
        x = round_trip(yaml_str, preserve_quotes=True)  # NOQA


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
        x = round_trip_load(TestIssues.json_str)  # NOQA

    def test_issue_184(self):
        yaml_str = dedent("""\
        test::test:
          # test
          foo:
            bar: baz
        """)
        d = round_trip_load(yaml_str)
        d['bar'] = 'foo'
        d.yaml_add_eol_comment('test1', 'bar')
        assert round_trip_dump(d) == yaml_str + 'bar: foo # test1\n'
