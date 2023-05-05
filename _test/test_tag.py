# coding: utf-8

import pytest  # type: ignore # NOQA
from typing import Any

from roundtrip import round_trip, round_trip_load, YAML  # type: ignore


def register_xxx(**kw: Any) -> None:
    from ruamel import yaml

    class XXX(yaml.comments.CommentedMap):
        @staticmethod
        def yaml_dump(dumper: Any, data: Any) -> Any:
            return dumper.represent_mapping('!xxx', data)

        @classmethod
        def yaml_load(cls, constructor: Any, node: Any) -> Any:
            data = cls()
            yield data
            constructor.construct_mapping(node, data)

    yaml.add_constructor('!xxx', XXX.yaml_load, constructor=yaml.RoundTripConstructor)
    yaml.add_representer(XXX, XXX.yaml_dump, representer=yaml.RoundTripRepresenter)


class TestIndentFailures:
    def test_tag(self) -> None:
        round_trip("""\
        !!python/object:__main__.Developer
        name: Anthon
        location: Germany
        language: python
        """)

    def test_full_tag(self) -> None:
        round_trip("""\
        !!tag:yaml.org,2002:python/object:__main__.Developer
        name: Anthon
        location: Germany
        language: python
        """)

    def test_standard_tag(self) -> None:
        round_trip("""\
        !!tag:yaml.org,2002:python/object:map
        name: Anthon
        location: Germany
        language: python
        """)

    def test_Y1(self) -> None:
        round_trip("""\
        !yyy
        name: Anthon
        location: Germany
        language: python
        """)

    def test_Y2(self) -> None:
        round_trip("""\
        !!yyy
        name: Anthon
        location: Germany
        language: python
        """)

    @pytest.mark.xfail(strict=True)  # type: ignore
    def test_spec_6_26_tag_shorthands(self) -> None:
        round_trip("""\
        %TAG !e! tag:example.com,2000:app/
        ---
        - !local foo
        - !!str bar
        - !e!tag%21 baz
        """)


class TestRoundTripCustom:
    def test_X1(self) -> None:
        register_xxx()
        round_trip("""\
        !xxx
        name: Anthon
        location: Germany
        language: python
        """)

    @pytest.mark.xfail(strict=True)  # type: ignore
    def test_X_pre_tag_comment(self) -> None:
        register_xxx()
        round_trip("""\
        -
          # hello
          !xxx
          name: Anthon
          location: Germany
          language: python
        """)

    @pytest.mark.xfail(strict=True)  # type: ignore
    def test_X_post_tag_comment(self) -> None:
        register_xxx()
        round_trip("""\
        - !xxx
          # hello
          name: Anthon
          location: Germany
          language: python
        """)

    def test_scalar_00(self) -> None:
        # https://stackoverflow.com/a/45967047/1307905
        round_trip("""\
        Outputs:
          Vpc:
            Value: !Ref: vpc    # first tag
            Export:
              Name: !Sub "${AWS::StackName}-Vpc"  # second tag
        """)


class TestIssue201:
    def test_encoded_unicode_tag(self) -> None:
        round_trip_load("""
        s: !!python/%75nicode 'abc'
        """)


class TestImplicitTaggedNodes:
    def test_scalar(self) -> None:
        data = round_trip("""\
        - !SString abcdefg
        - !SFloat 1.0
        - !SInt 1961
        - !SBool true
        - !SLit |
          glitter in the dark near the Tanhäuser gate
        """)
        # tagged scalers have string or string types as value
        assert data[0].count('d') == 1
        assert data[1].count('1') == 1
        assert data[2].count('1') == 2
        assert data[3].count('u') == 1
        assert data[4].count('a') == 4

    def test_mapping(self) -> None:
        round_trip("""\
        - !Mapping {a: 1, b: 2}
        """)

    def test_sequence(self) -> None:
        yaml = YAML()
        yaml.brace_single_entry_mapping_in_flow_sequence = True
        yaml.mapping_value_align = True
        yaml.round_trip("""
        - !Sequence [a, {b: 1}, {c: {d: 3}}]
        """)

    def test_sequence2(self) -> None:
        yaml = YAML()
        yaml.mapping_value_align = True
        yaml.round_trip("""
        - !Sequence [a, b: 1, c: {d: 3}]
        """)
