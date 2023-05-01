# coding: utf-8

import pytest  # type: ignore  # NOQA

import json

from typing import Any


def load(s: str, typ: Any = float) -> float:
    import ruamel.yaml

    yaml = ruamel.yaml.YAML()
    x = '{"low": %s }' % (s)
    print('input: [%s]' % (s), repr(x))
    # just to check it is loadable json
    res = json.loads(x)
    assert isinstance(res['low'], typ)
    ret_val = yaml.load(x)
    print(ret_val)
    return ret_val['low']  # type: ignore


class TestJSONNumbers:
    # based on http://stackoverflow.com/a/30462009/1307905
    # yaml number regex: http://yaml.org/spec/1.2/spec.html#id2804092
    #
    # -? [1-9] ( \. [0-9]* [1-9] )? ( e [-+] [1-9] [0-9]* )?
    #
    # which is not a superset of the JSON numbers
    def test_json_number_float(self) -> None:
        for x in (
            y.split('#')[0].strip()
            for y in """
        1.0  # should fail on YAML spec on 1-9 allowed as single digit
        -1.0
        1e-06
        3.1e-5
        3.1e+5
        3.1e5  # should fail on YAML spec: no +- after e
        """.splitlines()
        ):
            if not x:
                continue
            res = load(x)
            assert isinstance(res, float)

    def test_json_number_int(self) -> None:
        for x in (
            y.split('#')[0].strip()
            for y in """
        42
        """.splitlines()
        ):
            if not x:
                continue
            res = load(x, int)
            assert isinstance(res, int)
