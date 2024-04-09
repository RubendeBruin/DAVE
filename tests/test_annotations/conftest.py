import pytest
from DAVE import Scene


@pytest.fixture
def model():

    s = Scene()

    for i in range(5):
        s.new_point(f"point_{i}", position = (i, 0, 0))

    return s

@pytest.fixture
def cable():
    s = Scene()
    p1 = s.new_point("p1", position = (0, 0, 0))
    p2 = s.new_point("p2", position = (1, 0, 10))
    s.new_cable("cable", p1, p2)

    return s