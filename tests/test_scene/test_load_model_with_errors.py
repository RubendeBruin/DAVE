import pytest

from DAVE import Scene
from DAVE.helpers.string_functions import code_to_blocks


def test_code_to_blocks():
    blocks = code_to_blocks('a\n b\n c')
    assert blocks == ['a\n b\n c']


def test_code_to_blocks2():
    blocks = code_to_blocks('a = [1,\n2b\n3]')
    assert blocks == ['a = [1,\n2b\n3]']

def test_code_to_blocks3(test_files):
    blocks = code_to_blocks((test_files / 'block_separation_syntax.py').read_text())

    # for block in blocks:
    #     print('-------------------------------------')
    #     print(block)

    context = {}

    for b in blocks:
        exec(b, {}, context)

    # print(context)

    expect = {'a': 'This is\na multiple line string\n', 'b': '""" This is a string with triple quotes', 'c': 'This string continues on the next line', 'd': (1, 2, 3, [4, 5]), 'i': 5}
    assert context == expect


def test_load_model_with_errors(test_files):

    # this should load with errors
    s = Scene(test_files / 'model_with_errors.dave', allow_errors_during_load =True)

    # check if the frame is loaded
    s['Frame']  # should exist


def test_load_model_with_errors(test_files):

    # this should load with errors
    s = Scene(test_files / 'model_with_errors.dave', allow_errors_during_load =True)

    # check if the frame is loaded
    s['Frame']  # should exist
    s.delete('Frame')

    s.load(test_files / 'basic_nodes.dave')

    assert not s.errors_during_load

def test_load_model_with_errors_do_not_allow_errors(test_files):

    # this should not load with errors
    with pytest.raises(Exception):
        s = Scene(test_files / 'model_with_errors.dave', allow_errors_during_load =False)

