import vtk
import numpy as np

import vedo as vp
from vtk.util.numpy_support import vtk_to_numpy

import DAVE.nodes as dn

class DelayRenderingTillDone:
    """Little helper class to pause rendering and refresh using with(...)

    with(DelayRenderingTillDone(Viewport):
        do_updates


    Creates an attribute _DelayRenderingTillDone_lock on the parent viewport to
    keep this action exclusive to the first caller.

    """

    def __init__(self, viewport):
        self.viewport = viewport
        self.inactive = False

    def __enter__(self):
        try:
            if self.viewport._DelayRenderingTillDone_lock:
                self.inactive = True
                return
        except:
            pass

        self.viewport._DelayRenderingTillDone_lock = (
            True  # keep others from gaining control
        )
        self.viewport.screen.interactor.EnableRenderOff()
        for r in self.viewport.screen.renderers:
            r.DrawOff()

    def __exit__(self, *args, **kwargs):
        if self.inactive:
            return
        self.viewport.screen.interactor.EnableRenderOn()
        self.viewport.refresh_embeded_view()
        for r in self.viewport.screen.renderers:
            r.DrawOn()
        self.viewport._DelayRenderingTillDone_lock = False  # release lock


def transform_to_mat4x4(transform):
    mat4x4 = vtk.vtkMatrix4x4()
    for i in range(4):
        for j in range(4):
            mat4x4.SetElement(i, j, transform[j * 4 + i])
    return mat4x4

def mat4x4_from_point_on_frame(frame : dn.Frame, local_position : tuple):
    """Creates a mat4x4 from a point on a frame. Use result with actor.SetUserMatrix(m44)"""

    mat4x4 = transform_to_mat4x4(frame.global_transform)
    pos = frame.to_glob_position(local_position)

    mat4x4.SetElement(0, 3, pos[0])
    mat4x4.SetElement(1, 3, pos[1])
    mat4x4.SetElement(2, 3, pos[2])

    return mat4x4


def transform_from_point(x, y, z):
    mat4x4 = vtk.vtkMatrix4x4()
    mat4x4.SetElement(0, 3, x)
    mat4x4.SetElement(1, 3, y)
    mat4x4.SetElement(2, 3, z)
    return mat4x4


def transform_from_node(node):
    """Returns the vtkTransform that can be used to align the actor
    to the node.

    Actor.SetUserTransform(....)
    """
    t = vtk.vtkTransform()
    t.Identity()
    tr = node.global_transform

    mat4x4 = vtk.vtkMatrix4x4()
    for i in range(4):
        for j in range(4):
            mat4x4.SetElement(i, j, tr[j * 4 + i])

    t.PostMultiply()
    t.Concatenate(mat4x4)

    return t


def transform_from_direction(axis, position=(0, 0, 0), right=None):
    """
    Creates a transform that rotates the X-axis to the given direction
    Args:
        axis: requested direction, needs to be a unit vector
        position : optional, (0,0,0)
        right: optional: vector to right. Needs to be a unit vector

    Returns:
        vtk.vtkMatrix4x4
    """

    # copied from vtk / MatrixHelpers::ViewMatrix

    viewDir = np.array(axis, dtype=float)

    if right is None:
        temp = np.array((1, 0, 0), dtype=float)
        if np.dot(temp, viewDir) > 0.98:
            temp[0] = 0
            temp[1] = 1

        right = np.cross(viewDir, temp)
        right = right / np.linalg.norm(right)

    up = np.cross(right, viewDir)

    mat4x4 = vtk.vtkMatrix4x4()

    mat4x4.SetElement(0, 0, right[0])
    mat4x4.SetElement(1, 0, right[1])
    mat4x4.SetElement(2, 0, right[2])
    mat4x4.SetElement(0, 1, up[0])
    mat4x4.SetElement(1, 1, up[1])
    mat4x4.SetElement(2, 1, up[2])
    mat4x4.SetElement(0, 2, viewDir[0])
    mat4x4.SetElement(1, 2, viewDir[1])
    mat4x4.SetElement(2, 2, viewDir[2])

    mat4x4.SetElement(0, 3, position[0])
    mat4x4.SetElement(1, 3, position[1])
    mat4x4.SetElement(2, 3, position[2])

    return mat4x4


