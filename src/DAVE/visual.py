"""
  This Source Code Form is subject to the terms of the Mozilla Public
  License, v. 2.0. If a copy of the MPL was not distributed with this
  file, You can obtain one at http://mozilla.org/MPL/2.0/.

  Ruben de Bruin - 2019


  Some tools

"""

"""
visual visualizes a scene using vedo


nodeA class is VisualActor
this class contains a reference to a Node and a list of actors

a visual actor can be hidden by setting visible to False

each of the individual vtk-plotter actors has a "actor_type" property which is a enum ActorType

Note:
at this moment the outlines of the actors are created using a outline filter. This is expensive.
Probably more efficient to implement this using shaders. But only once VTK 9.0+ becomes standard as the shader
code will change.

"""

import vtkmodules.qt
vtkmodules.qt.PyQtImpl = 'PySide2'

import vedo as vp   # ref: https://github.com/marcomusy/vedo

# vp.settings.renderLinesAsTubes = True

import DAVE.scene as vf
import DAVE.settings as vc
import vtk
import numpy as np
from enum import Enum
from scipy.spatial import ConvexHull

def transform_to_mat4x4(transform):
    mat4x4 = vtk.vtkMatrix4x4()
    for i in range(4):
        for j in range(4):
            mat4x4.SetElement(i, j, transform[j * 4 + i])
    return mat4x4

def transform_from_point(x,y,z):
    mat4x4 = vtk.vtkMatrix4x4()
    mat4x4.SetElement(0, 3, x)
    mat4x4.SetElement(1, 3, y)
    mat4x4.SetElement(2, 3, z)
    return mat4x4

def transform_from_direction(axis):
    """
    Creates a transform that rotates the X-axis to the given direction
    Args:
        axis: requested direction

    Returns:
        vtk.vtkTransform
    """
    theta = np.arcsin(axis[2])
    phi = np.arctan2(axis[1], axis[0])
    t = vtk.vtkTransform()
    t.PostMultiply()
    # t.RotateX(90)  # put it along Z
    t.RotateY(np.rad2deg(theta))
    t.RotateZ(np.rad2deg(phi))

    return t

def update_line_to_points(line_actor, points):

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


def apply_parent_tranlation_on_transform(parent, t):

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

    vertices = []
    for i in range(trimesh.nVertices):
        vertices.append(trimesh.GetVertex(i))

    faces = []
    for i in range(trimesh.nFaces):
        faces.append(trimesh.GetFace(i))


    actor =  vp.Mesh([vertices, faces]).alpha(vc.ALPHA_BUOYANCY)

    actor.no_outline = True
    return actor

def vp_actor_from_obj(filename):
    # load the data
    filename = str(filename)
    source = vtk.vtkOBJReader()
    source.SetFileName(filename)
    #clean the data
    con = vtk.vtkCleanPolyData()
    con.SetInputConnection(source.GetOutputPort())
    con.Update()
    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInputConnection(con.GetOutputPort())
    mapper.Update()
    # actor = vtk.vtkActor()
    # actor.SetMapper(mapper)
    vpa = vp.Mesh(mapper.GetInputAsDataSet())
    vpa.flat()
    return vpa

class ActorType(Enum):
    FORCE = 1
    VISUAL = 2
    GEOMETRY = 3
    GLOBAL = 4
    CABLE = 5
    NOT_GLOBAL = 6
    BALLASTTANK = 7
    MESH_OR_CONNECTOR = 8
    COG = 9

class VisualOutline:
    parent_vp_actor = None
    outline_actor = None
    outline_transform = None

class VisualActor:

    def __init__(self, actors, node):
        self.actors = actors  # vedo actors
        self.node = node      # Node
        # self.visible = True
        self._original_colors = list()
        self._is_selected = False
        self._is_transparent = False
        self.label_actor = None

    def select(self):

        if self._is_selected:
            return

        self._original_colors = list()

        for actor in self.actors:
            self._original_colors.append(actor.color())
            actor.color(vc.COLOR_SELECT)

        self._is_selected = True


    def deselect(self):

        # print('resetting original colors 1')

        if not self._is_selected:
            return

        # print('resetting original colors 2')

        self._is_selected = False

        if self._original_colors:

            # if self.node is not None:
            #     print('setting ' + str(self.node.name))
            # else:
            #     print('setting properties')


            for actor, color in zip(self.actors, self._original_colors):
                actor.color(color)

        else:
            if self.actors:
                raise Exception("Original color not stored for visual belonging to {}".format(self.node.name))


    def make_transparent(self):

        if self._is_transparent:
            return

        for a in self.actors:
            a.alpha(0.4)

        self._is_transparent = True

    def reset_opacity(self):

        if not self._is_transparent:
            return

        for a in self.actors:
            if a.actor_type == ActorType.GLOBAL:
                a.alpha(0.4)
            else:
                a.alpha(1)

        self._is_transparent = False

    def set_dsa(self, d,s,a):
        for act in self.actors:
            act.lighting(diffuse=d, ambient=a, specular=s)

    def on(self):
        for a in self.actors:
            a.on()

    def off(self):
        for a in self.actors:
            a.off()

    @property
    def visible(self):
        return self.actors[0].GetVisibility()

    def setLabelPosition(self, position):
        if self.label_actor is not None:
            self.label_actor.SetAttachmentPoint(*position)

    def setLabel(self, txt):
        if self.label_actor is None:
            la = vtk.vtkCaptionActor2D()
            la.SetCaption(txt)

            position = self.actors[0].GetPosition()

            la.SetAttachmentPoint(*position)

            la.SetPickable(True)

            cap = la.GetTextActor().GetTextProperty()
            la.GetTextActor().SetPickable(True)

            size = 0.02

            cap.SetColor(0, 0, 0)
            la.SetWidth(100 * size)
            la.SetHeight(size)
            la.SetPosition(-size/2, -size/2)
            la.SetBorder(False)
            cap.SetBold(True)
            cap.SetItalic(False)

            la.no_outline = True

            self.label_actor = la

        else:
            self.label_actor.SetCaption(txt)

        return self.label_actor



