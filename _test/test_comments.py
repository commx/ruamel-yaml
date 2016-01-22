# coding: utf-8

"""
comment testing is all about roundtrips
these can be done in the "old" way by creating a file.data and file.roundtrip
but there is little flexibility in doing that

but some things are not easily tested, eog. how a
roundtrip changes

"""

import pytest

import ruamel.yaml
from roundtrip import round_trip, dedent, round_trip_load, round_trip_dump


class TestComments:
    def test_no_end_of_file_eol(self):
        """not excluding comments caused some problems if at the end of
        the file without a newline. First error, then included \0 """
        x = """\
        - europe: 10 # abc"""
        round_trip(x, extra='\n')
        with pytest.raises(AssertionError):
            round_trip(x, extra='a\n')

    def test_no_comments(self):
        round_trip("""
        - europe: 10
        - usa:
          - ohio: 2
          - california: 9
        """)

    def test_round_trip_ordering(self):
        round_trip("""
        a: 1
        b: 2
        c: 3
        b1: 2
        b2: 2
        d: 4
        e: 5
        f: 6
        """)

    def test_complex(self):
        round_trip("""
        - europe: 10 # top
        - usa:
          - ohio: 2
          - california: 9 # o
        """)

    def test_dropped(self):
        round_trip("""
        # comment
        scalar
        ...
        """, "scalar\n...\n")

    def test_main_mapping_begin_end(self):
        round_trip("""
        # C start a
        # C start b
        abc: 1
        ghi: 2
        klm: 3
        # C end a
        # C end b
        """)

    def test_main_mapping_begin_end_items_post(self):
        round_trip("""
        # C start a
        # C start b
        abc: 1      # abc comment
        ghi: 2
        klm: 3      # klm comment
        # C end a
        # C end b
        """)

    def test_main_sequence_begin_end(self):
        round_trip("""
        # C start a
        # C start b
        - abc
        - ghi
        - klm
        # C end a
        # C end b
        """)

    def test_main_sequence_begin_end_items_post(self):
        round_trip("""
        # C start a
        # C start b
        - abc      # abc comment
        - ghi
        - klm      # klm comment
        # C end a
        # C end b
        """)

    def test_main_mapping_begin_end_complex(self):
        round_trip("""
        # C start a
        # C start b
        abc: 1
        ghi: 2
        klm:
          3a: alpha
          3b: beta   # it is all greek to me
        # C end a
        # C end b
        """)

    def test_09(self):   # 2.9 from the examples in the spec
        round_trip("""
        hr: # 1998 hr ranking
          - Mark McGwire
          - Sammy Sosa
        rbi:
          # 1998 rbi ranking
        - Sammy Sosa
        - Ken Griffey
        """)

    def test_simple_map_middle_comment(self):
        round_trip("""
        abc: 1
        # C 3a
        # C 3b
        ghi: 2
        """)

    def test_map_in_map_0(self):
        round_trip("""
        map1: # comment 1
          # comment 2
          map2:
            key1: val1
        """)

    def test_map_in_map_1(self):
        # comment is moved from value to key
        round_trip("""
        map1:
          # comment 1
          map2:
            key1: val1
        """)

    def test_application_arguments(self):
        # application configur
        round_trip("""
        args:
          username: anthon
          passwd: secret
          fullname: Anthon van der Neut
          tmux:
            session-name: test
          loop:
            wait: 10
        """)

    def test_substitute(self):
        x = dedent("""
        args:
          username: anthon          # name
          passwd: secret            # password
          fullname: Anthon van der Neut
          tmux:
            session-name: test
          loop:
            wait: 10
        """)
        data = round_trip_load(x)
        data['args']['passwd'] = 'deleted password'
        # note the requirement to add spaces for alignment of comment
        x = x.replace(': secret          ', ': deleted password')
        assert round_trip_dump(data) == x


    def test_set_comment(self):
        round_trip("""
        !!set
        # the beginning
        ? a
        # next one is B (lowercase)
        ? b  #  You see? Promised you.
        ? c
        # this is the end
        """)

    @pytest.mark.xfail
    def XXXtest_set_comment_before_tag(self):
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

    def test_omap_comment_roundtrip(self):
        round_trip("""
        !!omap
        - a: 1
        - b: 2  # two
        - c: 3  # three
        - d: 4
        """)

    def test_omap_comment_roundtrip_pre_comment(self):
        round_trip("""
        !!omap
        - a: 1
        - b: 2  # two
        - c: 3  # three
        # last one
        - d: 4
        """)

    @pytest.mark.xfail
    def test_non_ascii_comment(self):
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
        """)


class TestMultiLevelGet:
    def test_mlget_00(self):
        x = dedent("""\
        a:
        - b:
          c: 42
        - d:
            f: 196
          e:
            g: 3.14
        """)
        d = round_trip_load(x)
        assert d.mlget(['a', 1, 'd', 'f'], list_ok=True) == 196
        with pytest.raises(AssertionError):
            d.mlget(['a', 1, 'd', 'f']) == 196

