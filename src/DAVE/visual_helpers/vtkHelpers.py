import logging

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


def print_vtkMatrix44(mat):
    for i in range(4):
        row = [mat.GetElement(i, j) for j in range(4)]
        print(row)


def SetTransformIfDifferent(
    actor: vtk.vtkProp3D, transform: vtk.vtkTransform, tol=1e-6
):
    """Does not really set the user-transform, instead just sets the real transform"""

    mat1 = transform.GetMatrix()
    SetMatrixIfDifferent(actor, mat1, tol)


def vtkMatricesAlmostEqual(mat0, mat1, tol=1e-6):
    """Returns true if they are equal within tolerance"""
    for i in range(4):
        for j in range(4):
            target = mat1.GetElement(i, j)
            if abs(mat0.GetElement(i, j) - target) > tol:
                return False
    return True


def SetMatrixIfDifferent(actor: vtk.vtkProp3D, mat1, tol=1e-6):

    mat0 = actor.GetMatrix()

    if not vtkMatricesAlmostEqual(mat0, mat1, tol):  # only change if not almost equal

        m0 = mat1.GetElement(0, 0)
        m1 = mat1.GetElement(0, 1)
        m2 = mat1.GetElement(0, 2)
        m4 = mat1.GetElement(1, 0)
        m5 = mat1.GetElement(1, 1)
        m6 = mat1.GetElement(1, 2)
        m8 = mat1.GetElement(2, 0)
        m9 = mat1.GetElement(2, 1)
        m10 = mat1.GetElement(2, 2)

        scale1 = (m0 * m0 + m4 * m4 + m8 * m8) ** 0.5
        scale2 = (m1 * m1 + m5 * m5 + m9 * m9) ** 0.5
        scale3 = (m2 * m2 + m6 * m6 + m10 * m10) ** 0.5

        actor.SetScale(scale1, scale2, scale3)

        x = mat1.GetElement(0, 3)
        y = mat1.GetElement(1, 3)
        z = mat1.GetElement(2, 3)

        actor.SetOrigin(0, 0, 0)
        actor.SetPosition(x, y, z)

        out = [0, 0, 0]
        vtk.vtkTransform.GetOrientation(out, mat1)

        actor.SetOrientation(*out)


def SetScaleIfDifferent(actor: vtk.vtkProp3D, scale: float, tol=1e-6):
    current_scale = actor.GetScale()[0]  # assume all components are identical
    if abs(current_scale - scale) > tol:
        actor.SetScale(scale)


def tranform_almost_equal(
    transform1: vtk.vtkTransform, transform2: vtk.vtkTransform, tol=1e-6
):
    """Returns True if the two transforms are almost equal. Testing is done on the absolute difference of the components of the matrix

    Note: the values of the matrix contains both the rotation and the offset. The order of magnitude of these can be different
    if large offsets are used.
    """
    m1 = transform1.GetMatrix()
    m2 = transform2.GetMatrix()

    for i in range(4):
        for j in range(4):
            if abs(m1.GetElement(i, j) - m2.GetElement(i, j)) > tol:
                return False
    return True


def transform_to_mat4x4(transform):
    mat4x4 = vtk.vtkMatrix4x4()
    for i in range(4):
        for j in range(4):
            mat4x4.SetElement(i, j, transform[j * 4 + i])
    return mat4x4


def mat4x4_from_point_on_frame(frame: dn.Frame, local_position: tuple):
    """Creates a mat4x4 from a point on a frame. Use result with actor matrix (m44)"""

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