class Viewport:

    def __init__(self, scene, jupyter = False):
        self.scene = scene
        self.visuals = list()
        self.outlines = list()
        self.screen = None
        """Becomes assigned when a screen is active (or was active...)"""

        self.vtkWidget = None
        """Qt viewport, if any"""

        self.global_visual = None
        """Visuals for the global environment"""

        self.mouseLeftEvent = None
        self.mouseRightEvent = None
        self.onEscapeKey = None
        "Function handles"

        self.Jupyter = jupyter

        # Settings
        self.show_geometry = True     # show or hide geometry objects (axis, pois, etc)
        self.show_force = True        # show forces
        self.show_meshes = True       # show meshes and connectors
        self.show_global = False      # show or hide the environment (sea)
        self.show_cog = True
        self.force_do_normalize = True # Normalize force size to 1.0 for plotting
        self.visual_alpha = 1.0       # show or hide visuals
        self.cog_do_normalize = False
        self.cog_scale = 1.0
        self.force_scale = 1.6        # Scale to be applied on (normalized) force magnitude
        self.geometry_scale = 1.0          # poi radius of the pois
        self.outline_width = vc.OUTLINE_WIDTH      # line-width of the outlines (cell-like shading)
        self.cable_line_width = 3.0   # line-width used for cable elements

        self.quick_updates_only = False # Do not perform slow updates ( make animations quicker)

        self._wavefield = None
        """WaveField object"""

    def show_only_labels_of_nodes_type(self, node_types):
        for vis in self.visuals:
            on = False

            if node_types is not None:
                if isinstance(vis.node, node_types):
                    on = True

            if vis.label_actor is not None:
                vis.label_actor.SetVisibility(on)


    def update_outlines(self):
        if self.screen is None:
            return

        if self.quick_updates_only:
            for outline in self.outlines:
                outline.outline_actor.SetVisibility(False)
            return

        for outline in self.outlines:
            outline.outline_actor.SetVisibility(outline.parent_vp_actor.GetVisibility())

        # list of already existing outlines
        _outlines = [a.parent_vp_actor for a in self.outlines]

        # loop over actors, add outlines if needed
        for vp_actor in self.screen.actors:

            if getattr(vp_actor, 'no_outline', False):
                continue

            data = vp_actor.GetMapper().GetInputAsDataSet()
            if isinstance(data, vtk.vtkPolyData):
                # this actor can have an outline
                if vp_actor not in _outlines:
                    # create outline and add to self.outlines

                    tr = vtk.vtkTransformPolyDataFilter()

                    tr.SetInputData(data) # can we make a connection using port? (maintain the pipeline : see issue vtkplotter #48)
                                          # remark: Better to implement using shaders, but wait till VTK 9 because this will change the shader code.
                    temp = vtk.vtkTransform()
                    temp.Identity()
                    tr.SetTransform(temp)
                    tr.Update()

                    ol = vtk.vtkPolyDataSilhouette()
                    ol.SetInputConnection(tr.GetOutputPort())
                    ol.SetEnableFeatureAngle(True)
                    ol.SetCamera(self.screen.renderer.GetActiveCamera())
                    ol.SetBorderEdges(True)

                    mapper = vtk.vtkPolyDataMapper()
                    mapper.SetInputConnection(ol.GetOutputPort())

                    actor = vtk.vtkActor()
                    actor.SetMapper(mapper)
                    actor.GetProperty().SetColor(0, 0, 0)
                    actor.GetProperty().SetLineWidth(self.outline_width)

                    self.screen.renderer.AddActor(actor)  # vtk actor

                    # store
                    record = VisualOutline()
                    record.outline_actor = actor
                    record.outline_transform = tr
                    record.parent_vp_actor = vp_actor
                    self.outlines.append(record)

        # Update transforms for outlines
        to_be_deleted = []
        for record in self.outlines:
            # is the parent actor still present?
            if record.parent_vp_actor in self.screen.actors:
                # update transform
                userTransform = record.parent_vp_actor.GetUserTransform()

                if userTransform is not None:
                    matrix = userTransform.GetMatrix()
                else:
                    matrix = vtk.vtkMatrix4x4()

                trans = vtk.vtkTransform()
                trans.Identity()
                trans.Concatenate(matrix)
                trans.Scale(record.parent_vp_actor.GetScale())

                record.outline_transform.SetTransform(trans)

                record.outline_actor.SetVisibility(record.parent_vp_actor.GetVisibility())

            else:
                # mark for deletion
                to_be_deleted.append(record)

        # Remove obsolete outlines
        to_be_deleted_actors = [oa.outline_actor for oa in to_be_deleted]
        self.screen.remove(to_be_deleted_actors)

        for record in to_be_deleted:
            self.outlines.remove(record)



    def create_world_actors(self):

        world_actors = []

        plane = vp.Plane(pos=(0,0,0), normal=(0,0,1), sx=1000, sy=1000).c(vc.COLOR_WATER)
        plane.texture(vc.TEXTURE_SEA)
        plane.lighting(ambient=1.0, diffuse=0.0, specular=0.0)
        plane.alpha(0.4)

        world_actors.append(plane)
        world_actors[0].actor_type = ActorType.GLOBAL

        if self.show_global:
            world_actors[0].on()
        else:
            world_actors[0].off()

        world_actors.append(vp.Line((0, 0, 0), (10, 0, 0)).c('red'))
        world_actors[-1].actor_type = ActorType.GEOMETRY

        world_actors.append(vp.Line((0, 0, 0), (0, 10, 0)).c('green'))
        world_actors[-1].actor_type = ActorType.GEOMETRY

        world_actors.append(vp.Line((0, 0, 0), (0, 0, 10)).c('blue'))
        world_actors[-1].actor_type = ActorType.GEOMETRY

        v = VisualActor(world_actors, None)
        self.visuals.append(v)

        self.global_visual = v

    def deselect_all(self):
        for v in self.visuals:
            v.deselect()

    def node_from_vtk_actor(self, actor):
        """
        Given a vkt actor, find the corresponding node
        Args:
            actor: vtkActor

        Returns:

        """
        for v in self.visuals:
            for a in v.actors:
                if a == actor:
                    return v.node
            if v.label_actor == actor:
                return v.node

        return None

    def actor_from_node(self, node):
        """Finds the VisualActor belonging to node"""
        for v in self.visuals:
            if v.node is node:
                return v
        return None

    def add_dynamic_wave_plane(self, waveplane):
        self.remove_dynamic_wave_plane()
        self.screen.renderer.AddActor(waveplane.actor)
        self._wavefield = waveplane

        if self.global_visual.visible:
            self._staticwaveplane = True
            self.global_visual.off()
        else:
            self._staticwaveplane = False

    def remove_dynamic_wave_plane(self):
        if self._wavefield is not None:
            self.screen.renderer.RemoveActor(self._wavefield.actor)
            self._wavefield = None

            if self._staticwaveplane:
                self.global_visual.on()




    def update_dynamic_waveplane(self, t):
        if self._wavefield is not None:
            self._wavefield.update(t)


    def hide_actors_of_type(self, types):
        for V in self.visuals:
            for A in V.actors:
                if A.actor_type in types:
                    A.off()


    def show_actors_of_type(self, types):
        for V in self.visuals:
            for A in V.actors:
                    if A.actor_type in types:
                        A.on()

    def set_alpha(self, alpha, exclude_nodes=None):
        """Sets the alpha (transparency) of for ALL actors in all visuals except the GLOBAL actors or visuals belonging to a node in exclude_nodes"""

        if exclude_nodes is None:
            exclude_nodes = []
        for V in self.visuals:
            for A in V.actors:

                if V.node in exclude_nodes:
                    continue

                if A.actor_type == ActorType.GLOBAL:
                    continue
                A.alpha(alpha)


    def level_camera(self):
        self.vtkWidget.GetRenderWindow().GetRenderers().GetFirstRenderer().GetActiveCamera().SetViewUp([0, 0, 1])
        self.refresh_embeded_view()

    def camera_reset(self):
        self.vtkWidget.GetRenderWindow().GetRenderers().GetFirstRenderer().ResetCamera()



    def toggle_2D(self):
        camera = self.renderer.GetActiveCamera()
        if camera.GetParallelProjection():
            camera.ParallelProjectionOff()
        else:
            camera.ParallelProjectionOn()

    def set_camera_direction(self, vector):
        # Points the camera in the given direction
        camera = self.vtkWidget.GetRenderWindow().GetRenderers().GetFirstRenderer().GetActiveCamera()
        vector = np.array(vector)
        vector = vector / np.linalg.norm(vector)

        if np.linalg.norm(np.cross(vector, (0,0,1))) < 1e-8:
            up = (0,-1,0)
        else:
            up = (0,0,1)

        camera.SetViewUp(up)
        tar = np.array(camera.GetFocalPoint())
        pos = np.array(camera.GetPosition())
        dist = np.linalg.norm(tar-pos)

        camera_position = tar - dist * vector

        camera.SetPosition(camera_position)



    def _scaled_force_vector(self, vector):

        r = np.array(vector)
        len = np.linalg.norm(r)
        if len == 0:
            return r
        if self.force_do_normalize:
            r *= (1000/len)
        r *= (self.force_scale / 1000)
        return r



    def create_visuals(self, recreate = False):
        """Visuals are created in their parent axis system

        Attributes:
            recreate : re-create already exisiting visuals
        """

        for N in self.scene._nodes:

            if not recreate:
                try:            # if we already have a visual, then no need to create another one
                    N.visual
                    if N.visual is not None:
                        continue
                except:
                    pass

            actors = []
            label_text = None

            if isinstance(N, vf.Buoyancy):

                # 0 : source-mesh
                # 1 : cob
                # 2 : water-plane
                # 3 : sumberged mesh

                # This is the source-mesh. Connect it to the parent
                vis = actor_from_trimesh(N.trimesh._TriMesh)

                if vc.COLOR_BUOYANCY_MESH_FILL is None:
                    vis = vp.Cube(side=0.00001)
                else:
                    vis.c(vc.COLOR_BUOYANCY_MESH_FILL)

                vis.actor_type = ActorType.MESH_OR_CONNECTOR

                if vc.COLOR_BUOYANCY_MESH_FILL is None:
                    vis.wireframe()

                if vis is not None:
                    actors.append(vis)

                # cob
                c = vp.Sphere(r=0.5, res = vc.RESOLUTION_SPHERE).c(vc.COLOR_WATER)
                c.actor_type = ActorType.MESH_OR_CONNECTOR
                actors.append(c)

                # waterplane
                exts = N.trimesh.get_extends()

                cx = 0.5 * (exts[0] + exts[1])
                dx = exts[1] - exts[0]
                cy = 0.5 * (exts[3] + exts[2])
                dy = exts[3] - exts[2]

                p = vp.Plane(pos = (cx,cy,0), normal = (0,0,1), sx = dx*1.1, sy = dy*1.1).c(vc.COLOR_WATER)
                p.actor_type = ActorType.NOT_GLOBAL
                actors.append(p)

            if isinstance(N, vf.Tank):

                # 0 : source-mesh
                # 1 : cog
                # 2 : filled part of mesh (added later)

                # This is the source-mesh. Connect it to the parent
                vis = actor_from_trimesh(N.trimesh._TriMesh)

                if vc.COLOR_TANK_MESH_FILL is not None:
                    vis.c(vc.COLOR_TANK_MESH_FILL)
                else:
                    vis.wireframe()
                    vis.c(vc.COLOR_TANK_MESH_LINES)

                vis.actor_type = ActorType.MESH_OR_CONNECTOR

                if vis is not None:
                    actors.append(vis)

                # cog
                c = vp.Sphere(r=0.5, res = vc.RESOLUTION_SPHERE).c(vc.COLOR_WATER)
                c.actor_type = ActorType.MESH_OR_CONNECTOR
                actors.append(c)

                label_text = N.name


            if isinstance(N, vf.ContactMesh):

                # 0 : source-mesh

                # This is the source-mesh. Connect it to the parent

                vis = actor_from_trimesh(N.trimesh._TriMesh)
                if not vis:
                    vis = vp.Cube(side=0.00001)

                vis.actor_type = ActorType.MESH_OR_CONNECTOR

                if vc.COLOR_CONTACT_MESH_FILL is not None:
                    vis.c(vc.COLOR_CONTACT_MESH_FILL)
                else:
                    vis.wireframe()
                    vis.c(vc.COLOR_CONTACT_MESH_LINES)

                vis.loaded_obj = True

                if vis is not None:
                    actors.append(vis)


            if isinstance(N, vf.Visual):
                file = self.scene.get_resource_path(N.path)
                # visual = vp.vtkio.load(file)
                visual = vp_actor_from_obj(file)
                visual.color(vc.COLOR_VISUAL)
                visual.loaded_obj = file
                visual.actor_type = ActorType.VISUAL
                actors.append(visual)


            if isinstance(N, vf.Axis):
                size = 1
                ar = vp.Arrow((0,0,0),(size,0,0), res=vc.RESOLUTION_ARROW).c(vc.COLOR_X)
                ag = vp.Arrow((0, 0, 0), (0, size, 0), res=vc.RESOLUTION_ARROW).c(vc.COLOR_Y)
                ab = vp.Arrow((0, 0, 0), (0, 0, size), res=vc.RESOLUTION_ARROW).c(vc.COLOR_Z)

                ar.actor_type = ActorType.GEOMETRY
                ag.actor_type = ActorType.GEOMETRY
                ab.actor_type = ActorType.GEOMETRY

                actors.append(ar)
                actors.append(ag)
                actors.append(ab)

            if isinstance(N, vf.RigidBody):
                size = 1

                box = vp_actor_from_obj(self.scene.get_resource_path('cog.obj'))
                box.color(vc.COLOR_COG)

                box.actor_type = ActorType.COG
                actors.append(box)

            if isinstance(N, vf.Point):
                size = 0.5
                p = vp.Sphere(pos=(0,0,0), r=size/2, res = vc.RESOLUTION_SPHERE)
                p.c(vc.COLOR_POI)
                p.actor_type = ActorType.GEOMETRY
                actors.append(p)

                label_text = N.name

            if isinstance(N, vf.ContactBall):
                p = vp.Sphere(pos=(0,0,0), r=N.radius, res = vc.RESOLUTION_SPHERE)
                p.c(vc.COLOR_FORCE)
                p.actor_type = ActorType.MESH_OR_CONNECTOR
                p._r = N.radius
                actors.append(p)

                point1 = ((0,0,0))
                a = vp.Line([point1, point1], lw=5).c(vc.COLOR_FORCE)
                a.actor_type = ActorType.MESH_OR_CONNECTOR

                actors.append(a)

            if isinstance(N, vf.WaveInteraction1):
                size = 2
                p = vp.Sphere(pos=(0,0,0), r=size/2, res = vc.RESOLUTION_SPHERE)
                p.c(vc.COLOR_WAVEINTERACTION)
                p.actor_type = ActorType.FORCE
                actors.append(p)

            if isinstance(N, vf.BallastSystem):

                pass

                # for t in N.tanks:
                #
                #     capacity = t.max
                #     volume = capacity / (1.025 * 9.81)
                #     side = volume**(1/3)
                #
                #     scale = 0.7
                #     p = vp.Cube(pos=(0,0,0), side=scale*side)
                #     p.c(vc.COLOR_POI)
                #     p.actor_type = ActorType.BALLASTTANK
                #     p._side = side
                #     actors.append(p)
                #
                #     # attach reference to the visual to the ballast tank as they may change position
                #     t.actor = p

            if isinstance(N, vf.Force):

                endpoint = self._scaled_force_vector(N.force)
                p = vp.Arrow(startPoint=(0,0,0), endPoint=endpoint, res=vc.RESOLUTION_ARROW)
                p.c(vc.COLOR_FORCE)
                p.actor_type = ActorType.FORCE
                p._force = endpoint

                actors.append(p)

                endpoint = self._scaled_force_vector(N.moment)
                p = vp.Arrow(startPoint=(0, 0, 0), endPoint=endpoint, res=vc.RESOLUTION_ARROW)
                p.actor_type = ActorType.FORCE
                p._moment = endpoint
                p.c(vc.COLOR_FORCE)
                actors.append(p)

                p = vp.Arrow(startPoint = 0.2 * endpoint, endPoint= 1.2 * endpoint, res=vc.RESOLUTION_ARROW)
                p.actor_type = ActorType.FORCE
                p.c(vc.COLOR_FORCE)
                actors.append(p)

            if isinstance(N, vf.Circle):
                axis = np.array(N.axis)
                axis /= np.linalg.norm(axis)
                p = vp.Cylinder(r=1)
                p.c(vc.COLOR_SHEAVE)
                p.actor_type = ActorType.GEOMETRY

                actors.append(p)

            if isinstance(N, vf.Cable):

                if N._vfNode.global_points:
                    a = vp.Line(N._vfNode.global_points, lw=3).c(vc.COLOR_CABLE)
                else:
                    a = vp.Line([(0,0,0),(0,0,0.1),(0,0,0)], lw=3).c(vc.COLOR_CABLE)

                a.actor_type = ActorType.CABLE
                actors.append(a)

                label_text = N.name

            if isinstance(N, vf.SPMT):

                gp = N.get_actual_global_points()
                if gp:
                    a = vp.Line(gp, lw=3).c(vc.COLOR_CABLE)
                else:
                    a = vp.Line([(0,0,0),(0,0,0.1),(0,0,0)], lw=3).c(vc.COLOR_CABLE)

                a.actor_type = ActorType.CABLE
                actors.append(a)

            if isinstance(N, vf.Beam):

                gp = N.global_positions

                if len(gp)>0:
                    a = vp.Line(gp, lw=5).c(vc.COLOR_BEAM)
                else:
                    a = vp.Line([(0,0,0),(0,0,0.1),(0,0,0)], lw=5).c(vc.COLOR_BEAM)

                a.actor_type = ActorType.CABLE
                actors.append(a)


            if isinstance(N, vf.Connector2d):

                points = list()

                for i in range(2):
                    points.append((0,0,0))

                a = vp.Line(points, lw=5).c(vc.COLOR_FORCE)
                a.actor_type = ActorType.CABLE

                actors.append(a)

            if isinstance(N, vf.LC6d):

                points = list()

                for i in range(2):
                    points.append((0,0,0))

                a = vp.Line(points, lw=5).c(vc.COLOR_FORCE)
                a.actor_type = ActorType.CABLE

                actors.append(a)

            va = VisualActor(actors, N)
            if label_text is not None:
                va.setLabel(N.name)
            N.visual = va

            N.visual.__just_created = True


            self.visuals.append(va)

            self.set_default_dsa()

    def position_visuals(self):
        """All visuals are aligned with their node"""

        to_be_removed = []

        for V in self.visuals:

            # check if the node still exists
            # if not, then remove the visual

            node = V.node
            if node not in self.scene._nodes:
                if len(V.actors) > 0:  # not all nodes have an actor
                    if V.actors[0].actor_type != ActorType.GLOBAL:  # global visuals do not have a corresponding node
                        to_be_removed.append(V)
                        continue
                else:
                    to_be_removed.append(V)
                    continue  # node does not have an actor


            # create a transform from the Node
            # or the parent of the Node
            # or skip (for example a poi without a parent)

            if V.node is None:
                continue

            if isinstance(V.node, vf.Visual):
                A = V.actors[0]

                # get the local (user set) transform
                t = vtk.vtkTransform()
                t.Identity()
                t.Translate(V.node.offset)
                t.Scale(V.node.scale)

                # # scale offset
                # scaled_offset = [V.node.offset[i] / V.node.scale[i] for i in range(3)]


                # calculate wxys from node.rotation
                r= V.node.rotation
                angle = (r[0]**2 + r[1]**2 + r[2]**2)**(0.5)
                if angle > 0:
                    t.RotateWXYZ(angle, r[0]/angle, r[1]/angle, r[2]/angle)

                # elm_matrix = t.GetMatrix()

                # Get the parent matrix (if any)
                if V.node.parent is not None:
                    apply_parent_tranlation_on_transform(V.node.parent, t)

                A.SetUserTransform(t)
                continue

            if isinstance(V.node, vf.Circle):
                A = V.actors[0]

                # get the local (user set) transform
                t = vtk.vtkTransform()
                t.Identity()

                # scale to flat disk
                t.Scale(V.node.radius, V.node.radius, 0.1)

                # rotate z-axis (length axis is cylinder) is direction of axis
                axis = V.node.axis / np.linalg.norm(V.node.axis)
                z = (0,0,1)
                rot_axis = np.cross(z, axis)
                rot_dot = np.dot(z,axis)
                if rot_dot > 1:
                    rot_dot = 1
                if rot_dot < -1:
                    rot_dot = -1

                angle = np.arccos(rot_dot)

                t.PostMultiply()
                t.RotateWXYZ(np.rad2deg(angle), rot_axis)

                t.Translate(V.node.parent.position)

                # Get the parent matrix (if any)
                if V.node.parent.parent is not None:
                    apply_parent_tranlation_on_transform(V.node.parent.parent, t)

                A.SetUserTransform(t)
                continue

            if isinstance(V.node, vf.Cable):

                # # check the number of points
                A = V.actors[0]

                # points = list()
                # for p in V.node._pois:
                #    points.append(p.global_position)

                points = V.node.get_points_for_visual()

                if len(points)==0:  # not yet created
                    continue

                update_line_to_points(A, points)

                V.setLabelPosition(np.mean(points, axis=0))

                continue

            if isinstance(V.node, vf.SPMT):

                A = V.actors[0]

                pts = V.node.get_actual_global_points()
                if len(pts)==0:
                    continue

                update_line_to_points(A, pts)

                continue

            if isinstance(V.node, vf.Beam):

                points = V.node.global_positions
                A = V.actors[0]
                update_line_to_points(A, points)

                V.setLabelPosition(np.mean(points, axis=0))

                continue

            if isinstance(V.node, vf.Connector2d):
                A = V.actors[0]

                points = list()
                points.append(node.nodeA.to_glob_position((0, 0, 0)))
                points.append(node.nodeB.to_glob_position((0, 0, 0)))

                A.points(points)

                continue

            if isinstance(V.node, vf.LC6d):
                A = V.actors[0]

                points = list()
                points.append(node.main.to_glob_position((0, 0, 0)))
                points.append(node.secondary.to_glob_position((0, 0, 0)))

                A.points(points)

                continue


            if isinstance(V.node, vf.BallastSystem):

                continue


            if isinstance(V.node, vf.Point):
                t = vtk.vtkTransform()
                t.Identity()
                t.Translate(V.node.global_position)
                V.actors[0].SetUserTransform(t)
                V.actors[0].SetScale(self.geometry_scale)

                V.setLabelPosition(V.node.global_position)
                continue

            if isinstance(V.node, vf.ContactBall):

                V.node.update()

                t = vtk.vtkTransform()
                t.Identity()
                t.Translate(V.node.parent.global_position)

                # check radius
                if V.actors[0]._r != V.node.radius:
                    temp = vp.Sphere(pos=(0,0,0), r=V.node.radius, res = vc.RESOLUTION_SPHERE)
                    V.actors[0].points(temp.points())
                    V.actors[0]._r = V.node.radius


                V.actors[0].SetUserTransform(t)
                V.actors[0].wireframe(V.node.contact_force_magnitude>0)

                if V.node.can_contact:
                    point1 =  V.node.parent.global_position
                    point2 = V.node.contactpoint
                    V.actors[1].points([point1, point2])
                    V.actors[1].on()
                else:
                    V.actors[1].off()


                continue

            if isinstance(V.node, vf.WaveInteraction1):
                t = vtk.vtkTransform()
                t.Identity()
                t.Translate(V.node.parent.to_glob_position(V.node.offset))
                V.actors[0].SetUserTransform(t)
                V.actors[0].SetScale(self.geometry_scale)
                continue


            if isinstance(V.node, vf.Force):

                # check is the arrows are still what they should be
                if not np.all(V.actors[0]._force == self._scaled_force_vector(V.node.force)):

                    self.screen.remove(V.actors[0])

                    endpoint = self._scaled_force_vector(V.node.force)


                    p = vp.Arrow(startPoint=(0, 0, 0), endPoint=endpoint, res=vc.RESOLUTION_ARROW)
                    p.actor_type = ActorType.FORCE
                    p._force = endpoint
                    p.c(vc.COLOR_FORCE)

                    V.actors[0] = p
                    self.screen.add(V.actors[0])

                # check is the arrows are still what they should be
                if not np.all(np.array(V.actors[1]._moment) == self._scaled_force_vector(V.node.moment)):
                    self.screen.remove(V.actors[1])
                    self.screen.remove(V.actors[2])

                    endpoint = self._scaled_force_vector(V.node.moment)
                    p = vp.Arrow(startPoint=(0, 0, 0), endPoint=endpoint, res=vc.RESOLUTION_ARROW)
                    p.actor_type = ActorType.FORCE
                    p._moment = endpoint
                    p.c(vc.COLOR_FORCE)
                    V.actors[1] = p

                    p = vp.Arrow(startPoint=0.2 * endpoint, endPoint=1.2 * endpoint, res=vc.RESOLUTION_ARROW)
                    p.actor_type = ActorType.FORCE
                    p.c(vc.COLOR_FORCE)
                    V.actors[2] = p
                    self.screen.add(V.actors[1])
                    self.screen.add(V.actors[2])

                t = V.actors[0].getTransform()
                t.Identity()
                t.Translate(V.node.parent.global_position)
                for a in V.actors:
                    a.SetUserTransform(t)

                continue

            if isinstance(V.node, vf.RigidBody):

                # Some custom code to place and scale the Actor[3] of the body.
                # This actor should be placed at the CoG position and scaled to a solid steel block

                t = vtk.vtkTransform()
                t.Identity()

                if self.cog_do_normalize:
                    scale = 1
                else:
                    scale = (V.node.mass / 8.050)**(1/3)  # density of steel

                t.Translate(V.node.cog)
                mat4x4 = transform_to_mat4x4(V.node.global_transform)

                for A in V.actors:
                    A.SetUserMatrix(mat4x4)

                t.PostMultiply()
                t.Concatenate(mat4x4)

                scale = scale * self.cog_scale

                V.actors[3].SetScale(scale)
                V.actors[3].SetUserTransform(t)

                # scale the arrows
                V.actors[0].SetScale(self.geometry_scale)
                V.actors[1].SetScale(self.geometry_scale)
                V.actors[2].SetScale(self.geometry_scale)

                continue


            if isinstance(V.node, vf.Buoyancy) or isinstance(V.node, vf.ContactMesh) or isinstance(V.node, vf.Tank):
                # Source mesh update is common for all mesh-like nodes
                #

                changed = False   # anything changed?

                if node.trimesh._new_mesh:
                    # self.screen.add(V.actors[0])
                    changed = True                  # yes, mesh has changed
                    node.trimesh._new_mesh = False


                # move the full mesh with the parent

                if node.parent is not None:
                    mat4x4 = transform_to_mat4x4(V.node.parent.global_transform)
                    current_transform = V.actors[0].getTransform().GetMatrix()

                    # if the current transform is identical to the new one,
                    # then we do not need to change anything (creating the mesh is slow)

                    for i in range(4):
                        for j in range(4):
                            if current_transform.GetElement(i, j) != mat4x4.GetElement(i, j):
                                changed = True     # yes, transform has changed
                                break

                    # Update the source-mesh position
                    #
                    # the source-mesh itself is updated in "add_new_actors_to_screen"
                    if changed:
                        V.actors[0].SetUserMatrix(mat4x4)

                if not changed:
                    continue    # skip the other update functions


            if isinstance(V.node, vf.Buoyancy):

                ## Buoyancy has multiple actors
                #
                # actor 0 : the source mesh
                # actor 1 : the CoB
                # actor 2 : the waterplane
                # actor 3 : the submerged part of the source mesh
                #

                # If we are here then either the source-mesh has been updated or the position has changed

                if self.quick_updates_only:
                    for a in V.actors:
                        a.off()
                    continue
                else:
                    if V.node.visible:
                        for a in V.actors:
                            a.on()

                # Update the CoB
                # move the CoB to the new (global!) position
                cob = V.node.cob
                V.actors[1].SetUserMatrix(transform_from_point(*cob))
                if V.node.displacement == 0:
                    V.actors[1].off()
                else:
                    V.actors[1].on()

                # update water-plane
                x1, x2, y1, y2, _, _ = V.node.trimesh.get_extends()
                x1 -= vc.VISUAL_BUOYANCY_PLANE_EXTEND
                x2 += vc.VISUAL_BUOYANCY_PLANE_EXTEND
                y1 -= vc.VISUAL_BUOYANCY_PLANE_EXTEND
                y2 += vc.VISUAL_BUOYANCY_PLANE_EXTEND
                p1 = V.node.parent.to_glob_position((x1, y1, 0))
                p2 = V.node.parent.to_glob_position((x2, y1, 0))
                p3 = V.node.parent.to_glob_position((x2, y2, 0))
                p4 = V.node.parent.to_glob_position((x1, y2, 0))

                corners = [(p1[0], p1[1], 0),
                           (p2[0], p2[1], 0),
                           (p4[0], p4[1], 0),
                           (p3[0], p3[1], 0)]
                V.actors[2].points(corners)

                if not V.node.visible:
                    V.actors[2].off()

                # Instead of updating, remove the old actor and create a new one

                # remove already existing submerged mesh (if any)
                if len(V.actors) > 3:
                    if self.screen is not None:
                        self.screen.remove(V.actors[3])
                        V.actors.remove(V.actors[3])

                mesh = V.node._vfNode.current_mesh

                if mesh.nVertices > 0:  # only add when available

                    vertices = []
                    for i in range(mesh.nVertices):
                        vertices.append(mesh.GetVertex(i))

                    faces = []
                    for i in range(mesh.nFaces):
                        faces.append(mesh.GetFace(i))

                    # vis = vp.Mesh([vertices, faces], wire=True).c((0, 0, 1))
                    vis = vp.Mesh([vertices, faces]).c(vc.COLOR_BUOYANCY_MESH_LINES)
                    vis.actor_type = ActorType.MESH_OR_CONNECTOR
                    vis.wireframe()
                    vis.lw(vc.LINEWIDTH_SUBMERGED_MESH)
                    V.actors.append(vis)

                    if not V.node.visible:
                        vis.off()

                    if self.screen is not None:
                        self.screen.add(vis)

                continue

            if isinstance(V.node, vf.ContactMesh):

                continue


            if isinstance(V.node, vf.Tank):

                ## Tank has multiple actors
                #
                # 0 : source-mesh
                # 1 : cog
                # 2 : filled part of mesh

                # If the source mesh has been updated, then V.node.trimesh._new_mesh is True
                if V.__just_created:
                    V._visual_volume = -1


                if self.quick_updates_only:
                    for a in V.actors:
                        a.off()
                    continue
                else:
                    if V.node.visible:
                        for a in V.actors:
                            a.on()

                # Update the actors
                V.node.update()

                # Update the CoB
                # move the CoB to the new (global!) position
                cob = V.node.cog

                points = V.actors[0].points(True)
                V.setLabelPosition(np.mean(points, axis=1))

                # print(f'cob = {cob}')

                V.actors[1].SetUserMatrix(transform_from_point(*cob))
                if V.node.volume == 0:
                    V.actors[1].off()
                else:
                    V.actors[1].on()


                # Fluid in tank

                # Construct a visual:
                #   - vertices
                #   - faces

                # If tank is full, then simply copy the mesh from the tank itself

                if V.node.fill_pct > 99.99 and not V.node.free_flooding:

                    # tank is full
                    vertices = points[0]
                    faces = V.actors[0].faces()

                else:

                    mesh = V.node._vfNode.current_mesh

                    if mesh.nVertices > 0:  # only add when available

                        vertices = []
                        for i in range(mesh.nVertices):
                            vertices.append(mesh.GetVertex(i))

                        faces = []
                        for i in range(mesh.nFaces):
                            faces.append(mesh.GetFace(i))


                        # create the lid using a convex hull
                        thickness_tolerance = 1e-4  # for numerical accuracy

                        verts = np.array(vertices)
                        z = verts[:,2]
                        maxz = np.max(z)
                        top_plane_verts = verts[z>=maxz-thickness_tolerance]

                        # make convex hull
                        d2 = top_plane_verts[:,0:2]

                        try:

                            hull = ConvexHull(d2)

                            points = top_plane_verts[hull.vertices, :]   # for 2-D the vertices are guaranteed to be in counterclockwise order

                            nVerts = len(vertices)

                            for point in points:
                                vertices.append([*point])

                            # construct faces
                            for i in range(len(points)-2):
                                faces.append([nVerts,nVerts+i+2,nVerts+i+1])
                        except:
                            pass


                    else:
                        vertices = []
                    # -------------------

                # we now have vertices and points and faces

                # do we already have an actor?
                need_new = False
                if len(V.actors) > 2:
                    # print(f'Already have an actor for {V.node.name}')
                    vis = V.actors[2]

                    pts = vis.GetMapper().GetInput().GetPoints()
                    npt = len(vertices)

                    # Update the existing actor if the number of vertices stay the same
                    # If not then delete the actor

                    # check for number of points
                    if pts.GetNumberOfPoints() == npt:
                        # print(f'setting points for {V.node.name}')
                        vis.points(vertices)

                    else:

                        # print(f'Number of points changed: {pts.GetNumberOfPoints()} was {npt}')

                        if self.screen is not None:
                            # print(f'Removing actor for for {V.node.name}')
                            self.screen.remove(V.actors[2])
                            V.actors.remove(V.actors[2])
                            need_new = True
                else:
                    need_new = True

                if len(vertices)>0:  # if we have an actor

                    if need_new:

                        # print(f'Creating new actor for for {V.node.name}')

                        vis = vp.Mesh([vertices, faces]).c(vc.COLOR_BUOYANCY_MESH_LINES)
                        vis.actor_type = ActorType.MESH_OR_CONNECTOR

                        V.actors.append(vis)

                        if self.screen is not None:
                            self.screen.add(vis, render=True)

                    if V.node.free_flooding:
                        vis.c(vc.COLOR_WATER_TANK_FREEFLOODING)
                    else:
                        if V.node.fill_pct > 94.9:
                            vis.c(vc.COLOR_WATER_TANK_95PLUS)
                        elif V.node.fill_pct < 5.1:
                            vis.c(vc.COLOR_WATER_TANK_5MIN)
                        else:
                            vis.c(vc.COLOR_WATER_TANK_SLACK)

                    vis.alpha(vc.ALPHA_WATER_TANK)

                    if not V.node.visible:
                        vis.off()



                V._visual_volume = V.node.volume

                continue

            if isinstance(V.node, vf.Axis):
                m44 = transform_to_mat4x4(V.node.global_transform)
                for a in V.actors:
                    a.SetScale(self.geometry_scale)
                    a.SetUserMatrix(m44)

                continue

            # --- default ---

            try:
                tr = V.node.global_transform
            except AttributeError:
                try:
                    tr = V.node.parent.global_transform
                except AttributeError:
                    continue

            mat4x4 = transform_to_mat4x4(tr)

            for A in V.actors:
                A.SetUserMatrix(mat4x4)



        acs = list()
        for V in  to_be_removed:
            self.visuals.remove(V)
            acs.extend(V.actors)
            if V.label_actor is not None:
                acs.append(V.label_actor)

        if acs:
            self.screen.remove(acs)

        self.update_outlines()

    def add_new_actors_to_screen(self):
        """Updates the screen with added actors"""

        to_be_added = []

        if self.screen:

            actors = self.screen.getMeshes()
            for va in self.visuals:
                for a in va.actors:
                    if not (a in actors):
                        to_be_added.append(a)
                        # self.screen.add(a)   # do not add directly to avoid frequent updates
                        #print('adding actor for {}'.format(va.node.name))
                if va.label_actor is not None:
                    if va.label_actor not in actors:
                        to_be_added.append(va.label_actor)

            if to_be_added:
                self.screen.add(to_be_added)

            # check if objs or meshes need to be re-loaded
            for va in self.visuals:
                if isinstance(va.node, vf.Visual):

                    try:
                        file = self.scene.get_resource_path(va.node.path)
                    except FileExistsError:
                        continue

                    if file == va.actors[0].loaded_obj:
                        continue

                    self.screen.clear(va.actors[0])

                    # update the obj
                    va.actors[0] = vp_actor_from_obj(file)
                    va.actors[0].loaded_obj = file
                    va.actors[0].color(vc.COLOR_VISUAL)
                    va.actors[0].actor_type = ActorType.VISUAL

                    if not va.node.visible:
                        va.actors[0].off()

                    self.screen.add(va.actors[0])

                if isinstance(va.node, vf.Buoyancy) or isinstance(va.node, vf.ContactMesh) or isinstance(va.node, vf.Tank):
                    if va.node.trimesh._new_mesh:

                        # va.node.update() # the whole scene is already updated when executing code

                        new_mesh = actor_from_trimesh(va.node.trimesh._TriMesh)
                        new_mesh.no_outline = True

                        if new_mesh is not None:
                            self.screen.clear(va.actors[0])

                            va.actors[0] = new_mesh
                            va.actors[0].actor_type = ActorType.MESH_OR_CONNECTOR

                            if va.node.parent is not None:
                                tr = va.node.parent.global_transform
                                mat4x4 = transform_to_mat4x4(tr)
                                va.actors[0].SetUserMatrix(mat4x4)

                            if isinstance(va.node, vf.Buoyancy):
                                va.actors[0].alpha(vc.ALPHA_BUOYANCY)
                                if vc.COLOR_BUOYANCY_MESH_FILL is None:
                                    va.actors[0].c(vc.COLOR_BUOYANCY_MESH_LINES)
                                    va.actors[0].wireframe()
                                else:
                                    va.actors[0].c(vc.COLOR_BUOYANCY_MESH_FILL)

                            elif isinstance(va.node, vf.ContactMesh):
                                if vc.COLOR_CONTACT_MESH_FILL is None:
                                    va.actors[0].c(vc.COLOR_CONTACT_MESH_LINES)
                                    va.actors[0].wireframe()
                                else:
                                    va.actors[0].c(vc.COLOR_CONTACT_MESH_FILL)

                            elif isinstance(va.node, vf.Tank):
                                if vc.COLOR_TANK_MESH_FILL is None:
                                    va.actors[0].c(vc.COLOR_TANK_MESH_LINES)
                                    va.actors[0].wireframe()
                                else:
                                    va.actors[0].c(vc.COLOR_TANK_MESH_FILL)

                            else:
                                raise Exception('Bug in add_new_actors_to_screen')

                            if not va.node.visible:
                                va.actors[0].off()

                            self.screen.add(va.actors[0])  # add after positioning

                            # va.node.trimesh._new_mesh = False  # is set to False by position_visuals

            self.set_default_dsa()



    def shutdown_qt(self):
        """Stops the renderer such that the application can close without issues"""

        if self.vtkWidget:
            ren = self.vtkWidget.GetRenderWindow()
            iren = ren.GetInteractor()
            ren.Finalize()
            iren.TerminateApp()



    def setup_screen(self,qtWidget = None):
        """Creates the plotter instance and stores it in self.screen"""

        if self.Jupyter and qtWidget is None:  # it is possible to launch the Gui from jupyter, so check for both

            # create embedded notebook (k3d) view
            import vedo as vtkp
            vtkp.settings.embedWindow(backend='k3d')
            self.screen = vp.Plotter(axes = 4, bg=vc.COLOR_BG1, bg2=vc.COLOR_BG2)

        else:

            if qtWidget is None:

                # create stand-alone interactive view
                import vedo as vtkp
                vtkp.settings.embedWindow(backend=None)

                self.screen = vp.plotter.Plotter(interactive=True, offscreen=False,
                    axes=4, bg=vc.COLOR_BG1, bg2=vc.COLOR_BG2)

            else:

                # create embedded Qt view
                import vedo as vtkp
                vtkp.settings.embedWindow(backend=None)

                self.screen = vp.plotter.Plotter(qtWidget=qtWidget,
                                            axes=4, bg=vc.COLOR_BG1, bg2=vc.COLOR_BG2)


    def show(self, qtWidget = None, camera = None):
        """Add actors to screen and show"""
        if self.screen is None:
            raise Exception("Please call setup_screen first")

        vp.settings.lightFollowsCamera = True

        self.create_world_actors()

        if camera is None:
            camera = dict()
            camera['viewup'] = [0, 0, 1]
            camera['pos'] = [10, -10, 5]
            camera['focalPoint'] = [0, 0, 0]

        if self.Jupyter and qtWidget is None:

            # show embedded
            for va in self.visuals:
                for a in va.actors:
                    if a.GetVisibility():
                        self.screen.add(a)

            return self.screen.show(camera=camera)

        else:

            screen = self.screen

            for va in self.visuals:
                for a in va.actors:
                    screen.add(a)

            self.screen.show(camera=camera)

            for r in self.screen.renderers:
                r.ResetCamera()

                # # Add SSAO
                # #
                # basicPasses = vtk.vtkRenderStepsPass()
                # ssao = vtk.vtkSSAOPass()
                # ssao.SetRadius(1)
                # ssao.SetDelegatePass(basicPasses)
                # ssao.SetBlur(True)
                # ssao.SetKernelSize(8)

                # r.SetPass(ssao)
                # # r.SetUseDepthPeeling(True)

                r.SetUseDepthPeeling(True)
                # r.SetMaximumNumberOfPeels(4)  # <-- default = 4


            self.update_outlines()
            screen.resetcam = False

            return screen

    def onMouseLeft(self, info):



        if self.mouseLeftEvent is not None:
            self.mouseLeftEvent(info)

    def zoom_all(self):
        for r in self.screen.renderers:
            r.ResetCamera()



    def onMouseRight(self, info):
        if self.mouseRightEvent is not None:
            self.mouseRightEvent(info)


    def show_embedded(self, target_frame):
        """target frame : QFrame """

        from PySide2.QtWidgets import QVBoxLayout
        from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor

        # add a widget to gui
        vl = QVBoxLayout()
        vl.setContentsMargins(0,0,0,0)
        self.target_frame = target_frame
        self.vtkWidget = QVTKRenderWindowInteractor(target_frame)

        vl.addWidget(self.vtkWidget)
        target_frame.setLayout(vl)

        self.setup_screen(qtWidget=self.vtkWidget)
        screen = self.show(qtWidget=self.vtkWidget)

        self.renwin = self.vtkWidget.GetRenderWindow()
        self.renderer = screen.renderers[0]

        self.renwin.AddRenderer(self.renderer)

        iren = self.renwin.GetInteractor()
        iren.SetInteractorStyle(vtk.vtkInteractorStyleTrackballCamera())

        iren.AddObserver("LeftButtonPressEvent", self._leftmousepress)
        iren.AddObserver("RightButtonPressEvent", screen._mouseright)
        iren.AddObserver("MiddleButtonPressEvent", screen._mousemiddle)
        iren.AddObserver("KeyPressEvent", self.keyPressFunction)
        iren.AddObserver(vtk.vtkCommand.InteractionEvent, self.keep_up_up)

        for r in screen.renderers:
            r.ResetCamera()

        iren.Start()

        # screen.mouseLeftClickFunction = self.onMouseLeft
        screen.mouseRightClickFunction = self.onMouseRight

        # Add some lights
        light1 = vtk.vtkLight()

        light1.SetIntensity(0.3)
        light1.SetLightTypeToCameraLight()
        light1.SetPosition(100, 100, 100)

        self.renderer.AddLight(light1)

        self.light = light1

    def _leftmousepress(self, iren, event):
        """Implements a "fuzzy" mouse pick function"""

        if self.mouseLeftEvent is not None:

            pos = self.screen.interactor.GetEventPosition()

            picker = vtk.vtkPropPicker()

            for j in range(5):

                if j==0:
                    x,y = 0,0
                elif j == 1:
                    x, y = -1, 1
                elif j == 2:
                    x, y = -1, -1
                elif j==3:
                    x, y = 1, 1
                else:
                    x, y = 1, -1

                if picker.Pick(pos[0]+2*x, pos[1]+2*y, 0, self.screen.renderer):
                    actor = picker.GetActor()  # gives an Actor
                    if actor is not None:
                        self.mouseLeftEvent(actor)
                        return

                    actor = picker.GetActor2D()
                    if actor is not None:
                        self.mouseLeftEvent(actor)
                        return


    def keep_up_up(self,obj, event_type):
        """Force z-axis up"""

        camera = self.screen.camera

        up = camera.GetViewUp()
        if abs(up[2]) < 0.2:
            factor = 1-(5*abs(up[2]))
            camera.SetViewUp(factor * up[0],
                             factor * up[1],
                            (1-factor) + factor*up[2])
        else:
            camera.SetViewUp(0,0,1)

        z = camera.GetPosition()[2]
        alpha = 1
        if z<0:

            dz = camera.GetDirectionOfProjection()[2]

            # alpha = (z + 10)/10
            alpha = 1-(10*dz)
            if alpha<0:
                alpha = 0
        self.global_visual.actors[0].alpha(vc.ALPHA_SEA*alpha)

    def keyPressFunction(self, obj, event):
        key = obj.GetKeySym()
        if key == 'Escape':
            if self.onEscapeKey is not None:
                self.onEscapeKey()




    def refresh_embeded_view(self):
        self.vtkWidget.update()

    def update_visibility(self):
        """Updates the visibility settings for all of the actors

        A visual can be hidden completely by setting visible to false
        An actor can be hidden depending on the actor-type using

        self.show_geometry = True
        self.show_force = True
        self.show_visual = True
        self.show_global = False
        """

        for v in self.visuals:

            if v.node is not None:
                if not v.node.visible:
                    for a in v.actors:
                        a.off()
                    continue


            for i,a in enumerate(v.actors):

                try:
                    a.actor_type
                except:
                    raise AttributeError('Missing actor_type for actor nr {} on node {}'.format(i, v.node.name))

                if a.actor_type == ActorType.FORCE:
                    if self.show_force:
                        a.on()
                    else:
                        a.off()

                elif a.actor_type == ActorType.MESH_OR_CONNECTOR:
                    if self.show_meshes:
                        a.on()
                    else:
                        a.off()

                elif a.actor_type == ActorType.COG:
                    if self.show_cog:
                        a.on()
                    else:
                        a.off()

                elif a.actor_type == ActorType.VISUAL:
                    if self.visual_alpha == 0:
                        a.off()
                    else:
                        a.on()
                        a.alpha(self.visual_alpha)


                elif a.actor_type == ActorType.GEOMETRY:
                    if self.show_geometry:
                        a.on()

                    else:
                        a.off()

                elif a.actor_type == ActorType.GLOBAL:
                    if self.show_global:
                        a.on()

                        if self.vtkWidget is not None:
                            arenderer = self.vtkWidget.GetRenderWindow().GetRenderers().GetFirstRenderer()
                            arenderer.GradientBackgroundOn()
                            arenderer.SetBackground2(vc.COLOR_BG2_ENV)
                            arenderer.SetBackground2(vc.COLOR_BG1_ENV)
                    else:
                        a.off()

                        if self.vtkWidget is not None:
                            arenderer = self.vtkWidget.GetRenderWindow().GetRenderers().GetFirstRenderer()
                            arenderer.GradientBackgroundOn()
                            arenderer.SetBackground2(vc.COLOR_BG2)
                            arenderer.SetBackground2(vc.COLOR_BG1)

                elif a.actor_type == ActorType.NOT_GLOBAL:
                    if self.show_global:
                        a.off()
                    else:
                        a.on()



                # Cables are a separate class

                elif a.actor_type == ActorType.CABLE:
                    if (self.visual_alpha>0) or self.show_force:
                        a.on()
                    else:
                        a.off()

        self.update_outlines()


    def set_dsa(self, d,s,a):
        for v in self.visuals:
            v.set_dsa(d,s,a)

    def set_default_dsa(self):
        self.set_dsa(vc.VISUAL_DIFFUSE, vc.VISUAL_SPECULAR, vc.VISUAL_AMBIENT)


