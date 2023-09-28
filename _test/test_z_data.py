# coding: utf-8

import sys
import os
import pytest  # type: ignore  # NOQA
import warnings  # NOQA
from typing import Any, Optional, List, Tuple
from pathlib import Path

base_path = Path('data')  # that is ruamel.yaml.data


class YAMLData:
    yaml_tag = '!YAML'

    def __init__(self, s: Any) -> None:
        self._s = s

    # Conversion tables for input. E.g. "<TAB>" is replaced by "\t"
    # fmt: off
    special = {
        'SPC': ' ',
        'TAB': '\t',
        '---': '---',
        '...': '...',
        'NL': '\n',
    }
    # fmt: on

    @property
    def value(self) -> Any:
        if hasattr(self, '_p'):
            return self._p  # type: ignore
        assert ' \n' not in self._s
        assert '\t\n' not in self._s
        self._p = self._s
        for k, v in YAMLData.special.items():
            k = '<' + k + '>'
            self._p = self._p.replace(k, v)
        return self._p

    def test_rewrite(self, s: str) -> str:
        assert ' \n' not in s
        assert '\t\n' not in s
        for k, v in YAMLData.special.items():
            k = '<' + k + '>'
            s = s.replace(k, v)
        return s

    @classmethod
    def from_yaml(cls, constructor: Any, node: Any) -> 'YAMLData':
        from ruamel.yaml.nodes import MappingNode

        if isinstance(node, MappingNode):
            return cls(constructor.construct_mapping(node))
        return cls(node.value)


class Python(YAMLData):
    yaml_tag = '!Python'


class Output(YAMLData):
    yaml_tag = '!Output'


class Assert(YAMLData):
    yaml_tag = '!Assert'

    @property
    def value(self) -> Any:
        from collections.abc import Mapping

        if hasattr(self, '_pa'):
            return self._pa  # type: ignore
        if isinstance(self._s, Mapping):
            self._s['lines'] = self.test_rewrite(self._s['lines'])  # type: ignore
        self._pa = self._s
        return self._pa


class Events(YAMLData):
    yaml_tag = '!Events'


class JSONData(YAMLData):
    yaml_tag = '!JSON'


class Dump(YAMLData):
    yaml_tag = '!Dump'


class Emit(YAMLData):
    yaml_tag = '!Emit'


def pytest_generate_tests(metafunc: Any) -> None:
    test_yaml = []
    paths = sorted(base_path.glob('**/*.yaml'))
    idlist = []
    for path in paths:
        # while developing tests put them in data/debug and run:
        #   auto -c "pytest _test/test_z_data.py" data/debug/*.yaml *.py _test/*.py
        if os.environ.get('RUAMELAUTOTEST') == '1':
            if path.parent.stem != 'debug':
                continue
        elif path.parent.stem == 'debug':
            # don't test debug entries for production
            continue
        stem = path.stem
        if stem.startswith('.#'):  # skip emacs temporary file
            continue
        idlist.append(stem)
        test_yaml.append([path])
    metafunc.parametrize(['yaml'], test_yaml, ids=idlist, scope='class')


