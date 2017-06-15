
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
  - it is no allowed to pass in a ``pathlib.Path`` as "stream" parameter to all
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

0.13.14 (2017-02-12):
  - fix for issue 97: clipped block scalar followed by empty lines and comment
    would result in two CommentTokens of which the first was dropped.
    (reported by Colm O'Connor)

0.13.13 (2017-01-28):
  - fix for issue 96: prevent insertion of extra empty line if indented mapping entries
    are separated by an empty line (reported by Derrick Sawyer)

0.13.11 (2017-01-23):
  - allow ':' in flow style scalars if not followed by space. Also don't
    quote such scalar as this is no longer necessary.
  - add python 3.6 manylinux wheel to PyPI

0.13.10 (2017-01-22):
  - fix for issue 93, insert spurious blank line before single line comment
    between indented sequence elements (reported by Alex)

0.13.9 (2017-01-18):
  - fix for issue 92, wrong import name reported by the-corinthian

0.13.8 (2017-01-18):
  - fix for issue 91, when a compiler is unavailable reported by Maximilian Hils
  - fix for deepcopy issue with TimeStamps not preserving 'T', reported on
    `StackOverflow Q&A <http://stackoverflow.com/a/41577841/1307905>`_ by
    `Quuxplusone <http://stackoverflow.com/users/1424877/quuxplusone>`_


0.13.7 (2016-12-27):
  - fix for issue 85, constructor.py importing unicode_literals caused mypy to fail
    on 2.7 (reported by Peter Amstutz)

0.13.6 (2016-12-27):
  - fix for issue 83, collections.OrderedDict not representable by SafeRepresenter
    (reported by Frazer McLean)

0.13.5 (2016-12-25):
  - fix for issue 84, deepcopy not properly working (reported by Peter Amstutz)

0.13.4 (2016-12-05):
  - another fix for issue 82, change to non-global resolver data broke implicit type
    specification

0.13.3 (2016-12-05):
  - fix for issue 82, deepcopy not working (reported by code monk)

0.13.2 (2016-11-28):
  - fix for comments after empty (null) values  (reported by dsw2127 and cokelaer)

0.13.1 (2016-11-22):
  - optimisations on memory usage when loading YAML from large files (py3: -50%, py2: -85%)

0.13.0 (2016-11-20):
  - if ``load()`` or ``load_all()`` is called with only a single argument
    (stream or string)
    a UnsafeLoaderWarning will be issued once. If appropriate you can surpress this
    warning by filtering it. Explicitly supplying the ``Loader=ruamel.yaml.Loader``
    argument, will also prevent it from being issued. You should however consider
    using ``safe_load()``, ``safe_load_all()`` if your YAML input does not use tags.
  - allow adding comments before and after keys (based on
    `StackOveflow Q&A <http://stackoverflow.com/a/40705671/1307905>`_  by
    `msinn <http://stackoverflow.com/users/7185467/msinn>`_)

----

For older changes see the file
`CHANGES <https://bitbucket.org/ruamel/yaml/src/default/CHANGES>`_
