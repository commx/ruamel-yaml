# coding: utf-8

"""
some helper functions that might be generally useful
"""

from __future__ import print_function
from __future__ import absolute_import

from .compat import text_type, binary_type
from .main import round_trip_load


# originally as comment
# https://github.com/pre-commit/pre-commit/pull/211#issuecomment-186466605
# if you use this in your code, I suggest adding a test in your test suite
# that check this routines output against a known piece of your YAML
# before upgrades to this code break your round-tripped YAML
def load_yaml_guess_indent(stream):
    # load a yaml file guess the indentation, if you use TABs ...
    if isinstance(stream, text_type):
        yaml_str = stream
    elif isinstance(stream, binary_type):
        yaml_str = stream.decode('utf-8')  # most likely, but the Reader checks BOM for this
    else:
        yaml_str = stream.read()
    indent = None  # default if not found for some reason
    prev_line_key_only = None
    for line in yaml_str.splitlines():
        rline = line.rstrip()
        if rline.startswith('- '):
            idx = 1
            while line[idx] == ' ':  # this will end as we rstripped
                idx += 1
            if line[idx] == '#':     # comment after -
                continue
            indent = idx
            break
        if rline.endswith(':'):
            idx = 0
            while line[idx] == ' ':  # this will end on ':'
                idx += 1
            prev_line_key_only = idx
            continue
        if prev_line_key_only is not None and rline:
            idx = 0
            while line[idx] in ' -':  # this will end on ':'
                idx += 1
            if idx > prev_line_key_only:
                indent = idx - prev_line_key_only
                break
        prev_line_key_only = None
    return round_trip_load(yaml_str), indent


def configobj_walker(cfg):
    """
    walks over a ConfigObj (INI file with comments) generating
    corresponding YAML output (including comments
    """
    from configobj import ConfigObj
    assert isinstance(cfg, ConfigObj)
    for c in cfg.initial_comment:
        if c.strip():
            yield c
    for s in _walk_section(cfg):
        if s.strip():
            yield s
    for c in cfg.final_comment:
        if c.strip():
            yield c


def _walk_section(s, level=0):
    from configobj import Section
    assert isinstance(s, Section)
    indent = u'  ' * level
    for name in s.scalars:
        for c in s.comments[name]:
            yield indent + c.strip()
        x = s[name]
        if u'\n' in x:
            i = indent + u'  '
            x = u'|\n' + i + x.strip().replace(u'\n', u'\n' + i)
        elif ':' in x:
            x = u"'" + x.replace(u"'", u"''") + u"'"
        line = u'{0}{1}: {2}'.format(indent, name, x)
        c = s.inline_comments[name]
        if c:
            line += u' ' + c
        yield line
    for name in s.sections:
        for c in s.comments[name]:
            yield indent + c.strip()
        line = u'{0}{1}:'.format(indent, name)
        c = s.inline_comments[name]
        if c:
            line += u' ' + c
        yield line
        for val in _walk_section(s[name], level=level+1):
            yield val

# def config_obj_2_rt_yaml(cfg):
#     from .comments import CommentedMap, CommentedSeq
#     from configobj import ConfigObj
#     assert isinstance(cfg, ConfigObj)
#     #for c in cfg.initial_comment:
#     #    if c.strip():
#     #        pass
#     cm = CommentedMap()
#     for name in s.sections:
#         cm[name] = d = CommentedMap()
#
#
#     #for c in cfg.final_comment:
#     #    if c.strip():
#     #        yield c
#     return cm
