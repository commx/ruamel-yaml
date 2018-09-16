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
        program_src = r'''
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
        '''
        assert save_and_run(dedent(program_src), tmpdir) == 0

    def test_issue_82rt(self, tmpdir):
        yaml_str = '[1, 2, 3, !si 10k, 100G]\n'
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

    def test_issue_150(self):
        from ruamel.yaml import YAML

        inp = """\
        base: &base_key
          first: 123
          second: 234

        child:
          <<: *base_key
          third: 345
        """
        yaml = YAML()
        data = yaml.load(inp)
        child = data['child']
        assert 'second' in dict(**child)

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
        r'{"sshKeys":[{"name":"AETROS\/google-k80-1","uses":0,"getLastUse":0,'
        '"fingerprint":"MD5:19:dd:41:93:a1:a3:f5:91:4a:8e:9b:d0:ae:ce:66:4c",'
        '"created":1509497961}]}'
    )

    json_str2 = '{"abc":[{"a":"1", "uses":0}]}'

    def test_issue_172(self):
        x = round_trip_load(TestIssues.json_str2)  # NOQA
        x = round_trip_load(TestIssues.json_str)  # NOQA

    def test_issue_176(self):
        # basic request by Stuart Berg
        from ruamel.yaml import YAML

        yaml = YAML()
        seq = yaml.load('[1,2,3]')
        seq[:] = [1, 2, 3, 4]

    def test_issue_176_preserve_comments_on_extended_slice_assignment(self):
        yaml_str = dedent("""\
        - a
        - b  # comment
        - c  # commment c
        # comment c+
        - d

        - e # comment
        """)
        seq = round_trip_load(yaml_str)
        seq[1::2] = ['B', 'D']
        res = round_trip_dump(seq)
        assert res == yaml_str.replace(' b ', ' B ').replace(' d\n', ' D\n')

    def test_issue_176_test_slicing(self):
        from ruamel.yaml.comments import CommentedSeq

        mss = round_trip_load('[0, 1, 2, 3, 4]')
        assert len(mss) == 5
        assert mss[2:2] == []
        assert mss[2:4] == [2, 3]
        assert isinstance(mss[2:4], CommentedSeq)
        assert mss[1::2] == [1, 3]

        # slice assignment
        m = mss[:]
        m[2:2] = [42]
        assert m == [0, 1, 42, 2, 3, 4]

        m = mss[:]
        m[:3] = [42, 43, 44]
        assert m == [42, 43, 44, 3, 4]
        m = mss[:]
        m[2:] = [42, 43, 44]
        assert m == [0, 1, 42, 43, 44]
        m = mss[:]
        m[:] = [42, 43, 44]
        assert m == [42, 43, 44]

        # extend slice assignment
        m = mss[:]
        m[2:4] = [42, 43, 44]
        assert m == [0, 1, 42, 43, 44, 4]
        m = mss[:]
        m[1::2] = [42, 43]
        assert m == [0, 42, 2, 43, 4]
        m = mss[:]
        with pytest.raises(TypeError, match='too many'):
            m[1::2] = [42, 43, 44]
        with pytest.raises(TypeError, match='not enough'):
            m[1::2] = [42]
        m = mss[:]
        m += [5]
        m[1::2] = [42, 43, 44]
        assert m == [0, 42, 2, 43, 4, 44]

        # deleting
        m = mss[:]
        del m[1:3]
        assert m == [0, 3, 4]
        m = mss[:]
        del m[::2]
        assert m == [1, 3]
        m = mss[:]
        del m[:]
        assert m == []

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

    def test_issue_219(self):
        yaml_str = dedent("""\
        [StackName: AWS::StackName]
        """)
        d = round_trip_load(yaml_str)  # NOQA

    def test_issue_219a(self):
        yaml_str = dedent("""\
        [StackName:
        AWS::StackName]
        """)
        d = round_trip_load(yaml_str)  # NOQA

    def test_issue_220(self, tmpdir):
        program_src = r'''
        from ruamel.yaml import YAML

        yaml_str = u"""\
        ---
        foo: ["bar"]
        """

        yaml = YAML(typ='safe', pure=True)
        d = yaml.load(yaml_str)
        print(d)
        '''
        assert save_and_run(dedent(program_src), tmpdir, optimized=True) == 0

    def test_issue_221_add(self):
        from ruamel.yaml.comments import CommentedSeq

        a = CommentedSeq([1, 2, 3])
        a + [4, 5]

    def test_issue_221_sort(self):
        from ruamel.yaml import YAML
        from ruamel.yaml.compat import StringIO

        yaml = YAML()
        inp = dedent("""\
        - d
        - a  # 1
        - c  # 3
        - e  # 5
        - b  # 2
        """)
        a = yaml.load(dedent(inp))
        a.sort()
        buf = StringIO()
        yaml.dump(a, buf)
        exp = dedent("""\
        - a  # 1
        - b  # 2
        - c  # 3
        - d
        - e  # 5
        """)
        assert buf.getvalue() == exp

    def test_issue_221_sort_reverse(self):
        from ruamel.yaml import YAML
        from ruamel.yaml.compat import StringIO

        yaml = YAML()
        inp = dedent("""\
        - d
        - a  # 1
        - c  # 3
        - e  # 5
        - b  # 2
        """)
        a = yaml.load(dedent(inp))
        a.sort(reverse=True)
        buf = StringIO()
        yaml.dump(a, buf)
        exp = dedent("""\
        - e  # 5
        - d
        - c  # 3
        - b  # 2
        - a  # 1
        """)
        assert buf.getvalue() == exp

    def test_issue_221_sort_key(self):
        from ruamel.yaml import YAML
        from ruamel.yaml.compat import StringIO

        yaml = YAML()
        inp = dedent("""\
        - four
        - One    # 1
        - Three  # 3
        - five   # 5
        - two    # 2
        """)
        a = yaml.load(dedent(inp))
        a.sort(key=str.lower)
        buf = StringIO()
        yaml.dump(a, buf)
        exp = dedent("""\
        - five   # 5
        - four
        - One    # 1
        - Three  # 3
        - two    # 2
        """)
        assert buf.getvalue() == exp

    def test_issue_221_sort_key_reverse(self):
        from ruamel.yaml import YAML
        from ruamel.yaml.compat import StringIO

        yaml = YAML()
        inp = dedent("""\
        - four
        - One    # 1
        - Three  # 3
        - five   # 5
        - two    # 2
        """)
        a = yaml.load(dedent(inp))
        a.sort(key=str.lower, reverse=True)
        buf = StringIO()
        yaml.dump(a, buf)
        exp = dedent("""\
        - two    # 2
        - Three  # 3
        - One    # 1
        - four
        - five   # 5
        """)
        assert buf.getvalue() == exp

    def test_issue_222(self):
        import ruamel.yaml
        from ruamel.yaml.compat import StringIO

        buf = StringIO()
        ruamel.yaml.safe_dump(['012923'], buf)
        assert buf.getvalue() == "['012923']\n"

    def test_issue_223(self):
        import ruamel.yaml

        yaml = ruamel.yaml.YAML(typ='safe')
        yaml.load('phone: 0123456789')

    def test_issue_232(self):
        import ruamel.yaml
        from ruamel import yaml

        with pytest.raises(ruamel.yaml.parser.ParserError):
            yaml.safe_load(']')
        with pytest.raises(ruamel.yaml.parser.ParserError):
            yaml.safe_load('{]')

    @pytest.mark.xfail(strict=True, reason='not a dict subclass', raises=TypeError)
    def test_issue_233(self):
        from ruamel.yaml import YAML
        import json

        yaml = YAML()
        data = yaml.load('{}')
        json_str = json.dumps(data)  # NOQA

    @pytest.mark.xfail(strict=True, reason='not a list subclass', raises=TypeError)
    def test_issue_233a(self):
        from ruamel.yaml import YAML
        import json

        yaml = YAML()
        data = yaml.load('[]')
        json_str = json.dumps(data)  # NOQA

    def test_issue_234(self):
        from ruamel.yaml import YAML

        inp = dedent("""\
        - key: key1
          ctx: [one, two]
          help: one
          cmd: >
            foo bar
            foo bar
        """)
        yaml = YAML(typ='safe', pure=True)
        data = yaml.load(inp)
        fold = data[0]['cmd']
        print(repr(fold))
        assert '\a' not in fold
