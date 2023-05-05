# coding: utf-8

from roundtrip import dedent  # type: ignore


class TestDedent:
    def test_start_newline(self) -> None:
        # fmt: off
        x = dedent("""
        123
          456
        """)
        # fmt: on
        assert x == '123\n  456\n'

    def test_start_space_newline(self) -> None:
        # special construct to prevent stripping of following whitespace
        # fmt: off
        x = dedent("   " """
        123
        """)
        # fmt: on
        assert x == '123\n'

    def test_start_no_newline(self) -> None:
        # special construct to prevent stripping of following whitespac
        x = dedent("""\
        123
          456
        """)
        assert x == '123\n  456\n'

    def test_preserve_no_newline_at_end(self) -> None:
        x = dedent("""
        123""")
        assert x == '123'

    def test_preserve_no_newline_at_all(self) -> None:
        x = dedent("""\
        123""")
        assert x == '123'

    def test_multiple_dedent(self) -> None:
        x = dedent(
            dedent("""
        123
        """)
        )
        assert x == '123\n'
