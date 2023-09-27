"""
Make a component with a body
All dofs free
New scene
Add component
Solve
Save
Change body in component such that some of the dofs are now fixed
reload --> fail: can not set dofs of a managed node
"""

from DAVE import *

def test_apply_to_changed_model(tmp_path):
    component_path = tmp_path / "component.dave"
    model_path = tmp_path / "model.dave"

    # make a component
    s = Scene()
    s.new_rigidbody("body", mass=1, fixed=False)
    s.save_scene(component_path)

    s = Scene()
    s.new_component("component", path=component_path)
    s.new_point("p1", position=(0, 0, 0), parent="component/body")
    s.new_point("p2", position=(1, 0, 1))
    s.new_cable("cable", connections=["p1", "p2"], EA=1000, length=10)

    # save
    s.save_scene(model_path)

    # reload component
    s = Scene(component_path)
    s["body"].fixed = True
    s.save_scene(component_path)

    s = Scene(model_path)


def test_apply_to_changed_model(tmp_path):
    component_path = tmp_path / "component.dave"
    model_path = tmp_path / "model.dave"

    # make a component
    s = Scene()
    s.new_rigidbody("body", mass=1, fixed=False)
    s.save_scene(component_path)

    s = Scene()
    s.new_component("component", path=component_path)
    s.new_point("p1", position=(0, 0, 0), parent="component/body")
    s.new_point("p2", position=(1, 0, 1))
    s.new_cable("cable", connections=["p1", "p2"], EA=1000, length=10)

    s.solve_statics()

    # save
    s.save_scene(model_path)

    s.print_python_code()

    # reload component
    s2 = Scene(model_path)
    assert s["component/body"].x != 0
    assert s2['component/body'].x == s['component/body'].x
