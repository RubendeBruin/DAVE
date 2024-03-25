"""Utilities for working with vtk actors in DAVE


vtkShow : debug function for quickly showing an actor
ApplyTexture : applies a texture to a vtk actor
DelayRenderingTillDone : context manager to pause rendering and refresh

SetTransformIfDifferent : sets the transform if different
SetMatrixIfDifferent : sets the matrix if different
SetScaleIfDifferent : sets the scale if different

tranform_almost_equal : returns True if the two transforms are almost equal
transform_to_mat4x4 : converts a vtkTransform to a vtkMatrix4x4
mat4x4_from_point_on_frame : creates a mat4x4 from a point on a frame
transform_from_point : creates a transform from a point
transform_from_node : creates a transform from a node
transform_from_direction : creates a transform from a direction

update_line_to_points : updates the points of a line-actor
update_vertices : updates the vertices of a mesh-actor
update_mesh     : updates the mesh of an actor from vertices and faces
update_mesh_from : updates the mesh of actor from other_actor

create_tube_data : creates tube data
get_color_array : gets the color array
apply_parent_translation_on_transform : applies the DAVE global-transform of "parent" on vtkTransform t
_create_moment_or_shear_line : creates a moment or shear line
create_momentline_actors : creates a momentline actor
create_shearline_actors : creates a shearline actor

VisualToSlice : slices the visual-node at global position 'slice_position' and normal 'slice_normal'

add_lid_to_open_mesh : adds a lid to an open mesh



"""
from pathlib import Path
from vtkmodules.util.numpy_support import vtk_to_numpy
from vtkmodules.vtkCommonCore import vtkUnsignedCharArray
from vtkmodules.vtkCommonDataModel import vtkPlane, vtkPolyLine
from vtkmodules.vtkCommonMath import vtkMatrix4x4
from vtkmodules.vtkFiltersCore import vtkCutter, vtkTubeFilter
from vtkmodules.vtkFiltersTexture import vtkImplicitTextureCoords

from vtkmodules.vtkIOImage import vtkImageReader2Factory
from vtkmodules.vtkInteractionWidgets import vtkOrientationMarkerWidget
from vtkmodules.vtkRenderingAnnotation import vtkAxesActor
from vtkmodules.vtkRenderingCore import vtkTexture, vtkProp3D

from scipy.spatial import ConvexHull

from DAVE.visual_helpers.constants import CABLE_COLORMAP
from DAVE.visual_helpers.vtkActorMakers import *

import DAVE.nodes as dn
from DAVE.settings_visuals import CABLE_DIA_WHEN_DIA_IS_ZERO


def vtkShow(actor):
    """Shows a vtk actor in a vedo plotter window"""

    from vtkmodules.vtkRenderingCore import (
        vtkRenderer,
        vtkRenderWindow,
        vtkRenderWindowInteractor,
    )

    # Create a rendering window and renderer
    renderer = vtkRenderer()
    renderWindow = vtkRenderWindow()
    renderWindow.AddRenderer(renderer)

    # Create a renderwindowinteractor
    interactor = vtkRenderWindowInteractor()
    interactor.SetRenderWindow(renderWindow)

    # Assign actor to the renderer
    renderer.AddActor(actor)

    # Render
    renderWindow.Render()

    # Enable user interface interactor
    interactor.Initialize()
    interactor.Start()


def ApplyTexture(
    actor: vtkActor, filename: str, repeat=False, edge_clamp=True, interpolate=True
):
    """Applies a texture to a vtkActor"""

    filename = str(filename)
    assert Path(filename).exists(), f"Texture file {filename} does not exist"

    readerFactory = vtkImageReader2Factory()
    textureFile = readerFactory.CreateImageReader2(filename)
    textureFile.SetFileName(filename)
    textureFile.Update()

    out_img = textureFile.GetOutput()

    # read the texture file
    tu = vtkTexture()
    tu.SetInputData(out_img)
    tu.SetInterpolate(interpolate)
    tu.SetRepeat(repeat)
    tu.SetEdgeClamp(edge_clamp)

    # get property
    prop = actor.GetProperty()

    if prop.GetInterpolation() == 3:  # Physically based
        tu.UseSRGBColorSpaceOn()
        prop.SetBaseColorTexture(tu)  # for PBR
        prop.SetColor(1, 1, 1)  # reset color to white
    else:
        actor.SetTexture(tu)  # for classic


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
        except AttributeError:
            pass

        self.viewport._DelayRenderingTillDone_lock = (
            True  # keep others from gaining control
        )
        self.viewport.interactor.EnableRenderOff()
        for r in self.viewport.renderers:
            r.DrawOff()

    def __exit__(self, *args, **kwargs):
        if self.inactive:
            return
        self.viewport.interactor.EnableRenderOn()
        self.viewport.refresh_embeded_view()
        for r in self.viewport.renderers:
            r.DrawOn()
        self.viewport._DelayRenderingTillDone_lock = False  # release lock


def print_vtkMatrix44(mat):
    for i in range(4):
        row = [mat.GetElement(i, j) for j in range(4)]
        print(row)


