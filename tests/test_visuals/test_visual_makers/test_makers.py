import DAVE.visual_helpers.vtkActorMakers as make
from DAVE.settings_visuals import TEXTURE_SEA
from DAVE.visual_helpers.vtkHelpers import update_line_to_points, ApplyTexture


def test_mesh():
    # Create a vtkActorMaker object
    vertices = [[0, 0, 0], [1, 0, 0], [0, 1, 0]]
    faces = [[0, 1, 2]]

    actor = make.Mesh(vertices, faces)

def test_dummy():
    actor = make.Dummy()

def test_cube():
    actor = make.Cube()

def test_sphere():
    actor = make.Sphere()

def test_from_file(resource_path):
    print(resource_path)
    actor = make.vp_actor_from_file(resource_path / "cylinder 1x1x1.obj")

def test_line():
    vertices = [[0, 0, 0], [1, 0, 0], [0, 1, 0]]
    actor = make.Line(vertices)
    update_line_to_points(actor, [[0, 0, 0], [1, -1, 1], [2, 2, 2], [1, 5, -2]])

def test_line_update():
    vertices = [[0, 0, 0], [1, 0, 0], [0, 1, 0]]

    actor = make.Line(points = vertices, lw=4)
    update_line_to_points(actor, [[0, 0, 0], [1, -1, 1], [2, 2, 2], [1, 5, -2]])  # numer of points changed
    update_line_to_points(actor, [[0, 0, 0], [1, 1, 1], [2, 2, 2], [5, 5, 5]]) # numer of points changed


def test_plane_with_texture():
    actor = make.PlaneXY(size=20)
    ApplyTexture(actor, TEXTURE_SEA)

def test_arrow():
    actor = make.Arrow()
