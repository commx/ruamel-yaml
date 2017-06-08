
import sys
from ruamel.yaml import YAML

data = {1: {1: [{1: 1, 2: 2}, {1: 1, 2: 2}], 2: 2}, 2: 42}

yaml = YAML()
yaml.explicit_start = True
yaml.dump(data, sys.stdout)
yaml.indent = 4
yaml.block_seq_indent = 2
yaml.dump(data, sys.stdout)


def sequence_indent_four(s):
    # this will fail on direclty nested lists: {1; [[2, 3], 4]}
    levels = []
    ret_val = ''
    for line in s.splitlines(True):
        ls = line.lstrip()
        indent = len(line) - len(ls)
        if ls.startswith('- '):
            if not levels or indent > levels[-1]:
                levels.append(indent)
            elif levels:
                if indent < levels[-1]:
                    levels = levels[:-1]
            # same -> do nothing
        else:
            if levels:
                if indent <= levels[-1]:
                    while levels and indent <= levels[-1]:
                        levels = levels[:-1]
        ret_val += '  ' * len(levels) + line
    return ret_val

yaml = YAML()
yaml.explicit_start = True
yaml.dump(data, sys.stdout, transform=sequence_indent_four)
