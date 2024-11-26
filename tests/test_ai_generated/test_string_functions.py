import pytest
from src.DAVE.helpers.string_functions import increment_string_end, code_to_blocks

def test_increment_string_end_with_number():
    result = increment_string_end("file123")
    assert result == "file124"

def test_increment_string_end_without_number():
    result = increment_string_end("file")
    assert result == "file2"

def test_increment_string_end_with_leading_zeros():
    result = increment_string_end("file001")
    assert result == "file002"

def test_code_to_blocks_single_block():
    result = code_to_blocks("print('Hello, World!')")
    assert result == ["print('Hello, World!')"]

def test_code_to_blocks_multiple_blocks():
    result = code_to_blocks("print('Hello')\n\nprint('World')")
    assert result == ["print('Hello')", "print('World')"]

def test_code_to_blocks_with_indentation():
    result = code_to_blocks("def foo():\n    print('Hello')\n\nprint('World')")
    assert result == ["def foo():\n    print('Hello')", "print('World')"]

def test_code_to_blocks_with_brackets():
    result = code_to_blocks("a = [1, 2, 3,\n4, 5, 6]\n\nprint('Done')")
    assert result == ["a = [1, 2, 3,\n4, 5, 6]", "print('Done')"]

def test_code_to_blocks_with_triple_quotes():
    result = code_to_blocks('"""\nThis is a docstring\n"""\n\nprint("Done")')
    assert result == ['"""\nThis is a docstring\n"""', 'print("Done")']

