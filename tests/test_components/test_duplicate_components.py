from DAVE import *


def test_load_more_complex_component(test_files):
    s = Scene()
    s.resource_provider.addPath(test_files)
    s.new_component(name="Component")
    s["Component"].path = r"res: complex_component.dave"

def test_import_and_prefix(test_files):
    s = Scene()
    s.resource_provider.addPath(test_files)
    s.import_scene("res: complex_component.dave")

    s.prefix_element_names("PF/")

    s.print_node_tree()
    assert "Shackle" not in s.node_names

def test_import_and_prefix2(test_files):
    s = Scene()
    s.resource_provider.addPath(test_files)
    s.import_scene("res: complex_component.dave", prefix="PF/")
    s.print_node_tree()
    assert "Shackle" not in s.node_names

def test_complex_component_names(test_files):
    s = Scene()
    s.resource_provider.addPath(test_files)
    s.new_component(name="Component")
    s["Component"].path = r"res: complex_component.dave"

    s.print_node_tree()
    assert "Shackle" not in s.node_names


def test_load_two_components(test_files):
    s = Scene()
    s.resource_provider.addPath(test_files)
    s.new_component(name="Component")
    s["Component"].path = r"res: complex_component.dave"

    s.new_component(name="Component2")
    s["Component2"].path = r"res: complex_component.dave"

def test_duplicate(test_files):
    s = Scene()
    s.resource_provider.addPath(test_files)
    s.new_component(name="Component")
    s["Component"].path = r"res: complex_component.dave"

    s.duplicate_node("Component")
