"""This module contains functions that create vtkActors for visualization purposes.


- vtkArrowActor
- vtkArrowHeadActor

Helpers:

- polyDataFromVerticesAndFaces - creates a vtkPolyData object from vertices and faces

Actor creators:

- vtkActorFromPolyData  # <--- this is always used to create an actor


- Mesh
- vp_actor_from_file

- actor_from_trimesh
- actor_from_vertices_and_faces

- Dummy
- Cube
- Sphere
- PlaneXY
- Arrow
- ArrowHead


"""
import numpy as np

from vtkmodules.util.numpy_support import numpy_to_vtkIdTypeArray, numpy_to_vtk
from vtkmodules.vtkCommonCore import vtkPoints, vtkIdTypeArray
from vtkmodules.vtkCommonDataModel import vtkPolyData, vtkCellArray
from vtkmodules.vtkCommonTransforms import vtkTransform
from vtkmodules.vtkFiltersGeneral import vtkTransformPolyDataFilter
from vtkmodules.vtkFiltersSources import (
    vtkSphereSource,
    vtkPlaneSource,
    vtkRegularPolygonSource,
    vtkCylinderSource,
    vtkConeSource,
    vtkArrowSource,
)
from vtkmodules.vtkIOGeometry import vtkOBJReader, vtkSTLReader
from vtkmodules.vtkRenderingCore import vtkActor, vtkPolyDataMapper

from DAVE.visual_helpers.constants import ACTOR_COLOR, ACTOR_ROUGHESS, ACTOR_METALIC


# VEDO:
def numpy2vtk(arr, dtype=None, deep=True, name=""):
    """
    Convert a numpy array into a `vtkDataArray`.
    Use `dtype='id'` for `vtkIdTypeArray` objects.
    """
    # https://github.com/Kitware/VTK/blob/master/Wrapping/Python/vtkmodules/util/numpy_support.py
    if arr is None:
        return None

    arr = np.ascontiguousarray(arr)

    if dtype == "id":
        varr = numpy_to_vtkIdTypeArray(arr.astype(np.int64), deep=deep)
    elif dtype:
        varr = numpy_to_vtk(arr.astype(dtype), deep=deep)
    else:
        # let numpy_to_vtk() decide what is best type based on arr type
        if arr.dtype == np.bool_:
            arr = arr.astype(np.uint8)
        varr = numpy_to_vtk(arr, deep=deep)

    if name:
        varr.SetName(name)
    return varr


def vtkActorFromPolyData(poly_data) -> vtkActor:
    """Creates a vtkActor from a vtkPolyData object"""
    mapper = vtkPolyDataMapper()
    mapper.SetInputData(poly_data)

    actor = vtkActor()
    actor.SetMapper(mapper)

    prop = actor.GetProperty()

    prop.SetInterpolationToPBR()
    prop.SetColor(ACTOR_COLOR)
    prop.SetMetallic(ACTOR_METALIC)
    prop.SetRoughness(ACTOR_ROUGHESS)

    return actor


def polyDataFromVerticesAndFaces(vertices, faces):
    """Creates a vtkPolyData object from vertices and faces"""
    poly = vtkPolyData()

    source_points = vtkPoints()
    source_points.SetData(numpy2vtk(vertices, dtype=np.float32))
    poly.SetPoints(source_points)

    source_polygons = vtkCellArray()

    faces = np.asarray(faces)

    ast = np.int32
    if vtkIdTypeArray().GetDataTypeSize() != 4:
        ast = np.int64

    if faces.ndim > 1:
        nf, nc = faces.shape
        hs = np.hstack((np.zeros(nf)[:, None] + nc, faces))
    else:
        nf = faces.shape[0]
        hs = faces
    arr = numpy_to_vtkIdTypeArray(hs.astype(ast).ravel(), deep=True)
    source_polygons.SetCells(nf, arr)

    poly.SetPolys(source_polygons)

    return poly


# ========== ACTOR MAKERS ==========


def Mesh(vertices, faces, do_clean=False):
    """creates a vtk Actor from vertices and faces"""

    if do_clean:
        vertices, faces = RemoveDuplicateVertices(vertices, faces)

    poly_data = polyDataFromVerticesAndFaces(vertices, faces)
    return vtkActorFromPolyData(poly_data)


