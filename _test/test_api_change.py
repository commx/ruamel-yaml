# coding: utf-8

from __future__ import print_function

"""
testing of anchors and the aliases referring to them
"""

import sys
import pytest
from ruamel.yaml import YAML
from ruamel.yaml.constructor import DuplicateKeyError
from ruamel.std.pathlib import Path


class TestNewAPI:
    def test_duplicate_keys_00(self):
        from ruamel.yaml.constructor import DuplicateKeyError
        yaml = YAML()
        with pytest.raises(DuplicateKeyError):
            yaml.load('{a: 1, a: 2}')

    def test_duplicate_keys_01(self):
        yaml = YAML(typ='safe', pure=True)
        with pytest.raises(DuplicateKeyError):
            yaml.load('{a: 1, a: 2}')

    # @pytest.mark.xfail(strict=True)
    def test_duplicate_keys_02(self):
        yaml = YAML(typ='safe')
        with pytest.raises(DuplicateKeyError):
            yaml.load('{a: 1, a: 2}')


class TestWrite:
    def test_dump_path(self, tmpdir):
        fn = Path(str(tmpdir)) / 'test.yaml'
        yaml = YAML()
        data = yaml.map()
        data['a'] = 1
        data['b'] = 2
        yaml.dump(data, fn)
        assert fn.read_text() == "a: 1\nb: 2\n"

    def test_dump_file(self, tmpdir):
        fn = Path(str(tmpdir)) / 'test.yaml'
        yaml = YAML()
        data = yaml.map()
        data['a'] = 1
        data['b'] = 2
        with open(str(fn), 'w') as fp:
            yaml.dump(data, fp)
        assert fn.read_text() == "a: 1\nb: 2\n"

    def test_dump_missing_stream(self):
        yaml = YAML()
        data = yaml.map()
        data['a'] = 1
        data['b'] = 2
        with pytest.raises(TypeError):
            yaml.dump(data)

    def test_dump_too_many_args(self, tmpdir):
        fn = Path(str(tmpdir)) / 'test.yaml'
        yaml = YAML()
        data = yaml.map()
        data['a'] = 1
        data['b'] = 2
        with pytest.raises(TypeError):
            yaml.dump(data, fn, True)

    def test_transform(self, tmpdir):
        def tr(s):
            return s.replace(' ', '  ')

        fn = Path(str(tmpdir)) / 'test.yaml'
        yaml = YAML()
        data = yaml.map()
        data['a'] = 1
        data['b'] = 2
        yaml.dump(data, fn, transform=tr)
        assert fn.read_text() == "a:  1\nb:  2\n"

    def test_print(self, capsys):
        yaml = YAML()
        data = yaml.map()
        data['a'] = 1
        data['b'] = 2
        yaml.dump(data, sys.stdout)
        out, err = capsys.readouterr()
        assert out == "a: 1\nb: 2\n"


class TestRead:
    def test_multi_load(self):
        # make sure reader, scanner, parser get reset
        yaml = YAML()
        yaml.load('a: 1')
        yaml.load('a: 1')  # did not work in 0.15.4
