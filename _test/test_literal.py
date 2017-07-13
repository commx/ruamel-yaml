# coding: utf-8
from __future__ import print_function

import pytest  # NOQA

from roundtrip import YAML


"""
YAML 1.0 allowed top level literal style without indentation:
  "Usually top level nodes are not indented" (example 4.21 in 4.6.3)
YAML 1.1 is a bit vague but says:
  "Regardless of style, scalar content must always be indented by at least one space"
  (4.4.3)
  "In general, the document’s node is indented as if it has a parent indented at -1 spaces."
  (4.3.3)
YAML 1.2 is again clear about top level literal scalar after directive in example 9.5:

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
    def test_top_literal_scalar_indent_example_9_5(self):
        yaml = YAML()
        s = '%!PS-Adobe-2.0'
        d = yaml.load("""
        --- |
          {}
        """.format(s))
        print(d)
        assert d == s + '\n'

    def test_top_literal_scalar_no_indent(self):
        yaml = YAML()
        s = 'testing123'
        d = yaml.load("""
        --- |
        {}
        """.format(s))
        print(d)
        assert d == s + '\n'

    def test_top_literal_scalar_no_indent_1_1(self):
        yaml = YAML()
        s = 'testing123'
        d = yaml.load("""
        %YAML 1.1
        --- |
        {}
        """.format(s))
        print(d)
        assert d == s + '\n'

    def test_top_literal_scalar_no_indent_1_1_old_style(self):
        from textwrap import dedent
        from ruamel.yaml import safe_load
        s = 'testing123'
        d = safe_load(dedent("""
        %YAML 1.1
        --- |
          {}
        """.format(s)))
        print(d)
        assert d == s + '\n'

    def test_top_literal_scalar_no_indent_1_1_raise(self):
        from ruamel.yaml.parser import ParserError
        yaml = YAML()
        yaml.top_level_block_style_scalar_no_indent_error_1_1 = True
        s = 'testing123'
        with pytest.raises(ParserError):
            yaml.load("""
            %YAML 1.1
            --- |
            {}
            """.format(s))

    def test_top_literal_scalar_indent_offset_one(self):
        yaml = YAML()
        s = 'testing123'
        d = yaml.load("""
        --- |1
         {}
        """.format(s))
        print(d)
        assert d == s + '\n'

    def test_top_literal_scalar_indent_offset_four(self):
        yaml = YAML()
        s = 'testing123'
        d = yaml.load("""
        --- |4
            {}
        """.format(s))
        print(d)
        assert d == s + '\n'

    def test_top_literal_scalar_indent_offset_two_leading_space(self):
        yaml = YAML()
        s = ' testing123'
        d = yaml.load("""
        --- |4
            {s}
            {s}
        """.format(s=s))
        print(d)
        assert d == (s + '\n') * 2

    def test_top_literal_scalar_no_indent_special(self):
        yaml = YAML()
        s = '%!PS-Adobe-2.0'
        d = yaml.load("""
        --- |
        {}
        """.format(s))
        print(d)
        assert d == s + '\n'

    def test_top_folding_scalar_indent(self):
        yaml = YAML()
        s = '%!PS-Adobe-2.0'
        d = yaml.load("""
        --- >
          {}
        """.format(s))
        print(d)
        assert d == s + '\n'

    def test_top_folding_scalar_no_indent(self):
        yaml = YAML()
        s = 'testing123'
        d = yaml.load("""
        --- >
        {}
        """.format(s))
        print(d)
        assert d == s + '\n'

    def test_top_folding_scalar_no_indent_special(self):
        yaml = YAML()
        s = '%!PS-Adobe-2.0'
        d = yaml.load("""
        --- >
        {}
        """.format(s))
        print(d)
        assert d == s + '\n'

    def test_top_literal_multi_doc(self):
        yaml = YAML(typ='safe', pure=True)
        s1 = 'abc'
        s2 = 'klm'
        for idx, d1 in enumerate(yaml.load_all("""
        --- |-
        {}
        --- |
        {}
        """.format(s1, s2))):
            print('d1:', d1)
            assert ['abc', 'klm\n'][idx] == d1


class Test_RoundTripLiteral:
    def test_rt_top_literal_scalar_no_indent(self):
        yaml = YAML()
        yaml.explicit_start = True
        s = 'testing123'
        ys = """
        --- |
        {}
        """.format(s)
        d = yaml.load(ys)
        yaml.dump(d, compare=ys)

    def test_rt_top_literal_scalar_indent(self):
        yaml = YAML()
        yaml.explicit_start = True
        yaml.indent = 4
        s = 'testing123'
        ys = """
        --- |
            {}
        """.format(s)
        d = yaml.load(ys)
        yaml.dump(d, compare=ys)

    def test_rt_top_plain_scalar_no_indent(self):
        yaml = YAML()
        yaml.explicit_start = True
        yaml.indent = 0
        s = 'testing123'
        ys = """
        ---
        {}
        """.format(s)
        d = yaml.load(ys)
        yaml.dump(d, compare=ys)

    def test_rt_top_plain_scalar_expl_indent(self):
        yaml = YAML()
        yaml.explicit_start = True
        yaml.indent = 4
        s = 'testing123'
        ys = """
        ---
            {}
        """.format(s)
        d = yaml.load(ys)
        yaml.dump(d, compare=ys)

    def test_rt_top_sq_scalar_expl_indent(self):
        yaml = YAML()
        yaml.explicit_start = True
        yaml.indent = 4
        s = "'testing: 123'"
        ys = """
        ---
            {}
        """.format(s)
        d = yaml.load(ys)
        yaml.dump(d, compare=ys)

    def test_rt_top_dq_scalar_expl_indent(self):
        # if yaml.indent is the default (None)
        # then write after the directive indicator
        yaml = YAML()
        yaml.explicit_start = True
        yaml.indent = 0
        s = '"\'testing123"'
        ys = """
        ---
        {}
        """.format(s)
        d = yaml.load(ys)
        yaml.dump(d, compare=ys)

    def test_rt_top_literal_scalar_no_indent_no_eol(self):
        yaml = YAML()
        yaml.explicit_start = True
        s = 'testing123'
        ys = """
        --- |-
        {}
        """.format(s)
        d = yaml.load(ys)
        yaml.dump(d, compare=ys)

    def test_rt_non_top_literal_scalar(self):
        yaml = YAML()
        s = 'testing123'
        ys = """
        - |
          {}
        """.format(s)
        d = yaml.load(ys)
        yaml.dump(d, compare=ys)
