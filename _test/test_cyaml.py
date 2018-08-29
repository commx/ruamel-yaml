# coding: utf-8

import platform
import pytest
from textwrap import dedent


@pytest.mark.skipif(
    platform.python_implementation() == 'Jython', reason='Jython throws RepresenterError'
)
def test_load_cyaml():
    import ruamel.yaml

    assert ruamel.yaml.__with_libyaml__
    from ruamel.yaml.cyaml import CLoader

    ruamel.yaml.load('abc: 1', Loader=CLoader)


def test_dump_cyaml():
    import ruamel.yaml

    data = {'a': 1, 'b': 2}
    res = ruamel.yaml.dump(
        data,
        Dumper=ruamel.yaml.cyaml.CSafeDumper,
        default_flow_style=False,
        allow_unicode=True,
    )
    assert res == 'a: 1\nb: 2\n'

@pytest.mark.xfail(strict=True)
def test_load_cyaml_1_2():
    # issue 155
    import ruamel.yaml

    assert ruamel.yaml.__with_libyaml__
    inp = dedent("""\
    %YAML 1.2
    ---
    num_epochs: 70000
    """)
    yaml = ruamel.yaml.YAML(typ='safe')
    yaml.load(inp)

@pytest.mark.xfail(strict=True)
def test_dump_cyaml_1_2():
    # issue 155
    import ruamel.yaml
    from ruamel.yaml.compat import StringIO

    assert ruamel.yaml.__with_libyaml__
    inp = dedent("""\
    %YAML 1.2
    ---
    num_epochs: 70000
    """)
    yaml = ruamel.yaml.YAML(typ='safe')
    yaml.version = (1, 2)
    yaml.default_flow_style = False
    data = {'a': 1, 'b': 2}
    exp = dedent("""\
    %YAML 1.2
    ---
    a: 1
    b: 2
    """)
    buf = StringIO()
    yaml.dump(data, buf)
    assert buf.getvalue() == exp
