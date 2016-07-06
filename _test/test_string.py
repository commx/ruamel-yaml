# coding: utf-8

from __future__ import print_function

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

import pytest
import platform

# from ruamel.yaml.compat import ordereddict
from roundtrip import round_trip, dedent, round_trip_load, round_trip_dump  # NOQA


class TestPreservedScalarString:
    def test_basic_string(self):
        round_trip("""
        a: abcdefg
        """, )

    def test_quoted_integer_string(self):
        round_trip("""
        a: '12345'
        """)

    @pytest.mark.skipif(platform.python_implementation() == 'Jython',
                        reason="Jython throws RepresenterError")
    def test_preserve_string(self):
        round_trip("""
            a: |
              abc
              def
            """, intermediate=dict(a='abc\ndef\n'))

    @pytest.mark.skipif(platform.python_implementation() == 'Jython',
                        reason="Jython throws RepresenterError")
    def test_preserve_string_strip(self):
        s = """
            a: |-
              abc
              def

            """
        round_trip(s, intermediate=dict(a='abc\ndef'))

    @pytest.mark.skipif(platform.python_implementation() == 'Jython',
                        reason="Jython throws RepresenterError")
    def test_preserve_string_keep(self):
            # with pytest.raises(AssertionError) as excinfo:
            round_trip("""
            a: |+
              ghi
              jkl


            b: x
            """, intermediate=dict(a='ghi\njkl\n\n\n', b='x'))

    @pytest.mark.skipif(platform.python_implementation() == 'Jython',
                        reason="Jython throws RepresenterError")
    def test_preserve_string_keep_at_end(self):
        # at EOF you have to specify the ... to get proper "closure"
        # of the multiline scalar
        round_trip("""
            a: |+
              ghi
              jkl

            ...
            """, intermediate=dict(a='ghi\njkl\n\n'))

    def test_fold_string(self):
        with pytest.raises(AssertionError) as excinfo:  # NOQA
            round_trip("""
            a: >
              abc
              def

            """, intermediate=dict(a='abc def\n'))

    def test_fold_string_strip(self):
        with pytest.raises(AssertionError) as excinfo:  # NOQA
            round_trip("""
            a: >-
              abc
              def

            """, intermediate=dict(a='abc def'))

    def test_fold_string_keep(self):
        with pytest.raises(AssertionError) as excinfo:  # NOQA
            round_trip("""
            a: >+
              abc
              def

            """, intermediate=dict(a='abc def\n\n'))


class TestQuotedScalarString:
    def test_single_quoted_string(self):
        round_trip("""
        a: 'abc'
        """, preserve_quotes=True)

    def test_double_quoted_string(self):
        round_trip("""
        a: "abc"
        """, preserve_quotes=True)

    def test_non_preserved_double_quoted_string(self):
        round_trip("""
        a: "abc"
        """, outp="""
        a: abc
        """)
