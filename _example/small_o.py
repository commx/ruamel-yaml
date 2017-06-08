from __future__ import print_function

import sys
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

ruamel.yaml.dump(code, sys.stdout, Dumper=ruamel.yaml.RoundTripDumper)

# the last statement can be done less efficient in time and memory with
# leaving out the end='' would cause a double newline at the end
# print(ruamel.yaml.dump(code, Dumper=ruamel.yaml.RoundTripDumper), end='')
