# coding: utf-8

import pytest  # type: ignore  # NOQA

from roundtrip import YAML  # type: ignore # does an automatic dedent on load


"""
YAML 1.0 allowed root level literal style without indentation:
  "Usually top level nodes are not indented" (example 4.21 in 4.6.3)
YAML 1.1 is a bit vague but says:
  "Regardless of style, scalar content must always be indented by at least one space"
  (4.4.3)
  "In general, the document’s node is indented as if it has a parent indented at -1 spaces."
  (4.3.3)
YAML 1.2 is again clear about root literal level scalar after directive in example 9.5:

%YAML 1.2
--- |
%!PS-Adobe-2.0
...
%YAML1.2
---
# Empty
...
"""


class TestNoIndent:
    def test_root_literal_scalar_indent_example_9_5(self) -> None:
        yaml = YAML()
        s = '%!PS-Adobe-2.0'
        inp = """
        --- |
          {}
        """
        d = yaml.load(inp.format(s))
        print(d)
        assert d == s + '\n'

    def test_root_literal_scalar_no_indent(self) -> None:
        yaml = YAML()
        s = 'testing123'
        inp = """
        --- |
        {}
        """
        d = yaml.load(inp.format(s))
        print(d)
        assert d == s + '\n'

    def test_root_literal_scalar_no_indent_1_1(self) -> None:
        yaml = YAML()
        s = 'testing123'
        inp = """
        %YAML 1.1
        --- |
        {}
        """
        d = yaml.load(inp.format(s))
        print(d)
        assert d == s + '\n'

    def test_root_literal_scalar_no_indent_1_1_old_style(self) -> None:
        from textwrap import dedent
        from ruamel.yaml import YAML

        yaml = YAML(typ='safe', pure=True)
        s = 'testing123'
        inp = """
        %YAML 1.1
        --- |
          {}
        """
        d = yaml.load(dedent(inp.format(s)))
        print(d)
        assert d == s + '\n'

    def test_root_literal_scalar_no_indent_1_1_no_raise(self) -> None:
        # from ruamel.yaml.parser import ParserError

        yaml = YAML()
        yaml.root_level_block_style_scalar_no_indent_error_1_1 = True
        s = 'testing123'
        # with pytest.raises(ParserError):
        if True:
            inp = """
            %YAML 1.1
            --- |
            {}
            """
            yaml.load(inp.format(s))

    def test_root_literal_scalar_indent_offset_one(self) -> None:
        yaml = YAML()
        s = 'testing123'
        inp = """
        --- |1
         {}
        """
        d = yaml.load(inp.format(s))
        print(d)
        assert d == s + '\n'

    def test_root_literal_scalar_indent_offset_four(self) -> None:
        yaml = YAML()
        s = 'testing123'
        inp = """
        --- |4
            {}
        """
        d = yaml.load(inp.format(s))
        print(d)
        assert d == s + '\n'

    def test_root_literal_scalar_indent_offset_two_leading_space(self) -> None:
        yaml = YAML()
        s = ' testing123'
        inp = """
        --- |4
            {s}
            {s}
        """
        d = yaml.load(inp.format(s=s))
        print(d)
        assert d == (s + '\n') * 2

    def test_root_literal_scalar_no_indent_special(self) -> None:
        yaml = YAML()
        s = '%!PS-Adobe-2.0'
        inp = """
        --- |
        {}
        """
        d = yaml.load(inp.format(s))
        print(d)
        assert d == s + '\n'

    def test_root_folding_scalar_indent(self) -> None:
        yaml = YAML()
        s = '%!PS-Adobe-2.0'
        inp = """
        --- >
          {}
        """
        d = yaml.load(inp.format(s))
        print(d)
        assert d == s + '\n'

    def test_root_folding_scalar_no_indent(self) -> None:
        yaml = YAML()
        s = 'testing123'
        inp = """
        --- >
        {}
        """
        d = yaml.load(inp.format(s))
        print(d)
        assert d == s + '\n'

    def test_root_folding_scalar_no_indent_special(self) -> None:
        yaml = YAML()
        s = '%!PS-Adobe-2.0'
        inp = """
        --- >
        {}
        """
        d = yaml.load(inp.format(s))
        print(d)
        assert d == s + '\n'

    def test_root_literal_multi_doc(self) -> None:
        yaml = YAML(typ='safe', pure=True)
        s1 = 'abc'
        s2 = 'klm'
        inp = """
        --- |-
        {}
        --- |
        {}
        """
        for idx, d1 in enumerate(yaml.load_all(inp.format(s1, s2))):
            print('d1:', d1)
            assert ['abc', 'klm\n'][idx] == d1

    def test_root_literal_doc_indent_directives_end(self) -> None:
        yaml = YAML()
        yaml.explicit_start = True
        inp = """
        --- |-
          %YAML 1.3
          ---
          this: is a test
        """
        yaml.round_trip(inp)

    def test_root_literal_doc_indent_document_end(self) -> None:
        yaml = YAML()
        yaml.explicit_start = True
        inp = """
        --- |-
          some more
          ...
          text
        """
        yaml.round_trip(inp)

    def test_root_literal_doc_indent_marker(self) -> None:
        yaml = YAML()
        yaml.explicit_start = True
        inp = """
        --- |2
           some more
          text
        """
        d = yaml.load(inp)
        print(type(d), repr(d))
        yaml.round_trip(inp)

    def test_nested_literal_doc_indent_marker(self) -> None:
        yaml = YAML()
        yaml.explicit_start = True
        inp = """
        ---
        a: |2
           some more
          text
        """
        d = yaml.load(inp)
        print(type(d), repr(d))
        yaml.round_trip(inp)


