# coding: utf-8

"""
testing of anchors and the aliases referring to them
"""

import pytest
from ruamel.yaml import YAML
from ruamel.yaml.constructor import DuplicateKeyError


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
