
import sys  # NOQA
import ruamel.yaml
import test_appliance


def main(args=None):
    collections = []
    import test_yaml

    collections.append(test_yaml)
    if ruamel.yaml.__with_libyaml__:
        import test_yaml_ext

        collections.append(test_yaml_ext)
    test_appliance.run(collections, args)


if __name__ == '__main__':
    main()