def Dummy():
    """Creates a tiny actor that does nothing"""
    return Mesh([[0, 0, 0]], [], do_clean=False)
    # return vtkActorFromPolyData(almost_empty)


def Cube(side=1):
    """Creates a cube actor with a side length of side"""
    vertices = [
        [0, 0, 0],
        [side, 0, 0],
        [0, side, 0],
        [side, side, 0],
        [0, 0, side],
        [side, 0, side],
        [0, side, side],
        [side, side, side],
    ]
    faces = [
        [0, 1, 3, 2],
        [4, 5, 7, 6],
        [0, 1, 5, 4],
        [2, 3, 7, 6],
        [0, 2, 6, 4],
        [1, 3, 7, 5],
    ]
    return Mesh(vertices, faces)


def Sphere(r=1, res=8):
    source = vtkSphereSource()
    source.SetRadius(r)
    source.SetThetaResolution(res)
    source.SetPhiResolution(res)
    source.Update()

    return vtkActorFromPolyData(source.GetOutput())


def PlaneXY(size=1):
    """Creates a plane actor with a normal vector and a position"""

    source = vtkPlaneSource()
    source.SetOrigin(-size / 2, -size / 2, 0)
    source.SetPoint1(size / 2, -size / 2, 0)
    source.SetPoint2(-size / 2, size / 2, 0)
    source.Update()

    return vtkActorFromPolyData(source.GetOutput())


def actor_from_trimesh(trimesh):
    """Creates a vedo.Mesh from a DAVEcore.TriMesh"""

    if trimesh.nFaces == 0:
        return Dummy

    vertices = [trimesh.GetVertex(i) for i in range(trimesh.nVertices)]
    # are the vertices unique?

    faces = [trimesh.GetFace(i) for i in range(trimesh.nFaces)]

    return Mesh(vertices, faces)


def RemoveDuplicateVertices(vertices, faces):
    """Cleans up the structure by removing duplicate vertices"""

    vertices = np.array(vertices, dtype=float)
    if vertices.ndim > 1:
        unique_vertices = np.unique(vertices, axis=0)
    else:
        unique_vertices = np.unique(vertices)

    if len(unique_vertices) != len(vertices):  # reconstruct faces and vertices
        unique_vertices, indices = np.unique(vertices, axis=0, return_inverse=True)
        f = np.array(faces)
        better_faces = indices[f]
        return unique_vertices, better_faces
    else:
        # no work done
        return vertices, faces


def actor_from_vertices_and_faces(vertices, faces):
    """Creates a mesh based on the given vertices and faces. Cleans up
    the structure before creating by removing duplicate vertices"""

    # TODO: remove this function, it is redundant as Mesh can be used instead like so:

    return Mesh(vertices, faces, do_clean=True)


def polydata_from_file(filename):
    """Creates a vtkPolyData object from a file"""
    # load the data
    filename = str(filename)

    source = None

    if filename.lower().endswith("obj"):
        source = vtkOBJReader()
    elif filename.lower().endswith("stl"):
        source = vtkSTLReader()

    if source is None:
        raise NotImplementedError(
            f"No reader implemented for reading file {filename}. Only .stl and .obj are supported."
        )

    source.SetFileName(filename)

    print("reading file", filename)
    source.Update()

    return source


def vp_actor_from_file(filename):
    source = polydata_from_file(filename)

    # # clean the data
    # con = vtk.vtkCleanPolyData()
    # con.SetInputConnection(source.GetOutputPort())
    # con.Update()
    #
    #
    # normals = vtk.vtkPolyDataNormals()
    # normals.SetInputConnection(con.GetOutputPort())
    # normals.ConsistencyOn()
    # normals.AutoOrientNormalsOn()

    mapper = vtkPolyDataMapper()
    mapper.SetInputConnection(source.GetOutputPort())
    mapper.Update()

    #
    # # We are not importing textures and materials.
    # # Set color to 'w' to enforce an uniform color
    # vpa = vp.Mesh(mapper.GetInputAsDataSet(), c="w")  # need to set color here

    # vpa = vp.Mesh(filename, c="w")

    actor = vtkActorFromPolyData(mapper.GetInputAsDataSet())

    return actor


