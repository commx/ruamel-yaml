from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals


from textwrap import dedent

import pytest

import ruamel.yaml


def rt(s):
    return ruamel.yaml.dump(
        ruamel.yaml.load(s, Loader=ruamel.yaml.RoundTripLoader),
        Dumper=ruamel.yaml.RoundTripDumper,
    ).strip() + '\n'


def test_roundtrip_inline_list():
    s = 'a: [a, b, c]\n'
    output = rt(s)
    assert s == output

def test_roundtrip_mapping_of_inline_lists():
    s = dedent("""\
    a: [a, b, c]
    j: [k, l, m]
    """)
    output = rt(s)
    assert s == output

def test_roundtrip_mapping_of_inline_lists_comments():
    s = dedent("""\
    # comment A
    a: [a, b, c]
    # comment B
    j: [k, l, m]
    """)
    output = rt(s)
    assert s == output

def test_roundtrip_mapping_of_inline_sequence_eol_comments():
    s = dedent("""\
    # comment A
    a: [a, b, c]  # comment B
    j: [k, l, m]  # comment C
    """)
    output = rt(s)
    assert s == output


# first test by explicitly setting flow style
def test_added_inline_list():
    s1 = dedent("""
    a:
    - b
    - c
    - d
    """)
    s = 'a: [b, c, d]\n'
    data = ruamel.yaml.load(s1, Loader=ruamel.yaml.RoundTripLoader)
    val = data['a']
    val.fa.set_flow_style()
    # print(type(val), '_yaml_format' in dir(val))
    output = ruamel.yaml.dump(data, Dumper=ruamel.yaml.RoundTripDumper)
    assert s == output

############# flow mappings

def test_roundtrip_flow_mapping():
    s = dedent("""\
    - {a: 1, b: hallo}
    - {j: fka, k: 42}
    """)
    data = ruamel.yaml.load(s, Loader=ruamel.yaml.RoundTripLoader)
    output = ruamel.yaml.dump(data, Dumper=ruamel.yaml.RoundTripDumper)
    assert s == output

def test_roundtrip_sequence_of_inline_mappings_eol_comments():
    s = dedent("""\
    # comment A
    - {a: 1, b: hallo}  # comment B
    - {j: fka, k: 42}  # comment C
    """)
    output = rt(s)
    assert s == output



############# indentation

@pytest.mark.xfail
def test_roundtrip_four_space_indents():
    s = (
        'a:\n'
        '-   foo\n'
        '-   bar\n'
    )
    output = rt(s)
    assert s == output