def SetTransformIfDifferent(actor: vtkProp3D, transform: vtkTransform, tol=1e-6):
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


def SetMatrixIfDifferent(actor: vtkProp3D, target_matrix, tol=1e-6):
    mat0 = actor.GetMatrix()

    mat1 = vtkMatrix4x4()
    mat1.DeepCopy(target_matrix)

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

        # scale back  (this is a work-around for a work-around for a work-around :-( )
        # orientation can not be determined accurately if scale difference is too large

        if abs(scale1) > 0:
            mat1.SetElement(0, 0, m0 / scale1)
            mat1.SetElement(1, 0, m4 / scale1)
            mat1.SetElement(2, 0, m8 / scale1)

        if abs(scale2) > 0:
            mat1.SetElement(0, 1, m1 / scale2)
            mat1.SetElement(1, 1, m5 / scale2)
            mat1.SetElement(2, 1, m9 / scale2)

        if abs(scale3) > 0:
            mat1.SetElement(0, 2, m2 / scale3)
            mat1.SetElement(1, 2, m6 / scale3)
            mat1.SetElement(2, 2, m10 / scale3)

        vtkTransform.GetOrientation(out, mat1)

        # no longer restore, we're working on a copy

        actor.SetOrientation(*out)


def SetScaleIfDifferent(actor: vtkProp3D, scale: float, tol=1e-6):
    current_scale = actor.GetScale()[0]  # assume all components are identical
    if abs(current_scale - scale) > tol:
        actor.SetScale(scale)


def tranform_almost_equal(transform1: vtkTransform, transform2: vtkTransform, tol=1e-6):
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
    mat4x4 = vtkMatrix4x4()
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
    mat4x4 = vtkMatrix4x4()
    mat4x4.SetElement(0, 3, x)
    mat4x4.SetElement(1, 3, y)
    mat4x4.SetElement(2, 3, z)
    return mat4x4


def transform_from_node(node):
    """Returns the vtkTransform that can be used to align the actor
    to the node.

    Actor.SetUserTransform(....)
    """
    t = vtkTransform()
    t.Identity()
    tr = node.global_transform

    mat4x4 = vtkMatrix4x4()
    for i in range(4):
        for j in range(4):
            mat4x4.SetElement(i, j, tr[j * 4 + i])

    t.PostMultiply()
    t.Concatenate(mat4x4)

    return t


