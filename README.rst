
ruamel.yaml
===========

``ruamel.yaml`` is a YAML 1.2 loader/dumper package for Python.

Starting with version 0.15.0 the way YAML files are loaded and dumped
is changing. See the API doc for details.  Currently existing
functionality will throw a warning before being changed/removed.
**For production systems you should pin the version being used with
``ruamel.yaml<=0.15``**. There might be bug fixes in the 0.14 series,
but new functionality is likely only to be available via the new API.

If your package uses ``ruamel.yaml`` and is not listed on PyPI, drop
me an email, preferably with some infomormation on how you use the
package (or a link to bitbucket/github) and I'll keep you informed
when the status of the API is stable enough to make the transition.

* `Overview <http://yaml.readthedocs.org/en/latest/overview.html>`_
* `Installing <http://yaml.readthedocs.org/en/latest/install.html>`_
* `Basic Usage <http://yaml.readthedocs.org/en/latest/basicuse.html>`_
* `Details <http://yaml.readthedocs.org/en/latest/detail.html>`_
* `Examples <http://yaml.readthedocs.org/en/latest/example.html>`_
* `API <http://yaml.readthedocs.org/en/latest/api.html>`_
* `Differences with PyYAML <http://yaml.readthedocs.org/en/latest/pyyaml.html>`_

.. image:: https://readthedocs.org/projects/yaml/badge/?version=stable
   :target: https://yaml.readthedocs.org/en/stable

ChangeLog
=========

.. should insert NEXT: at the beginning of line for next key

0.15.15 (2017-06-27):
  - fix for issue 135, typ='safe' not dumping in Python 2.7
    (reported by Andrzej Ostrowski <https://bitbucket.org/aostr123/>`_)

0.15.14 (2017-06-25):
  - fix for issue 133, in setup.py: change ModuleNotFoundError to
    ImportError (reported and fix by
    `Asley Drake  <https://github.com/aldraco>`_)

0.15.13 (2017-06-24):
  - suppress duplicate key warning on mappings with merge keys (reported by
    Cameron Sweeney)

0.15.12 (2017-06-24):
  - remove fatal dependency of setup.py on wheel package (reported by
    Cameron Sweeney)

0.15.11 (2017-06-24):
  - fix for issue 130, regression in nested merge keys (reported by
    `David Fee <https://bitbucket.org/dfee/>`_)

0.15.10 (2017-06-23):
  - top level PreservedScalarString not indented if not explicitly asked to
  - remove Makefile (not very useful anyway)
  - some mypy additions

0.15.9 (2017-06-16):
  - fix for issue 127: tagged scalars were always quoted and seperated
    by a newline when in a block sequence (reported and largely fixed by
    `Tommy Wang <https://bitbucket.org/twang817/>`_)

0.15.8 (2017-06-15):
  - allow plug-in install via ``install ruamel.yaml[jinja2]``

0.15.7 (2017-06-14):
  - add plug-in mechanism for load/dump pre resp. post-processing

0.15.6 (2017-06-10):
  - a set() with duplicate elements now throws error in rt loading
  - support for toplevel column zero literal/folded scalar in explicit documents

0.15.5 (2017-06-08):
  - repeat `load()` on a single `YAML()` instance would fail.

0.15.4 (2017-06-08):
  - `transform` parameter on dump that expects a function taking a
    string and returning a string. This allows transformation of the output
    before it is written to stream. This forces creation of the complete output in memory!
  - some updates to the docs

0.15.3 (2017-06-07):
  - No longer try to compile C extensions on Windows. Compilation can be forced by setting
    the environment variable `RUAMEL_FORCE_EXT_BUILD` to some value
    before starting the `pip install`.

0.15.2 (2017-06-07):
  - update to conform to mypy 0.511: mypy --strict

0.15.1 (2017-06-07):
  - `duplicate keys  <http://yaml.readthedocs.io/en/latest/api.html#duplicate-keys>`_
    in mappings generate an error (in the old API this change generates a warning until 0.16)
  - dependecy on ruamel.ordereddict for 2.7 now via extras_require

0.15.0 (2017-06-04):
  - it is now allowed to pass in a ``pathlib.Path`` as "stream" parameter to all
    load/dump functions
  - passing in a non-supported object (e.g. a string) as "stream" will result in a
    much more meaningful YAMLStreamError.
  - assigning a normal string value to an existing CommentedMap key or CommentedSeq
    element will result in a value cast to the previous value's type if possible.
  - added ``YAML`` class for new API

0.14.12 (2017-05-14):
  - fix for issue 119, deepcopy not returning subclasses (reported and PR by
    Constantine Evans <cevans@evanslabs.org>)

0.14.11 (2017-05-01):
  - fix for issue 103 allowing implicit documents after document end marker line (``...``)
    in YAML 1.2

0.14.10 (2017-04-26):
  - fix problem with emitting using cyaml

0.14.9 (2017-04-22):
  - remove dependency on ``typing`` while still supporting ``mypy``
    (http://stackoverflow.com/a/43516781/1307905)
  - fix unclarity in doc that stated 2.6 is supported (reported by feetdust)

0.14.8 (2017-04-19):
  - fix Text not available on 3.5.0 and 3.5.1, now proactively setting version guards
    on all files (reported by `João Paulo Magalhães <https://bitbucket.org/jpmag/>`_)

0.14.7 (2017-04-18):
  - round trip of integers (decimal, octal, hex, binary) now preserve
    leading zero(s) padding and underscores. Underscores are presumed
    to be at regular distances (i.e. ``0o12_345_67`` dumps back as
    ``0o1_23_45_67`` as the space from the last digit to the
    underscore before that is the determining factor).

0.14.6 (2017-04-14):
  - binary, octal and hex integers are now preserved by default. This
    was a known deficiency. Working on this was prompted by the issue report (112)
    from devnoname120, as well as the additional experience with `.replace()`
    on `scalarstring` classes.
  - fix issues 114: cannot install on Buildozer (reported by mixmastamyk).
    Setting env. var ``RUAMEL_NO_PIP_INSTALL_CHECK`` will suppress ``pip``-check.

0.14.5 (2017-04-04):
  - fix issue 109: None not dumping correctly at top level (reported by Andrea Censi)
  - fix issue 110: .replace on Preserved/DoubleQuoted/SingleQuoted ScalarString
    would give back "normal" string (reported by sandres23)

0.14.4 (2017-03-31):
  - fix readme

0.14.3 (2017-03-31):
  - fix for 0o52 not being a string in YAML 1.1 (reported on
    `StackOverflow Q&A 43138503 <http://stackoverflow.com/a/43138503/1307905>`_ by
    `Frank D <http://stackoverflow.com/users/7796630/frank-d>`_)

0.14.2 (2017-03-23):
  - fix for old default pip on Ubuntu 14.04 (reported by Sébastien Maccagnoni-Munch)

0.14.1 (2017-03-22):
  - fix Text not available on 3.5.0 and 3.5.1 (reported by Charles Bouchard-Légaré)

0.14.0 (2017-03-21):
  - updates for mypy --strict
  - preparation for moving away from inheritance in Loader and Dumper, calls from e.g.
    the Representer to the Serializer.serialize() are now done via the attribute
    .serializer.serialize(). Usage of .serialize() outside of Serializer will be
    deprecated soon
  - some extra tests on main.py functions

----

For older changes see the file
`CHANGES <https://bitbucket.org/ruamel/yaml/src/default/CHANGES>`_
