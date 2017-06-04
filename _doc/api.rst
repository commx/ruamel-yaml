

Departure from previous API
---------------------------

With version 0.15.0 `ruamel.yaml` starts to depart from the previous (PyYAML) way
of loading and dumping.  During a transition period the original
`load()` and `dump()` in its various formats will still be supported,
but this is not guaranteed to be so with the transition to 1.0.

At the latest with 1.0, but possible earlier transition error and
warning messages will be issued, so any packages depending on
ruamel.yaml should pin the version with which they are testing.

Up to 0.15.0, the loaders (``load()``, ``safe_load()``,
``round_trip_load()``, ``load_all``, etc.) took, apart from the input
stream, a ``version`` argument to allow downgrading to YAML 1.1,
sometimes needed for
documents without directive. When round-tripping, there was an option to
preserve quotes.

Up to 0.15.0, the dumpers (``dump()``, ``safe_dump``,
``round_trip_dump()``, ``dump_all()``, etc.) had a plethora of
arguments, some inhereted from ``PyYAML``, some added in
``ruamel.yaml``. The only required argument is the ``data`` to be
dumped. If the stream argument is not provided to the dumper, then a
string representation is build up in memory and returned to the
caller.

Starting with 0.15.0 ``load()`` and ``dump()`` are methods on a
``YAML`` instance and only take the stream,
resp. the data and stram argument. All other parameters  are set on the instance
of ``YAML`` before calling ``load()`` or ``dump()``

Before 0.15.0::

    from pathlib import Path
    from ruamel import yaml

    data = yaml.safe_load("abc: 1")
    out = path('/tmp/out.yaml')
    with out.open('w') as fp:
        yaml.safe_dump(data, fp, default_flow_style=False)

after:

    from ruamel.yaml import YAML

    yaml = YAML(typ='safe')
    yaml.default_flow_style = False
    data = yaml.load("abc: 1")
    out = path('/tmp/out.yaml')
    yaml.dump(data, out)

If you previously used an keyword argument `explicit_start=True` you
now do ``yaml.explicit_start = True`` before calling ``dump()``. The
``Loader`` and ``Dumper`` keyword arguments are not supported that
way. You can provide the `typ` keyword to `rt`  (default),
`safe`, `unsafe` or `base` (for round-trip load/dump, safe_load/dump,
load/dump resp. using the BaseLoader / BaseDumper. More fine-control
is possible by setting the attributes `.Parser`, `.Constructor`,
`.Emitter`, etc., to the class of the type to create for that stage
(typically a subclass of an existing class implementing that).

All data is dumped (not just for round-trip-mode) with `.allow_unicode
= True`

You can of course have multiple YAML instances active at the same
time, with different load and/or dump behaviour.

Initially only the typical operations are supported, but in principle
all functionality of the old interface will be available via
``YAML`` instances (if you are using something that isn't let me know).

Reason for API change
---------------------

``ruamel.yaml`` inherited the way of doing things from ``PyYAML``. In
particular when calling the function ``load()`` or ``dump()`` a
temporary instances of  ``Loader()`` resp. ``Dumper()``  were
created that were discarded on termination of the function.

This way of doing things leads to several problems:

- it is impossible to return information to the caller apart from the
  constructed data structure. E.g. if you would get a YAML document
  version number from a directive, there is no way to let the caller
  know apart from handing back special data structures. The same
  problem exists when trying to do on the fly
  analysis of a document for indentation width.

- these instances were composites of the various load/dump steps and
  if you wanted to enhance one of the steps, you needed e.g. subclass
  the emitter and make a new composite (dumper) as well, providing all
  of the parameters (i.e. copy paste

- many routines (like ``add_representer()``) have a direct global
  impact on all of the following calls to ``dump()`` and those are
  difficult if not impossible to turn back. This forces the need to
  subclass ``Loaders`` and ``Dumpers``, a long time problem in PyYAML
  as some attributes were not `deep_copied`` although a bug-report
  (and fix) had been available a long time.

- If you want to set an attribute, e.g. to control whether literal
  block style scalars are allowed to have trailing spaces on a line
  instead of being dumped as double quoted scalars, you have to change
  the ``dump()`` family of routines, all of the ``Dumpers()`` as well
  as the actual functionality change in `emitter.Emitter()`. The
  functionality change takes changing 4 (four!) lines in one file, and being able
  to enable that another 50+ line changes (non-contiguous) in 3 more files resulting
  in diff that is far over 200 lines long.

- replacing libyaml with something that doesn't both support `0o52`
  and `052` for the integer ``42`` (instead of ``52`` as per YAML 1.2)
  is difficult


With ``ruamel.yaml>=0.15.0`` the various steps "know" about the
``YAML`` instance and can pick up setting, as well as report back
information via that instance. Representers, etc., are added to a
reusable instance and different YAML instances can co-exists.

This change eases development and helps prevent regressions.
