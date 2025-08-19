
"""
testing of anchors and the aliases referring to them
"""

import pytest  # type: ignore  # NOQA

from roundtrip import round_trip, dedent, round_trip_load, round_trip_dump, YAML # type: ignore # NOQA
from typing import Any


def load(s: str) -> Any:
    return round_trip_load(dedent(s))


def compare(d: Any, s: str) -> None:
    assert round_trip_dump(d) == dedent(s)


class TestMerge:
    def test_remove_key_before_merge(self) -> None:
        data = load("""
        a: &aa
          b: 1
          c: 2
        d:
          e: 3
          f: 4
          <<: *aa
          g: 5
          h: 6
        """)
        del data['d']['f']
        compare(
            data,
            """
        a: &aa
          b: 1
          c: 2
        d:
          e: 3
          <<: *aa
          g: 5
          h: 6
        """,
        )

    def test_remove_key_after_merge(self) -> None:
        data = load("""
        a: &aa
          b: 1
          c: 2
        d:
          e: 3
          f: 4
          <<: *aa
          g: 5
          h: 6
        """)
        del data['d']['g']
        compare(
            data,
            """
        a: &aa
          b: 1
          c: 2
        d:
          e: 3
          f: 4
          <<: *aa
          h: 6
        """,
        )