class WaveField():

    def __init__(self):
        self.actor = None
        self.pts = None
        self.nt = 0
        self.elevation = None

        self.texture = vtk.vtkTexture()
        input = vtk.vtkJPEGReader()
        input.SetFileName(vc.TEXTURE_SEA)
        self.texture.SetInputConnection(input.GetOutputPort())
        self.ttp = vtk.vtkTextureMapToPlane()


    def update(self, t):
        t = np.mod(t, self.period)
        i = int(self.nt * t/self.period)

        count = 0
        for ix,xx in enumerate(self.x):
            for iy, yy in enumerate(self.y):
                self.pts.SetPoint(count, xx,yy,self.elevation[iy,ix,i])
                count += 1
        self.pts.Modified()

    def create_waveplane(self, wave_direction, wave_amplitude, wave_length, wave_period, nt, nx, ny, dx,dy):

        x = np.linspace(-dx, dx, nx)
        y = np.linspace(-dy, dy, ny)
        xv, yv = np.meshgrid(x, y)

        u = np.array((np.cos(np.deg2rad(wave_direction)), np.sin(np.deg2rad(wave_direction))))

        dist_phasor = np.exp(1j * (xv*u[0] + yv*u[1]) * (2*np.pi/ wave_length))

        t = np.linspace(0,wave_period, nt)
        time_phasor = np.exp(-1j * (2 * np.pi * t / wave_period))

        elevation = np.zeros((*xv.shape, nt))

        for i in range(nt):
            elevation[:,:,i] = wave_amplitude * np.real(time_phasor[i] * dist_phasor)


        # the vtk stuff

        # make grid
        pts = vtk.vtkPoints()
        for ix,xx in enumerate(x):
            for iy, yy in enumerate(y):
                pts.InsertNextPoint(yy,xx,elevation[iy,ix,1])

        grid = vtk.vtkStructuredGrid()
        grid.SetDimensions(ny,nx,1)
        grid.SetPoints(pts)

        # make mapper
        filter = vtk.vtkStructuredGridGeometryFilter()
        filter.SetInputData(grid)

        # texture stuff
        self.ttp.SetInputConnection(filter.GetOutputPort())

        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputConnection(self.ttp.GetOutputPort())

        actor = vtk.vtkActor()
        actor.SetMapper(mapper)
        actor.SetTexture(self.texture)

        actor.GetProperty().SetAmbient(1.0)
        actor.GetProperty().SetDiffuse(0.0)
        actor.GetProperty().SetSpecular(0.0)

        self.pts = pts
        self.actor = actor
        self.elevation = elevation
        self.nt = nt
        self.period = wave_period
        self.x = x
        self.y = y


