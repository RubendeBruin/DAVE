from DAVE import *
from DAVE import DAVE_ADDITIONAL_RUNTIME_MODULES
from DAVE.nds.abstracts import NodeSingleton


class DummySingleton(NodeSingleton):

    def __init__(self, scene, name):
        super().__init__(scene=scene, name=name)
        self.a = 1
        self.b = 2

    def give_python_code(self):
        return f'DummySingleton(scene=s, name = "{self.name}")'

DAVE_ADDITIONAL_RUNTIME_MODULES['DummySingleton'] = DummySingleton

def test_overwrire_singleton():

    s = Scene()
    sn = DummySingleton(scene=s, name = 'DummySingleton')

    sn2 = DummySingleton(scene=s, name = 'DummySingleton2')

    assert sn not in s._nodes
    assert sn2 in s._nodes


def test_can_copy():
    s = Scene()
    DummySingleton(scene=s, name = 'DummySingleton')

    s2 = s.copy()
    assert s2.node_exists("DummySingleton")
    assert s.node_exists("DummySingleton")

def test_not_imported_when_exists():

    # create a temporary folder
    import tempfile
    temp_folder = tempfile.mkdtemp()
    component_name = temp_folder + "/test.dave"


    s = Scene()
    sn = DummySingleton(scene=s, name = 'DummySingleton')
    s.save_scene(component_name)

    s2 = Scene(component_name)
    assert s2.node_exists("DummySingleton")

    sn.name = "Original"
    s.new_component("component", path = component_name)

    assert s.node_exists("Original")
    assert not s.node_exists("DummySingleton")

def test_imported_when_not_exists():

    # create a temporary folder
    import tempfile
    temp_folder = tempfile.mkdtemp()
    component_name = temp_folder + "/test.dave"


    s = Scene()
    sn = DummySingleton(scene=s, name = 'DummySingleton')
    s.save_scene(component_name)

    s = Scene()

    assert not s.node_exists("DummySingleton")

    s.new_component("component", path = component_name)

    assert s.node_exists("component/DummySingleton")
    assert s.nodes_where(kind = DummySingleton)
