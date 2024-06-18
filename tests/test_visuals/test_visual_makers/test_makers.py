import pytest

import DAVE.visual_helpers.vtkActorMakers as make
from DAVE.settings_visuals import TEXTURE_SEA
from DAVE.visual_helpers.vtkHelpers import update_line_to_points, ApplyTexture, vtkShow, update_vertices, \
    update_mesh_from


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


def test_points_update_on_mesh():
    vertices = [[0, 0, 0], [1, 0, 0], [0, 1, 0]]
    faces = [[0, 1, 2]]
    actor = make.Mesh(vertices, faces)

    update_vertices(actor, vertices)

def test_points_update_on_mesh_reduce():
    """Would expect this to fail, but it doesn't."""
    vertices = [[0, 0, 0], [1, 0, 0], [0, 1, 0]]
    faces = [[0, 1, 2]]
    actor = make.Mesh(vertices, faces)
    actor.GetMapper().Update()

    update_vertices(actor, [(0,0,0)])
    actor.GetMapper().Update()

    # vtkShow(actor)
@pytest.mark.skip(reason="This test is interactive")
def test_cube_to_sphere():
    actor = make.Cube()
    sphere = make.Sphere()
    update_mesh_from(actor, sphere)

    update_vertices(sphere, [(0,0,0)])

    vtkShow(actor)

@pytest.mark.skip(reason="This test is interactive")
def test_plane_with_texture():
    actor = make.PlaneXY(size=20)

    ApplyTexture(actor, TEXTURE_SEA)
    vtkShow(actor)

def test_arrow():
    actor = make.Arrow()

def test_lines():
    line1 = [(0, 0, 0), (1, 0, 0)]
    line2 = [(0, 2, 0), (0, 1, 0)]
    line3 = [(1, 1, 1), (0, 1, 0),(0,4,7)]

    lines = [line1, line2, line3]

    actor = make.Lines(lines)

    # vtkShow(actor)