def transform_from_direction(axis, position, scale=1, right=None):
    """
    Creates a transform that rotates the X-axis to the given direction
    Args:
        axis: requested direction, needs to be a unit vector
        scale: scale factor
        position: position of the transform
        right: optional: vector to right. Needs to be a unit vector

    Returns:
        vtkMatrix4x4
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

    mat4x4 = vtkMatrix4x4()

    mat4x4.SetElement(0, 0, right[0] * scale)
    mat4x4.SetElement(1, 0, right[1] * scale)
    mat4x4.SetElement(2, 0, right[2] * scale)
    mat4x4.SetElement(0, 1, up[0] * scale)
    mat4x4.SetElement(1, 1, up[1] * scale)
    mat4x4.SetElement(2, 1, up[2] * scale)
    mat4x4.SetElement(0, 2, viewDir[0] * scale)
    mat4x4.SetElement(1, 2, viewDir[1] * scale)
    mat4x4.SetElement(2, 2, viewDir[2] * scale)

    mat4x4.SetElement(0, 3, position[0])
    mat4x4.SetElement(1, 3, position[1])
    mat4x4.SetElement(2, 3, position[2])

    return mat4x4


def update_line_to_points(line_actor, points):
    """Updates the points of a line-actor"""

    source = line_actor.GetMapper().GetInput()

    pts = source.GetPoints()

    npt = len(points)

    _points = vtkPoints()
    _points.SetNumberOfPoints(npt)
    for i, pt in enumerate(points):
        _points.SetPoint(i, pt)
    source.SetPoints(_points)

    # Only need to update the lines if the number of points has changed
    if pts.GetNumberOfPoints() != npt:
        _lines = vtkCellArray()
        _lines.InsertNextCell(npt)
        for i in range(npt):
            _lines.InsertCellPoint(i)
        source.SetLines(_lines)

    source.Modified()


def update_mesh_from(actor, other_actor, apply_soure_transform=True):
    """Updates the mesh of actor from other_actor"""

    source = other_actor.GetMapper().GetInput()

    target = vtkPolyData()
    if apply_soure_transform:
        # get source transform
        # apply on target

        tr = vtkTransformPolyDataFilter()
        tr.SetInputData(source)

        t = vtkTransform()
        t.SetMatrix(other_actor.GetMatrix())

        tr.SetTransform(t)
        tr.Update()
        target.DeepCopy(tr.GetOutput())  # copy to targe

    else:
        target.DeepCopy(source)  # copy to target

    actor.GetMapper().SetInputData(target)
    actor.GetMapper().Modified()


def update_vertices(mesh_actor, vertices):
    """Updates the vertices of a mesh-actor,"""

    source = mesh_actor.GetMapper().GetInput()

    npt = len(vertices)

    _points = vtkPoints()
    _points.SetNumberOfPoints(npt)
    for i, pt in enumerate(vertices):
        _points.SetPoint(i, pt)
    source.SetPoints(_points)

    source.Modified()


def update_mesh(mesh_actor, vertices, faces):
    """Updates the mesh of an actor from vertices and faces"""

    polydata = polyDataFromVerticesAndFaces(vertices=vertices, faces=faces)
    mesh_actor.GetMapper().SetInputData(polydata)

def update_mesh_to_empty(actor):
    """Updates the mesh of an actor to an empty mesh"""
    polydata = vtkPolyData()
    actor.GetMapper().SetInputData(polydata)

def create_tube_data(new_points, diameter, colors=None):
    """Updates the points of a line-actor"""

    points = vtkPoints()
    for p in new_points:
        points.InsertNextPoint(p)

    line = vtkPolyLine()
    line.GetPointIds().SetNumberOfIds(len(new_points))
    for i in range(len(new_points)):
        line.GetPointIds().SetId(i, i)

    lines = vtkCellArray()
    lines.InsertNextCell(line)

    polyln = vtkPolyData()
    polyln.SetPoints(points)
    polyln.SetLines(lines)

    if colors is not None:
        cc = get_color_array(colors)
        cc.SetName("TubeColors")
        polyln.GetPointData().SetScalars(cc)

    tuf = vtkTubeFilter()
    tuf.SetCapping(False)
    tuf.SetNumberOfSides(12)
    tuf.SetInputData(polyln)

    if diameter < 1e-6:
        diameter = CABLE_DIA_WHEN_DIA_IS_ZERO

    tuf.SetRadius(diameter / 2)

    tuf.Update()

    return tuf.GetOutput()


def get_color_array(c):
    """Returns a vtkUnsignedCharArray with the colors in c as RGB-255 values stored in CABLE_COLORMAP

    c is a list of floats for which the corrsponding colors should be returned

    """

    cc = vtkUnsignedCharArray()
    cc.SetName("TubeColors")
    cc.SetNumberOfComponents(3)
    cc.SetNumberOfTuples(len(c))

    vmin = min(c) * 0.95
    vmax = max(c) * 1.05

    # scale the colors to the range 0-1 using vmin and vmax
    colors = [CABLE_COLORMAP((col - vmin) / (vmax - vmin)) for col in c]

    for i, (r, g, b, _) in enumerate(colors):
        cc.InsertTuple3(i, int(255 * r), int(255 * g), int(255 * b))
    return cc


def apply_parent_translation_on_transform(parent, t: vtkTransform):
    """Applies the DAVE global-transform of "parent" on vtkTransform t"""

    if parent is None:
        return

    tr = parent.global_transform

    mat4x4 = vtkMatrix4x4()
    for i in range(4):
        for j in range(4):
            mat4x4.SetElement(i, j, tr[j * 4 + i])

    t.PostMultiply()
    t.Concatenate(mat4x4)


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

    actor_axis = Line([start, end])
    actor_axis.SetColor([0, 0, 0])
    actor_axis.SetLineWidth(3)
    actor_graph = Line(line)
    actor_graph.SetColor(color)
    actor_graph.SetLineWidth(3)

    return actor_axis, actor_graph


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
    t = vtkTransform()
    t.Identity()
    t.Translate(visual_node.offset)
    t.Scale(visual_node.scale)

    # calculate wxys from node.rotation
    r = visual_node.rotation
    angle = (r[0] ** 2 + r[1] ** 2 + r[2] ** 2) ** 0.5
    if angle > 0:
        t.RotateWXYZ(angle, r[0] / angle, r[1] / angle, r[2] / angle)

    # Get the parent matrix if any
    if visual_node.parent is not None:
        apply_parent_translation_on_transform(visual_node.parent, t)

    A.SetUserTransform(t)

    # do the slice
    plane = vtkPlane()
    plane.SetOrigin(*slice_position)
    plane.SetNormal(*slice_normal)

    cutter = vtkCutter()
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


def add_lid_to_open_mesh(vertices: list, faces: list):
    # create the lid using a convex hull
    #
    #

    assert isinstance(
        vertices, list
    ), "Vertices should be a list - update is preformed in-place"
    assert isinstance(
        faces, list
    ), "Faces should be a list - update is preformed in-place"

    thickness_tolerance = 1e-4  # for numerical accuracy

    verts = np.array(vertices)
    z = verts[:, 2]
    maxz = np.max(z)
    top_plane_verts = verts[z >= maxz - thickness_tolerance]

    # make convex hull
    d2 = top_plane_verts[:, 0:2]

    try:
        hull = ConvexHull(d2)

        points = top_plane_verts[
            hull.vertices, :
        ]  # for 2-D the vertices are guaranteed to be in counterclockwise order

        nVerts = len(vertices)

        for point in points:
            vertices.append([*point])

        # construct faces
        for i in range(len(points) - 2):
            faces.append([nVerts, nVerts + i + 2, nVerts + i + 1])
    except:
        pass


if __name__ == "__main__":
    from DAVE.visual_helpers.vtkActorMakers import Cube

    c = Cube()
    vtkShow(c)
