# coding: utf-8

"""
collections.OrderedDict is a new class not supported by PyYAML (issue 83 by Frazer McLean)

This is now so integrated in Python that it can be mapped to !!omap

"""

import pytest  # type: ignore  # NOQA


from roundtrip import round_trip, dedent, round_trip_load, round_trip_dump  # type: ignore # NOQA


class TestOrderedDict:
    def test_ordereddict(self) -> None:
        from collections import OrderedDict

        assert round_trip_dump(OrderedDict()) == '!!omap []\n'
