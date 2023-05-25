# coding: utf-8

import pytest  # type: ignore  # NOQA

from roundtrip import round_trip, round_trip_load_all, round_trip_dump_all  # type: ignore


class TestDocument:
    def test_single_doc_begin_end(self) -> None:
        inp = """\
        ---
        - a
        - b
        ...
        """
        round_trip(inp, explicit_start=True, explicit_end=True)

    def test_multi_doc_begin_end(self) -> None:
        inp = """\
        ---
        - a
        ...
        ---
        - b
        ...
        """
        docs = list(round_trip_load_all(inp))
        assert docs == [['a'], ['b']]
        out = round_trip_dump_all(docs, explicit_start=True, explicit_end=True)
        assert out == '---\n- a\n...\n---\n- b\n...\n'

    def test_multi_doc_no_start(self) -> None:
        inp = """\
        - a
        ...
        ---
        - b
        ...
        """
        docs = list(round_trip_load_all(inp))
        assert docs == [['a'], ['b']]

    def test_multi_doc_no_end(self) -> None:
        inp = """\
        - a
        ---
        - b
        """
        docs = list(round_trip_load_all(inp))
        assert docs == [['a'], ['b']]

    def test_multi_doc_ends_only(self) -> None:
        # this is ok in 1.2
        inp = """\
        - a
        ...
        - b
        ...
        """
        docs = list(round_trip_load_all(inp, version=(1, 2)))
        assert docs == [['a'], ['b']]

    def test_single_scalar_comment(self) -> None:
        from ruamel import yaml

        inp = """\
        one # comment
        two
        """
        with pytest.raises(yaml.parser.ParserError):
            d = list(round_trip_load_all(inp, version=(1, 2)))  # NOQA

    def test_scalar_after_seq_document(self) -> None:
        from ruamel import yaml

        inp = """\
        [ 42 ]
        hello
        """
        with pytest.raises(yaml.parser.ParserError):
            d = list(round_trip_load_all(inp, version=(1, 2)))  # NOQA

    def test_yunk_after_explicit_document_end(self) -> None:
        from ruamel import yaml

        inp = """\
        hello: world
        ... this is no comment
        """
        with pytest.raises(yaml.parser.ParserError):
            d = list(round_trip_load_all(inp, version=(1, 2)))  # NOQA

    def test_multi_doc_ends_only_1_1(self) -> None:
        from ruamel import yaml

        # this is not ok in 1.1
        with pytest.raises(yaml.parser.ParserError):
            inp = """\
            - a
            ...
            - b
            ...
            """
            docs = list(round_trip_load_all(inp, version=(1, 1)))
            assert docs == [['a'], ['b']]  # not True, but not reached
