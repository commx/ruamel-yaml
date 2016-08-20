# coding: utf-8

from __future__ import print_function, absolute_import, division, unicode_literals

import datetime


class TimeStamp(datetime.datetime):
    def __init__(self, *args, **kw):
        self._yaml = dict(t=False, tz=None, delta=0)

    def __new__(cls, *args, **kw):  # datetime is immutable
        return datetime.datetime.__new__(cls, *args, **kw)
