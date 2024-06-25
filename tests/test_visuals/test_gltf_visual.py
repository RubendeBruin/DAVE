from DAVE import DG, Visual, Scene, Frame
from DAVE.visual_helpers.simple_scene_renderer import SimpleSceneRenderer
from DAVE.visual_helpers.vtkActorMakers import polydata_from_file
from DAVE.visual_helpers.vtkHelpers import PolyDataToSlice
from vtkmodules.vtkCommonDataModel import vtkPolyData


def test_render_gltf():

    s = Scene()
    v = s.new_visual("Visual", path = r"res: koala_hull.glb")
    # v.rotation = (90,0,0)

    # DG(s)
    #
    # renderer = SimpleSceneRenderer(s)
    # renderer.show()

def test_create_polydata_from_gltf():
    s = Scene()

    filename_obj = s.get_resource_path("res: cube.obj")
    data_obj = polydata_from_file(filename_obj)
    assert isinstance(data_obj.GetOutput(), vtkPolyData)


    filename = s.get_resource_path("res: koala_hull.glb")
    data = polydata_from_file(filename)


    assert isinstance(data.GetOutput(), vtkPolyData)
