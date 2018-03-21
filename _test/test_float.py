# coding: utf-8

from __future__ import print_function, absolute_import, division, unicode_literals

import pytest  # NOQA

from roundtrip import round_trip, dedent, round_trip_load, round_trip_dump  # NOQA
from ruamel.yaml.error import MantissaNoDotYAML1_1Warning

# http://yaml.org/type/int.html is where underscores in integers are defined


class TestFloat:
    def test_round_trip_non_exp(self):
        data = round_trip("""\
        - 1.0
        - 1.00
        - 23.100
        - -1.0
        - -1.00
        - -23.100
        - 42.
        - -42.
        - +42.
        """)
        print(data)
        assert 0.999 < data[0] < 1.001
        assert 0.999 < data[1] < 1.001
        assert 23.099 < data[2] < 23.101
        assert 0.999 < -data[3] < 1.001
        assert 0.999 < -data[4] < 1.001
        assert 23.099 < -data[5] < 23.101
        assert 41.999 < data[6] < 42.001
        assert 41.999 < -data[7] < 42.001
        assert 41.999 < data[8] < 42.001

    def test_round_trip_zeros_0(self):
        data = round_trip("""\
        - 0.
        - +0.
        - -0.
        - 0.0
        - +0.0
        - -0.0
        - 0.00
        - +0.00
        - -0.00
        """)
        print(data)
        for d in data:
            assert -0.00001 < d < 0.00001

    # @pytest.mark.xfail(strict=True)
    def test_round_trip_zeros_1(self):
        # not sure if this should be supported, but it is
        data = round_trip("""\
        - 00.0
        - +00.0
        - -00.0
        """)
        print(data)
        for d in data:
            assert -0.00001 < d < 0.00001

    def Xtest_round_trip_non_exp_trailing_dot(self):
        data = round_trip("""\
        """)
        print(data)

    def test_round_trip_exp_00(self):
        data = round_trip("""\
        - 42e56
        - 42E56
        - 42.0E56
        - +42.0e56
        - 42.0E+056
        - +42.00e+056
        """)
        print(data)
        for d in data:
            assert 41.99e56 < d < 42.01e56

    # @pytest.mark.xfail(strict=True)
    def test_round_trip_exp_00f(self):
        data = round_trip("""\
        - 42.E56
        """)
        print(data)
        for d in data:
            assert 41.99e56 < d < 42.01e56

    def test_round_trip_exp_01(self):
        data = round_trip("""\
        - -42e56
        - -42E56
        - -42.0e56
        - -42.0E+056
        """)
        print(data)
        for d in data:
            assert -41.99e56 > d > -42.01e56

    def test_round_trip_exp_02(self):
        data = round_trip("""\
        - 42e-56
        - 42E-56
        - 42.0E-56
        - +42.0e-56
        - 42.0E-056
        - +42.0e-056
        """)
        print(data)
        for d in data:
            assert 41.99e-56 < d < 42.01e-56

    def test_round_trip_exp_03(self):
        data = round_trip("""\
        - -42e-56
        - -42E-56
        - -42.0e-56
        - -42.0E-056
        """)
        print(data)
        for d in data:
            assert -41.99e-56 > d > -42.01e-56

    def test_round_trip_exp_04(self):
        round_trip("""\
        - 1.2e+34
        - 1.23e+034
        - 1.230e+34
        - 1.023e+34
        - -1.023e+34
        - 250e6
        """)

    def test_round_trip_exp_05(self):
        data = round_trip("""\
        - 3.0517578123e-56
        - 3.0517578123E-56
        - 3.0517578123e-056
        - 3.0517578123E-056
        """)
        print(data)
        for d in data:
            assert 3.0517578122e-56 < d < 3.0517578124e-56
            
    def test_yaml_1_1_no_dot(self):
        with pytest.warns(MantissaNoDotYAML1_1Warning):
            round_trip_load("""\
            %YAML 1.1
            ---
            - 1e6
            """)


class TestCalculations(object):
    def test_mul_00(self):
        # issue 149 reported by jan.brezina@tul.cz
        d = round_trip_load("""\
        - 0.1
        """)
        d[0] *= -1
        x = round_trip_dump(d)
        assert x == '- -0.1\n'
