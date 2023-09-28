# coding: utf-8

from typing import Any

import pytest  # type: ignore  # NOQA


# cannot do "from .roundtrip" because of pytest, so mypy cannot find this
from roundtrip import (  # type: ignore
    round_trip,
    na_round_trip,
    round_trip_load,
    round_trip_dump,
    dedent,
    save_and_run,
    YAML,
)  # NOQA


class TestIssues:
    def test_issue_61(self) -> None:
        s = dedent(
            """
        def1: &ANCHOR1
            key1: value1
        def: &ANCHOR
            <<: *ANCHOR1
            key: value
        comb:
            <<: *ANCHOR
        """,
        )
        data = round_trip_load(s)
        assert str(data['comb']) == str(data['def'])
        assert str(data['comb']) == "{'key': 'value', 'key1': 'value1'}"

    #    def test_issue_82(self, tmpdir):
    #        program_src = r'''
    #        from ruamel import yaml
    #        import re
    #
    #        class SINumber(yaml.YAMLObject):
    #            PREFIXES = {'k': 1e3, 'M': 1e6, 'G': 1e9}
    #            yaml_loader = yaml.Loader
    #            yaml_dumper = yaml.Dumper
    #            yaml_tag = '!si'
    #            yaml_implicit_pattern = re.compile(
    #                r'^(?P<value>[0-9]+(?:\.[0-9]+)?)(?P<prefix>[kMG])$')
    #
    #            @classmethod
    #            def from_yaml(cls, loader, node):
    #                return cls(node.value)
    #
    #            @classmethod
    #            def to_yaml(cls, dumper, data):
    #                return dumper.represent_scalar(cls.yaml_tag, str(data))
    #
    #            def __init__(self, *args):
    #                m = self.yaml_implicit_pattern.match(args[0])
    #                self.value = float(m.groupdict()['value'])
    #                self.prefix = m.groupdict()['prefix']
    #
    #            def __str__(self) -> None:
    #                return str(self.value)+self.prefix
    #
    #            def __int__(self) -> None:
    #                return int(self.value*self.PREFIXES[self.prefix])
    #
    #        # This fails:
    #        yaml.add_implicit_resolver(SINumber.yaml_tag, SINumber.yaml_implicit_pattern)
    #
    #        ret = yaml.load("""
    #        [1,2,3, !si 10k, 100G]
    #        """, Loader=yaml.Loader)
    #        for idx, l in enumerate([1, 2, 3, 10000, 100000000000]):
    #            assert int(ret[idx]) == l
    #        '''
    #        assert save_and_run(dedent(program_src), tmpdir) == 0

    def test_issue_82rt(self, tmpdir: Any) -> None:
        yaml_str = '[1, 2, 3, !si 10k, 100G]\n'
        x = round_trip(yaml_str, preserve_quotes=True)  # NOQA

    def test_issue_102(self) -> None:
        yaml_str = dedent(
            """
        var1: #empty
        var2: something #notempty
        var3: {} #empty object
        var4: {a: 1} #filled object
        var5: [] #empty array
        """,
        )
        x = round_trip(yaml_str, preserve_quotes=True)  # NOQA

    def test_issue_150(self) -> None:
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

    def test_issue_160(self) -> None:
        from ruamel.yaml.compat import StringIO

        s = dedent(
            """\
        root:
            # a comment
            - {some_key: "value"}

        foo: 32
        bar: 32
        """,
        )
        a = round_trip_load(s)
        del a['root'][0]['some_key']
        buf = StringIO()
        round_trip_dump(a, buf, block_seq_indent=4)
        exp = dedent(
            """\
        root:
            # a comment
            - {}

        foo: 32
        bar: 32
        """,
        )
        assert buf.getvalue() == exp

    def test_issue_161(self) -> None:
        yaml_str = dedent(
            """\
        mapping-A:
          key-A:{}
        mapping-B:
        """,
        )
        for comment in ['', ' # no-newline', '  # some comment\n', '\n']:
            s = yaml_str.format(comment)
            res = round_trip(s)  # NOQA

    def test_issue_161a(self) -> None:
        yaml_str = dedent(
            """\
        mapping-A:
          key-A:{}
        mapping-B:
        """,
        )
        for comment in ['\n# between']:
            s = yaml_str.format(comment)
            res = round_trip(s)  # NOQA

    def test_issue_163(self) -> None:
        s = dedent(
            """\
        some-list:
        # List comment
        - {}
        """,
        )
        x = round_trip(s, preserve_quotes=True)  # NOQA

    json_str = (
        r'{"sshKeys":[{"name":"AETROS\/google-k80-1","uses":0,"getLastUse":0,'
        '"fingerprint":"MD5:19:dd:41:93:a1:a3:f5:91:4a:8e:9b:d0:ae:ce:66:4c",'
        '"created":1509497961}]}'
    )

    json_str2 = '{"abc":[{"a":"1", "uses":0}]}'

    def test_issue_172(self) -> None:
        x = round_trip_load(TestIssues.json_str2)  # NOQA
        x = round_trip_load(TestIssues.json_str)  # NOQA

    def test_issue_176(self) -> None:
        # basic request by Stuart Berg
        from ruamel.yaml import YAML

        yaml = YAML()
        seq = yaml.load('[1,2,3]')
        seq[:] = [1, 2, 3, 4]

    def test_issue_176_preserve_comments_on_extended_slice_assignment(self) -> None:
        yaml_str = dedent(
            """\
        - a
        - b  # comment
        - c  # commment c
        # comment c+
        - d

        - e # comment
        """,
        )
        seq = round_trip_load(yaml_str)
        seq[1::2] = ['B', 'D']
        res = round_trip_dump(seq)
        assert res == yaml_str.replace(' b ', ' B ').replace(' d\n', ' D\n')

    def test_issue_176_test_slicing(self) -> None:
        mss = round_trip_load('[0, 1, 2, 3, 4]')
        assert len(mss) == 5
        assert mss[2:2] == []
        assert mss[2:4] == [2, 3]
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

    def test_issue_184(self) -> None:
        yaml_str = dedent(
            """\
        test::test:
          # test
          foo:
            bar: baz
        """,
        )
        d = round_trip_load(yaml_str)
        d['bar'] = 'foo'
        d.yaml_add_eol_comment('test1', 'bar')
        assert round_trip_dump(d) == yaml_str + 'bar: foo # test1\n'

    def test_issue_219(self) -> None:
        yaml_str = dedent(
            """\
        [StackName: AWS::StackName]
        """,
        )
        d = round_trip_load(yaml_str)  # NOQA

    def test_issue_219a(self) -> None:
        yaml_str = dedent(
            """\
        [StackName:
        AWS::StackName]
        """,
        )
        d = round_trip_load(yaml_str)  # NOQA

    def test_issue_220(self, tmpdir: Any) -> None:
        program_src = r'''
        from ruamel.yaml import YAML

        yaml_str = """\
        ---
        foo: ["bar"]
        """

        yaml = YAML(typ='safe', pure=True)
        d = yaml.load(yaml_str)
        print(d)
        '''
        assert save_and_run(dedent(program_src), tmpdir, optimized=True) == 0

    def test_issue_221_add(self) -> None:
        from ruamel.yaml.comments import CommentedSeq

        a = CommentedSeq([1, 2, 3])
        a + [4, 5]

    def test_issue_221_sort(self) -> None:
        from ruamel.yaml import YAML
        from ruamel.yaml.compat import StringIO

        yaml = YAML()
        inp = dedent(
            """\
        - d
        - a  # 1
        - c  # 3
        - e  # 5
        - b  # 2
        """,
        )
        a = yaml.load(dedent(inp))
        a.sort()
        buf = StringIO()
        yaml.dump(a, buf)
        exp = dedent(
            """\
        - a  # 1
        - b  # 2
        - c  # 3
        - d
        - e  # 5
        """,
        )
        assert buf.getvalue() == exp

    def test_issue_221_sort_reverse(self) -> None:
        from ruamel.yaml import YAML
        from ruamel.yaml.compat import StringIO

        yaml = YAML()
        inp = dedent(
            """\
        - d
        - a  # 1
        - c  # 3
        - e  # 5
        - b  # 2
        """,
        )
        a = yaml.load(dedent(inp))
        a.sort(reverse=True)
        buf = StringIO()
        yaml.dump(a, buf)
        exp = dedent(
            """\
        - e  # 5
        - d
        - c  # 3
        - b  # 2
        - a  # 1
        """,
        )
        assert buf.getvalue() == exp

    def test_issue_221_sort_key(self) -> None:
        from ruamel.yaml import YAML
        from ruamel.yaml.compat import StringIO

        yaml = YAML()
        inp = dedent(
            """\
        - four
        - One    # 1
        - Three  # 3
        - five   # 5
        - two    # 2
        """,
        )
        a = yaml.load(dedent(inp))
        a.sort(key=str.lower)
        buf = StringIO()
        yaml.dump(a, buf)
        exp = dedent(
            """\
        - five   # 5
        - four
        - One    # 1
        - Three  # 3
        - two    # 2
        """,
        )
        assert buf.getvalue() == exp

    def test_issue_221_sort_key_reverse(self) -> None:
        from ruamel.yaml import YAML
        from ruamel.yaml.compat import StringIO

        yaml = YAML()
        inp = dedent(
            """\
        - four
        - One    # 1
        - Three  # 3
        - five   # 5
        - two    # 2
        """,
        )
        a = yaml.load(dedent(inp))
        a.sort(key=str.lower, reverse=True)
        buf = StringIO()
        yaml.dump(a, buf)
        exp = dedent(
            """\
        - two    # 2
        - Three  # 3
        - One    # 1
        - four
        - five   # 5
        """,
        )
        assert buf.getvalue() == exp

    def test_issue_222(self) -> None:
        import ruamel.yaml
        from ruamel.yaml.compat import StringIO

        yaml = ruamel.yaml.YAML(typ='safe')
        buf = StringIO()
        yaml.dump(['012923'], buf)
        assert buf.getvalue() == "['012923']\n"

    def test_issue_223(self) -> None:
        import ruamel.yaml

        yaml = ruamel.yaml.YAML(typ='safe')
        yaml.load('phone: 0123456789')

    def test_issue_232(self) -> None:
        import ruamel.yaml

        yaml = YAML(typ='safe', pure=True)

        with pytest.raises(ruamel.yaml.parser.ParserError):
            yaml.load(']')
        with pytest.raises(ruamel.yaml.parser.ParserError):
            yaml.load('{]')

    def test_issue_233(self) -> None:
        from ruamel.yaml import YAML
        import json

        yaml = YAML()
        data = yaml.load('{}')
        json_str = json.dumps(data)  # NOQA

    def test_issue_233a(self) -> None:
        from ruamel.yaml import YAML
        import json

        yaml = YAML()
        data = yaml.load('[]')
        json_str = json.dumps(data)  # NOQA

    def test_issue_234(self) -> None:
        from ruamel.yaml import YAML

        inp = dedent(
            """\
        - key: key1
          ctx: [one, two]
          help: one
          cmd: >
            foo bar
            foo bar
        """,
        )
        yaml = YAML(typ='safe', pure=True)
        data = yaml.load(inp)
        fold = data[0]['cmd']
        print(repr(fold))
        assert '\a' not in fold

    def test_issue_236(self) -> None:
        inp = """
        conf:
          xx: {a: "b", c: []}
          asd: "nn"
        """
        d = round_trip(inp, preserve_quotes=True)  # NOQA

    def test_issue_238(self, tmpdir: Any) -> None:
        program_src = r"""
        import ruamel.yaml
        from ruamel.yaml.compat import StringIO

        yaml = ruamel.yaml.YAML(typ='unsafe')


        class A:
            def __setstate__(self, d):
                self.__dict__ = d


        class B:
            pass


        a = A()
        b = B()

        a.x = b
        b.y = [b]
        assert a.x.y[0] == a.x

        buf = StringIO()
        yaml.dump(a, buf)

        data = yaml.load(buf.getvalue())
        assert data.x.y[0] == data.x
        """
        assert save_and_run(dedent(program_src), tmpdir) == 0

    def test_issue_239(self) -> None:
        inp = """
        first_name: Art
        occupation: Architect
        # I'm safe
        about: Art Vandelay is a fictional character that George invents...
        # we are not :(
        # help me!
        ---
        # what?!
        hello: world
        # someone call the Batman
        foo: bar # or quz
        # Lost again
        ---
        I: knew
        # final words
        """
        d = YAML().round_trip_all(inp)  # NOQA

    def test_issue_242(self) -> None:
        from ruamel.yaml.comments import CommentedMap

        d0 = CommentedMap([('a', 'b')])
        assert d0['a'] == 'b'

    def test_issue_245(self) -> None:
        from ruamel.yaml import YAML

        inp = """
        d: yes
        """
        for typ in ['safepure', 'rt', 'safe']:
            if typ.endswith('pure'):
                pure = True
                typ = typ[:-4]
            else:
                pure = None

            yaml = YAML(typ=typ, pure=pure)
            yaml.version = (1, 1)
            d = yaml.load(inp)
            print(typ, yaml.parser, yaml.resolver)
            assert d['d'] is True

    def test_issue_249(self) -> None:
        yaml = YAML()
        inp = dedent(
            """\
        # comment
        -
          - 1
          - 2
          - 3
        """,
        )
        exp = dedent(
            """\
        # comment
        - - 1
          - 2
          - 3
        """,
        )
        yaml.round_trip(inp, outp=exp)  # NOQA

    def test_issue_250(self) -> None:
        inp = """
        # 1.
        - - 1
        # 2.
        - map: 2
        # 3.
        - 4
        """
        d = round_trip(inp)  # NOQA

    # @pytest.mark.xfail(strict=True, reason='bla bla', raises=AssertionError)
    def test_issue_279(self) -> None:
        from ruamel.yaml import YAML
        from ruamel.yaml.compat import StringIO

        yaml = YAML()
        yaml.indent(sequence=4, offset=2)
        inp = dedent(
            """\
        experiments:
          - datasets:
        # ATLAS EWK
              - {dataset: ATLASWZRAP36PB, frac: 1.0}
              - {dataset: ATLASZHIGHMASS49FB, frac: 1.0}
        """,
        )
        a = yaml.load(inp)
        buf = StringIO()
        yaml.dump(a, buf)
        print(buf.getvalue())
        assert buf.getvalue() == inp

    def test_issue_280(self) -> None:
        from ruamel.yaml import YAML
        from ruamel.yaml.representer import RepresenterError
        from collections import namedtuple
        from sys import stdout

        T = namedtuple('T', ('a', 'b'))
        t = T(1, 2)
        yaml = YAML()
        with pytest.raises(RepresenterError, match='cannot represent'):
            yaml.dump({'t': t}, stdout)

    def test_issue_282(self) -> None:
        # update from list of tuples caused AttributeError
        import ruamel.yaml

        yaml_data = ruamel.yaml.comments.CommentedMap([('a', 'apple'), ('b', 'banana')])
        yaml_data.update([('c', 'cantaloupe')])
        yaml_data.update({'d': 'date', 'k': 'kiwi'})
        assert 'c' in yaml_data.keys()
        assert 'c' in yaml_data._ok

    def test_issue_284(self) -> None:
        import ruamel.yaml

        inp = dedent(
            """\
        plain key: in-line value
        : # Both empty
        "quoted key":
        - entry
        """,
        )
        yaml = ruamel.yaml.YAML(typ='rt')
        yaml.version = (1, 2)
        d = yaml.load(inp)
        assert d[None] is None

        yaml = ruamel.yaml.YAML(typ='rt')
        yaml.version = (1, 1)
        with pytest.raises(ruamel.yaml.parser.ParserError, match='expected <block end>'):
            d = yaml.load(inp)

    def test_issue_285(self) -> None:
        from ruamel.yaml import YAML

        yaml = YAML()
        inp = dedent(
            """\
        %YAML 1.1
        ---
        - y
        - n
        - Y
        - N
        """,
        )
        a = yaml.load(inp)
        assert a[0]
        assert a[2]
        assert not a[1]
        assert not a[3]

    def test_issue_286(self) -> None:
        from ruamel.yaml import YAML
        from ruamel.yaml.compat import StringIO

        yaml = YAML()
        inp = dedent(
            """\
        parent_key:
        - sub_key: sub_value

        # xxx""",
        )
        a = yaml.load(inp)
        a['new_key'] = 'new_value'
        buf = StringIO()
        yaml.dump(a, buf)
        assert buf.getvalue().endswith('xxx\nnew_key: new_value\n')

    def test_issue_288(self) -> None:
        import sys
        from ruamel.yaml.compat import StringIO
        from ruamel.yaml import YAML

        yamldoc = dedent(
            """\
        ---
        # Reusable values
        aliases:
          # First-element comment
          - &firstEntry First entry
          # Second-element comment
          - &secondEntry Second entry

          # Third-element comment is
          # a multi-line value
          - &thirdEntry Third entry

        # EOF Comment
        """,
        )

        yaml = YAML()
        yaml.indent(mapping=2, sequence=4, offset=2)
        yaml.explicit_start = True
        yaml.preserve_quotes = True
        yaml.width = sys.maxsize
        data = yaml.load(yamldoc)
        buf = StringIO()
        yaml.dump(data, buf)
        assert buf.getvalue() == yamldoc

    def test_issue_288a(self) -> None:
        import sys
        from ruamel.yaml.compat import StringIO
        from ruamel.yaml import YAML

        yamldoc = dedent(
            """\
        ---
        # Reusable values
        aliases:
          # First-element comment
          - &firstEntry First entry
          # Second-element comment
          - &secondEntry Second entry

          # Third-element comment is
           # a multi-line value
          - &thirdEntry Third entry

        # EOF Comment
        """,
        )

        yaml = YAML()
        yaml.indent(mapping=2, sequence=4, offset=2)
        yaml.explicit_start = True
        yaml.preserve_quotes = True
        yaml.width = sys.maxsize
        data = yaml.load(yamldoc)
        buf = StringIO()
        yaml.dump(data, buf)
        assert buf.getvalue() == yamldoc

    def test_issue_290(self) -> None:
        import sys
        from ruamel.yaml.compat import StringIO
        from ruamel.yaml import YAML

        yamldoc = dedent(
            """\
        ---
        aliases:
          # Folded-element comment
          # for a multi-line value
          - &FoldedEntry >
            THIS IS A
            FOLDED, MULTI-LINE
            VALUE

          # Literal-element comment
          # for a multi-line value
          - &literalEntry |
            THIS IS A
            LITERAL, MULTI-LINE
            VALUE

          # Plain-element comment
          - &plainEntry Plain entry
        """,
        )

        yaml = YAML()
        yaml.indent(mapping=2, sequence=4, offset=2)
        yaml.explicit_start = True
        yaml.preserve_quotes = True
        yaml.width = sys.maxsize
        data = yaml.load(yamldoc)
        buf = StringIO()
        yaml.dump(data, buf)
        assert buf.getvalue() == yamldoc

    def test_issue_290a(self) -> None:
        import sys
        from ruamel.yaml.compat import StringIO
        from ruamel.yaml import YAML

        yamldoc = dedent(
            """\
        ---
        aliases:
          # Folded-element comment
          # for a multi-line value
          - &FoldedEntry >
            THIS IS A
            FOLDED, MULTI-LINE
            VALUE

          # Literal-element comment
          # for a multi-line value
          - &literalEntry |
            THIS IS A
            LITERAL, MULTI-LINE
            VALUE

          # Plain-element comment
          - &plainEntry Plain entry
        """,
        )

        yaml = YAML()
        yaml.indent(mapping=2, sequence=4, offset=2)
        yaml.explicit_start = True
        yaml.preserve_quotes = True
        yaml.width = sys.maxsize
        data = yaml.load(yamldoc)
        buf = StringIO()
        yaml.dump(data, buf)
        assert buf.getvalue() == yamldoc

    # @pytest.mark.xfail(strict=True, reason='should fail pre 0.15.100', raises=AssertionError)
    def test_issue_295(self) -> None:
        # deepcopy also makes a copy of the start and end mark, and these did not
        # have any comparison beyond their ID, which of course changed, breaking
        # some old merge_comment code
        import copy

        inp = dedent(
            """
        A:
          b:
          # comment
          - l1
          - l2

        C:
          d: e
          f:
          # comment2
          - - l31
            - l32
            - l33: '5'
        """,
        )
        data = round_trip_load(inp)  # NOQA
        dc = copy.deepcopy(data)
        assert round_trip_dump(dc) == inp

    def test_issue_300(self) -> None:
        from ruamel.yaml import YAML

        inp = dedent(
            """
        %YAML 1.2
        %TAG ! tag:example.com,2019/path#fragment
        ---
        null
        """,
        )
        YAML().load(inp)

    def test_issue_300a(self) -> None:
        import ruamel.yaml

        inp = dedent(
            """
        %YAML 1.1
        %TAG ! tag:example.com,2019/path#fragment
        ---
        null
        """,
        )
        yaml = YAML()
        with pytest.raises(
            ruamel.yaml.scanner.ScannerError, match='while scanning a directive',
        ):
            yaml.load(inp)

    def test_issue_304(self) -> None:
        inp = """
        %YAML 1.2
        %TAG ! tag:example.com,2019:
        ---
        !foo null
        ...
        """
        d = na_round_trip(inp)  # NOQA

    def test_issue_305(self) -> None:
        inp = """
        %YAML 1.2
        ---
        !<tag:example.com,2019/path#foo> null
        ...
        """
        d = na_round_trip(inp)  # NOQA

    def test_issue_307(self) -> None:
        inp = """
        %YAML 1.2
        %TAG ! tag:example.com,2019/path#
        ---
        null
        ...
        """
        d = na_round_trip(inp)  # NOQA

    def test_issue_445(self) -> None:
        from ruamel.yaml import YAML
        from ruamel.yaml.compat import StringIO

        yaml = YAML()
        yaml.version = '1.1'
        data = yaml.load('quote: I have seen things')
        buf = StringIO()
        yaml.dump(data, buf)
        assert buf.getvalue() == '%YAML 1.1\n---\nquote: I have seen things\n'
        yaml = YAML()
        yaml.version = [1, 1]
        data = yaml.load('quote: I have seen things')
        buf = StringIO()
        yaml.dump(data, buf)
        assert buf.getvalue() == '%YAML 1.1\n---\nquote: I have seen things\n'

    def test_issue_447(self) -> None:
        from ruamel.yaml import YAML

        YAML().load('{\n\t"FOO": "BAR"\n}')

    def test_issue_449(self) -> None:
        inp = """\
        emoji_index: !!python/name:materialx.emoji.twemoji
        """
        d = na_round_trip(inp)  # NOQA

    def test_issue_455(self) -> None:
        from ruamel.yaml import YAML

        cm = YAML().map(a=97, b=98)
        cm.update({'c': 42, 'd': 196})
        cm.update(c=99, d=100)
        prev = None
        for k, v in cm.items():
            if prev is not None:
                assert prev + 1 == v
            prev = v
            assert ord(k) == v
        assert len(cm) == 4

    def test_issue_453(self) -> None:
        from io import StringIO
        from ruamel.yaml import YAML

        inp = dedent(
            """
        to-merge: &anchor
          merge-key: should not be duplicated

        to-merge2: &anchor2
          merge-key2: should not be duplicated

        usage:
          <<: [*anchor, *anchor2]
          usage-key: usage-value
        """,
        )
        yaml = YAML()
        data = yaml.load(inp)
        data['usage'].insert(0, 'insert-key', 'insert-value')
        out_stream = StringIO()
        yaml.dump(data, out_stream)
        result = out_stream.getvalue()
        print(result)
        assert inp.replace('usage:\n', 'usage:\n  insert-key: insert-value\n') == result

    def test_issue_454(self) -> None:
        inp = """
        test1: 🎉
        test2: "🎉"
        test3: '🎉'
        """
        d = round_trip(inp, preserve_quotes=True)  # NOQA

    def test_so_75631454(self) -> None:
        from ruamel.yaml import YAML
        from ruamel.yaml.compat import StringIO

        inp = dedent(
            """
        test:
            long: "This is a sample text
                across two lines."
        """,
        )
        yaml = YAML()
        yaml.preserve_quotes = True
        yaml.indent(mapping=4)
        yaml.width = 27
        data = yaml.load(inp)
        buf = StringIO()
        yaml.dump(data, buf)
        assert buf.getvalue() == inp

    def test_issue_458(self) -> None:
        from io import StringIO
        from ruamel.yaml import YAML

        yaml = YAML()
        out_stream = StringIO()
        in_string = 'a' * 128
        yaml.dump(in_string, out_stream)
        result = out_stream.getvalue()
        assert in_string == result.splitlines()[0]

    def test_issue_459(self) -> None:
        from io import StringIO
        from ruamel.yaml import YAML

        MYOBJ = {
            'data': dedent(
                """\
              example: "first"
              data:
                - flag: true
                  integer: 1
                  float: 1.0
                  string: "this is a string"
                  list:
                    - first
                    - second
                    - third
                  circle:
                    x: 10cm
                    y: 10cm
                    radius: 2.24cm

                - flag: false
                  integer: 2
                  float: 2.0
                  string: "this is another string"
                  list:
                    - first
                    - second
                    - third
                  circle:
                    x: 20cm
                    y: 20cm
                    radius: 2.24cm
              """,
            ),
        }
        yaml = YAML()
        yaml.width = 60
        out_stream = StringIO()
        yaml.dump([MYOBJ], out_stream)
        data = yaml.load(out_stream.getvalue())
        assert data[0]['data'] == MYOBJ['data']

    def test_issue_461(self) -> None:
        from ruamel.yaml import YAML

        yaml = YAML()

        inp = dedent(
            """
        first name: Roy
        last name: Rogers
        city: somewhere
        """,
        )
        yaml = YAML()
        data = yaml.load(inp)
        data.pop('last name')
        assert data.pop('not there', 'xxx') == 'xxx'
        data.insert(1, 'last name', 'Beaty', comment='he has seen things')

    def test_issue_463(self) -> None:
        import sys
        from ruamel.yaml.compat import StringIO
        from ruamel.yaml import YAML

        yaml = YAML()

        inp = dedent(
            """
        first_name: Art
        """,
        )
        data = yaml.load(inp)
        _ = data.merge
        data.insert(0, 'some_key', 'test')
        yaml.dump(data, sys.stdout)
        buf = StringIO()
        yaml.dump(data, buf)
        exp = dedent(
            """
        some_key: test
        first_name: Art
        """,
        )
        assert buf.getvalue() == exp

    def test_issue_464(self) -> None:
        # document end marker without newline threw error in 0.17.27
        from ruamel.yaml import YAML

        yaml = YAML()
        yaml.load('---\na: True\n...')

    def test_issue_467(self) -> None:
        import ruamel.yaml

        yaml = ruamel.yaml.YAML()
        yaml.constructor.add_constructor(yaml.resolver.DEFAULT_MAPPING_TAG, lambda x, y: None)

#    @pytest.mark.xfail(strict=True, reason='bla bla', raises=AssertionError)
#    def test_issue_ xxx(self) -> None:
#        inp = """
#        """
#        d = round_trip(inp)  # NOQA
