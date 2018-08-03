from __future__ import absolute_import
from __future__ import print_function

import ruamel.yaml as yaml
import codecs
import tempfile
import os
import os.path
from ruamel.yaml.compat import PY2, PY3, StringIO, BytesIO

if PY2:

    def _unicode_open(file, encoding, errors='strict'):
        info = codecs.lookup(encoding)
        if isinstance(info, tuple):
            reader = info[2]
            writer = info[3]
        else:
            reader = info.streamreader
            writer = info.streamwriter
        srw = codecs.StreamReaderWriter(file, reader, writer, errors)
        srw.encoding = encoding
        return srw


if PY3:

    def test_unicode_input(unicode_filename, verbose=False):
        with open(unicode_filename, 'rb') as fp:
            data = fp.read().decode('utf-8')
        value = ' '.join(data.split())
        output = yaml.load(data)
        assert output == value, (output, value)
        output = yaml.load(StringIO(data))
        assert output == value, (output, value)
        for input in [
            data.encode('utf-8'),
            codecs.BOM_UTF8 + data.encode('utf-8'),
            codecs.BOM_UTF16_BE + data.encode('utf-16-be'),
            codecs.BOM_UTF16_LE + data.encode('utf-16-le'),
        ]:
            if verbose:
                print('INPUT:', repr(input[:10]), '...')
            output = yaml.load(input)
            assert output == value, (output, value)
            output = yaml.load(BytesIO(input))
            assert output == value, (output, value)


else:

    def test_unicode_input(unicode_filename, verbose=False):
        with open(unicode_filename, 'rb') as fp:
            data = fp.read().decode('utf-8')
        value = ' '.join(data.split())
        output = yaml.load(_unicode_open(StringIO(data.encode('utf-8')), 'utf-8'))
        assert output == value, (output, value)
        for input in [
            data,
            data.encode('utf-8'),
            codecs.BOM_UTF8 + data.encode('utf-8'),
            codecs.BOM_UTF16_BE + data.encode('utf-16-be'),
            codecs.BOM_UTF16_LE + data.encode('utf-16-le'),
        ]:
            if verbose:
                print('INPUT:', repr(input[:10]), '...')
            output = yaml.load(input)
            assert output == value, (output, value)
            output = yaml.load(StringIO(input))
            assert output == value, (output, value)


test_unicode_input.unittest = ['.unicode']


def test_unicode_input_errors(unicode_filename, verbose=False):
    with open(unicode_filename, 'rb') as fp:
        data = fp.read().decode('utf-8')
    for input in [
        data.encode('latin1', 'ignore'),
        data.encode('utf-16-be'),
        data.encode('utf-16-le'),
        codecs.BOM_UTF8 + data.encode('utf-16-be'),
        codecs.BOM_UTF16_BE + data.encode('utf-16-le'),
        codecs.BOM_UTF16_LE + data.encode('utf-8') + b'!',
    ]:
        try:
            yaml.load(input)
        except yaml.YAMLError as exc:
            if verbose:
                print(exc)
        else:
            raise AssertionError('expected an exception')
        try:
            yaml.load(BytesIO(input) if PY3 else StringIO(input))
        except yaml.YAMLError as exc:
            if verbose:
                print(exc)
        else:
            raise AssertionError('expected an exception')


test_unicode_input_errors.unittest = ['.unicode']

if PY3:

    def test_unicode_output(unicode_filename, verbose=False):
        with open(unicode_filename, 'rb') as fp:
            data = fp.read().decode('utf-8')
        value = ' '.join(data.split())
        for allow_unicode in [False, True]:
            data1 = yaml.dump(value, allow_unicode=allow_unicode)
            for encoding in [None, 'utf-8', 'utf-16-be', 'utf-16-le']:
                stream = StringIO()
                yaml.dump(value, stream, encoding=encoding, allow_unicode=allow_unicode)
                data2 = stream.getvalue()
                data3 = yaml.dump(value, encoding=encoding, allow_unicode=allow_unicode)
                if encoding is not None:
                    assert isinstance(data3, bytes)
                    data3 = data3.decode(encoding)
                stream = BytesIO()
                if encoding is None:
                    try:
                        yaml.dump(
                            value, stream, encoding=encoding, allow_unicode=allow_unicode
                        )
                    except TypeError as exc:
                        if verbose:
                            print(exc)
                        data4 = None
                    else:
                        raise AssertionError('expected an exception')
                else:
                    yaml.dump(value, stream, encoding=encoding, allow_unicode=allow_unicode)
                    data4 = stream.getvalue()
                    if verbose:
                        print('BYTES:', data4[:50])
                    data4 = data4.decode(encoding)
                for copy in [data1, data2, data3, data4]:
                    if copy is None:
                        continue
                    assert isinstance(copy, str)
                    if allow_unicode:
                        try:
                            copy[4:].encode('ascii')
                        except UnicodeEncodeError as exc:
                            if verbose:
                                print(exc)
                        else:
                            raise AssertionError('expected an exception')
                    else:
                        copy[4:].encode('ascii')
                assert isinstance(data1, str), (type(data1), encoding)
                assert isinstance(data2, str), (type(data2), encoding)


