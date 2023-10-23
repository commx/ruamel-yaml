# coding: utf-8

"""
testing of YAML.register_class and @yaml_object
"""

import pytest  # type: ignore  # NOQA  
from typing import Any
from ruamel.yaml.comments import TaggedScalar, CommentedMap  # NOQA

from roundtrip import YAML  # type: ignore


class User0:
    def __init__(self, name: str, age: int) -> None:
        self.name = name
        self.age = age


class User1:
    yaml_tag = '!user'

    def __init__(self, name: str, age: int) -> None:
        self.name = name
        self.age = age

    @classmethod
    def to_yaml(cls, representer: Any, node: Any) -> Any:
        return representer.represent_scalar(cls.yaml_tag, '{.name}-{.age}'.format(node, node))

    @classmethod
    def from_yaml(cls, constructor: Any, node: Any) -> Any:
        return cls(*node.value.split('-'))


class TestRegisterClass:
    def test_register_0_rt(self) -> None:
        yaml = YAML()
        yaml.register_class(User0)
        ys = """
        - !User0
          name: Anthon
          age: 18
        """
        d = yaml.load(ys)
        yaml.dump(d, compare=ys, unordered_lines=True)

    def test_register_0_safe(self) -> None:
        # default_flow_style = None
        yaml = YAML(typ='safe')
        yaml.register_class(User0)
        ys = """
        - !User0 {age: 18, name: Anthon}
        """
        d = yaml.load(ys)
        yaml.dump(d, compare=ys)

    def test_register_0_unsafe(self) -> None:
        # default_flow_style = None
        with pytest.warns(PendingDeprecationWarning):
            yaml = YAML(typ='unsafe')
        yaml.register_class(User0)
        ys = """
        - !User0 {age: 18, name: Anthon}
        """
        d = yaml.load(ys)
        yaml.dump(d, compare=ys)

    def test_register_1_rt(self) -> None:
        yaml = YAML()
        yaml.register_class(User1)
        ys = """
        - !user Anthon-18
        """
        d = yaml.load(ys)
        yaml.dump(d, compare=ys)

    def test_register_1_safe(self) -> None:
        yaml = YAML(typ='safe')
        yaml.register_class(User1)
        ys = """
        [!user Anthon-18]
        """
        d = yaml.load(ys)
        yaml.dump(d, compare=ys)

    def test_register_1_unsafe(self) -> None:
        with pytest.warns(PendingDeprecationWarning):
            yaml = YAML(typ='unsafe')
        yaml.register_class(User1)
        ys = """
        [!user Anthon-18]
        """
        d = yaml.load(ys)
        yaml.dump(d, compare=ys)


class TestDecorator:
    def test_decorator_implicit(self) -> None:
        from ruamel.yaml import yaml_object

        yml = YAML()

        @yaml_object(yml)
        class User2:
            def __init__(self, name: str, age: int) -> None:
                self.name = name
                self.age = age

        ys = """
        - !User2
          name: Anthon
          age: 18
        """
        d = yml.load(ys)
        yml.dump(d, compare=ys, unordered_lines=True)

    def test_decorator_explicit(self) -> None:
        from ruamel.yaml import yaml_object

        yml = YAML()

        @yaml_object(yml)
        class User3:
            yaml_tag = '!USER'

            def __init__(self, name: str, age: int) -> None:
                self.name = name
                self.age = age

            @classmethod
            def to_yaml(cls, representer: Any, node: Any) -> Any:
                return representer.represent_scalar(
                    cls.yaml_tag, '{.name}-{.age}'.format(node, node),
                )

            @classmethod
            def from_yaml(cls, constructor: Any, node: Any) -> Any:
                return cls(*node.value.split('-'))

        ys = """
        - !USER Anthon-18
        """
        d = yml.load(ys)
        yml.dump(d, compare=ys)
