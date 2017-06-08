from __future__ import print_function

import ruamel.yaml

inp = """\
features:
  show: true
  items:
    - widget: full_width.html  # full width 1
      title: Some Title
      description: >
          Foobar.
      vimeo_id: 20913
      zoom_image: some_url.png
    - widget: 3x_container.html
      items:
          - widget: 3x.html
            title: Some Widget Title
            image: 'foobar.png'
            description: >
                Some Description.
          - widget: 3x.html
            title: Some new title here
            image: ajax_uploads/png1_2.png
            description: >
                Some Description.
"""

code = ruamel.yaml.load(inp, ruamel.yaml.RoundTripLoader)

res = ruamel.yaml.dump(code, Dumper=ruamel.yaml.RoundTripDumper)
print(res, end='')
code2 = ruamel.yaml.load(res, ruamel.yaml.RoundTripLoader)

res2 = ruamel.yaml.dump(code2, Dumper=ruamel.yaml.RoundTripDumper)
assert res == res2

inp = """\
features:
  show: true
  items:
    # full width 1
    - widget: full_width.html
      title: Some Title
      description: >
        Foobar.
      vimeo_id: 20913
      zoom_image: some_url.png

    - widget: 3x_container.html
      items:
          - widget: 3x.html
            title: Some Widget Title
            image: 'foobar.png'
            description: >
                Some Description.

          - widget: 3x.html
            title: Some new title here
            image: ajax_uploads/png1_2.png
            description: >
                Some Description.
"""