def Arrow(startPoint=(0, 0, 0), endPoint=(1, 0, 0), res=8):
    """Creates a vtkActor representing an arrow from startpoint to endpoint.
    All transforms are on the mesh itself.

    So placing the actor at 0,0,0 will show the arrow starting at startPoint

    """

    axis = np.asarray(endPoint) - np.asarray(startPoint)
    length = np.linalg.norm(axis)

    if length == 0:
        phi = 0
        theta = 0
    else:
        axis = axis / length
        phi = np.arctan2(axis[1], axis[0])
        theta = np.arccos(axis[2])

    arr = vtkArrowSource()
    arr.SetShaftResolution(res)
    arr.SetTipResolution(res)
    arr.Update()

    t = vtkTransform()
    t.Translate(startPoint)
    t.RotateZ(np.rad2deg(phi))
    t.RotateY(np.rad2deg(theta))
    t.RotateY(-90)  # put it along Z
    t.Scale(length, length, length)

    t.Update()

    tf = vtkTransformPolyDataFilter()
    tf.SetInputData(arr.GetOutput())
    tf.SetTransform(t)
    tf.Update()

    return vtkActorFromPolyData(tf.GetOutput())


def ArrowHead(
    startPoint=(0, 0, 0),
    endPoint=(1, 0, 0),
    res=12,
):
    """Creates a vtkActor representing an arrow HEAD (aka Cone) from startpoint to endpoint.
    All transforms are on the mesh itself.

    So placing the actor at 0,0,0 will show the arrow starting at startPoint

    """
    startPoint = np.asarray(startPoint)
    endPoint = np.asarray(endPoint)

    axis = endPoint - startPoint
    length = np.linalg.norm(axis)

    if length == 0:
        phi = 0
        theta = 0
    else:
        axis = axis / length

        phi = np.arctan2(axis[1], axis[0])
        theta = np.arccos(axis[2])

    arr = vtkConeSource()
    arr.SetResolution(res)
    arr.SetRadius(0.25)

    arr.Update()

    t = vtkTransform()
    t.Translate(startPoint + 0.5 * (endPoint - startPoint))
    t.RotateZ(np.rad2deg(phi))
    t.RotateY(np.rad2deg(theta))
    t.RotateY(-90)  # put it along Z
    t.Scale(length, length, length)

    t.Update()

    tf = vtkTransformPolyDataFilter()
    tf.SetInputData(arr.GetOutput())
    tf.SetTransform(t)
    tf.Update()

    return vtkActorFromPolyData(tf.GetOutput())


def Line(points, color=(1, 1, 1), lw=1):
    """Creates a line actor from a list of points"""
    poly = vtkPolyData()
    poly.SetPoints(vtkPoints())
    poly.GetPoints().SetData(numpy2vtk(points, dtype=np.float32))

    lines = vtkCellArray()
    lines.InsertNextCell(len(points))
    for i in range(len(points)):
        lines.InsertCellPoint(i)
    poly.SetLines(lines)

    actor = vtkActorFromPolyData(poly)
    actor.GetProperty().SetColor(color)

    actor.GetProperty().SetLineWidth(lw)

    return actor


def Cylinder(pos=(0, 0, 0), r=1, height=2.0, axis=(0, 0, 1), res=24):
    """Creates a cylinder actor with a position, radius, height, axis and resolution"""
    source = vtkCylinderSource()
    source.SetRadius(r)
    source.SetHeight(height)
    source.SetResolution(res)
    source.SetCenter(pos)
    source.Update()

    # the cylinder is created along the Y-axis, so we need to rotate it to the given axis
    # the rotation axis is the cross product of the Y-axis and the given axis

    axis = np.asarray(axis)
    axis_n = axis / np.linalg.norm(axis)
    rot_axis = np.cross([0, 1, 0], axis_n)
    # the rotation angle is the angle between the Y-axis and the given axis
    rot_angle = np.arccos(np.dot([0, 1, 0], axis_n))
    # create a transform
    t = vtkTransform()
    t.RotateWXYZ(np.rad2deg(rot_angle), *rot_axis)
    t.Update()
    # apply the transform to the cylinder
    tf = vtkTransformPolyDataFilter()
    tf.SetInputData(source.GetOutput())
    tf.SetTransform(t)
    tf.Update()

    return vtkActorFromPolyData(tf.GetOutput())


def Circle(r, res=36):
    source = vtkRegularPolygonSource()
    source.SetNumberOfSides(res)
    source.SetRadius(r)
    source.Update()

    return vtkActorFromPolyData(source.GetOutput())
