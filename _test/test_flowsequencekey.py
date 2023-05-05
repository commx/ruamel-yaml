# coding: utf-8

"""
test flow style sequences as keys roundtrip

"""

# import pytest

from roundtrip import round_trip  # type: ignore


class TestFlowStyleSequenceKey:
    def test_so_39595807(self) -> None:
        inp = """\
        %YAML 1.2
        ---
        [2, 3, 4]:
          a:
          - 1
          - 2
          b: Hello World!
          c: 'Voilà!'
        """
        round_trip(inp, preserve_quotes=True, explicit_start=True, version=(1, 2))
