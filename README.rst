
ruamel.yaml
===========

``ruamel.yaml`` is a YAML 1.2 loader/dumper package for Python.

* `Overview <http://yaml.readthedocs.org/en/latest/overview.html>`_
* `Installing <http://yaml.readthedocs.org/en/latest/install.html>`_
* `Details <http://yaml.readthedocs.org/en/latest/detail.html>`_
* `Examples <http://yaml.readthedocs.org/en/latest/example.html>`_
* `Differences with PyYAML <http://yaml.readthedocs.org/en/latest/pyyaml.html>`_

.. image:: https://readthedocs.org/projects/yaml/badge/?version=stable
   :target: https://yaml.readthedocs.org/en/stable

ChangeLog
=========

::

  0.12.5 (2016-08-20):
    - fixing issue 45 preserving datetime formatting (submitted by altuin)
      Several formatting parameters are preserved with some normalisation:
      - preserve 'T', 't' is replaced by 'T', multiple spaces between date
        and time reduced to one.
      - optional space before timezone is removed
      - still using microseconds, but now rounded (.1234567 -> .123457)
      - Z/-5/+01:00 preserved

  0.12.4 (2016-08-19):
    - Fix for issue 44: missing preserve_quotes keyword argument (reported
      by M. Crusoe)

  0.12.3 (2016-08-17):
    - correct 'in' operation for merged CommentedMaps in round-trip mode
      (implementation inspired by J.Ngo, but original not working for merges)
    - iteration over round-trip loaded mappings, that contain merges. Also
      keys(), items(), values() (Py3/Py2) and iterkeys(), iteritems(),
      itervalues(), viewkeys(), viewitems(), viewvalues() (Py2)
    - reuse of anchor name now generates warning, not an error. Round-tripping such
      anchors works correctly. This inherited PyYAML issue was brought to attention
      by G. Coddut (and was long standing https://bugs.debian.org/cgi-bin/bugreport.cgi?bug=515634)
      suppressing the warning:
          import warnings
          from ruamel.yaml.error import ReusedAnchorWarning
          warnings.simplefilter("ignore", ReusedAnchorWarning)

  0.12.2 (2016-08-16):
    - minor improvements based on feedback from M. Crusoe
      https://bitbucket.org/ruamel/yaml/issues/42/

  0.12.0 (2016-08-16):
    - drop support for Python 2.6
    - include initial Type information (inspired by M. Crusoe)

  0.11.15 (2016-08-07):
    - Change to prevent FutureWarning in NumPy, as reported by tgehring
    ("comparison to None will result in an elementwise object comparison in the future")

  0.11.14 (2016-07-06):
    - fix preserve_quotes missing on original Loaders (as reported
      by Leynos, bitbucket issue 38)

  0.11.13 (2016-07-06):
    - documentation only, automated linux wheels

  0.11.12 (2016-07-06):
    - added support for roundtrip of single/double quoted scalars using:
      ruamel.yaml.round_trip_load(stream, preserve_quotes=True)

  0.11.0 (2016-02-18):
    - RoundTripLoader loads 1.2 by default (no sexagesimals, 012 octals nor
      yes/no/on/off booleans
