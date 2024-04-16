"""Reproduce:

make a component
load the component
add a tag
save
open component
remove the tagged node
try to re-load the saved file
Proposed solution:

tags are not critical, place in try/ignore"""
import tempfile
from DAVE import *


def test_issue156():

    # get a temporary folder
    folder = tempfile.mkdtemp()
    component_file = folder + "/component.dave"

    c = Scene()
    c.new_point("p1")

    c.save_scene(component_file)

    s = Scene()
    s.new_component("c1", component_file)

    # add tag to point
    s["c1/p1"].add_tag("tag1")
    s["c1/p1"].color = (1,2,3)
    s2 = s.copy() # should work

    # check that the tag is still there
    assert s2["c1/p1"].has_tag("tag1")
    assert s2["c1/p1"].color == (1,2,3)

    # remove the point from the component
    c.clear()
    c.save_scene(component_file)

    s3 = s.copy() # should work, even though the point is missing

    # check that the point is not there
    assert s3.name_available("c1/p1")



