import numpy as np
from DAVE.tools import something_orthogonal_to

def test_something_orthogonal_to():
    x = np.array([1,0,0])
    y = something_orthogonal_to(x)
    assert np.allclose(np.dot(x,y),0)

    x = np.array([0,1,0])
    y = something_orthogonal_to(x)
    assert np.allclose(np.dot(x,y),0)

    x = np.array([0,0,1])
    y = something_orthogonal_to(x)
    assert np.allclose(np.dot(x,y),0)

    x = np.array([1,1,1])
    y = something_orthogonal_to(x)
    assert np.allclose(np.dot(x,y),0)

    x = np.array([0,0,0])
    y = something_orthogonal_to(x)
    assert np.allclose(np.dot(x,y),0)

def test_something_orthogonal_to_randoms():
    np.random.seed(3145621)
    for i in range(100):
        x = np.random.rand(3)
        y = something_orthogonal_to(x)
        assert np.allclose(np.dot(x,y),0)