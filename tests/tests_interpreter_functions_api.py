import sys
sys.path.insert(0, '/users/mitchellbailey/dmd-interpreter-api')

from interpreter_functions_api import *
from utils.interpreter_helpers import *

import pytest
import csv
from ast import literal_eval


file = open('./tests/test_cases.csv', mode='r', encoding='utf-8-sig')
rows = [x for x in csv.reader(file)]
file.close()

test_dict = {x[0]: x[1:] for x in rows}


@pytest.mark.parametrize("inp, expected",
                         list(zip(test_dict['inp'], test_dict['exin'])))
def test_exInput(inp, expected):
    assert exInput(inp) == bool(int(expected))


@pytest.mark.parametrize("inp, expected",
                         list(zip(test_dict['inp'], test_dict['muttype'])))
def test_getType(inp, expected):
    assert getType(inp) == expected


@pytest.mark.parametrize("inp, expected",
                         list(zip(test_dict['inp'], test_dict['nums'])))
def test_getNums(inp, expected):
    assert getNums(inp) == literal_eval(expected)


@pytest.mark.parametrize("inp, expected",
                         list(zip(test_dict['inp'], test_dict['ref'])))
def test_getNums(inp, expected):
    assert getRef(inp) == expected


@pytest.mark.parametrize("num, ref, expected",
                         [(2795, 'nm_004006.2',
                          {'nm_004006.2': 2795, 'exon': 21,
                           'nc_000023.11': 32484927,
                           'nc_000023.10': 32503044}),
                         (32484927, 'nc_000023.11',
                          {'nm_004006.2': 2795, 'exon': 21,
                           'nc_000023.11': 32484927,
                           'nc_000023.10': 32503044}),
                         (32503044, 'nc_000023.10',
                          {'nm_004006.2': 2795, 'exon': 21,
                           'nc_000023.11': 32484927,
                           'nc_000023.10': 32503044}),
                         (6381, 'nm_004006.2',
                          {'nm_004006.2': 6381, 'exon': 45,
                           'nc_000023.11': 32216973,
                           'nc_000023.10': 32235090}),
                         (32216973, 'nc_000023.11',
                          {'nm_004006.2': 6381, 'exon': 45,
                           'nc_000023.11': 32216973,
                           'nc_000023.10': 32235090})])
def test_convert(num, ref, expected):
    assert convert(num, ref) == expected
