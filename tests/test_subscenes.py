"""Tests for components in components"""

from pathlib import Path
from DAVE import *

def test_nested_components_creates():

    # # create a logger
    # import logging
    # logger = logging.getLogger()
    # logger.setLevel(logging.DEBUG)
    #
    # logging.info("DEMO")

    s = Scene()
    path = Path(__file__).parent / 'files'
    s.add_resources_paths(path)
    s.new_component('outer_component', 'res: outer_component.dave')

    _ = s.get_implicitly_created_nodes()
    assert len(s.get_implicitly_created_nodes()) == 3
    c = s.get_created_by_dict()

    c_outer = s['outer_component']
    c_inner = s['outer_component/inner_component']
    point = s['outer_component/inner_component/p']
    frame = s['outer_component/frame_by_outer_component']

    assert c_inner.creates(point)
    assert not c_outer.creates(point)
    assert c_outer.creates(frame)

    s = s.copy()

    c_outer = s['outer_component']
    c_inner = s['outer_component/inner_component']
    point = s['outer_component/inner_component/p']
    frame = s['outer_component/frame_by_outer_component']

    assert c_inner.creates(point)
    assert not c_outer.creates(point)
    assert c_outer.creates(frame)