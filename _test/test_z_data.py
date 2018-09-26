# coding: utf-8

from __future__ import print_function, unicode_literals

import pytest  # NOQA

import warnings  # NOQA

from ruamel.std.pathlib import Path

base_path = Path('data')  # that is ruamel.yaml.data


class YAMLData(object):
    yaml_tag = '!YAML'

    def __init__(self, s):
        self._s = s

    # fmt: off
    special = {
        'SPC': ' ',
        'TAB': '\t',
        '---': '---',
        '...': '...',
    }
    # fmt: on

    @property
    def value(self):
        if hasattr(self, '_p'):
            return self._p
        assert ' \n' not in self._s
        assert '\t\n' not in self._s
        self._p = self._s
        for k, v in YAMLData.special.items():
            k = '<' + k + '>'
            self._p = self._p.replace(k, v)
        return self._p

    def test_rewrite(self, s):
        assert ' \n' not in s
        assert '\t\n' not in s
        for k, v in YAMLData.special.items():
            k = '<' + k + '>'
            s = s.replace(k, v)
        return s

    @classmethod
    def from_yaml(cls, constructor, node):
        from ruamel.yaml.nodes import MappingNode

        if isinstance(node, MappingNode):
            return cls(constructor.construct_mapping(node))
        return cls(node.value)


class Output(YAMLData):
    yaml_tag = '!Output'


class Assert(YAMLData):
    yaml_tag = '!Assert'

    @property
    def value(self):
        from ruamel.yaml.compat import Mapping

        if hasattr(self, '_pa'):
            return self._pa
        if isinstance(self._s, Mapping):
            self._s['lines'] = self.test_rewrite(self._s['lines'])
        self._pa = self._s
        return self._pa


def pytest_generate_tests(metafunc):
    from ruamel.yaml import YAML

    yaml = YAML(typ='safe', pure=True)
    # yaml = YAML()
    yaml.register_class(YAMLData)
    yaml.register_class(Output)
    yaml.register_class(Assert)
    test_yaml = []
    paths = sorted(base_path.glob('*.yaml'))
    idlist = []
    for path in paths:
        idlist.append(path.stem)
        x = yaml.load_all(path)
        test_yaml.append([list(x)])
    metafunc.parametrize(['yaml'], test_yaml, ids=idlist, scope='class')


class TestYAMLData(object):
    def yaml(self, yaml_version=None):
        from ruamel.yaml import YAML

        y = YAML()
        y.preserve_quotes = True
        if yaml_version:
            y.version = yaml_version
        return y

    def yaml_load(self, value, yaml_version=None):
        yaml = self.yaml(yaml_version=yaml_version)
        data = yaml.load(value)
        return yaml, data

    def run_rt(self, input, output=None, yaml_version=None):
        from ruamel.yaml.compat import StringIO

        yaml, data = self.yaml_load(input.value, yaml_version=yaml_version)
        buf = StringIO()
        yaml.dump(data, buf)
        expected = input.value if output is None else output.value
        assert buf.getvalue() == expected

    def run_load_assert(self, input, confirm, yaml_version=None):
        from ruamel.yaml.compat import Mapping

        d = self.yaml_load(input.value, yaml_version=yaml_version)[1]  # NOQA
        print('confirm.value', confirm.value, type(confirm.value))
        if isinstance(confirm.value, Mapping):
            r = range(confirm.value['range'])
            lines = confirm.value['lines'].splitlines()
            for idx in r:  # NOQA
                for line in lines:
                    line = 'assert ' + line
                    print(line)
                    exec(line)
        else:
            for line in confirm.value.splitlines():
                line = 'assert ' + line
                print(line)
                exec(line)

    def test_yaml_data(self, yaml):
        from ruamel.yaml.compat import Mapping

        idx = 0
        typ = None
        yaml_version = None
        if isinstance(yaml[0], Mapping):
            d = yaml[0]
            typ = d.get('type')
            yaml_version = d.get('yaml_version')
            idx += 1
        data = output = confirm = None
        for doc in yaml[idx:]:
            if isinstance(doc, Output):
                output = doc
            elif isinstance(doc, Assert):
                confirm = doc
            elif isinstance(doc, YAMLData):
                data = doc
        if typ is None:
            if data is not None and output is not None:
                typ = 'rt'
            elif data is not None and confirm is not None:
                typ = 'load_assert'
            else:
                assert data is not None
                typ = 'rt'
        print('type:', typ)
        print('data:', data.value)
        print('output:', output.value if output is not None else output)
        if typ == 'rt':
            self.run_rt(data, output, yaml_version=yaml_version)
        elif typ == 'load_assert':
            self.run_load_assert(data, confirm, yaml_version=yaml_version)
        else:
            assert False
