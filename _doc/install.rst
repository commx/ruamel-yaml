Installing
==========

``ruamel.yaml`` can be installed from PyPI_ using::

    pip install ruamel.yaml

There is a a commandline utility ``yaml`` available after installing::

   pip install ruamel.yaml.cmd

that allows for round-trip testing/re-indenting and conversion of YAML
files (JSON,INI,HTML tables)

Optional requirements
---------------------

If you have the C yaml library and headers installed, as well as
the header files for your Python executables then you can use the
non-roundtrip but faster C loader and emitter.

On Debian systems you should use::

    sudo apt-get install libyaml-dev python-dev python3-dev

you can leave out ``python3-dev`` if you don't use python3

For CentOS (7) based systems you should do::

   sudo yum install libyaml-devel python-devel

