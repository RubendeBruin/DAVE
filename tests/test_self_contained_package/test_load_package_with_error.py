from DAVE import *

def test_load_with_error(test_files):
    """Test loading a file with an error"""

    s = Scene()
    passed = False
    try:
        s.load(test_files / "package_with_error.dave.zip")

    except Exception as E:
        if "This exception is deliberate" in str(E):
            passed = True

    assert passed, "The error was not raised"