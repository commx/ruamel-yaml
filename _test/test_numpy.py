# coding: utf-8

#  try:
#      import numpy
#  except:  # NOQA
#      numpy = None


#  def Xtest_numpy() -> None:
#      import ruamel.yaml
#
#      if numpy is None:
#          return
#      data = numpy.arange(10)
#      print('data', type(data), data)
#
#      buf = io.BytesIO()
#      ruamel.yaml.dump(data)  # needs updating to use buffer
#      yaml_str = buf.getvalue().decode('utf-8')
#      datb = ruamel.yaml.load(yaml_str)
#      print('datb', type(datb), datb)
#
#      print('\nYAML', yaml_str)
#      assert data == datb
