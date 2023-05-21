import pytest
from DAVE import *

class NotAllowed(Manager):
    def __init__(self, scene, name):
        super().__init__(scene, name)

    def creates(self, node):
        pass

    def delete(self):
        pass

    def name(self):
        pass


def test_not_allowed():
    s = Scene()

    with pytest.raises(AssertionError):
        na = NotAllowed(s, 'na')