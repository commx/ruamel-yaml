# coding: utf-8

"""
various test cases for string scalars in YAML files
'|' for preserved newlines
'>' for folded (newlines become spaces)

and the chomping modifiers:
'-' for stripping: final line break and any trailing empty lines are excluded
'+' for keeping: final line break and empty lines are preserved
''  for clipping: final line break preserved, empty lines at end not
    included in content (no modifier)

"""

import pytest  # type: ignore
import platform

# from ruamel.yaml.compat import ordereddict
from roundtrip import round_trip, dedent, round_trip_load, round_trip_dump  # type: ignore # NOQA


class TestLiteralScalarString:
    def test_basic_string(self) -> None:
        round_trip("""
        a: abcdefg
        """)

    def test_quoted_integer_string(self) -> None:
        round_trip("""
        a: '12345'
        """)

    @pytest.mark.skipif(  # type: ignore
        platform.python_implementation() == 'Jython', reason='Jython throws RepresenterError',
    )
    def test_preserve_string(self) -> None:
        inp = """
        a: |
          abc
          def
        """
        round_trip(inp, intermediate=dict(a='abc\ndef\n'))

    @pytest.mark.skipif(  # type: ignore
        platform.python_implementation() == 'Jython', reason='Jython throws RepresenterError',
    )
    def test_preserve_string_strip(self) -> None:
        s = """
        a: |-
          abc
          def

        """
        round_trip(s, intermediate=dict(a='abc\ndef'))

    @pytest.mark.skipif(  # type: ignore
        platform.python_implementation() == 'Jython', reason='Jython throws RepresenterError',
    )
    def test_preserve_string_keep(self) -> None:
        # with pytest.raises(AssertionError) as excinfo:
        inp = """
            a: |+
              ghi
              jkl


            b: x
            """
        round_trip(inp, intermediate=dict(a='ghi\njkl\n\n\n', b='x'))

    @pytest.mark.skipif(  # type: ignore
        platform.python_implementation() == 'Jython', reason='Jython throws RepresenterError',
    )
    def test_preserve_string_keep_at_end(self) -> None:
        # at EOF you have to specify the ... to get proper "closure"
        # of the multiline scalar
        inp = """
            a: |+
              ghi
              jkl

            ...
            """
        round_trip(inp, intermediate=dict(a='ghi\njkl\n\n'))

    def test_fold_string(self) -> None:
        inp = """
        a: >
          abc
          def

        """
        round_trip(inp)

    def test_fold_string_strip(self) -> None:
        inp = """
        a: >-
          abc
          def

        """
        round_trip(inp)

    def test_fold_string_keep(self) -> None:
        with pytest.raises(AssertionError) as excinfo:  # NOQA
            inp = """
            a: >+
              abc
              def

            """
            round_trip(inp, intermediate=dict(a='abc def\n\n'))


class TestQuotedScalarString:
    def test_single_quoted_string(self) -> None:
        inp = """
        a: 'abc'
        """
        round_trip(inp, preserve_quotes=True)

    def test_double_quoted_string(self) -> None:
        inp = """
        a: "abc"
        """
        round_trip(inp, preserve_quotes=True)

    def test_non_preserved_double_quoted_string(self) -> None:
        inp = """
        a: "abc"
        """
        exp = """
        a: abc
        """
        round_trip(inp, outp=exp)


class TestReplace:
    """inspired by issue 110 from sandres23"""

    def test_replace_preserved_scalar_string(self) -> None:
        import ruamel

        s = dedent("""\
        foo: |
          foo
          foo
          bar
          foo
        """)
        data = round_trip_load(s, preserve_quotes=True)
        so = data['foo'].replace('foo', 'bar', 2)
        assert isinstance(so, ruamel.yaml.scalarstring.LiteralScalarString)
        assert so == dedent("""
        bar
        bar
        bar
        foo
        """)

    def test_replace_double_quoted_scalar_string(self) -> None:
        import ruamel

        s = dedent("""\
        foo: "foo foo bar foo"
        """)
        data = round_trip_load(s, preserve_quotes=True)
        so = data['foo'].replace('foo', 'bar', 2)
        assert isinstance(so, ruamel.yaml.scalarstring.DoubleQuotedScalarString)
        assert so == 'bar bar bar foo'


class TestWalkTree:
    def test_basic(self) -> None:
        from ruamel.yaml.comments import CommentedMap
        from ruamel.yaml.scalarstring import walk_tree

        data = CommentedMap()
        data[1] = 'a'
        data[2] = 'with\nnewline\n'
        walk_tree(data)
        exp = """\
        1: a
        2: |
          with
          newline
        """
        assert round_trip_dump(data) == dedent(exp)

    def test_map(self) -> None:
        from ruamel.yaml.compat import ordereddict
        from ruamel.yaml.comments import CommentedMap
        from ruamel.yaml.scalarstring import walk_tree, preserve_literal
        from ruamel.yaml.scalarstring import DoubleQuotedScalarString as dq
        from ruamel.yaml.scalarstring import SingleQuotedScalarString as sq

        data = CommentedMap()
        data[1] = 'a'
        data[2] = 'with\nnew : line\n'
        data[3] = '${abc}'
        data[4] = 'almost:mapping'
        m = ordereddict([('\n', preserve_literal), ('${', sq), (':', dq)])
        walk_tree(data, map=m)
        exp = """\
        1: a
        2: |
          with
          new : line
        3: '${abc}'
        4: "almost:mapping"
        """
        assert round_trip_dump(data) == dedent(exp)
