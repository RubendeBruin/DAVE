import sys

from DAVE import ModelInvalidException
import traceback
from DAVE import *

def test_modelinvalidexception():
    asserted = False
    try:
        try:
            i = 1/0
        except Exception as m:
            raise ModelInvalidException(str(m))

    except ModelInvalidException as m:
        assert str(m) == "division by zero"
        msg = traceback.format_exc()

        print(msg)
        asserted = True

    assert asserted

def test_traceback():

    s = Scene()
    code = 's.new_frame("frame")\ns.new_frame("frame")'  # This code will raise an exception
    try:
        s.run_code(code)
    except Exception as m:
        assert len(m.__notes__) > 0

def test_traceback_syntax_error():

    s = Scene()
    code = 's.new_frame("frame")\ns.new_frame("frame")\n\nSynax error will be raised here'  # This code will raise a SyntaxError

    try:
        s.run_code(code)
    except Exception as m:
        assert len(m.__notes__) >0