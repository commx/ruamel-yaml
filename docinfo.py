
from __future__ import annotations

"""
DocInfo

Although it was possible to read tag directives before this, all handle/prefix
pairs for all documents in all streams were stored in one dictionary per
YAML instance, making it impossible to distinguish where such a pair came
from without sublassing the scanner.

ToDo:
DocInfo can be used by a yaml dumper to dump a class
- if connected to the root of a data structure
- if provided to the dumper?
"""

from typing import Optional, Tuple
from dataclasses import dataclass, field, MISSING  # NOQA


@dataclass(order=True, frozen=True)
class Version:
    major: int
    minor: int

    # def __repr__(self):
    #     return f'Version("{self.major}.{self.minor}")'


def version(
    major: int | str | Tuple[int, int] | None,
    minor: Optional[int] = None,
) -> Optional[Version]:
    if major is None:
        assert minor is None
        return None
    if isinstance(major, str):
        assert minor is None
        parts = major.split('.')
        assert len(parts) == 2
        return Version(int(parts[0]), int(parts[1]))
    elif isinstance(major, tuple):
        assert minor is None
        assert len(major) == 2
        major, minor = major
    assert minor is not None
    return Version(major, minor)


@dataclass(frozen=True)
class Tag:
    handle: str
    prefix: str


@dataclass
class DocInfo:
    """
    Store document information, can be used for analysis of a loaded YAML document
    requested_version: if explicitly set before load
    doc_version: from %YAML directive
    tags: from %TAG directives in scanned order
    """
    requested_version: Optional[Version] = None
    doc_version: Optional[Version] = None
    tags: list[Tag] = field(default_factory=list)
