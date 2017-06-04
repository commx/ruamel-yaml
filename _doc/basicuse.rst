Basic Usage
===========

*This is the new (0.15+) interface for ``ruamel.yaml``, it is still in
the process of being fleshed out*. Please pin your dependency to
``ruamel.yaml<0.15`` for production software.

------

You load a YAML document using::

   from ruamel.yaml import YAML

   yaml=YAML(typ='safe')   # default if not specfied is round-trip

   yaml.load(doc)

in this ``doc`` can be a file pointer (i.e. an object that has the
`.read()` method, a string or a ``pathlib.Path()``. `typ='safe'`
accomplishes the same as what ``safe_load()`` did before: loading of a
document without resolving unknow tags.

Dumping works in the same way::

   from ruamel.yaml import YAML

   yaml=YAML()
   yaml.default_flow_style = False
   yaml.dump({a: [1, 2], s)

in this ``s`` can be a file pointer (i.e. an object that has the
`.write()` method, a ``pathlib.Path()`` or ``None`` (the default, which causes the
YAML documented to be returned as a string.

*If you have `yaml.dump()`
return the YAML doc as string, do not just ``print`` that returned
value*. In that case use `yaml.dump(data, sys.stdout)`, which is more
efficient (and shows that you know what you are doing).

More examples
-------------

Using the C based SafeLoader (at this time is inherited from
libyaml/PyYAML and e.g. loads ``0o52`` as well as ``052`` load as integer ``42``)::

   from ruamel.yaml import YAML

   yaml=YAML(typ="safe")
   yaml.load("""a:\n  b: 2\n  c: 3\n""")

Using the Python based SafeLoader (YAML 1.2 support, ``052`` loads as ``52``)::

   from ruamel.yaml import YAML

   yaml=YAML(typ="safe", pure=True)
   yaml.load("""a:\n  b: 2\n  c: 3\n""")
