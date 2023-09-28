# coding: utf-8

"""
testing of anchors and the aliases referring to them
"""

import pytest  # type: ignore  # NOQA
import platform

from roundtrip import round_trip, dedent, round_trip_load, round_trip_dump, YAML # type: ignore # NOQA
from typing import Any


def load(s: str) -> Any:
    return round_trip_load(dedent(s))


def compare(d: Any, s: str) -> None:
    assert round_trip_dump(d) == dedent(s)


class TestAnchorsAliases:
    def test_anchor_id_renumber(self) -> None:
        from ruamel.yaml.serializer import Serializer

        assert Serializer.ANCHOR_TEMPLATE == 'id{:03d}'
        data = load("""
        a: &id002
          b: 1
          c: 2
        d: *id002
        """)
        compare(
            data,
            """
        a: &id001
          b: 1
          c: 2
        d: *id001
        """,
        )

    def test_template_matcher(self) -> None:
        """test if id matches the anchor template"""
        from ruamel.yaml.serializer import templated_id

        assert templated_id('id001')
        assert templated_id('id999')
        assert templated_id('id1000')
        assert templated_id('id0001')
        assert templated_id('id0000')
        assert not templated_id('id02')
        assert not templated_id('id000')
        assert not templated_id('x000')

    # def test_re_matcher(self) -> None:
    #     import re
    #     assert re.compile('id(?!000)\\d{3,}').match('id001')
    #     assert not re.compile('id(?!000\\d*)\\d{3,}').match('id000')
    #     assert re.compile('id(?!000$)\\d{3,}').match('id0001')

    def test_anchor_assigned(self) -> None:
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

    def test_anchor_id_retained(self) -> None:
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
        compare(
            data,
            """
        a: &id001
          b: 1
          c: 2
        d: *id001
        e: &etemplate
          b: 1
          c: 2
        f: *etemplate
        """,
        )

    @pytest.mark.skipif(  # type: ignore
        platform.python_implementation() == 'Jython', reason='Jython throws RepresenterError',
    )
    def test_alias_before_anchor(self) -> None:
        from ruamel.yaml.composer import ComposerError

        with pytest.raises(ComposerError):
            data = load("""
            d: *id002
            a: &id002
              b: 1
              c: 2
            """)
            data = data

    def test_anchor_on_sequence(self) -> None:
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
        r = data['nut1']
        assert isinstance(r, CommentedSeq)
        assert r.yaml_anchor() is not None
        assert r.yaml_anchor().value == 'alice'

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

    def test_merge_00(self) -> None:
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

    def test_merge_accessible(self) -> None:
        from ruamel.yaml.comments import CommentedMap, merge_attrib

        data = load("""
        k: &level_2 { a: 1, b2 }
        l: &level_1 { a: 10, c: 3 }
        m:
          <<: *level_1
          c: 30
          d: 40
        """)
        d = data['m']
        assert isinstance(d, CommentedMap)
        assert hasattr(d, merge_attrib)

    def test_merge_01(self) -> None:
        data = load(self.merge_yaml)
        compare(data, self.merge_yaml)

    def test_merge_nested(self) -> None:
        yaml = """
        a:
          <<: &content
            1: plugh
            2: plover
          0: xyzzy
        b:
          <<: *content
        """
        data = round_trip(yaml)  # NOQA

    def test_merge_nested_with_sequence(self) -> None:
        yaml = """
        a:
          <<: &content
            <<: &y2
              1: plugh
            2: plover
          0: xyzzy
        b:
          <<: [*content, *y2]
        """
        data = round_trip(yaml)  # NOQA

    def test_add_anchor(self) -> None:
        from ruamel.yaml.comments import CommentedMap

        data = CommentedMap()
        data_a = CommentedMap()
        data['a'] = data_a
        data_a['c'] = 3
        data['b'] = 2
        data.yaml_set_anchor('klm', always_dump=True)
        data['a'].yaml_set_anchor('xyz', always_dump=True)
        compare(
            data,
            """
        &klm
        a: &xyz
          c: 3
        b: 2
        """,
        )

    # this is an error in PyYAML
    def test_reused_anchor(self) -> None:
        from ruamel.yaml.error import ReusedAnchorWarning

        yaml = """
        - &a
          x: 1
        - <<: *a
        - &a
          x: 2
        - <<: *a
        """
        with pytest.warns(ReusedAnchorWarning):
            data = round_trip(yaml)  # NOQA

    def test_issue_130(self) -> None:
        # issue 130 reported by Devid Fee
        import ruamel.yaml

        ys = dedent("""\
        components:
          server: &server_component
            type: spark.server:ServerComponent
            host: 0.0.0.0
            port: 8000
          shell: &shell_component
            type: spark.shell:ShellComponent

        services:
          server: &server_service
            <<: *server_component
          shell: &shell_service
            <<: *shell_component
            components:
              server: {<<: *server_service}
        """)
        yaml = ruamel.yaml.YAML(typ='safe', pure=True)
        data = yaml.load(ys)
        assert data['services']['shell']['components']['server']['port'] == 8000

    def test_issue_130a(self) -> None:
        # issue 130 reported by Devid Fee
        import ruamel.yaml

        ys = dedent("""\
        components:
          server: &server_component
            type: spark.server:ServerComponent
            host: 0.0.0.0
            port: 8000
          shell: &shell_component
            type: spark.shell:ShellComponent

        services:
          server: &server_service
            <<: *server_component
            port: 4000
          shell: &shell_service
            <<: *shell_component
            components:
              server: {<<: *server_service}
        """)
        yaml = ruamel.yaml.YAML(typ='safe', pure=True)
        data = yaml.load(ys)
        assert data['services']['shell']['components']['server']['port'] == 4000


