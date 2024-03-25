from DAVE.visual_helpers.vtkActorMakers import Mesh
from DAVE.visual_helpers.vtkHelpers import add_lid_to_open_mesh, vtkShow


def test_add_lid():
    # Create a vtkActorMaker object
    vertices = [[0, 0, 0], [1, 0, 1], [0, 1, 1], [0,0,1]]
    faces = [[0, 1, 2], [0, 2, 3], [0, 3, 1]]


    add_lid_to_open_mesh(vertices, faces)

    assert faces[-1] == [4, 6, 5]   # other values can also be ok if alogrithm has changed

    # print(faces)
    #
    # actor = Mesh(vertices, faces)
    # vtkShow(actor)