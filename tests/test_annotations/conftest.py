import pytest
from DAVE import Scene


@pytest.fixture
def model():

    s = Scene()

    for i in range(5):
        s.new_point(f"point_{i}", position = (i, 0, 0))

    return s