def transform_from_direction(axis, position=(0, 0, 0), right=None, scale = 1):
    """
    Creates a transform that rotates the X-axis to the given direction
    Args:
        axis: requested direction, needs to be a unit vector
        position : optional, (0,0,0)
        right: optional: vector to right. Needs to be a unit vector

        optional: scale [1]

    Returns:
        vtk.vtkMatrix4x4
    """

    # copied from vtk / MatrixHelpers::ViewMatrix

    viewDir = np.array(axis, dtype=float)

    if right is None:
        temp = np.array((1, 0, 0), dtype=float)
        if abs(np.dot(temp, viewDir)) > 0.98:
            temp[0] = 0
            temp[1] = 1

        right = np.cross(viewDir, temp)
        right = right / np.linalg.norm(right)

    up = np.cross(right, viewDir)

    mat4x4 = vtk.vtkMatrix4x4()

    mat4x4.SetElement(0, 0, right[0]*scale)
    mat4x4.SetElement(1, 0, right[1]*scale)
    mat4x4.SetElement(2, 0, right[2]*scale)
    mat4x4.SetElement(0, 1, up[0]*scale)
    mat4x4.SetElement(1, 1, up[1]*scale)
    mat4x4.SetElement(2, 1, up[2]*scale)
    mat4x4.SetElement(0, 2, viewDir[0]*scale)
    mat4x4.SetElement(1, 2, viewDir[1]*scale)
    mat4x4.SetElement(2, 2, viewDir[2]*scale)

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


def apply_parent_translation_on_transform(parent, t: vtk.vtkTransform):
    """Applies the DAVE global-transform of "parent" on vtkTransform t"""

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
    relative_to_slice_position=False,
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
            ax.plot(x, y, "k-", linewidth=0.5)

    return x, y

def vtkArrowActor(
        startPoint=(0,0,0),
        endPoint=(1,0,0),
        res = 12
    ):

    """Creates a vtkActor representing an arrow from startpoint to endpoint.
    All transforms are on the mesh itself.

    So placing the actor at 0,0,0 will show the arrow starting at startPoint

    """


    axis = np.asarray(endPoint) - np.asarray(startPoint)
    length = np.linalg.norm(axis)

    axis = axis / length

    phi = np.arctan2(axis[1], axis[0])
    theta = np.arccos(axis[2])

    arr = vtk.vtkArrowSource()
    arr.SetShaftResolution(res)
    arr.SetTipResolution(res)
    arr.Update()

    # sz = 0.02
    #
    # self.arr.SetTipRadius(sz)
    # self.arr.SetShaftRadius(sz / 1.75)
    # self.arr.SetTipLength(sz * 15)
    # self.arr.Update()

    t = vtk.vtkTransform()
    t.Translate(startPoint)
    t.RotateZ(np.rad2deg(phi))
    t.RotateY(np.rad2deg(theta))
    t.RotateY(-90)  # put it along Z
    t.Scale(length, length, length)

    t.Update()

    tf = vtk.vtkTransformPolyDataFilter()
    tf.SetInputData(arr.GetOutput())
    tf.SetTransform(t)
    tf.Update()

    # # mapper
    # mapper = vtk.vtkPolyDataMapper()
    # mapper.SetInputData(tf.GetOutput())
    #
    # # Actor.
    # actor = vtk.vtkActor()
    # actor.SetMapper(mapper)

    actor = vp.Mesh(tf.GetOutput())

    return actor

def vtkArrowHeadActor(
        startPoint=(0,0,0),
        endPoint=(1,0,0),
        res = 12,
    ):

    """Creates a vtkActor representing an arrow HEAD (aka Cone) from startpoint to endpoint.
    All transforms are on the mesh itself.

    So placing the actor at 0,0,0 will show the arrow starting at startPoint

    """
    startPoint = np.asarray(startPoint)
    endPoint = np.asarray(endPoint)

    axis = endPoint-startPoint
    length = np.linalg.norm(axis)

    axis = axis / length

    phi = np.arctan2(axis[1], axis[0])
    theta = np.arccos(axis[2])

    arr = vtk.vtkConeSource()
    arr.SetResolution(res)
    arr.SetRadius(0.25)

    arr.Update()

    t = vtk.vtkTransform()
    t.Translate(startPoint + 0.5*(endPoint-startPoint))
    t.RotateZ(np.rad2deg(phi))
    t.RotateY(np.rad2deg(theta))
    t.RotateY(-90)  # put it along Z
    t.Scale(length, length, length)

    t.Update()

    tf = vtk.vtkTransformPolyDataFilter()
    tf.SetInputData(arr.GetOutput())
    tf.SetTransform(t)
    tf.Update()

    # # mapper
    # mapper = vtk.vtkPolyDataMapper()
    # mapper.SetInputData(tf.GetOutput())
    #
    # # Actor.
    # actor = vtk.vtkActor()
    # actor.SetMapper(mapper)

    actor = vp.Mesh(tf.GetOutput())

    return actor