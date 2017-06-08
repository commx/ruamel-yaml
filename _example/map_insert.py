import sys
from ruamel.yaml import YAML

yaml_str = """\
first_name: Art
occupation: Architect  # This is an occupation comment
about: Art Vandelay is a fictional character that George invents...
"""

yaml = YAML()
data = yaml.load(yaml_str)
data.insert(1, 'last name', 'Vandelay', comment="new key")
yaml.dump(data, sys.stdout)
