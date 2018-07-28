# coding: utf-8

import pytest   # NOQA

from roundtrip import round_trip, round_trip_load_all


class TestDocument:
    def test_single_doc_begin_end(self):
        round_trip("""\
        ---
        - a
        - b
        ...
        """, explicit_start=True, explicit_end=True)

    def test_multi_doc_begin_end(self):
        from ruamel import yaml
        docs = list(round_trip_load_all("""\
        ---
        - a
        ...
        ---
        - b
        ...
        """))
        assert docs == [['a'], ['b']]
        out = yaml.dump_all(docs, Dumper=yaml.RoundTripDumper, explicit_start=True,
                            explicit_end=True)
        assert out == "---\n- a\n...\n---\n- b\n...\n"

    def test_multi_doc_no_start(self):
        docs = list(round_trip_load_all("""\
        - a
        ...
        ---
        - b
        ...
        """))
        assert docs == [['a'], ['b']]

    def test_multi_doc_no_end(self):
        docs = list(round_trip_load_all("""\
        - a
        ---
        - b
        """))
        assert docs == [['a'], ['b']]

    def test_multi_doc_ends_only(self):
        # this is ok in 1.2
        docs = list(round_trip_load_all("""\
        - a
        ...
        - b
        ...
        """, version=(1, 2)))
        assert docs == [['a'], ['b']]

    def test_multi_doc_ends_only_1_1(self):
        from ruamel import yaml
        # this is not ok in 1.1
        with pytest.raises(yaml.parser.ParserError):
            docs = list(round_trip_load_all("""\
            - a
            ...
            - b
            ...
            """, version=(1, 1)))
            assert docs == [['a'], ['b']]  # not True, but not reached
