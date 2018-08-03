# coding: utf-8

from __future__ import print_function

import pytest  # NOQA

from roundtrip import round_trip, dedent, round_trip_load, round_trip_dump  # NOQA


def load(s):
    return round_trip_load(dedent(s))


def compare(data, s, **kw):
    assert round_trip_dump(data, **kw) == dedent(s)


def compare_eol(data, s):
    assert round_trip_dump(data).replace('\n', '|\n') == dedent(s).replace('EOL', "").replace(
        '\n', '|\n'
    )


# @pytest.mark.xfail


class TestCommentsManipulation:

    # list
    def test_seq_set_comment_on_existing_explicit_column(self):
        data = load(
            """
        - a   # comment 1
        - b
        - c
        """
        )
        data.yaml_add_eol_comment('comment 2', key=1, column=6)
        compare(
            data,
            """
        - a   # comment 1
        - b   # comment 2
        - c
        """,
        )

    def test_seq_overwrite_comment_on_existing_explicit_column(self):
        data = load(
            """
        - a   # comment 1
        - b
        - c
        """
        )
        data.yaml_add_eol_comment('comment 2', key=0, column=6)
        compare(
            data,
            """
        - a   # comment 2
        - b
        - c
        """,
        )

    def test_seq_first_comment_explicit_column(self):
        data = load(
            """
        - a
        - b
        - c
        """
        )
        data.yaml_add_eol_comment('comment 1', key=1, column=6)
        compare(
            data,
            """
        - a
        - b   # comment 1
        - c
        """,
        )

    def test_seq_set_comment_on_existing_column_prev(self):
        data = load(
            """
        - a   # comment 1
        - b
        - c
        - d     # comment 3
        """
        )
        data.yaml_add_eol_comment('comment 2', key=1)
        compare(
            data,
            """
        - a   # comment 1
        - b   # comment 2
        - c
        - d     # comment 3
        """,
        )

    def test_seq_set_comment_on_existing_column_next(self):
        data = load(
            """
        - a   # comment 1
        - b
        - c
        - d     # comment 3
        """
        )
        print(data._yaml_comment)
        # print(type(data._yaml_comment._items[0][0].start_mark))
        # ruamel.yaml.error.Mark
        # print(type(data._yaml_comment._items[0][0].start_mark))
        data.yaml_add_eol_comment('comment 2', key=2)
        compare(
            data,
            """
        - a   # comment 1
        - b
        - c     # comment 2
        - d     # comment 3
        """,
        )

    def test_seq_set_comment_on_existing_column_further_away(self):
        """
        no comment line before or after, take the latest before
        the new position
        """
        data = load(
            """
        - a   # comment 1
        - b
        - c
        - d
        - e
        - f     # comment 3
        """
        )
        print(data._yaml_comment)
        # print(type(data._yaml_comment._items[0][0].start_mark))
        # ruamel.yaml.error.Mark
        # print(type(data._yaml_comment._items[0][0].start_mark))
        data.yaml_add_eol_comment('comment 2', key=3)
        compare(
            data,
            """
        - a   # comment 1
        - b
        - c
        - d   # comment 2
        - e
        - f     # comment 3
        """,
        )

    def test_seq_set_comment_on_existing_explicit_column_with_hash(self):
        data = load(
            """
        - a   # comment 1
        - b
        - c
        """
        )
        data.yaml_add_eol_comment('#  comment 2', key=1, column=6)
        compare(
            data,
            """
        - a   # comment 1
        - b   #  comment 2
        - c
        """,
        )

    # dict

    def test_dict_set_comment_on_existing_explicit_column(self):
        data = load(
            """
        a: 1   # comment 1
        b: 2
        c: 3
        d: 4
        e: 5
        """
        )
        data.yaml_add_eol_comment('comment 2', key='c', column=7)
        compare(
            data,
            """
        a: 1   # comment 1
        b: 2
        c: 3   # comment 2
        d: 4
        e: 5
        """,
        )

    def test_dict_overwrite_comment_on_existing_explicit_column(self):
        data = load(
            """
        a: 1   # comment 1
        b: 2
        c: 3
        d: 4
        e: 5
        """
        )
        data.yaml_add_eol_comment('comment 2', key='a', column=7)
        compare(
            data,
            """
        a: 1   # comment 2
        b: 2
        c: 3
        d: 4
        e: 5
        """,
        )

    def test_map_set_comment_on_existing_column_prev(self):
        data = load(
            """
            a: 1   # comment 1
            b: 2
            c: 3
            d: 4
            e: 5     # comment 3
            """
        )
        data.yaml_add_eol_comment('comment 2', key='b')
        compare(
            data,
            """
            a: 1   # comment 1
            b: 2   # comment 2
            c: 3
            d: 4
            e: 5     # comment 3
            """,
        )

    def test_map_set_comment_on_existing_column_next(self):
        data = load(
            """
            a: 1   # comment 1
            b: 2
            c: 3
            d: 4
            e: 5     # comment 3
            """
        )
        data.yaml_add_eol_comment('comment 2', key='d')
        compare(
            data,
            """
            a: 1   # comment 1
            b: 2
            c: 3
            d: 4     # comment 2
            e: 5     # comment 3
            """,
        )

    def test_map_set_comment_on_existing_column_further_away(self):
        """
        no comment line before or after, take the latest before
        the new position
        """
        data = load(
            """
            a: 1   # comment 1
            b: 2
            c: 3
            d: 4
            e: 5     # comment 3
            """
        )
        data.yaml_add_eol_comment('comment 2', key='c')
        print(round_trip_dump(data))
        compare(
            data,
            """
            a: 1   # comment 1
            b: 2
            c: 3   # comment 2
            d: 4
            e: 5     # comment 3
            """,
        )

    # @pytest.mark.xfail
    def test_before_top_map_rt(self):
        data = load(
            """
        a: 1
        b: 2
        """
        )
        data.yaml_set_start_comment('Hello\nWorld\n')
        compare(
            data,
            """
        # Hello
        # World
        a: 1
        b: 2
        """.format(
                comment='#'
            ),
        )

    def test_before_top_map_replace(self):
        data = load(
            """
        # abc
        # def
        a: 1 # 1
        b: 2
        """
        )
        data.yaml_set_start_comment('Hello\nWorld\n')
        compare(
            data,
            """
        # Hello
        # World
        a: 1 # 1
        b: 2
        """.format(
                comment='#'
            ),
        )

    def test_before_top_map_from_scratch(self):
        from ruamel.yaml.comments import CommentedMap

        data = CommentedMap()
        data['a'] = 1
        data['b'] = 2
        data.yaml_set_start_comment('Hello\nWorld\n')
        # print(data.ca)
        # print(data.ca._items)
        compare(
            data,
            """
            # Hello
            # World
            a: 1
            b: 2
            """.format(
                comment='#'
            ),
        )

    def test_before_top_seq_rt(self):
        data = load(
            """
        - a
        - b
        """
        )
        data.yaml_set_start_comment('Hello\nWorld\n')
        print(round_trip_dump(data))
        compare(
            data,
            """
        # Hello
        # World
        - a
        - b
        """,
        )

    def test_before_top_seq_rt_replace(self):
        data = load(
            """
        # this
        # that
        - a
        - b
        """.format(
                comment='#'
            )
        )
        data.yaml_set_start_comment('Hello\nWorld\n')
        print(round_trip_dump(data))
        compare(
            data,
            """
        # Hello
        # World
        - a
        - b
        """.format(
                comment='#'
            ),
        )

    def test_before_top_seq_from_scratch(self):
        from ruamel.yaml.comments import CommentedSeq

        data = CommentedSeq()
        data.append('a')
        data.append('b')
        data.yaml_set_start_comment('Hello\nWorld\n')
        print(round_trip_dump(data))
        compare(
            data,
            """
        # Hello
        # World
        - a
        - b
        """.format(
                comment='#'
            ),
        )

    # nested variants
    def test_before_nested_map_rt(self):
        data = load(
            """
        a: 1
        b:
          c: 2
          d: 3
        """
        )
        data['b'].yaml_set_start_comment('Hello\nWorld\n')
        compare(
            data,
            """
        a: 1
        b:
        # Hello
        # World
          c: 2
          d: 3
        """.format(
                comment='#'
            ),
        )

    def test_before_nested_map_rt_indent(self):
        data = load(
            """
        a: 1
        b:
          c: 2
          d: 3
        """
        )
        data['b'].yaml_set_start_comment('Hello\nWorld\n', indent=2)
        compare(
            data,
            """
        a: 1
        b:
          # Hello
          # World
          c: 2
          d: 3
        """.format(
                comment='#'
            ),
        )
        print(data['b'].ca)

    def test_before_nested_map_from_scratch(self):
        from ruamel.yaml.comments import CommentedMap

        data = CommentedMap()
        datab = CommentedMap()
        data['a'] = 1
        data['b'] = datab
        datab['c'] = 2
        datab['d'] = 3
        data['b'].yaml_set_start_comment('Hello\nWorld\n')
        compare(
            data,
            """
        a: 1
        b:
        # Hello
        # World
          c: 2
          d: 3
        """.format(
                comment='#'
            ),
        )

    def test_before_nested_seq_from_scratch(self):
        from ruamel.yaml.comments import CommentedMap, CommentedSeq

        data = CommentedMap()
        datab = CommentedSeq()
        data['a'] = 1
        data['b'] = datab
        datab.append('c')
        datab.append('d')
        data['b'].yaml_set_start_comment('Hello\nWorld\n', indent=2)
        compare(
            data,
            """
        a: 1
        b:
          # Hello
          # World
        - c
        - d
        """.format(
                comment='#'
            ),
        )

    def test_before_nested_seq_from_scratch_block_seq_indent(self):
        from ruamel.yaml.comments import CommentedMap, CommentedSeq

        data = CommentedMap()
        datab = CommentedSeq()
        data['a'] = 1
        data['b'] = datab
        datab.append('c')
        datab.append('d')
        data['b'].yaml_set_start_comment('Hello\nWorld\n', indent=2)
        compare(
            data,
            """
        a: 1
        b:
          # Hello
          # World
          - c
          - d
        """.format(
                comment='#'
            ),
            indent=4,
            block_seq_indent=2,
        )

    def test_map_set_comment_before_and_after_non_first_key_00(self):
        # http://stackoverflow.com/a/40705671/1307905
        data = load(
            """
        xyz:
          a: 1    # comment 1
          b: 2

        test1:
          test2:
            test3: 3
                """
        )
        data.yaml_set_comment_before_after_key(
            'test1', 'before test1 (top level)', after='before test2'
        )
        data['test1']['test2'].yaml_set_start_comment('after test2', indent=4)
        compare(
            data,
            """
        xyz:
          a: 1    # comment 1
          b: 2

        # before test1 (top level)
        test1:
          # before test2
          test2:
            # after test2
            test3: 3
        """,
        )

    def test_map_set_comment_before_and_after_non_first_key_01(self):
        data = load(
            """
        xyz:
          a: 1    # comment 1
          b: 2

        test1:
          test2:
            test3: 3
        """
        )
        data.yaml_set_comment_before_after_key(
            'test1', 'before test1 (top level)', after='before test2\n\n'
        )
        data['test1']['test2'].yaml_set_start_comment('after test2', indent=4)
        # EOL is needed here as dedenting gets rid of spaces (as well as does Emacs
        compare_eol(
            data,
            """
        xyz:
          a: 1    # comment 1
          b: 2

        # before test1 (top level)
        test1:
          # before test2
          EOL
          test2:
            # after test2
            test3: 3
        """,
        )

    def test_map_set_comment_before_and_after_non_first_key_02(self):
        data = load(
            """
        xyz:
          a: 1    # comment 1
          b: 2

        test1:
          test2:
            test3: 3
        """
        )
        data.yaml_set_comment_before_after_key(
            'test1', 'xyz\n\nbefore test1 (top level)', after='\nbefore test2', after_indent=4
        )
        data['test1']['test2'].yaml_set_start_comment('after test2', indent=4)
        # EOL is needed here as dedenting gets rid of spaces (as well as does Emacs
        compare_eol(
            data,
            """
        xyz:
          a: 1    # comment 1
          b: 2

        # xyz

        # before test1 (top level)
        test1:
            EOL
            # before test2
          test2:
            # after test2
            test3: 3
        """,
        )
