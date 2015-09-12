

def test_load_cyaml():
    import ruamel.yaml
    assert ruamel.yaml.__with_libyaml__
    from ruamel.yaml.cyaml import CLoader
    ruamel.yaml.load("abc: 1", Loader=CLoader)
