import os
import tempfile
import warnings

from DAVE import *
from DAVE.gui import Gui


def make_temp_component(filename):
    s = Scene()

    f = s.new_frame(name='Frame')
    s.new_tank(name='Tank', parent='Frame').trimesh.load_file('res: cube.obj')

    s.save_scene(filename)

def make_temp_component_no_tank(filename):
    s = Scene()

    f = s.new_frame(name='Frame')

    s.save_scene(filename)

def model(filename):
    s = Scene()

    make_temp_component(filename)
    s.new_component("component", path = filename)

    return s

def test_copied():
    filename = tempfile.mktemp(suffix='.dave')

    s = model(filename)

    s['component/Tank'].fill_pct = 50

    s2 = s.copy()

    os.remove(filename)
    assert s['component/Tank'].fill_pct == 50
    assert s2['component/Tank'].fill_pct == 50

def test_copy_does_not_fail_when_component_has_changed():
    filename = tempfile.mktemp(suffix='.dave')

    s = model(filename)

    s['component/Tank'].fill_pct = 50

    make_temp_component_no_tank(filename) # now the component has changed, the tank is no longer present

    s2 = s.copy()  # should not fail




if __name__ == '__main__':
    filename = tempfile.mktemp(suffix='.dave')

    s = model(filename)

    s['component/Tank'].fill_pct = 50

    PV = s['component/Tank'].unmanaged_property_values()
    n = s['component/Tank']
    cde = f'\nPV["{n.name}"] = {PV}'

    PV = {'component/Tank': PV}

    for k, pv in PV.items():
        try:
            node = s[k]
            for p,v in pv:
                setattr(node, p,v)
        except:
            pass # perfectly valid, the node is not present in the scene anymore or had changed type


    print(cde)

    # s2 = s.copy()
    #
    # os.remove(filename)
    # assert s['component/Tank'].fill_pct == 50
    # assert s2['component/Tank'].fill_pct == 50
    #
    # Gui(s2, block=True, autosave_enabled=False)