else:

    def test_unicode_output(unicode_filename, verbose=False):
        with open(unicode_filename, 'rb') as fp:
            data = fp.read().decode('utf-8')
        value = ' '.join(data.split())
        for allow_unicode in [False, True]:
            data1 = yaml.dump(value, allow_unicode=allow_unicode)
            for encoding in [None, 'utf-8', 'utf-16-be', 'utf-16-le']:
                stream = StringIO()
                yaml.dump(
                    value,
                    _unicode_open(stream, 'utf-8'),
                    encoding=encoding,
                    allow_unicode=allow_unicode,
                )
                data2 = stream.getvalue()
                data3 = yaml.dump(value, encoding=encoding, allow_unicode=allow_unicode)
                stream = StringIO()
                yaml.dump(value, stream, encoding=encoding, allow_unicode=allow_unicode)
                data4 = stream.getvalue()
                for copy in [data1, data2, data3, data4]:
                    if allow_unicode:
                        try:
                            copy[4:].encode('ascii')
                        except (UnicodeDecodeError, UnicodeEncodeError) as exc:
                            if verbose:
                                print(exc)
                        else:
                            raise AssertionError('expected an exception')
                    else:
                        copy[4:].encode('ascii')
                assert isinstance(data1, str), (type(data1), encoding)
                data1.decode('utf-8')
                assert isinstance(data2, str), (type(data2), encoding)
                data2.decode('utf-8')
                if encoding is None:
                    assert isinstance(data3, unicode), (type(data3), encoding)  # NOQA
                    assert isinstance(data4, unicode), (type(data4), encoding)  # NOQA
                else:
                    assert isinstance(data3, str), (type(data3), encoding)
                    data3.decode(encoding)
                    assert isinstance(data4, str), (type(data4), encoding)
                    data4.decode(encoding)


test_unicode_output.unittest = ['.unicode']


def test_file_output(unicode_filename, verbose=False):
    with open(unicode_filename, 'rb') as fp:
        data = fp.read().decode('utf-8')
    handle, filename = tempfile.mkstemp()
    os.close(handle)
    try:
        stream = StringIO()
        yaml.dump(data, stream, allow_unicode=True)
        data1 = stream.getvalue()
        if PY3:
            stream = BytesIO()
            yaml.dump(data, stream, encoding='utf-16-le', allow_unicode=True)
            data2 = stream.getvalue().decode('utf-16-le')[1:]
            with open(filename, 'w', encoding='utf-16-le') as stream:
                yaml.dump(data, stream, allow_unicode=True)
            with open(filename, 'r', encoding='utf-16-le') as fp0:
                data3 = fp0.read()
            with open(filename, 'wb') as stream:
                yaml.dump(data, stream, encoding='utf-8', allow_unicode=True)
            with open(filename, 'r', encoding='utf-8') as fp0:
                data4 = fp0.read()
        else:
            with open(filename, 'wb') as stream:
                yaml.dump(data, stream, allow_unicode=True)
            with open(filename, 'rb') as fp0:
                data2 = fp0.read()
            with open(filename, 'wb') as stream:
                yaml.dump(data, stream, encoding='utf-16-le', allow_unicode=True)
            with open(filename, 'rb') as fp0:
                data3 = fp0.read().decode('utf-16-le')[1:].encode('utf-8')
            stream = _unicode_open(open(filename, 'wb'), 'utf-8')
            yaml.dump(data, stream, allow_unicode=True)
            stream.close()
            with open(filename, 'rb') as fp0:
                data4 = fp0.read()
        assert data1 == data2, (data1, data2)
        assert data1 == data3, (data1, data3)
        assert data1 == data4, (data1, data4)
    finally:
        if os.path.exists(filename):
            os.unlink(filename)


test_file_output.unittest = ['.unicode']


def test_unicode_transfer(unicode_filename, verbose=False):
    with open(unicode_filename, 'rb') as fp:
        data = fp.read().decode('utf-8')
    for encoding in [None, 'utf-8', 'utf-16-be', 'utf-16-le']:
        input = data
        if PY3:
            if encoding is not None:
                input = ('\ufeff' + input).encode(encoding)
            output1 = yaml.emit(yaml.parse(input), allow_unicode=True)
            if encoding is None:
                stream = StringIO()
            else:
                stream = BytesIO()
            yaml.emit(yaml.parse(input), stream, allow_unicode=True)
            output2 = stream.getvalue()
            assert isinstance(output1, str), (type(output1), encoding)
            if encoding is None:
                assert isinstance(output2, str), (type(output1), encoding)
            else:
                assert isinstance(output2, bytes), (type(output1), encoding)
                output2.decode(encoding)
        else:
            if encoding is not None:
                input = (u'\ufeff' + input).encode(encoding)
            output1 = yaml.emit(yaml.parse(input), allow_unicode=True)
            stream = StringIO()
            yaml.emit(yaml.parse(input), _unicode_open(stream, 'utf-8'), allow_unicode=True)
            output2 = stream.getvalue()
            if encoding is None:
                assert isinstance(output1, unicode), (type(output1), encoding)  # NOQA
            else:
                assert isinstance(output1, str), (type(output1), encoding)
                output1.decode(encoding)
            assert isinstance(output2, str), (type(output2), encoding)
            output2.decode('utf-8')


test_unicode_transfer.unittest = ['.unicode']

if __name__ == '__main__':
    import test_appliance

    test_appliance.run(globals())