if __name__ == "__main__":

    wavefield = WaveField()


    # def create_waveplane(self, wave_direction, wave_amplitude, wave_length, wave_period, nt, nx, ny, dx, dy):
    wavefield.create_waveplane(30, 2, 100, 7, 50, 40, 40, 100, 100)
    wavefield.update(0)

    wavefield.actor.GetMapper().Update()
    data = wavefield.actor.GetMapper().GetInputAsDataSet()

    code = 'import numpy as np\nimport bpy\n'
    code += '\nvertices = np.array(['

    for i in range(data.GetNumberOfPoints()):
        point = data.GetPoint(i)
        code += '\n    {}, {}, {},'.format(*point)

    code = code[:-1] # remove the last ,

    code += """], dtype=np.float32)


num_vertices = vertices.shape[0] // 3

# Polygons are defined in loops. Here, we define one quad and two triangles
vertex_index = np.array(["""

    poly_length = []
    counter = 0
    poly_start = []

    for i in range(data.GetNumberOfCells()):
        cell = data.GetCell(i)

        if isinstance(cell, vtk.vtkLine):
            print("Cell nr {} is a line, not adding to mesh".format(i))
            continue

        code += '\n    '

        for ip in range(cell.GetNumberOfPoints()):
            code += '{},'.format(cell.GetPointId(ip))

        poly_length.append(cell.GetNumberOfPoints())
        poly_start.append(counter)
        counter += cell.GetNumberOfPoints()

    code = code[:-1]  # remove the last ,

    code += """], dtype=np.int32)

# For each polygon the start of its vertex indices in the vertex_index array
loop_start = np.array([
    """

    for p in poly_start:
        code += '{}, '.format(p)

    code = code[:-1]  # remove the last ,

    code += """], dtype=np.int32)

# Length of each polygon in number of vertices
loop_total = np.array([
    """

    for p in poly_length:
        code += '{}, '.format(p)

    code = code[:-1]  # remove the last ,

    code += """], dtype=np.int32)

num_vertex_indices = vertex_index.shape[0]
num_loops = loop_start.shape[0]

# Create mesh object based on the arrays above

mesh = bpy.data.meshes.new(name='created mesh')

mesh.vertices.add(num_vertices)
mesh.vertices.foreach_set("co", vertices)

mesh.loops.add(num_vertex_indices)
mesh.loops.foreach_set("vertex_index", vertex_index)

mesh.polygons.add(num_loops)
mesh.polygons.foreach_set("loop_start", loop_start)
mesh.polygons.foreach_set("loop_total", loop_total)


"""

    wavefield.nt  # number of key-frames


    for i_source_frame in range(wavefield.nt):
        t = wavefield.period * i_source_frame / wavefield.nt

        n_frame = 30 * t # todo: replace with frames per second

        # update wave-field
        wavefield.update(t)
        wavefield.actor.GetMapper().Update()
        # data = v.actor.GetMapper().GetInputAsDataSet()


        code += '\nvertices = np.array(['

        for i in range(data.GetNumberOfPoints()):
            point = data.GetPoint(i)
            code += '\n    {}, {}, {},'.format(*point)

        code = code[:-1]  # remove the last ,

        code += """], dtype=np.float32)
        
mesh.vertices.foreach_set("co", vertices)
for vertex in mesh.vertices:
        """
        code += 'vertex.keyframe_insert(data_path="co", frame = {})'.format(np.round(n_frame))


    code += """
# We're done setting up the mesh values, update mesh object and 
# let Blender do some checks on it
mesh.update()
mesh.validate()

# Create Object whose Object Data is our new mesh
obj = bpy.data.objects.new('created object', mesh)

# Add *Object* to the scene, not the mesh
scene = bpy.context.scene
scene.collection.objects.link(obj)

# Select the new object and make it active
bpy.ops.object.select_all(action='DESELECT')
obj.select_set(True)
bpy.context.view_layer.objects.active = obj"""

    with open('c:/data/test.py', 'w') as data:
        data.write(code)



















