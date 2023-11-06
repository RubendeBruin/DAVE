from DAVE import *
import pytest
def test_model_invalid_exception():
    with pytest.raises(ModelInvalidException):
        exec("raise ModelInvalidException('something is very wrong')")
