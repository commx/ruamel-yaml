# coding: utf-8

"""
testing of anchors and the aliases referring to them
"""

import pytest
from textwrap import dedent
import platform

from roundtrip import round_trip, dedent, round_trip_load, round_trip_dump  # NOQA


def load(s):
    return round_trip_load(dedent(s))


def compare(data, s):
    assert round_trip_dump(data) == dedent(s)


class TestAnchorsAliases:
    def test_anchor_id_renumber(self):
        from ruamel.yaml.serializer import Serializer
        assert Serializer.ANCHOR_TEMPLATE == 'id%03d'
        data = load("""
        a: &id002
          b: 1
          c: 2
        d: *id002
        """)
        compare(data, """
        a: &id001
          b: 1
          c: 2
        d: *id001
        """)

    def test_template_matcher(self):
        """test if id matches the anchor template"""
        from ruamel.yaml.serializer import templated_id
        assert templated_id(u'id001')
        assert templated_id(u'id999')
        assert templated_id(u'id1000')
        assert templated_id(u'id0001')
        assert templated_id(u'id0000')
        assert not templated_id(u'id02')
        assert not templated_id(u'id000')
        assert not templated_id(u'x000')

    # def test_re_matcher(self):
    #     import re
    #     assert re.compile(u'id(?!000)\\d{3,}').match('id001')
    #     assert not re.compile(u'id(?!000\\d*)\\d{3,}').match('id000')
    #     assert re.compile(u'id(?!000$)\\d{3,}').match('id0001')

    def test_anchor_assigned(self):
        from ruamel.yaml.comments import CommentedMap
        data = load("""
        a: &id002
          b: 1
          c: 2
        d: *id002
        e: &etemplate
          b: 1
          c: 2
        f: *etemplate
        """)
        d = data['d']
        assert isinstance(d, CommentedMap)
        assert d.yaml_anchor() is None  # got dropped as it matches pattern
        e = data['e']
        assert isinstance(e, CommentedMap)
        assert e.yaml_anchor().value == 'etemplate'
        assert e.yaml_anchor().always_dump is False

    def test_anchor_id_retained(self):
        data = load("""
        a: &id002
          b: 1
          c: 2
        d: *id002
        e: &etemplate
          b: 1
          c: 2
        f: *etemplate
        """)
        compare(data, """
        a: &id001
          b: 1
          c: 2
        d: *id001
        e: &etemplate
          b: 1
          c: 2
        f: *etemplate
        """)

    @pytest.mark.skipif(platform.python_implementation() == 'Jython',
                        reason="Jython throws RepresenterError")
    def test_alias_before_anchor(self):
        from ruamel.yaml.composer import ComposerError
        with pytest.raises(ComposerError):
            data = load("""
            d: *id002
            a: &id002
              b: 1
              c: 2
            """)
            data = data

    def test_anchor_on_sequence(self):
        # as reported by Bjorn Stabell
        # https://bitbucket.org/ruamel/yaml/issue/7/anchor-names-not-preserved
        from ruamel.yaml.comments import CommentedSeq
        data = load("""
        nut1: &alice
         - 1
         - 2
        nut2: &blake
         - some data
         - *alice
        nut3:
         - *blake
         - *alice
        """)
        l = data['nut1']
        assert isinstance(l, CommentedSeq)
        assert l.yaml_anchor() is not None
        assert l.yaml_anchor().value == 'alice'

    merge_yaml = dedent("""
        - &CENTER {x: 1, y: 2}
        - &LEFT {x: 0, y: 2}
        - &BIG {r: 10}
        - &SMALL {r: 1}
        # All the following maps are equal:
        # Explicit keys
        - x: 1
          y: 2
          r: 10
          label: center/small
        # Merge one map
        - <<: *CENTER
          r: 10
          label: center/medium
        # Merge multiple maps
        - <<: [*CENTER, *BIG]
          label: center/big
        # Override
        - <<: [*BIG, *LEFT, *SMALL]
          x: 1
          label: center/huge
        """)

    def test_merge_00(self):
        data = load(self.merge_yaml)
        d = data[4]
        ok = True
        for k in d:
            for o in [5, 6, 7]:
                x = d.get(k)
                y = data[o].get(k)
                if not isinstance(x, int):
                    x = x.split('/')[0]
                    y = y.split('/')[0]
                if x != y:
                    ok = False
                    print('key', k, d.get(k), data[o].get(k))
        assert ok

    def test_merge_accessible(self):
        from ruamel.yaml.comments import CommentedMap, merge_attrib
        data = load("""
        k: &level_2 { a: 1, b2 }
        l: &level_1 { a: 10, c: 3 }
        m:
          << : *level_1
          c: 30
          d: 40
        """)
        d = data['m']
        assert isinstance(d, CommentedMap)
        assert hasattr(d, merge_attrib)

    def test_merge_01(self):
        data = load(self.merge_yaml)
        compare(data, self.merge_yaml)

    def test_merge_nested(self):
        yaml = '''
        a:
          <<: &content
            1: plugh
            2: plover
          0: xyzzy
        b:
          <<: *content
        '''
        data = round_trip(yaml)  # NOQA

    def test_merge_nested_with_sequence(self):
        yaml = '''
        a:
          <<: &content
            <<: &y2
              1: plugh
            2: plover
          0: xyzzy
        b:
          <<: [*content, *y2]
        '''
        data = round_trip(yaml)  # NOQA

    def test_add_anchor(self):
        from ruamel.yaml.comments import CommentedMap
        data = CommentedMap()
        data_a = CommentedMap()
        data['a'] = data_a
        data_a['c'] = 3
        data['b'] = 2
        data.yaml_set_anchor('klm', always_dump=True)
        data['a'].yaml_set_anchor('xyz', always_dump=True)
        compare(data, """
        &klm
        a: &xyz
          c: 3
        b: 2
        """)
