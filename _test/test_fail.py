# coding: utf-8

# there is some work to do
# provide a failing test xyz and a non-failing xyz_no_fail ( to see
# what the current failing output is.
# on fix of ruamel.yaml, move the marked test to the appropriate test (without mark)
# and remove remove the xyz_no_fail

import pytest

from roundtrip import round_trip, dedent, round_trip_load, round_trip_dump


class TestCommentFailures:
    @pytest.mark.xfail
    def test_set_comment_before_tag(self):
        # no comments before tags
        round_trip("""
        # the beginning
        !!set
        # or this one?
        ? a
        # next one is B (lowercase)
        ? b  #  You see? Promised you.
        ? c
        # this is the end
        """)

    def test_set_comment_before_tag_no_fail(self):
        # no comments before tags
        assert round_trip_dump(round_trip_load("""
        # the beginning
        !!set
        # or this one?
        ? a
        # next one is B (lowercase)
        ? b  #  You see? Promised you.
        ? c
        # this is the end
        """)) == dedent("""
        !!set
        # or this one?
        ? a
        # next one is B (lowercase)
        ? b  #  You see? Promised you.
        ? c
        # this is the end
        """)

    @pytest.mark.xfail
    def test_comment_dash_line(self):
        round_trip("""
        - # abc
           a: 1
           b: 2
        """)

    def test_comment_dash_line_fail(self):
        x = """
        - # abc
           a: 1
           b: 2
        """
        data = round_trip_load(x)
        # this is not nice
        assert round_trip_dump(data) == dedent("""
          # abc
        - a: 1
          b: 2
        """)


class TestIndentFailures:

    @pytest.mark.xfail
    def test_roundtrip_four_space_indents(self):
        s = (
            'a:\n'
            '-   foo\n'
            '-   bar\n'
        )
        output = round_trip(s)
        assert s == output

    def test_roundtrip_four_space_indents_no_fail(self):
        assert round_trip_dump(round_trip_load("""
        a:
        -   foo
        -   bar
        """)) == dedent("""
        a:
        - foo
        - bar
        """)

    @pytest.mark.xfail
    def test_roundtrip_four_space_indents_expl_indent(self):
        s = (
            'a:\n'
            '- foo\n'
            '- bar\n'
        )
        output = round_trip_dump(round_trip_load(s), indent=4)
        assert s == output

    def test_roundtrip_four_space_indents_expl_indent_no_fail(self):
        assert round_trip_dump(round_trip_load("""
        a:
        -   foo
        -   bar
        """), indent=4) == dedent("""
        a:
        -   foo
        -   bar
        """)

    @pytest.mark.xfail
    def test_indent_not_retained(self):
        round_trip("""
        verbosity: 1                  # 0 is minimal output, -1 none
        base_url: http://gopher.net
        special_indices: [1, 5, 8]
        also_special:
        - a
        - 19
        - 32
        asia and europe: &asia_europe
            Turkey: Ankara
            Russia: Moscow
        countries:
            Asia:
                <<: *asia_europe
                Japan: Tokyo # 東京
            Europe:
                <<: *asia_europe
                Spain: Madrid
                Italy: Rome
            Antarctica:
            -   too cold
        """)

    def test_indent_not_retained_no_fail(self):
        assert round_trip_dump(round_trip_load("""
        verbosity: 1                  # 0 is minimal output, -1 none
        base_url: http://gopher.net
        special_indices: [1, 5, 8]
        also_special:
        - a
        - 19
        - 32
        asia and europe: &asia_europe
            Turkey: Ankara
            Russia: Moscow
        countries:
            Asia:
                <<: *asia_europe
                Japan: Tokyo # 東京
            Europe:
                <<: *asia_europe
                Spain: Madrid
                Italy: Rome
            Antarctica:
            -   too cold
        """), indent=4) == dedent("""
        verbosity: 1                  # 0 is minimal output, -1 none
        base_url: http://gopher.net
        special_indices: [1, 5, 8]
        also_special:
        -   a
        -   19
        -   32
        asia and europe: &asia_europe
            Turkey: Ankara
            Russia: Moscow
        countries:
            Asia:
                <<: *asia_europe
                Japan: Tokyo # 東京
            Europe:
                <<: *asia_europe
                Spain: Madrid
                Italy: Rome
            Antarctica:
            -   too cold
        """)

    def Xtest_indent_top_level_no_fail(self):
        round_trip("""
        -   a:
            - b
        """, indent=4)


class TestTagFailures:
    @pytest.mark.xfail
    def test_standard_short_tag(self):
        round_trip("""\
        !!map
        name: Anthon
        location: Germany
        language: python
        """)

    def test_standard_short_tag_no_fail(self):
        assert round_trip_dump(round_trip_load("""
        !!map
        name: Anthon
        location: Germany
        language: python
        """)) == dedent("""
        name: Anthon
        location: Germany
        language: python
        """)
