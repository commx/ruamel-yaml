Examples
========

Basic round trip of parsing YAML to Python objects, modifying
and generating YAML::

  from __future__ import print_function

  import ruamel.yaml

  inp = """\
  # example
  name:
    # details
    family: Smith   # very common
    given: Alice    # one of the siblings
  """

  code = ruamel.yaml.load(inp, ruamel.yaml.RoundTripLoader)
  code['name']['given'] = 'Bob'

  print(ruamel.yaml.dump(code, Dumper=ruamel.yaml.RoundTripDumper), end='')

.. example code small.py

Resulting in ::

  # example
  name:
    # details
    family: Smith   # very common
    given: Bob      # one of the siblings


.. example output small.py


YAML handcrafted anchors and references as well as key merging
is preserved. The merged keys can transparently be accessed
using ``[]`` and ``.get()``::

  import ruamel.yaml

  inp = """\
  - &CENTER {x: 1, y: 2}
  - &LEFT {x: 0, y: 2}
  - &BIG {r: 10}
  - &SMALL {r: 1}
  # All the following maps are equal:
  # Explicit keys
  - x: 1
    y: 2
    r: 10
    label: center/big
  # Merge one map
  - <<: *CENTER
    r: 10
    label: center/big
  # Merge multiple maps
  - <<: [*CENTER, *BIG]
    label: center/big
  # Override
  - <<: [*BIG, *LEFT, *SMALL]
    x: 1
    label: center/big
  """

  data = ruamel.yaml.load(inp, ruamel.yaml.RoundTripLoader)
  assert data[7]['y'] == 2


.. example code anchor_merge.py