def update_line_to_points(line_actor, points):
    """Updates the points of a line-actor"""

    source = line_actor.GetMapper().GetInput()

    pts = source.GetPoints()

    npt = len(points)

    # check for number of points
    if pts.GetNumberOfPoints() == npt:
        line_actor.points(points)
        return
    else:

        _points = vtk.vtkPoints()
        _points.SetNumberOfPoints(npt)
        for i, pt in enumerate(points):
            _points.SetPoint(i, pt)

        _lines = vtk.vtkCellArray()
        _lines.InsertNextCell(npt)
        for i in range(npt):
            _lines.InsertCellPoint(i)
        source.SetLines(_lines)
        source.SetPoints(_points)

        source.Modified()


def apply_parent_translation_on_transform(parent, t):

    if parent is None:
        return

    tr = parent.global_transform

    mat4x4 = vtk.vtkMatrix4x4()
    for i in range(4):
        for j in range(4):
            mat4x4.SetElement(i, j, tr[j * 4 + i])

    t.PostMultiply()
    t.Concatenate(mat4x4)


def actor_from_trimesh(trimesh):
    """Creates a vedo.Mesh from a pyo3d.TriMesh"""

    if trimesh.nFaces == 0:
        return vp.Cube(side=0.00001)

    vertices = [trimesh.GetVertex(i) for i in range(trimesh.nVertices)]
    # are the vertices unique?

    faces = [trimesh.GetFace(i) for i in range(trimesh.nFaces)]

    return actor_from_vertices_and_faces(vertices, faces)


def actor_from_vertices_and_faces(vertices, faces):
    """Creates a mesh based on the given vertices and faces. Cleans up
    the structure before creating by removing duplicate vertices"""
    unique_vertices = np.unique(vertices, axis=0)

    if len(unique_vertices) != len(vertices):  # reconstruct faces and vertices
        unique_vertices, indices = np.unique(vertices, axis=0, return_inverse=True)
        f = np.array(faces)
        better_faces = indices[f]
        actor = vp.Mesh([unique_vertices, better_faces])
    else:
        actor = vp.Mesh([vertices, faces])

    return actor


def vp_actor_from_file(filename):
    # load the data
    filename = str(filename)

    source = None
    if filename.endswith("obj"):
        source = vtk.vtkOBJReader()
    elif filename.endswith("stl"):
        source = vtk.vtkSTLReader()

    if source is None:
        raise NotImplementedError(f"No reader implemented for reading file {filename}")

    source.SetFileName(filename)

    # # clean the data
    # con = vtk.vtkCleanPolyData()
    # con.SetInputConnection(source.GetOutputPort())
    # con.Update()
    # #
    #
    # # data = normals.GetOutput()
    # # for i in range(data.GetNumberOfPoints()):
    # #     point = data.GetPoint(i)
    # #     print(point)
    #
    # normals = vtk.vtkPolyDataNormals()
    # normals.SetInputConnection(con.GetOutputPort())
    # normals.ConsistencyOn()
    # normals.AutoOrientNormalsOn()

    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInputConnection(source.GetOutputPort())
    mapper.Update()
    #
    # # We are not importing textures and materials.
    # # Set color to 'w' to enforce an uniform color
    vpa = vp.Mesh(mapper.GetInputAsDataSet(), c="w")  # need to set color here

    # vpa = vp.Mesh(filename, c="w")

    return vpa


def _create_moment_or_shear_line(what, frame: dn.Frame, scale_to=2, at=None):
    """see create_momentline_actors, create_shearline_actors"""

    if at is None:
        at = frame

    lsm = frame.give_load_shear_moment_diagram(at)

    x, Fz, My = lsm.give_shear_and_moment()

    report_axis = at

    start = report_axis.to_glob_position((x[0], 0, 0))
    end = report_axis.to_glob_position((x[-1], 0, 0))

    n = len(x)
    scale = scale_to

    if what == "Moment":
        value = My
        color = "green"
    elif what == "Shear":
        value = Fz
        color = "blue"
    else:
        raise ValueError(f"What should be Moment or Shear, not {what}")

    if np.max(np.abs(value)) < 1e-6:
        scale = 0
    else:
        scale = scale / np.max(np.abs(value))
    line = [report_axis.to_glob_position((x[i], 0, scale * value[i])) for i in range(n)]

    actor_axis = vp.Line((start, end)).c("black").lw(3)
    actor_graph = vp.Line(line).c(color).lw(3)

    return (actor_axis, actor_graph)


