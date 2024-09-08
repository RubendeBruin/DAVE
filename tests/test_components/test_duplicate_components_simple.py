from DAVE import *
def test_two_components(test_files):
    s = Scene()
    s.resource_provider.addPath(test_files)
    s.new_component(name="Component")
    s["Component"].path = r"res: inner_component.dave"

    s.new_component(name="Component2")
    s["Component2"].path = r"res: inner_component.dave"

def test_duplicate(test_files):
    s = Scene()
    s.resource_provider.addPath(test_files)
    s.new_component(name="Component")
    s["Component"].path = r"res: inner_component.dave"

    s.duplicate_node("Component")
