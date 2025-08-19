
from __future__ import annotations

if False:  # MYPY
    from typing import Any, Dict, List, Union, Optional, Iterator  # NOQA


merge_attrib = '_yaml_merge'


class MergeValue:
    attrib = merge_attrib

    def __init__(self) -> None:
        self.value = []
        self.sequence = None
        self.merge_pos = None  # position of merge in the mapping

    def __getitem__(self, index):
        return self.value[index]

    def __setitem__(self, index, val):
        self.value[index] = val

    def __repr__(self) -> Any:
        return f'MergeValue({self.value!r})'

    def __len__(self):
        return len(self.value)

    def append(self, elem):
        self.value.append(elem)

    def extend(self, elements):
        self.value.extend(elements)

    def set_sequence(self, seq):
        # print('mergevalue.set_sequence node', node.anchor)
        self.sequence = seq
