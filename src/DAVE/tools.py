import numbers
from DAVE.scene import *

def assert1f(var, name = "Variable"):
    if not isinstance(var, numbers.Number):
        raise ValueError(name + " should be a number but {} is not a number.".format(var[i]))

def assert3f(var, name = "Variable"):
    """Asserts that variable has length three and contains only numbers"""
    assert len(var) == 3, name + " should have length 3 but has length {}".format(len(var))
    for i in range(3):
        if not isinstance(var[i], numbers.Number):
            raise ValueError(name + " should contain three numbers but {} is not a number.".format(var[i]))

def assert6f(var, name = "Variable"):
    """Asserts that variable has length six and contains only numbers"""
    assert len(var) == 6, name + " should have length 6 but has length {}".format(len(var))
    for i in range(6):
        if not isinstance(var[i], numbers.Number):
            raise ValueError(name + " should contain six numbers but {} is not a number.".format(var[i]))

def assertPoi(var, name = "Node"):
    if isinstance(var, Poi):
        return
    else:
        raise ValueError(name + " be of type Poi but is a ".format(type(var)))