import pytest
from src.DAVE.helpers.code_error_extract import get_code_error

def test_get_code_error_valid_code():
    code = "print('Hello, World!')\nprint('Goodbye, World!')"
    try:
        exec(code)
    except Exception:
        error_message = get_code_error(code)
        assert "An error occurred on line" in error_message

def test_get_code_error_syntax_error():
    code = "print('Hello, World!'\nprint('Goodbye, World!')"
    try:
        exec(code)
    except SyntaxError:
        error_message = get_code_error(code)
        assert "An error occurred on line 1" in error_message

def test_get_code_error_runtime_error():
    code = "print('Hello, World!')\n1 / 0\nprint('Goodbye, World!')"
    try:
        exec(code)
    except ZeroDivisionError:
        error_message = get_code_error(code)
        assert "An error occurred on line" in error_message
        assert "1 / 0" in error_message

def test_get_code_error_no_error():
    code = "print('Hello, World!')\nprint('Goodbye, World!')"
    error_message = get_code_error(code)
    assert error_message == "No error occurred"