class TestMergeKeysValues:

    yaml_str = dedent("""\
    - &mx
      a: x1
      b: x2
      c: x3
    - &my
      a: y1
      b: y2  # masked by the one in &mx
      d: y4
    -
      a: 1
      <<: [*mx, *my]
      m: 6
    """)

    # in the following d always has "expanded" the merges

    def test_merge_for(self) -> None:
        from ruamel.yaml import YAML

        d = YAML(typ='safe', pure=True).load(self.yaml_str)
        data = round_trip_load(self.yaml_str)
        count = 0
        for x in data[2]:
            count += 1
            print(count, x)
        assert count == len(d[2])

    def test_merge_keys(self) -> None:
        from ruamel.yaml import YAML

        d = YAML(typ='safe', pure=True).load(self.yaml_str)
        data = round_trip_load(self.yaml_str)
        count = 0
        for x in data[2].keys():
            count += 1
            print(count, x)
        assert count == len(d[2])

    def test_merge_values(self) -> None:
        from ruamel.yaml import YAML

        d = YAML(typ='safe', pure=True).load(self.yaml_str)
        data = round_trip_load(self.yaml_str)
        count = 0
        for x in data[2].values():
            count += 1
            print(count, x)
        assert count == len(d[2])

    def test_merge_items(self) -> None:
        from ruamel.yaml import YAML

        d = YAML(typ='safe', pure=True).load(self.yaml_str)
        data = round_trip_load(self.yaml_str)
        count = 0
        for x in data[2].items():
            count += 1
            print(count, x)
        assert count == len(d[2])

    def test_len_items_delete(self) -> None:
        from ruamel.yaml import YAML

        d = YAML(typ='safe', pure=True).load(self.yaml_str)
        data = round_trip_load(self.yaml_str)
        x = data[2].items()
        print('d2 items', d[2].items(), len(d[2].items()), x, len(x))
        ref = len(d[2].items())
        print('ref', ref)
        assert len(x) == ref
        del data[2]['m']
        ref -= 1
        assert len(x) == ref
        del data[2]['d']
        ref -= 1
        assert len(x) == ref
        del data[2]['a']
        ref -= 1
        assert len(x) == ref

    def test_issue_196_cast_of_dict(self, capsys: Any) -> None:
        from ruamel.yaml import YAML

        yaml = YAML()
        mapping = yaml.load("""\
        anchored: &anchor
          a : 1

        mapping:
          <<: *anchor
          b: 2
        """)['mapping']

        for k in mapping:
            print('k', k)
        for k in mapping.copy():
            print('kc', k)

        print('v', list(mapping.keys()))
        print('v', list(mapping.values()))
        print('v', list(mapping.items()))
        print(len(mapping))
        print('-----')

        # print({**mapping})
        # print(type({**mapping}))
        # assert 'a' in {**mapping}
        assert 'a' in mapping
        x = {}
        for k in mapping:
            x[k] = mapping[k]
        assert 'a' in x
        assert 'a' in mapping.keys()
        assert mapping['a'] == 1
        assert mapping.__getitem__('a') == 1
        assert 'a' in dict(mapping)
        assert 'a' in dict(mapping.items())

    def test_values_of_merged(self) -> None:
        from ruamel.yaml import YAML

        yaml = YAML()
        data = yaml.load(dedent(self.yaml_str))
        assert list(data[2].values()) == [1, 6, 'x2', 'x3', 'y4']

    def test_issue_213_copy_of_merge(self) -> None:
        from ruamel.yaml import YAML

        yaml = YAML()
        d = yaml.load("""\
        foo: &foo
          a: a
        foo2:
          <<: *foo
          b: b
        """)['foo2']
        assert d['a'] == 'a'
        d2 = d.copy()
        assert d2['a'] == 'a'
        print('d', d)
        del d['a']
        assert 'a' not in d
        assert 'a' in d2


