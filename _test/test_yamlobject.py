# coding: utf-8

import sys
from typing import Any
import pytest  # type: ignore # NOQA

from roundtrip import save_and_run  # type: ignore # NOQA


def test_monster(tmpdir: Any) -> None:
    program_src = '''\
    import ruamel.yaml
    from textwrap import dedent

    class Monster(ruamel.yaml.YAMLObject):
        yaml_tag = '!Monster'

        def __init__(self, name, hp, ac, attacks):
            self.name = name
            self.hp = hp
            self.ac = ac
            self.attacks = attacks

        def __repr__(self):
            return "%s(name=%r, hp=%r, ac=%r, attacks=%r)" % (
                self.__class__.__name__, self.name, self.hp, self.ac, self.attacks)

    yaml = ruamel.yaml.YAML(typ='safe', pure='True')
    yaml = ruamel.yaml.YAML()
    data = yaml.load(dedent("""\\
        --- !Monster
        name: Cave spider
        hp: [2,6]    # 2d6
        ac: 16
        attacks: [BITE, HURT]
    """))
    # normal dump, keys will be sorted
    from io import BytesIO
    buf = BytesIO()
    yaml.dump(data, buf)
    print(buf.getvalue().decode('utf-8'))
    assert buf.getvalue().decode('utf8') == dedent("""\\
        !Monster
        name: Cave spider
        hp: [2, 6]   # 2d6
        ac: 16
        attacks: [BITE, HURT]
    """)
    '''
    assert save_and_run(program_src, tmpdir) == 0


@pytest.mark.skipif(sys.version_info < (3, 0), reason='no __qualname__')  # type: ignore
def test_qualified_name00(tmpdir: Any) -> None:
    """issue 214"""
    program_src = """\
    from ruamel.yaml import YAML
    from ruamel.yaml.compat import StringIO

    class A:
        def f(self):
            pass

    yaml = YAML(typ='unsafe', pure=True)
    yaml.explicit_end = True
    buf = StringIO()
    yaml.dump(A.f, buf)
    res = buf.getvalue()
    print('res', repr(res))
    assert res == "!!python/name:__main__.A.f ''\\n...\\n"
    x = yaml.load(res)
    assert x == A.f
    """
    assert save_and_run(program_src, tmpdir) == 0


@pytest.mark.skipif(sys.version_info < (3, 0), reason='no __qualname__')  # type: ignore
def test_qualified_name01(tmpdir: Any) -> None:
    """issue 214"""
    from ruamel.yaml import YAML
    import ruamel.yaml.comments
    from ruamel.yaml.compat import StringIO

    yaml = YAML(typ='unsafe', pure=True)
    yaml.explicit_end = True
    buf = StringIO()
    yaml.dump(ruamel.yaml.comments.CommentedBase.yaml_anchor, buf)
    res = buf.getvalue()
    assert res == "!!python/name:ruamel.yaml.comments.CommentedBase.yaml_anchor ''\n...\n"
    x = yaml.load(res)
    assert x == ruamel.yaml.comments.CommentedBase.yaml_anchor
