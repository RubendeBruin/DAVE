import pytest
from DAVE import *

def test_node_name_available():

    s = Scene()
    s.new_frame(name = 'Frame' )
    s.new_visual(name = 'Visual' , parent = 'Frame', path = 'res: cube_with_bevel.obj')

    with pytest.raises(ValueError):
        s._verify_name_available('Visual')

    with pytest.raises(ValueError):
        s._verify_name_available('Frame')

def test_node_rename_visual():

    s = Scene()
    s.new_frame(name = 'Frame' )
    s.new_visual(name = 'Visual' , parent = 'Frame', path = 'res: cube_with_bevel.obj')

    with pytest.raises(Exception):
        s['Visual'].name = "Frame"


def test_node_rename_point():
    s = Scene()
    s.new_frame(name='Frame')
    s.new_point(name='Visual', parent='Frame')

    with pytest.raises(Exception):
        s['Visual'].name = "Frame"

