from DAVE import *

def test_component_with_artefact(test_files):
    s = Scene()

    s.new_component(name="Component", path = test_files / "component_with_artefact.dave")

    assert not hasattr(s, "should_not_be_imported")

    s["Component/ShouldBeImported"]  # fails if not imported


