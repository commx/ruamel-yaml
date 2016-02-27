# coding: utf-8

import pytest   # NOQA

from roundtrip import round_trip


class TestIndentFailures:

    def test_tag(self):
        round_trip("""\
        !!python/object:__main__.Developer
        name: Anthon
        location: Germany
        language: python
        """)

    def test_full_tag(self):
        round_trip("""\
        !!tag:yaml.org,2002:python/object:__main__.Developer
        name: Anthon
        location: Germany
        language: python
        """)

    def test_standard_tag(self):
        round_trip("""\
        !!tag:yaml.org,2002:python/object:map
        name: Anthon
        location: Germany
        language: python
        """)
