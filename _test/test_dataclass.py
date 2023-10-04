

from dataclasses import dataclass, fields, InitVar   # NOQA
from textwrap import dedent
from io import BytesIO
from typing import ClassVar, Union


class TestDataClasses:
    def test_1(self) -> None:
        from ruamel.yaml import YAML

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

    def test_yamltag(self) -> None:
        from ruamel.yaml import YAML

        yaml = YAML()

        @yaml.register_class
        @dataclass
        class DC:
            yaml_tag: ClassVar = '!dc_example'
            abc: int
            klm: int

        dc = DC(abc=5, klm=42)
        buf = BytesIO()
        yaml.dump(dc, buf)
        assert buf.getvalue() == dedent("""\
        !dc_example
        abc: 5
        klm: 42
        """).encode('utf-8')
        dc2 = yaml.load(buf.getvalue())
        assert len(fields(dc2)) == 2  # class var is not a field
        assert dc2.abc == dc.abc
        assert dc2.klm == dc.klm

    def test_initvar(self) -> None:
        from ruamel.yaml import YAML

        yaml = YAML()

        @yaml.register_class
        @dataclass
        class DC:
            abc: int
            klm: int
            xyz: InitVar[Union[str, None]] = None

            def __post_init__(self, xyz: Union[str, None]) -> None:
                # assert xyz == self.xyz  # self.xyz is always None
                if xyz is not None:
                    self.klm += len(xyz)

        dc = DC(abc=5, klm=42, xyz='provided')
        # this actually doesn't raise an attribute error, I would have expected it not to work
        # at all, but it has the default value
        assert dc.xyz is None  # type: ignore
        buf = BytesIO()
        yaml.dump(dc, buf)
        assert buf.getvalue() == dedent("""\
        !DC
        abc: 5
        klm: 50
        """).encode('utf-8')

        yaml_str = dedent("""\
        !DC
        abc: 18
        klm: 55
        xyz: some string
        """)
        dc2 = yaml.load(yaml_str)
        assert dc2.xyz is None
        assert dc2.klm == 55 + len('some string')

    def test_initvar_not_in_yaml(self) -> None:
        from ruamel.yaml import YAML

        yaml = YAML()

        @yaml.register_class
        @dataclass
        class DC:
            abc: int
            klm: int
            xyz: InitVar[Union[str, None]] = 'hello'

            def __post_init__(self, xyz: Union[str, None]) -> None:
                # assert xyz == self.xyz  # self.xyz is always None
                if xyz is not None:
                    self.klm += len(xyz)

        dc = DC(abc=5, klm=42, xyz='provided')
        assert dc.abc == 5
        assert dc.xyz == 'hello'  # type: ignore
        buf = BytesIO()
        yaml.dump(dc, buf)
        assert buf.getvalue() == dedent("""\
        !DC
        abc: 5
        klm: 50
        """).encode('utf-8')

        yaml_str = dedent("""\
        !DC
        abc: 18
        klm: 55
        """)
        dc2 = yaml.load(yaml_str)
        assert dc2.xyz == 'hello'
        assert dc2.klm == 55 + len('hello')
