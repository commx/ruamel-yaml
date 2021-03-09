
import ruamel.yaml
YAML = ruamel.yaml.YAML

import test_emitter
import warnings

warnings.simplefilter('ignore', ruamel.yaml.error.UnsafeLoaderWarning)


def test_loader_error(error_filename, verbose=False):
    yaml = YAML(typ='safe', pure=True)
    try:
        with open(error_filename, 'rb') as fp0:
            list(yaml.load_all(fp0))
    except yaml.YAMLError as exc:
        if verbose:
            print('%s:' % exc.__class__.__name__, exc)
    else:
        raise AssertionError('expected an exception')


test_loader_error.unittest = ['.loader-error']


def test_loader_error_string(error_filename, verbose=False):
    yaml = YAML(typ='safe', pure=True)
    try:
        with open(error_filename, 'rb') as fp0:
            list(yaml.load_all(fp0.read()))
    except yaml.YAMLError as exc:
        if verbose:
            print('%s:' % exc.__class__.__name__, exc)
    else:
        raise AssertionError('expected an exception')


test_loader_error_string.unittest = ['.loader-error']


def test_loader_error_single(error_filename, verbose=False):
    yaml = YAML(typ='safe', pure=True)
    try:
        with open(error_filename, 'rb') as fp0:
            yaml.load(fp0.read())
    except yaml.YAMLError as exc:
        if verbose:
            print('%s:' % exc.__class__.__name__, exc)
    else:
        raise AssertionError('expected an exception')


test_loader_error_single.unittest = ['.single-loader-error']


def test_emitter_error(error_filename, verbose=False):
    yaml = YAML(typ='safe', pure=True)
    with open(error_filename, 'rb') as fp0:
        events = list(yaml.load(fp0, Loader=test_emitter.EventsLoader))
    try:
        ruamel.yaml.emit(events)
    except yaml.YAMLError as exc:
        if verbose:
            print('%s:' % exc.__class__.__name__, exc)
    else:
        raise AssertionError('expected an exception')


test_emitter_error.unittest = ['.emitter-error']


def test_dumper_error(error_filename, verbose=False):
    yaml = YAML(typ='safe', pure=True)
    with open(error_filename, 'rb') as fp0:
        code = fp0.read()
    try:
        import yaml

        exec(code)
    except yaml.YAMLError as exc:
        if verbose:
            print('%s:' % exc.__class__.__name__, exc)
    else:
        raise AssertionError('expected an exception')


test_dumper_error.unittest = ['.dumper-error']

if __name__ == '__main__':
    import test_appliance

    test_appliance.run(globals())