class Test_RoundTripLiteral:
    def test_rt_root_literal_scalar_no_indent(self) -> None:
        yaml = YAML()
        yaml.explicit_start = True
        s = 'testing123'
        ys = """
        --- |
        {}
        """
        ys = ys.format(s)
        d = yaml.load(ys)
        yaml.dump(d, compare=ys)

    def test_rt_root_literal_scalar_indent(self) -> None:
        yaml = YAML()
        yaml.explicit_start = True
        yaml.indent = 4
        s = 'testing123'
        ys = """
        --- |
            {}
        """
        ys = ys.format(s)
        d = yaml.load(ys)
        yaml.dump(d, compare=ys)

    def test_rt_root_plain_scalar_no_indent(self) -> None:
        yaml = YAML()
        yaml.explicit_start = True
        yaml.indent = 0
        s = 'testing123'
        ys = """
        ---
        {}
        """
        ys = ys.format(s)
        d = yaml.load(ys)
        yaml.dump(d, compare=ys)

    def test_rt_root_plain_scalar_expl_indent(self) -> None:
        yaml = YAML()
        yaml.explicit_start = True
        yaml.indent = 4
        s = 'testing123'
        ys = """
        ---
            {}
        """
        ys = ys.format(s)
        d = yaml.load(ys)
        yaml.dump(d, compare=ys)

    def test_rt_root_sq_scalar_expl_indent(self) -> None:
        yaml = YAML()
        yaml.explicit_start = True
        yaml.indent = 4
        s = "'testing: 123'"
        ys = """
        ---
            {}
        """
        ys = ys.format(s)
        d = yaml.load(ys)
        yaml.dump(d, compare=ys)

    def test_rt_root_dq_scalar_expl_indent(self) -> None:
        # if yaml.indent is the default (None)
        # then write after the directive indicator
        yaml = YAML()
        yaml.explicit_start = True
        yaml.indent = 0
        s = '"\'testing123"'
        ys = """
        ---
        {}
        """
        ys = ys.format(s)
        d = yaml.load(ys)
        yaml.dump(d, compare=ys)

    def test_rt_root_literal_scalar_no_indent_no_eol(self) -> None:
        yaml = YAML()
        yaml.explicit_start = True
        s = 'testing123'
        ys = """
        --- |-
        {}
        """
        ys = ys.format(s)
        d = yaml.load(ys)
        yaml.dump(d, compare=ys)

    def test_rt_non_root_literal_scalar(self) -> None:
        yaml = YAML()
        s = 'testing123'
        ys = """
        - |
          {}
        """
        ys = ys.format(s)
        d = yaml.load(ys)
        yaml.dump(d, compare=ys)

    def test_regular_spaces(self) -> None:
        import ruamel.yaml

        yaml = ruamel.yaml.YAML()
        ys = "key: |\n\n\n   content\n"
        d = yaml.load(ys)
        assert d['key'] == '\n\ncontent\n'

    def test_irregular_spaces_content(self) -> None:
        import ruamel.yaml

        yaml = ruamel.yaml.YAML()
        ys = "key: |\n  \n   \n  irregular content\n"
        with pytest.raises(ruamel.yaml.scanner.ScannerError):
            d = yaml.load(ys)
            print(d)

    def test_irregular_spaces_comment(self) -> None:
        import ruamel.yaml

        yaml = ruamel.yaml.YAML()
        ys = "key: |\n  \n   \n  # comment\n"
        with pytest.raises(ruamel.yaml.scanner.ScannerError):
            d = yaml.load(ys)
            print(d)