def create_momentline_actors(frame: dn.Frame, scale_to=2, at=None):
    """Returns an actor that visualizes the moment-line for the given frame.

    Args:
        frame : Frame node to report the momentline for
        scale_to : absolute maximum of the line [m]
        at : Optional: [Frame] to report the momentline in
    """
    return _create_moment_or_shear_line("Moment", frame, scale_to, at)


def create_shearline_actors(frame: dn.Frame, scale_to=2, at=None):
    """Returns an actor that visualizes the shear-line for the given frame.

    Args:
        frame : Frame node to report the shearline for
        scale_to : absolute maximum of the line [m]
        at : Optional: [Frame] to report the shearline in
    """
    return _create_moment_or_shear_line("Shear", frame, scale_to, at)


def VisualToSlice(
    visual_node: "Visual",
    slice_position=(0, 0, 0),
    slice_normal=(0, 0, 1),
    projection_x=(1, 0, 0),
    projection_y=(0, 1, 0),
    relative_to_slice_position = False,
    ax=None,
    **kwargs,
):
    """Slices the visual-node at global position 'slice_position' and normal 'slice_normal'. This results in a slice
    in the global 3D space. This is then projected onto a plane defined by the two global vectors 'projection_x' and
    'projection_y'.

    If 'relative_to_slice_position' is True, then the slice is defined relative to the slice-position, otherwise the
    global coordinates are used.

    Optionally plots the result in ax
    if provided, kwargs are passed to the plt.plot function. Otherwise the line is drawn as 'k-' and lw = 0.5

    Returns x,y
    where x and y are (2, nsegements) so segment i is defined by:
    x[0,i], y[0,i] to x[1,i], y[1,i]
    """

    # load the node visual
    # apply the transform
    # -- copy-paste from DAVE.visuals

    scene = visual_node._scene

    file = scene.get_resource_path(visual_node.path)
    A = vp_actor_from_file(file)

    # get the local (user set) transform
    t = vtk.vtkTransform()
    t.Identity()
    t.Translate(visual_node.offset)
    t.Scale(visual_node.scale)

    # calculate wxys from node.rotation
    r = visual_node.rotation
    angle = (r[0] ** 2 + r[1] ** 2 + r[2] ** 2) ** (0.5)
    if angle > 0:
        t.RotateWXYZ(angle, r[0] / angle, r[1] / angle, r[2] / angle)

    # Get the parent matrix if any
    if visual_node.parent is not None:
        apply_parent_translation_on_transform(visual_node.parent, t)

    A.SetUserTransform(t)

    # do the slice
    plane = vtk.vtkPlane()
    plane.SetOrigin(*slice_position)
    plane.SetNormal(*slice_normal)

    cutter = vtk.vtkCutter()
    cutter.SetCutFunction(plane)
    cutter.SetInputData(A.polydata())
    cutter.Update()

    data = cutter.GetOutput()
    arr1d = vtk_to_numpy(data.GetLines().GetData())
    points3d = np.array(vtk_to_numpy(data.GetPoints().GetData()))

    if relative_to_slice_position:
        points3d -= slice_position

    # project the points onto a 2d plane
    px = points3d.dot(projection_x)
    py = points3d.dot(projection_y)

    points = np.array((px, py))

    # code from vedo.Mesh.lines()
    i = 0
    conn = []
    n = len(arr1d)
    for idummy in range(n):
        cell = [arr1d[i + k + 1] for k in range(arr1d[i])]
        conn.append(cell)
        i += arr1d[i] + 1
        if i >= n:
            break

    x = [([points[0][i] for i in segment]) for segment in conn]
    y = [([points[1][i] for i in segment]) for segment in conn]
    x = np.array(x).transpose()
    y = np.array(y).transpose()



    if ax is not None:
        if kwargs:
            ax.plot(x, y, **kwargs)
        else:
            ax.plot(x, y, 'k-', linewidth = 0.5)

    return x,y
