

from dataclasses import dataclass, fields   # NOQA
from ruamel.yaml import YAML
from textwrap import dedent


def test_1() -> None:
    yaml = YAML()

    @yaml.register_class
    @dataclass
    class DC:
        abc: int
        klm: int
        xyz: int = 0

        def __post_init__(self) -> None:
            self.xyz = self.abc + self.klm

    dc = DC(abc=5, klm=42)
    assert dc.xyz == 47

    yaml_str = dedent("""\
    !DC
    abc: 13
    klm: 37
    """)
    dc2 = yaml.load(yaml_str)
    assert dc2.xyz == 50
