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

----

YAML handcrafted anchors and references as well as key merging
are preserved. The merged keys can transparently be accessed
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

----

The ``CommentedMap``, which is the ``dict`` like construct one gets when round-trip loading,
supports insertion of a key into a particular position, while optionally adding a comment::

  yaml_str = """\
  first_name: Art
  occupation: Architect  # This is an occupation comment
  about: Art Vandelay is a fictional character that George invents...
  """

  data = ruamel.yaml.round_trip_load(yaml_str)
  data.insert(1, 'last name', 'Vandelay', comment="new key")
  print(ruamel.yaml.round_trip_dump(data))

gives::

  first_name: Art
  last name: Vandelay    # new key
  occupation: Architect  # This is an occupation comment
  about: Art Vandelay is a fictional character that George invents...

Please note that the comment is aligned with that of its neighbour (if available).

The above was inspired by a `question <http://stackoverflow.com/a/36970608/1307905>`_
posted by *demux* on StackOverflow.