class TestDuplicateKeyThroughAnchor:
    def test_duplicate_key_00(self) -> None:
        from ruamel.yaml import version_info
        from ruamel.yaml import YAML
        from ruamel.yaml.constructor import DuplicateKeyFutureWarning, DuplicateKeyError

        s = dedent("""\
        &anchor foo:
            foo: bar
            *anchor : duplicate key
            baz: bat
            *anchor : duplicate key
        """)
        if version_info < (0, 15, 1):
            pass
        elif version_info < (0, 16, 0):
            with pytest.warns(DuplicateKeyFutureWarning):
                YAML(typ='safe', pure=True).load(s)
            with pytest.warns(DuplicateKeyFutureWarning):
                YAML(typ='rt').load(s)
        else:
            with pytest.raises(DuplicateKeyError):
                YAML(typ='safe', pure=True).load(s)
            with pytest.raises(DuplicateKeyError):
                YAML(typ='rt').load(s)

    def test_duplicate_key_01(self) -> None:
        # so issue https://stackoverflow.com/a/52852106/1307905
        from ruamel.yaml import version_info
        from ruamel.yaml.constructor import DuplicateKeyError

        s = dedent("""\
        - &name-name
          a: 1
        - &help-name
          b: 2
        - <<: *name-name
          <<: *help-name
        """)
        if version_info < (0, 15, 1):
            pass
        else:
            with pytest.raises(DuplicateKeyError):
                yaml = YAML(typ='safe')
                yaml.load(s)
            with pytest.raises(DuplicateKeyError):
                yaml = YAML()
                yaml.load(s)


class TestFullCharSetAnchors:
    def test_master_of_orion(self) -> None:
        # https://bitbucket.org/ruamel/yaml/issues/72/not-allowed-in-anchor-names
        # submitted by Shalon Wood
        yaml_str = """
        - collection: &Backend.Civilizations.RacialPerk
            items:
                  - key: perk_population_growth_modifier
        - *Backend.Civilizations.RacialPerk
        """
        data = load(yaml_str)  # NOQA

    def test_roundtrip_00(self) -> None:
        yaml_str = """
        - &dotted.words.here
          a: 1
          b: 2
        - *dotted.words.here
        """
        data = round_trip(yaml_str)  # NOQA

    def test_roundtrip_01(self) -> None:
        yaml_str = """
        - &dotted.words.here[a, b]
        - *dotted.words.here
        """
        data = load(yaml_str)  # NOQA
        compare(data, yaml_str.replace('[', ' ['))  # an extra space is inserted
