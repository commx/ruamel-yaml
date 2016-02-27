from __future__ import print_function

# import sys
import ruamel.yaml
from ruamel.yaml.comments import CommentedMap

# class MyObj():
#     name = "boby"
#     age = 34
#
# print(ruamel.yaml.dump(MyObj())) # , Dumper=ruamel.yaml.RoundTripDumper), end='')
#
# inp = """\
# boby:       # this is the name
#    age: 34  # in years
# """
#
# print('====', ruamel.yaml.load(inp))
#
#
# data1 = ruamel.yaml.load(inp, Loader=ruamel.yaml.RoundTripLoader)
# print('<<<', data1.ca.items)
# print(ruamel.yaml.dump(data1, Dumper=ruamel.yaml.RoundTripDumper), end='')
#
# print('----------------')


class MyObj():
    name = "boby"
    age = 34

    def convert_to_yaml_struct(self):
        x = CommentedMap()
        a = CommentedMap()
        x[data.name] = a
        x.yaml_add_eol_comment('this is the name', 'boby', 11)
        a['age'] = data.age
        a.yaml_add_eol_comment('in years', 'age', 11)
        print('>>>', x.ca.items)
        return x

    @staticmethod
    def yaml_representer(dumper, data, flow_style=False):
        assert isinstance(dumper, ruamel.yaml.RoundTripDumper)
        return dumper.represent_dict(data.convert_to_yaml_struct())


ruamel.yaml.RoundTripDumper.add_representer(MyObj, MyObj.yaml_representer)

data = MyObj()

print(ruamel.yaml.dump(data, Dumper=ruamel.yaml.RoundTripDumper), end='')