class TestYAMLData:
    def yaml(
        self, yaml_version: Optional[Any] = None, typ: Any = 'rt', pure: Any = None,
    ) -> Any:
        from ruamel.yaml import YAML

        y = YAML(typ=typ, pure=pure)
        y.preserve_quotes = True
        if yaml_version:
            y.version = yaml_version
        y.composer.warn_double_anchors = False
        return y

    def docs(self, path: Path) -> List[Any]:
        from ruamel.yaml import YAML

        tyaml = YAML(typ='safe', pure=True)
        tyaml.register_class(YAMLData)
        tyaml.register_class(Python)
        tyaml.register_class(Output)
        tyaml.register_class(Assert)
        tyaml.register_class(Events)
        tyaml.register_class(JSONData)
        tyaml.register_class(Dump)
        tyaml.register_class(Emit)
        return list(tyaml.load_all(path))

    def yaml_load(self, value: Any, yaml_version: Optional[Any] = None) -> Tuple[Any, Any]:
        yaml = self.yaml(yaml_version=yaml_version)
        data = yaml.load(value)
        return yaml, data

    def round_trip(
        self, input: Any, output: Optional[Any] = None, yaml_version: Optional[Any] = None,
    ) -> None:
        from ruamel.yaml.compat import StringIO

        yaml, data = self.yaml_load(input.value, yaml_version=yaml_version)
        buf = StringIO()
        yaml.dump(data, buf)
        expected = input.value if output is None else output.value
        value = buf.getvalue()
        print('>>>> rt output\n', value.replace(' ', '\u2423'), sep='')  # 2423 open box
        assert value == expected

    def gen_events(
        self, input: Any, output: Any, yaml_version: Optional[Any] = None,
    ) -> None:
        from ruamel.yaml.compat import StringIO

        buf = StringIO()
        yaml = self.yaml(yaml_version=yaml_version)
        indent = 0
        try:
            for event in yaml.parse(input.value):
                compact = event.compact_repr()
                assert compact[0] in '+=-'
                if compact[0] == '-':
                    indent -= 1
                print(f'{" "*indent}{compact}', file=buf)
                if compact[0] == '+':
                    indent += 1

        except Exception as e:  # NOQA
            print('=EXCEPTION', file=buf)  # exceptions not indented
            if '=EXCEPTION' not in output.value:
                raise
        print('>>>> buf\n', buf.getvalue(), sep='')
        assert buf.getvalue() == output.value

    def load_compare_json(
        self, input: Any, output: Any, yaml_version: Optional[Any] = None,
    ) -> None:
        import json
        from ruamel.yaml.compat import StringIO
        from ruamel.yaml.comments import CommentedMap, TaggedScalar

        def serialize_obj(obj: Any) -> Any:
            if isinstance(obj, CommentedMap):
                return {k: v for k, v in obj.items()}  # NOQA
            elif isinstance(obj, TaggedScalar):
                return str(obj.value)
            elif isinstance(obj, set):
                return {k: None for k in obj}
            return str(obj)

        buf = StringIO()
        yaml = self.yaml(typ='rt', yaml_version=yaml_version)
        for data in yaml.load_all(input.value):
            if isinstance(data, dict):
                data = {str(k): v for k, v in data.items()}
            json.dump(data, buf, sort_keys=True, indent=2, default=serialize_obj)
            buf.write('\n')
        print('>>>> buf\n', buf.getvalue(), sep='')
        # jsons = json.dumps(json.loads(output.value))  # normalize formatting of JSON
        assert buf.getvalue() == output.value

    def load_compare_emit(
        self, input: Any, output: Any, yaml_version: Optional[Any] = None,
    ) -> None:
        from ruamel.yaml.compat import StringIO

        buf = StringIO()
        yaml = self.yaml(yaml_version=yaml_version)
        yaml.preserve_quotes = True
        data = input.value
        if data.startswith('---') or '\n--- ' in data or '\n---' in data:
            yaml.explicit_start = True
        data = list(yaml.load_all(data))
        yaml.dump_all(data, buf)
        print('>>>> buf\n', buf.getvalue(), sep='')
        assert buf.getvalue() == output.value

    def load_assert(
        self, input: Any, confirm: Any, yaml_version: Optional[Any] = None,
    ) -> None:
        from collections.abc import Mapping

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

    def run_python(
        self, python: Any, data: Any, tmpdir: Any, input: Optional[Any] = None,
    ) -> None:
        from roundtrip import save_and_run  # type: ignore

        if input is not None:
            (tmpdir / 'input.yaml').write_text(input.value, encoding='utf-8')
        assert save_and_run(python.value, base_dir=tmpdir, output=data.value) == 0

    def insert_comments(self, data: Any, actions: Any) -> None:
        """this is to automatically insert based on:
          path (a.1.b),
          position (before, after, between), and
          offset (absolute/relative)
        """
        raise NotImplementedError
        expected = []
        for line in data.value.splitlines(True):
            idx = line.index['?']
            if idx < 0:
                expected.append(line)
                continue
            assert line.lstrip()[0] == '#'  # it has to be comment line
        print(data)
        assert ''.join(expected) == data.value

    # this is executed by pytest the methods with names not starting with
    # test_ are helper methods
    def test_yaml_data(self, yaml: Any, tmpdir: Any) -> None:
        from collections.abc import Mapping

        idx = 0
        typs = []  # list of test to be performed
        yaml_version = None

        docs = self.docs(yaml)
        if isinstance(docs[0], Mapping):
            d = docs[0]
            if d.get('skip'):
                pytest.skip('explicit skip')
            if '1.3-mod' in d.get('tags', []):
                pytest.skip('YAML 1.3')
            typ = d.get('type')
            if isinstance(typ, str):
                typs.append(typ)
            elif isinstance(typ, list):
                typs.extend(typ[:])
            del typ
            yaml_version = d.get('yaml_version')
            if 'python' in d:
                if not check_python_version(d['python']):
                    pytest.skip('unsupported version')
            idx += 1
        data = output = confirm = python = events = json = dump = emit = None
        for doc in docs[idx:]:
            if isinstance(doc, Output):
                output = doc
            elif isinstance(doc, Events):
                events = doc
            elif isinstance(doc, JSONData):
                json = doc
            elif isinstance(doc, Dump):
                dump = doc  # NOQA
            elif isinstance(doc, Emit):
                emit = doc  # NOQA
            elif isinstance(doc, Assert):
                confirm = doc
            elif isinstance(doc, Python):
                python = doc
                if len(typs) == 0:
                    typs = ['python_run']
            elif isinstance(doc, YAMLData):
                data = doc
            else:
                print('no handler for type:', type(doc), repr(doc))
                raise AssertionError()
        if len(typs) == 0:
            if data is not None and output is not None:
                typs = ['rt']
            elif data is not None and confirm is not None:
                typs = ['load_assert']
            else:
                assert data is not None
                typs = ['rt']
        print('type:', typs)
        if data is not None:
            print('>>>> data:\n', data.value.replace(' ', '\u2423'), sep='', end='')
        if events is not None:
            print('>>>> events:\n', events.value, sep='')
        else:
            print('>>>> output:\n', output.value if output is not None else output, sep='')
        for typ in typs:
            if typ == 'rt':
                self.round_trip(data, output, yaml_version=yaml_version)
            elif typ == 'python_run':
                inp = None if output is None or data is None else data
                self.run_python(
                    python, output if output is not None else data, tmpdir, input=inp,
                )
            elif typ == 'load_assert':
                self.load_assert(data, confirm, yaml_version=yaml_version)
            elif typ == 'comment':
                actions: List[Any] = []
                self.insert_comments(data, actions)
            elif typ == 'events':
                if events is None:
                    print('need to specify !Events for type:', typ)
                    sys.exit(1)
                self.gen_events(data, events, yaml_version=yaml_version)
            elif typ == 'json':
                if json is None:
                    print('need to specify !JSON for type:', typ)
                    sys.exit(1)
                self.load_compare_json(data, json, yaml_version=yaml_version)
            elif typ == 'dump':
                continue
            elif typ == 'emit':
                self.load_compare_emit(data, emit)
            else:
                f'\n>>>>>> run type unknown: "{typ}" <<<<<<\n'
                raise AssertionError()


def check_python_version(match: Any, current: Optional[Any] = None) -> bool:
    """
    version indication, return True if version matches.
    match should be something like 3.6+, or [2.7, 3.3] etc. Floats
    are converted to strings. Single values are made into lists.
    """
    if current is None:
        current = list(sys.version_info[:3])
    if not isinstance(match, list):
        match = [match]
    for m in match:
        minimal = False
        if isinstance(m, float):
            m = str(m)
        if m.endswith('+'):
            minimal = True
            m = m[:-1]
        # assert m[0].isdigit()
        # assert m[-1].isdigit()
        m = [int(x) for x in m.split('.')]
        current_len = current[: len(m)]
        # print(m, current, current_len)
        if minimal:
            if current_len >= m:
                return True
        else:
            if current_len == m:
                return True
    return False
