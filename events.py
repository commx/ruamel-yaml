# coding: utf-8

# Abstract classes.

from typing import Any, Dict, Optional, List  # NOQA

SHOW_LINES = False


def CommentCheck() -> None:
    pass


class Event:
    __slots__ = 'start_mark', 'end_mark', 'comment'

    def __init__(
        self, start_mark: Any = None, end_mark: Any = None, comment: Any = CommentCheck
    ) -> None:
        self.start_mark = start_mark
        self.end_mark = end_mark
        # assert comment is not CommentCheck
        if comment is CommentCheck:
            comment = None
        self.comment = comment

    def __repr__(self) -> Any:
        if True:
            arguments = []
            if hasattr(self, 'value'):
                # if you use repr(getattr(self, 'value')) then flake8 complains about
                # abuse of getattr with a constant. When you change to self.value
                # then mypy throws an error
                arguments.append(repr(self.value))
            for key in ['anchor', 'tag', 'implicit', 'flow_style', 'style']:
                v = getattr(self, key, None)
                if v is not None:
                    arguments.append(f'{key!s}={v!r}')
            if self.comment not in [None, CommentCheck]:
                arguments.append(f'comment={self.comment!r}')
            if SHOW_LINES:
                arguments.append(
                    f'({self.start_mark.line}:{self.start_mark.column}/'
                    f'{self.end_mark.line}:{self.end_mark.column})'
                )
            arguments = ', '.join(arguments)  # type: ignore
        else:
            attributes = [
                key
                for key in ['anchor', 'tag', 'implicit', 'value', 'flow_style', 'style']
                if hasattr(self, key)
            ]
            arguments = ', '.join([f'{key!s}={getattr(self, key)!r}' for key in attributes])
            if self.comment not in [None, CommentCheck]:
                arguments += f', comment={self.comment!r}'
        return f'{self.__class__.__name__!s}({arguments!s})'


class NodeEvent(Event):
    __slots__ = ('anchor',)

    def __init__(
        self, anchor: Any, start_mark: Any = None, end_mark: Any = None, comment: Any = None
    ) -> None:
        Event.__init__(self, start_mark, end_mark, comment)
        self.anchor = anchor


class CollectionStartEvent(NodeEvent):
    __slots__ = 'tag', 'implicit', 'flow_style', 'nr_items'

    def __init__(
        self,
        anchor: Any,
        tag: Any,
        implicit: Any,
        start_mark: Any = None,
        end_mark: Any = None,
        flow_style: Any = None,
        comment: Any = None,
        nr_items: Optional[int] = None,
    ) -> None:
        NodeEvent.__init__(self, anchor, start_mark, end_mark, comment)
        self.tag = tag
        self.implicit = implicit
        self.flow_style = flow_style
        self.nr_items = nr_items


class CollectionEndEvent(Event):
    __slots__ = ()


# Implementations.


class StreamStartEvent(Event):
    __slots__ = ('encoding',)

    def __init__(
        self,
        start_mark: Any = None,
        end_mark: Any = None,
        encoding: Any = None,
        comment: Any = None,
    ) -> None:
        Event.__init__(self, start_mark, end_mark, comment)
        self.encoding = encoding


class StreamEndEvent(Event):
    __slots__ = ()


class DocumentStartEvent(Event):
    __slots__ = 'explicit', 'version', 'tags'

    def __init__(
        self,
        start_mark: Any = None,
        end_mark: Any = None,
        explicit: Any = None,
        version: Any = None,
        tags: Any = None,
        comment: Any = None,
    ) -> None:
        Event.__init__(self, start_mark, end_mark, comment)
        self.explicit = explicit
        self.version = version
        self.tags = tags


class DocumentEndEvent(Event):
    __slots__ = ('explicit',)

    def __init__(
        self,
        start_mark: Any = None,
        end_mark: Any = None,
        explicit: Any = None,
        comment: Any = None,
    ) -> None:
        Event.__init__(self, start_mark, end_mark, comment)
        self.explicit = explicit


class AliasEvent(NodeEvent):
    __slots__ = 'style'

    def __init__(
        self,
        anchor: Any,
        start_mark: Any = None,
        end_mark: Any = None,
        style: Any = None,
        comment: Any = None,
    ) -> None:
        NodeEvent.__init__(self, anchor, start_mark, end_mark, comment)
        self.style = style


class ScalarEvent(NodeEvent):
    __slots__ = 'tag', 'implicit', 'value', 'style'

    def __init__(
        self,
        anchor: Any,
        tag: Any,
        implicit: Any,
        value: Any,
        start_mark: Any = None,
        end_mark: Any = None,
        style: Any = None,
        comment: Any = None,
    ) -> None:
        NodeEvent.__init__(self, anchor, start_mark, end_mark, comment)
        self.tag = tag
        self.implicit = implicit
        self.value = value
        self.style = style


class SequenceStartEvent(CollectionStartEvent):
    __slots__ = ()


class SequenceEndEvent(CollectionEndEvent):
    __slots__ = ()


class MappingStartEvent(CollectionStartEvent):
    __slots__ = ()


class MappingEndEvent(CollectionEndEvent):
    __slots__ = ()
