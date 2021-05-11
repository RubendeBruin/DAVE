"""
  This Source Code Form is subject to the terms of the Mozilla Public
  License, v. 2.0. If a copy of the MPL was not distributed with this
  file, You can obtain one at http://mozilla.org/MPL/2.0/.

  Ruben de Bruin - 2019

"""

"""
visual visualizes a scene using vtk and vedo helpers

Basic data structure:


Viewport
 - visuals (VisualActors)
    - [node] -> reference to corresponding node 
    - actors [dict]
        - [ActorType]


Viewport
============

Viewport is the main class which handles the viewport (ie: Plotter).
It supports embedded plotting (in a qt application) as well as stand-alone or via Jupyter or screenshots


Visual-Actors
------------------

A viewport contains VisualActors.
this class contains a reference to a Node and a list of actors

a visual actor can be hidden by setting visible to False

each of the individual vtk-plotter actors has a "actor_type" property which is a enum ActorType.

ActorType is used for general control of these actors. At the moment this is only Scaling which is implemented in "position visuals"

self.visuals contains a list of visuals

       each visual
       - may have a node. The node tells us exactly what the visual represents
       - has a dict of actors. On of them is always called "main"
       - each actor
           - may have an ActorType property. This is yet another way to tell what kind of feature the visual represents

        
        Updates the visibility settings for all of the actors

        A visual can be hidden completely by setting visible to false
        An actor can be hidden depending on the actor-type using


Creating and updating actors
-----------------------------

Creating and updating of actors is done by Viewport:

When a new viewport has been created:
- create_world_actors : Creates the global scenery

When new nodes are added to the screen:
- create_visuals      : Creates actors for nodes in the scene that do not yet have one

When the nodes in the scene have moved:
- position_visuals    : Updates the positions of existing visuals
                        Removes visuals for which the node is no longer present in the scene
                        Applies scaling for non-physical actors
                        Updates the geometry for visuals where needed (meshes)
                        Updates the "paint_state" property for tanks and contact nodes (see paint)
                        
When the nodes in the screen have changed:                    
- add_new_actors_to_screen:
                        Checks all visuals for actors that are not yet added to the screen. Adds them
                        Checks for Visual and Mesh nodes that need to be reloaded by checking _new_mesh
                            if so then only reloads the main component; the other components are handled by (position_visuals)                                                    
  
Painting

-  update_painting : paints all actors of a visual according to the node-type
                     and paint-definition in VieportSettings (called internally when needed)
-  update_visibility : updates the paint for all non-selected nodes
                       updates the outlines
-  update_outlines : Updates the outlines of all actors
                     Hides outlines for invisble actors, except if they are xray

Painting definition

Paint is stored in a nested dictionary.

painters['node-class']['actor_key']

- Some actors may change paint based on their state. This state gets post-fixed to the node-class
    - Tanks will change color based on their fill
        empty
        partial
        full
        freeflooding
    - Contact-balls will change color based on contact or not 
        free
        contact
  
  for these nodes the entry becomes:
    painters['node-class:paint_state']['actor_key']
  

"""

import vtkmodules.qt

from DAVE.settings_visuals import (
    ViewportSettings,
    ActorSettings,
    RESOLUTION_SPHERE,
    RESOLUTION_ARROW,
    COLOR_BG1,
    COLOR_BG2,
    COLOR_WATER,
    TEXTURE_SEA,
    VISUAL_BUOYANCY_PLANE_EXTEND,
    COLOR_SELECT,
    LIGHT_TEXTURE_SKYBOX,
    ALPHA_SEA,
)


vtkmodules.qt.PyQtImpl = "PySide2"

import vedo as vp  # ref: https://github.com/marcomusy/vedo

# vp.settings.renderLinesAsTubes = True

import DAVE.scene as vf
import DAVE.scene as dn

from typing import List

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


def transform_from_point(x, y, z):
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
    """Updates the points of a line-actor"""

    pts = line_actor._polydata.GetPoints()

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
        line_actor._polydata.SetLines(_lines)
        line_actor._polydata.SetPoints(_points)

        line_actor._polydata.Modified()


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
    the structure before creating by removed duplicate vertices"""
    unique_vertices = np.unique(vertices, axis=0)

    if len(unique_vertices) != len(vertices):  # reconstruct faces and vertices
        unique_vertices, indices = np.unique(vertices, axis=0, return_inverse=True)
        f = np.array(faces)
        better_faces = indices[f]
        actor = vp.Mesh([unique_vertices, better_faces])
    else:
        actor = vp.Mesh([vertices, faces])

    return actor


def vp_actor_from_obj(filename):
    # load the data
    filename = str(filename)
    source = vtk.vtkOBJReader()
    source.SetFileName(filename)
    # clean the data
    con = vtk.vtkCleanPolyData()
    con.SetInputConnection(source.GetOutputPort())
    con.Update()
    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInputConnection(con.GetOutputPort())
    mapper.Update()

    # We are not importing textures and materials.
    # Set color to 'w' to enforce an uniform color
    vpa = vp.Mesh(mapper.GetInputAsDataSet(), c="w")  # need to set color here

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
    """A VisualActor is the visual representation of a node or the global environment

    node is a reference to the node it represents. If node is None then this is the global environment ("scenery")

    a VisualActor can contain a number of vtk actors or vedo-actors. These are stored in a dictionary

    An visualActor may have a label_actor. This is a 2D annotation

    The appearance of a visual may change when it is selected. This is handled by select and deselect



    """

    def __init__(self, actors: dict, node):

        # check if 'main' is available
        if "main" not in actors:
            raise ValueError(
                f"one of the actors shall be called main, but got only keys: {actors.keys()}"
            )

        self.actors = actors  # dict of vedo actors. There shall be one called 'main'
        self.node = node  # Node
        self.label_actor = None

        self.paint_state = ""  # some nodes change paint depending on their state

        self._is_selected = False
        self._is_sub_selected = (
            False  # parent of this object is selected - render transparent
        )

    def select(self):
        if self._is_selected:
            return

        for key, actor in self.actors.items():
            actor.color(COLOR_SELECT)

        self._is_selected = True

    def make_transparent(self):
        """Makes an actor transparent - this can be done when a parent node is selected"""

        for a in self.actors.values():
            a.alpha(0.4)

    def on(self):
        for a in self.actors.values():
            a.on()

    def off(self):
        for a in self.actors.values():
            a.off()

    @property
    def visible(self):
        return self.actors["main"].GetVisibility()

    def setLabelPosition(self, position):
        if self.label_actor is not None:
            self.label_actor.SetAttachmentPoint(*position)

    def setLabel(self, txt):
        if self.label_actor is None:
            la = vtk.vtkCaptionActor2D()
            la.SetCaption(txt)

            position = self.actors["main"].GetPosition()

            la.SetAttachmentPoint(*position)

            la.SetPickable(True)

            cap = la.GetTextActor().GetTextProperty()
            la.GetTextActor().SetPickable(True)

            size = 0.02

            cap.SetColor(0, 0, 0)
            la.SetWidth(100 * size)
            la.SetHeight(size)
            la.SetPosition(-size / 2, -size / 2)
            la.SetBorder(False)
            cap.SetBold(True)
            cap.SetItalic(False)

            la.no_outline = True

            self.label_actor = la

        else:
            self.label_actor.SetCaption(txt)

        return self.label_actor


class Viewport:
    """
    Viewport provides a view of a Scene.

    Use:
    v = Viewport(scene)
    v.show()


    """

    def __init__(self, scene, jupyter=False):
        self.scene = scene
        self.visuals: List[VisualActor] = list()
        self.outlines: List[VisualOutline] = list()
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

        self.settings = ViewportSettings()

        self.quick_updates_only = (
            False  # Do not perform slow updates ( make animations quicker)
        )

        self._wavefield = None
        """WaveField object"""

    @staticmethod
    def show_as_qt_app(s):
        from PySide2.QtWidgets import QWidget, QApplication

        app = QApplication()
        widget = QWidget()
        widget.show()

        from DAVE.settings_visuals import PAINTERS_DEFAULT

        v = Viewport(scene=s)
        v.settings.painter_settings = PAINTERS_DEFAULT
        v.show_embedded(widget)
        v.quick_updates_only = False

        v.create_world_actors()
        v.create_visuals()
        v.add_new_actors_to_screen()
        v.position_visuals()
        v.update_visibility()

        app.exec_()

    def show_only_labels_of_nodes_type(self, node_types):
        for vis in self.visuals:
            on = False

            if node_types is not None:
                if isinstance(vis.node, node_types):
                    on = True

            if vis.label_actor is not None:
                vis.label_actor.SetVisibility(on)

    def update_outlines(self):
        """Updates the outlines of all actors in the viewport

        Update comprises
        - setting the visibility
            An outline copies the visibility of its parent actor.
            Except if the parent actor has a property "xray" which is set to true
        - removing obsolete outlines
        - adding new outlines
        - updating the transforms

        """
        if self.screen is None:
            return

        # Hide and quit if only doing quick updates
        if self.quick_updates_only:
            for outline in self.outlines:
                outline.outline_actor.SetVisibility(False)
            return

        # Control outline visibility
        for outline in self.outlines:
            if getattr(outline.parent_vp_actor, "xray", False):
                outline.outline_actor.SetVisibility(True)
            else:
                if outline.parent_vp_actor.GetVisibility():
                    outline.outline_actor.SetVisibility(True)
                else:
                    outline.outline_actor.SetVisibility(False)

        # list of already existing outlines
        _outlines = [a.parent_vp_actor for a in self.outlines]

        # loop over actors, add outlines if needed
        for vp_actor in self.screen.actors:

            if isinstance(
                vp_actor.GetProperty(), vtkmodules.vtkRenderingCore.vtkProperty2D
            ):  # annotations
                continue

            if vp_actor.GetProperty().GetRepresentation() == 1:  # wireframe
                continue

            if getattr(vp_actor, "no_outline", False):
                continue

            data = vp_actor.GetMapper().GetInputAsDataSet()
            if isinstance(data, vtk.vtkPolyData):
                # this actor can have an outline
                if vp_actor not in _outlines:
                    # create outline and add to self.outlines

                    tr = vtk.vtkTransformPolyDataFilter()

                    tr.SetInputData(data)

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
                    actor.GetProperty().SetLineWidth(self.settings.outline_width)

                    # print(f'Added outline for {vp_actor}')

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

                record.outline_actor.SetVisibility(
                    getattr(record.parent_vp_actor, "xray", False)
                    or record.parent_vp_actor.GetVisibility()
                )

            else:
                # mark for deletion
                to_be_deleted.append(record)

        # Remove obsolete outlines
        to_be_deleted_actors = [oa.outline_actor for oa in to_be_deleted]
        self.screen.remove(to_be_deleted_actors)

        for record in to_be_deleted:
            self.outlines.remove(record)

    def create_world_actors(self):
        """Creates the sea"""

        world_actors = dict()

        plane = vp.Plane(pos=(0, 0, 0), normal=(0, 0, 1), sx=1000, sy=1000).c(
            COLOR_WATER
        )
        plane.texture(TEXTURE_SEA)
        plane.lighting(ambient=1.0, diffuse=0.0, specular=0.0)
        plane.alpha(0.4)

        world_actors["sea"] = plane
        world_actors["sea"].actor_type = ActorType.GLOBAL

        if self.settings.show_global:
            world_actors["sea"].on()
        else:
            world_actors["sea"].off()

        world_actors["main"] = vp.Line((0, 0, 0), (10, 0, 0)).c("red")
        world_actors["main"].actor_type = ActorType.GEOMETRY

        world_actors["y"] = vp.Line((0, 0, 0), (0, 10, 0)).c("green")
        world_actors["y"].actor_type = ActorType.GEOMETRY

        world_actors["z"] = vp.Line((0, 0, 0), (0, 0, 10)).c("blue")
        world_actors["z"].actor_type = ActorType.GEOMETRY

        v = VisualActor(world_actors, None)
        self.visuals.append(v)

        self.global_visual = v

    def deselect_all(self):

        for v in self.visuals:
            v._is_selected = False
            self.update_painting()

    def node_from_vtk_actor(self, actor):
        """
        Given a vkt actor, find the corresponding node
        Args:
            actor: vtkActor

        Returns:

        """
        for v in self.visuals:
            for a in v.actors.values():
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
            for A in V.actors.values():
                if A.actor_type in types:
                    A.off()

    def show_actors_of_type(self, types):
        for V in self.visuals:
            for A in V.actors.values():
                if A.actor_type in types:
                    A.on()

    def set_alpha(self, alpha, exclude_nodes=None):
        """Sets the alpha (transparency) of for ALL actors in all visuals except the GLOBAL actors or visuals belonging to a node in exclude_nodes"""

        if exclude_nodes is None:
            exclude_nodes = []
        for V in self.visuals:
            for A in V.actors.values():

                if V.node in exclude_nodes:
                    continue

                if A.actor_type == ActorType.GLOBAL:
                    continue
                A.alpha(alpha)

    def level_camera(self):
        self.vtkWidget.GetRenderWindow().GetRenderers().GetFirstRenderer().GetActiveCamera().SetViewUp(
            [0, 0, 1]
        )
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
        camera = (
            self.vtkWidget.GetRenderWindow()
            .GetRenderers()
            .GetFirstRenderer()
            .GetActiveCamera()
        )
        vector = np.array(vector)
        vector = vector / np.linalg.norm(vector)

        if np.linalg.norm(np.cross(vector, (0, 0, 1))) < 1e-8:
            up = (0, -1, 0)
        else:
            up = (0, 0, 1)

        camera.SetViewUp(up)
        tar = np.array(camera.GetFocalPoint())
        pos = np.array(camera.GetPosition())
        dist = np.linalg.norm(tar - pos)

        camera_position = tar - dist * vector

        camera.SetPosition(camera_position)

    def _scaled_force_vector(self, vector):

        r = np.array(vector)
        len = np.linalg.norm(r)
        if len == 0:
            return r
        if self.settings.force_do_normalize:
            r *= 1000 / len
        r *= self.settings.force_scale / 1000
        return r

    def create_visuals(self, recreate=False):
        """Creates actors for nodes in the scene that do not yet have one

        Visuals are created in their parent axis system


        Attributes:
            recreate : re-create already exisiting visuals
        """

        for N in self.scene._nodes:

            if not recreate:
                try:  # if we already have a visual, then no need to create another one
                    N.visual
                    if N.visual is not None:
                        continue
                except:
                    pass

            actors = dict()
            label_text = None

            if isinstance(N, vf.Buoyancy):

                # source-mesh : main
                # cob
                # water-plane
                # sumberged mesh

                # This is the source-mesh. Connect it to the parent
                vis = actor_from_trimesh(
                    N.trimesh._TriMesh
                )  # returns a small cube if no trimesh is defined

                vis.actor_type = ActorType.MESH_OR_CONNECTOR

                actors["main"] = vis

                # cob
                c = vp.Sphere(r=0.5, res=RESOLUTION_SPHERE)
                c.actor_type = ActorType.MESH_OR_CONNECTOR
                actors["cob"] = c

                # waterplane
                #
                (
                    minimum_x,
                    maximum_x,
                    minimum_y,
                    maximum_y,
                    minimum_z,
                    maximum_z,
                ) = N.trimesh.get_extends()

                vertices = [
                    (minimum_x, minimum_y, 0),
                    (maximum_x, minimum_y, 0),
                    (maximum_x, maximum_y, 0),
                    (minimum_x, maximum_y, 0),
                ]
                faces = [(0, 1, 2, 3)]

                p = vp.Mesh([vertices, faces])  # waterplane, ok to create like this

                p.actor_type = ActorType.NOT_GLOBAL
                actors["waterplane"] = p

            if isinstance(N, vf.Tank):

                # source-mesh
                # cog
                # filled part of mesh (added later)

                # This is the source-mesh. Connect it to the parent
                vis = actor_from_trimesh(N.trimesh._TriMesh)

                vis.actor_type = ActorType.MESH_OR_CONNECTOR

                actors["main"] = vis

                # cog
                c = vp.Sphere(r=0.1, res=RESOLUTION_SPHERE)
                c.actor_type = ActorType.MESH_OR_CONNECTOR
                actors["cog"] = c

                label_text = N.name

            if isinstance(N, vf.ContactMesh):

                # 0 : source-mesh

                # This is the source-mesh. Connect it to the parent

                vis = actor_from_trimesh(N.trimesh._TriMesh)
                if not vis:
                    vis = vp.Cube(side=0.00001)

                vis.actor_type = ActorType.MESH_OR_CONNECTOR

                vis.loaded_obj = True

                actors["main"] = vis

            if isinstance(N, vf.Visual):
                file = self.scene.get_resource_path(N.path)
                # visual = vp.vtkio.load(file)
                visual = vp_actor_from_obj(file)
                visual.loaded_obj = file
                visual.actor_type = ActorType.VISUAL
                actors["main"] = visual

            if isinstance(N, vf.Axis):
                size = 1
                ar = vp.Arrow((0, 0, 0), (size, 0, 0), res=RESOLUTION_ARROW)
                ag = vp.Arrow((0, 0, 0), (0, size, 0), res=RESOLUTION_ARROW)
                ab = vp.Arrow((0, 0, 0), (0, 0, size), res=RESOLUTION_ARROW)

                ar.actor_type = ActorType.GEOMETRY
                ag.actor_type = ActorType.GEOMETRY
                ab.actor_type = ActorType.GEOMETRY

                ar.PickableOn()
                ag.PickableOn()
                ab.PickableOn()

                actors["main"] = ar
                actors["y"] = ag
                actors["z"] = ab

            if isinstance(N, vf.RigidBody):
                size = 1

                # a rigidbody is also an axis

                box = vp_actor_from_obj(self.scene.get_resource_path("cog.obj"))

                box.actor_type = ActorType.COG
                actors["x"] = actors["main"]
                actors["main"] = box

            if isinstance(N, vf.Point):
                size = 0.5
                p = vp.Sphere(pos=(0, 0, 0), r=size / 2, res=RESOLUTION_SPHERE)
                p.actor_type = ActorType.GEOMETRY
                actors["main"] = p

                label_text = N.name

            if isinstance(N, vf.ContactBall):
                p = vp.Sphere(pos=(0, 0, 0), r=N.radius, res=RESOLUTION_SPHERE)
                p.actor_type = ActorType.MESH_OR_CONNECTOR
                p._r = N.radius
                actors["main"] = p

                point1 = (0, 0, 0)
                a = vp.Line([point1, point1], lw=5)
                a.actor_type = ActorType.MESH_OR_CONNECTOR

                actors["contact"] = a

            if isinstance(N, vf.WaveInteraction1):
                size = 2
                p = vp.Sphere(pos=(0, 0, 0), r=size / 2, res=RESOLUTION_SPHERE)
                p.actor_type = ActorType.FORCE
                actors["main"] = p

            if isinstance(N, vf.Force):

                endpoint = self._scaled_force_vector(N.force)
                p = vp.Arrow(
                    startPoint=(0, 0, 0), endPoint=endpoint, res=RESOLUTION_ARROW
                )
                p.PickableOn()
                p.actor_type = ActorType.FORCE
                p._force = endpoint

                actors["main"] = p

                endpoint = self._scaled_force_vector(N.moment)
                p = vp.Arrow(
                    startPoint=(0, 0, 0), endPoint=endpoint, res=RESOLUTION_ARROW
                )
                p.PickableOn()
                p.actor_type = ActorType.FORCE
                p._moment = endpoint
                actors["moment1"] = p

                p = vp.Arrow(
                    startPoint=0.2 * endpoint,
                    endPoint=1.2 * endpoint,
                    res=RESOLUTION_ARROW,
                )
                p.PickableOn()
                p.actor_type = ActorType.FORCE
                actors["moment2"] = p

            if isinstance(N, vf.Circle):
                axis = np.array(N.axis)
                axis /= np.linalg.norm(axis)
                p = vp.Cylinder(r=1)
                p.actor_type = ActorType.GEOMETRY

                actors["main"] = p

            if isinstance(N, vf.Cable):

                if N._vfNode.global_points:
                    a = vp.Line(N._vfNode.global_points)
                else:
                    a = vp.Line([(0, 0, 0), (0, 0, 0.1), (0, 0, 0)])

                a.PickableOn()

                a.actor_type = ActorType.CABLE
                actors["main"] = a

                label_text = N.name

            if isinstance(N, vf.SPMT):

                gp = N.get_actual_global_points()
                if gp:
                    a = vp.Line(gp, lw=3)
                else:
                    a = vp.Line([(0, 0, 0), (0, 0, 0.1), (0, 0, 0)], lw=3)

                a.actor_type = ActorType.CABLE
                actors["main"] = a

            if isinstance(N, vf.Beam):

                gp = N.global_positions

                if len(gp) > 0:
                    a = vp.Line(gp)
                else:
                    a = vp.Line([(0, 0, 0), (0, 0, 0.1), (0, 0, 0)])

                a.actor_type = ActorType.CABLE
                actors["main"] = a

            if isinstance(N, vf.Connector2d):

                points = list()

                for i in range(2):
                    points.append((0, 0, 0))

                a = vp.Line(points)
                a.actor_type = ActorType.CABLE

                actors["main"] = a

            if isinstance(N, vf.LC6d):

                points = list()

                for i in range(2):
                    points.append((0, 0, 0))

                a = vp.Line(points)
                a.actor_type = ActorType.CABLE

                actors["main"] = a

            if not actors:  # no actors created
                print(f"No actors created for node {N.name}")
                continue

            va = VisualActor(actors, N)
            if label_text is not None:
                va.setLabel(N.name)
            N.visual = va

            N.visual.__just_created = True

            self.visuals.append(va)

            # self.set_default_dsa()

    def position_visuals(self):
        """When the nodes in the scene have moved:
        Updates the positions of existing visuals
        Removes visuals for which the node is no longer present in the scene
        Applies scaling for non-physical actors
        Updates the geometry for visuals where needed (meshes)
        Updates the "paint_state" property for tanks and contact nodes (see paint)"""

        to_be_removed = []

        for V in self.visuals:

            # check if the node still exists
            # if not, then remove the visual

            node = V.node
            if node not in self.scene._nodes:
                if V.actors:  # not all nodes have an actor
                    if (
                        V.actors["main"].actor_type != ActorType.GLOBAL
                    ):  # global visuals do not have a corresponding node
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
                A = V.actors["main"]

                # get the local (user set) transform
                t = vtk.vtkTransform()
                t.Identity()
                t.Translate(V.node.offset)
                t.Scale(V.node.scale)

                # # scale offset
                # scaled_offset = [V.node.offset[i] / V.node.scale[i] for i in range(3)]

                # calculate wxys from node.rotation
                r = V.node.rotation
                angle = (r[0] ** 2 + r[1] ** 2 + r[2] ** 2) ** (0.5)
                if angle > 0:
                    t.RotateWXYZ(angle, r[0] / angle, r[1] / angle, r[2] / angle)

                # elm_matrix = t.GetMatrix()

                # Get the parent matrix (if any)
                if V.node.parent is not None:
                    apply_parent_translation_on_transform(V.node.parent, t)

                A.SetUserTransform(t)
                continue

            if isinstance(V.node, vf.Circle):
                A = V.actors["main"]

                # get the local (user set) transform
                t = vtk.vtkTransform()
                t.Identity()

                # scale to flat disk
                t.Scale(V.node.radius, V.node.radius, 0.1)

                # rotate z-axis (length axis is cylinder) is direction of axis
                axis = V.node.axis / np.linalg.norm(V.node.axis)
                z = (0, 0, 1)
                rot_axis = np.cross(z, axis)
                rot_dot = np.dot(z, axis)
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
                    apply_parent_translation_on_transform(V.node.parent.parent, t)

                A.SetUserTransform(t)
                continue

            if isinstance(V.node, vf.Cable):

                # # check the number of points
                A = V.actors["main"]

                points = V.node.get_points_for_visual()

                if len(points) == 0:  # not yet created
                    continue

                update_line_to_points(A, points)

                V.setLabelPosition(np.mean(points, axis=0))

                continue

            if isinstance(V.node, vf.SPMT):

                A = V.actors["main"]

                pts = V.node.get_actual_global_points()
                if len(pts) == 0:
                    continue

                update_line_to_points(A, pts)

                continue

            if isinstance(V.node, vf.Beam):

                points = V.node.global_positions
                A = V.actors["main"]
                update_line_to_points(A, points)

                V.setLabelPosition(np.mean(points, axis=0))

                continue

            if isinstance(V.node, vf.Connector2d):
                A = V.actors["main"]

                points = list()
                points.append(node.nodeA.to_glob_position((0, 0, 0)))
                points.append(node.nodeB.to_glob_position((0, 0, 0)))

                A.points(points)

                continue

            if isinstance(V.node, vf.LC6d):
                A = V.actors["main"]

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
                V.actors["main"].SetUserTransform(t)
                V.actors["main"].SetScale(self.settings.geometry_scale)

                V.setLabelPosition(V.node.global_position)
                continue

            if isinstance(V.node, vf.ContactBall):

                V.node.update()

                t = vtk.vtkTransform()
                t.Identity()
                t.Translate(V.node.parent.global_position)

                # check radius
                if V.actors["main"]._r != V.node.radius:
                    temp = vp.Sphere(
                        pos=(0, 0, 0), r=V.node.radius, res=RESOLUTION_SPHERE
                    )
                    V.actors["main"].points(temp.points())
                    V.actors["main"]._r = V.node.radius

                V.actors["main"].SetUserTransform(t)
                # V.actors["main"].wireframe(V.node.contact_force_magnitude > 0)

                if V.node.can_contact:
                    point1 = V.node.parent.global_position
                    point2 = V.node.contactpoint
                    V.actors["contact"].points([point1, point2])
                    V.actors["contact"].on()
                else:
                    V.actors["contact"].off()

                # update paint settings
                if V.node.contact_force_magnitude > 0:  # do we have contact?
                    V.paint_state = "contact"
                else:
                    V.paint_state = "free"

                self.update_painting(V)

                continue

            if isinstance(V.node, vf.WaveInteraction1):
                t = vtk.vtkTransform()
                t.Identity()
                t.Translate(V.node.parent.to_glob_position(V.node.offset))
                V.actors["main"].SetUserTransform(t)
                V.actors["main"].SetScale(self.settings.geometry_scale)
                continue

            if isinstance(V.node, vf.Force):

                # check is the arrows are still what they should be
                if not np.all(
                    V.actors["main"]._force == self._scaled_force_vector(V.node.force)
                ):

                    self.screen.remove(V.actors["main"])

                    endpoint = self._scaled_force_vector(V.node.force)

                    p = vp.Arrow(
                        startPoint=(0, 0, 0), endPoint=endpoint, res=RESOLUTION_ARROW
                    )
                    p.PickableOn()
                    p.actor_type = ActorType.FORCE
                    p._force = endpoint

                    V.actors["main"] = p
                    self.screen.add(V.actors["main"])

                # check is the arrows are still what they should be
                if not np.all(
                    np.array(V.actors["moment1"]._moment)
                    == self._scaled_force_vector(V.node.moment)
                ):
                    self.screen.remove(V.actors["moment1"])
                    self.screen.remove(V.actors["moment2"])

                    endpoint = self._scaled_force_vector(V.node.moment)
                    p = vp.Arrow(
                        startPoint=(0, 0, 0), endPoint=endpoint, res=RESOLUTION_ARROW
                    )
                    p.PickableOn()
                    p.actor_type = ActorType.FORCE
                    p._moment = endpoint
                    V.actors["moment1"] = p

                    p = vp.Arrow(
                        startPoint=0.2 * endpoint,
                        endPoint=1.2 * endpoint,
                        res=RESOLUTION_ARROW,
                    )
                    p.PickableOn()
                    p.actor_type = ActorType.FORCE
                    V.actors["moment2"] = p
                    self.screen.add(V.actors["moment1"])
                    self.screen.add(V.actors["moment2"])

                t = V.actors["main"].getTransform()
                t.Identity()
                t.Translate(V.node.parent.global_position)
                for a in V.actors.values():
                    a.SetUserTransform(t)

                continue

            if isinstance(V.node, vf.RigidBody):

                # Some custom code to place and scale the Actor[3] of the body.
                # This actor should be placed at the CoG position and scaled to a solid steel block

                t = vtk.vtkTransform()
                t.Identity()

                if self.settings.cog_do_normalize:
                    scale = 1
                else:
                    scale = (V.node.mass / 8.050) ** (1 / 3)  # density of steel

                t.Translate(V.node.cog)
                mat4x4 = transform_to_mat4x4(V.node.global_transform)

                for A in V.actors.values():
                    A.SetUserMatrix(mat4x4)

                t.PostMultiply()
                t.Concatenate(mat4x4)

                scale = scale * self.settings.cog_scale

                V.actors["main"].SetScale(scale)
                V.actors["main"].SetUserTransform(t)

                # scale the arrows
                V.actors["x"].SetScale(self.settings.geometry_scale)
                V.actors["y"].SetScale(self.settings.geometry_scale)
                V.actors["z"].SetScale(self.settings.geometry_scale)

                continue

            if (
                isinstance(V.node, vf.Buoyancy)
                or isinstance(V.node, vf.ContactMesh)
                or isinstance(V.node, vf.Tank)
            ):
                # Source mesh update is common for all mesh-like nodes
                #

                # print(f'Updating source mesh for {V.node.name}')

                changed = False  # anything changed?

                if node.trimesh._new_mesh:
                    changed = True  # yes, mesh has changed
                    node.trimesh._new_mesh = False  # one time only

                # move the full mesh with the parent

                if node.parent is not None:
                    mat4x4 = transform_to_mat4x4(V.node.parent.global_transform)
                    current_transform = V.actors["main"].getTransform().GetMatrix()

                    # if the current transform is identical to the new one,
                    # then we do not need to change anything (creating the mesh is slow)

                    for i in range(4):
                        for j in range(4):
                            if current_transform.GetElement(i, j) != mat4x4.GetElement(
                                i, j
                            ):
                                changed = True  # yes, transform has changed
                                break

                    # Update the source-mesh position
                    #
                    # the source-mesh itself is updated in "add_new_actors_to_screen"
                    if changed:
                        V.actors["main"].SetUserMatrix(mat4x4)

                if not changed:
                    continue  # skip the other update functions

            if isinstance(V.node, vf.Buoyancy):

                ## Buoyancy has multiple actors
                #
                # actor 0 : the source mesh :: main
                # actor 1 : the CoB
                # actor 2 : the waterplane
                # actor 3 : the submerged part of the source mesh
                #

                # If we are here then either the source-mesh has been updated or the position has changed

                if self.quick_updates_only:
                    for a in V.actors.values():
                        a.off()
                    continue

                # Update the CoB
                # move the CoB to the new (global!) position
                cob = V.node.cob
                V.actors["cob"].SetUserMatrix(transform_from_point(*cob))

                # update water-plane
                x1, x2, y1, y2, _, _ = V.node.trimesh.get_extends()
                x1 -= VISUAL_BUOYANCY_PLANE_EXTEND
                x2 += VISUAL_BUOYANCY_PLANE_EXTEND
                y1 -= VISUAL_BUOYANCY_PLANE_EXTEND
                y2 += VISUAL_BUOYANCY_PLANE_EXTEND
                p1 = V.node.parent.to_glob_position((x1, y1, 0))
                p2 = V.node.parent.to_glob_position((x2, y1, 0))
                p3 = V.node.parent.to_glob_position((x2, y2, 0))
                p4 = V.node.parent.to_glob_position((x1, y2, 0))

                corners = [
                    (p1[0], p1[1], 0),
                    (p2[0], p2[1], 0),
                    (p3[0], p3[1], 0),
                    (p4[0], p4[1], 0),
                ]
                V.actors["waterplane"].points(corners)

                # Instead of updating, remove the old actor and create a new one

                # remove already existing submerged mesh (if any)
                if "submerged_mesh" in V.actors:
                    if self.screen is not None:
                        self.screen.remove(V.actors["submerged_mesh"])
                        del V.actors["submerged_mesh"]

                mesh = V.node._vfNode.current_mesh

                if mesh.nVertices > 0:  # only add when available

                    vis = actor_from_trimesh(mesh)

                    vis.actor_type = ActorType.MESH_OR_CONNECTOR
                    V.actors["submerged_mesh"] = vis
                    self.update_painting(V)

                    if self.screen is not None:
                        self.screen.add(vis)

                continue

            if isinstance(V.node, vf.ContactMesh):

                continue

            if isinstance(V.node, vf.Tank):

                ## Tank has multiple actors
                #
                # main : source-mesh
                # cog : cog
                # fluid : filled part of mesh

                # If the source mesh has been updated, then V.node.trimesh._new_mesh is True
                if V.__just_created:
                    V._visual_volume = -1

                if self.quick_updates_only:
                    for a in V.actors.values():
                        a.off()
                    continue
                else:
                    if V.node.visible:
                        for a in V.actors.values():
                            a.on()

                # Update the actors
                V.node.update()

                points = V.actors["main"].points(True)
                V.setLabelPosition(np.mean(points, axis=1))

                # Update the CoG
                # move the CoG to the new (global!) position
                V.actors["cog"].SetUserMatrix(transform_from_point(*V.node.cog))

                if V.node.volume <= 1:  # the "cog node" has a volume of
                    V.actors["cog"].off()
                else:
                    V.actors["cog"].on()

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

                    else:
                        vertices = []
                    # -------------------

                # paint settings
                if V.node.free_flooding:
                    V.paint_state = "freeflooding"
                else:
                    if V.node.fill_pct >= 95:
                        V.paint_state = "full"
                    elif V.node.fill_pct <= 5:
                        V.paint_state = "empty"
                    else:
                        V.paint_state = "partial"

                # we now have vertices and points and faces

                # do we already have an actor?
                need_new = False
                if "fluid" in V.actors:
                    # print(f'Already have an actor for {V.node.name}')
                    vis = V.actors["fluid"]
                    pts = vis._polydata.GetPoints()
                    npt = len(vertices)

                    # Update the existing actor if the number of vertices stay the same
                    # If not then delete the actor

                    # check for number of points
                    if pts.GetNumberOfPoints() == npt:
                        # print(f'setting points for {V.node.name}')
                        vis.points(vertices)

                    else:

                        if self.screen is not None:
                            self.screen.remove(V.actors["fluid"])
                            del V.actors["fluid"]
                            need_new = True
                else:
                    need_new = True

                if len(vertices) > 0:  # if we have an actor

                    if need_new:

                        # print(f'Creating new actor for for {V.node.name}')

                        vis = actor_from_vertices_and_faces(vertices, faces)

                        vis.actor_type = ActorType.MESH_OR_CONNECTOR

                        V.actors["fluid"] = vis

                        if self.screen is not None:
                            self.screen.add(vis, render=True)

                    if not V.node.visible:
                        vis.off()

                V._visual_volume = V.node.volume

                self.update_painting(V)

                continue

            if isinstance(V.node, vf.Axis):
                m44 = transform_to_mat4x4(V.node.global_transform)
                for a in V.actors.values():
                    a.SetScale(self.settings.geometry_scale)
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

            for A in V.actors.values():
                A.SetUserMatrix(mat4x4)

        acs = list()
        for V in to_be_removed:
            self.visuals.remove(V)
            acs.extend(list(V.actors.values()))
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
                for a in va.actors.values():
                    if not (a in actors):
                        to_be_added.append(a)

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

                    if file == va.actors["main"].loaded_obj:
                        continue

                    self.screen.clear(va.actors["main"])

                    # update the obj
                    va.actors["main"] = vp_actor_from_obj(file)
                    va.actors["main"].loaded_obj = file
                    va.actors["main"].actor_type = ActorType.VISUAL

                    if not va.node.visible:
                        va.actors["main"].off()

                    self.screen.add(va.actors["main"])

                if (
                    isinstance(va.node, vf.Buoyancy)
                    or isinstance(va.node, vf.ContactMesh)
                    or isinstance(va.node, vf.Tank)
                ):
                    if va.node.trimesh._new_mesh:

                        # va.node.update() # the whole scene is already updated when executing code

                        new_mesh = actor_from_trimesh(va.node.trimesh._TriMesh)
                        new_mesh.no_outline = True

                        if new_mesh is not None:
                            self.screen.clear(va.actors["main"])

                            va.actors["main"] = new_mesh
                            va.actors["main"].actor_type = ActorType.MESH_OR_CONNECTOR

                            if va.node.parent is not None:
                                tr = va.node.parent.global_transform
                                mat4x4 = transform_to_mat4x4(tr)
                                va.actors["main"].SetUserMatrix(mat4x4)

                            else:
                                print("Trimesh without a parent")

                            if not va.node.visible:
                                va.actors["main"].off()

                            self.screen.add(va.actors["main"])  # add after positioning

                            # va.node.trimesh._new_mesh = False  # is set to False by position_visuals

            # self.set_default_dsa()

    def shutdown_qt(self):
        """Stops the renderer such that the application can close without issues"""

        if self.vtkWidget:
            ren = self.vtkWidget.GetRenderWindow()
            iren = ren.GetInteractor()
            ren.Finalize()
            iren.TerminateApp()

    def setup_screen(self):
        """Creates the plotter instance and stores it in self.screen"""

        qtWidget = self.vtkWidget

        if (
            self.Jupyter and qtWidget is None
        ):  # it is possible to launch the Gui from jupyter, so check for both

            # create embedded notebook (k3d) view
            import vedo as vtkp

            vtkp.settings.embedWindow(backend="k3d")
            self.screen = vp.Plotter(axes=4, bg=COLOR_BG1, bg2=COLOR_BG2)

        else:

            if qtWidget is None:

                # create stand-alone interactive view
                import vedo as vtkp

                vtkp.settings.embedWindow(backend=None)

                self.screen = vp.plotter.Plotter(
                    interactive=True,
                    offscreen=False,
                    axes=4,
                    bg=COLOR_BG1,
                    bg2=COLOR_BG2,
                )

            else:

                # create embedded Qt view
                import vedo as vtkp

                vtkp.settings.embedWindow(backend=None)

                self.screen = vp.plotter.Plotter(
                    qtWidget=qtWidget, axes=4, bg=COLOR_BG1, bg2=COLOR_BG2
                )

    def show(self, camera=None, include_outlines=True):
        """Add actors to screen and show

        If purpose is to show embedded, then call show_embedded instead
        """
        if self.screen is None:
            raise Exception("Please call setup_screen first")

        # vp.settings.lightFollowsCamera = True

        self.create_world_actors()

        if camera is None:
            camera = dict()
            camera["viewup"] = [0, 0, 1]
            camera["pos"] = [10, -10, 5]
            camera["focalPoint"] = [0, 0, 0]

        if self.Jupyter and self.qtWidget is None:

            # show embedded
            for va in self.visuals:
                for a in va.actors.values():
                    if a.GetVisibility():
                        self.screen.add(a)

            return self.screen.show(camera=camera)

        else:

            screen = self.screen

            for va in self.visuals:
                for a in va.actors.values():
                    screen.add(a)

            if include_outlines:
                for outline in self.outlines:
                    screen.add(outline.outline_actor)

            """ For reference: this is how to load an cubemap texture

            Problem is that the default VTK orientation is not with the Z-axis up. So some magic needs to be done
            to have the cubemap and environmental light texture in the right orientation

            # load env texture
            cubemap_path_root = r'C:\\datapath\\skybox2-'

            files = [cubemap_path_root + name + '.jpg' for name in ['posx', 'negx', 'posy', 'negy', 'posz', 'negz']]

            cubemap = vtk.vtkTexture()
            cubemap.SetCubeMap(True)

            for i,file in enumerate(files):
                readerFactory = vtk.vtkImageReader2Factory()
                # textureFile = readerFactory.CreateImageReader2(file)
                textureFile = readerFactory.CreateImageReader2(r'c:\data\white.png')
                textureFile.SetFileName(r'c:\data\white.png')
                textureFile.Update()

                cubemap.SetInputDataObject(i, textureFile.GetOutput())

            # make skybox actor
            skybox = vtk.vtkSkybox()
            skybox.SetTexture(cubemap)

            self.screen.add(skybox)"""

            # Make a white skybox texture for light emission
            # cubemap = vtk.vtkTexture()
            # cubemap.SetCubeMap(True)
            #
            readerFactory = vtk.vtkImageReader2Factory()

            from pathlib import Path

            if not Path.exists(LIGHT_TEXTURE_SKYBOX):
                raise ValueError(f"No image found here: {LIGHT_TEXTURE_SKYBOX}")

            textureFile = readerFactory.CreateImageReader2(str(LIGHT_TEXTURE_SKYBOX))
            textureFile.SetFileName(str(LIGHT_TEXTURE_SKYBOX))
            textureFile.Update()
            texture = vtk.vtkTexture()
            texture.SetInputDataObject(textureFile.GetOutput())
            #
            # for i in range(6):
            #     cubemap.SetInputDataObject(i, textureFile.GetOutput())
            #

            self.screen.show(camera=camera, verbose=False)

            # texture = vtk.vtkTexture()
            # input = vtk.vtkPNGReader()
            # input.SetFileName(str(LIGHT_TEXTURE_SKYBOX))
            # input.Modified()
            # texture.SetInputDataObject(input.GetOutput())

            for r in self.screen.renderers:
                r.ResetCamera()

                r.UseImageBasedLightingOn()
                r.SetEnvironmentTexture(texture)

                # # Add SSAO
                # #
                # basicPasses = vtk.vtkRenderStepsPass()
                # ssao = vtk.vtkSSAOPass()
                # ssao.SetRadius(1)
                # ssao.SetDelegatePass(basicPasses)
                # ssao.SetBlur(True)
                # ssao.SetKernelSize(8)
                #
                # r.SetPass(ssao)
                #

                r.SetUseDepthPeeling(True)

                r.Modified()

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
        vl.setContentsMargins(0, 0, 0, 0)
        self.target_frame = target_frame
        self.vtkWidget = QVTKRenderWindowInteractor(target_frame)

        vl.addWidget(self.vtkWidget)
        target_frame.setLayout(vl)

        self.setup_screen()
        screen = self.show()

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

        screen.mouseRightClickFunction = self.onMouseRight

    def _leftmousepress(self, iren, event):
        """Implements a "fuzzy" mouse pick function"""

        if self.mouseLeftEvent is not None:

            pos = self.screen.interactor.GetEventPosition()

            picker = vtk.vtkPropPicker()

            for j in range(5):

                if j == 0:
                    x, y = 0, 0
                elif j == 1:
                    x, y = -1, 1
                elif j == 2:
                    x, y = -1, -1
                elif j == 3:
                    x, y = 1, 1
                else:
                    x, y = 1, -1

                if picker.Pick(pos[0] + 2 * x, pos[1] + 2 * y, 0, self.screen.renderer):
                    actor = picker.GetActor()  # gives an Actor
                    if actor is not None:
                        self.mouseLeftEvent(actor)
                        return

                    actor = picker.GetActor2D()
                    if actor is not None:
                        self.mouseLeftEvent(actor)
                        return

    def keep_up_up(self, obj, event_type):
        """Force z-axis up"""

        camera = self.screen.camera

        up = camera.GetViewUp()
        if abs(up[2]) < 0.2:
            factor = 1 - (5 * abs(up[2]))
            camera.SetViewUp(
                factor * up[0], factor * up[1], (1 - factor) + factor * up[2]
            )
        else:
            camera.SetViewUp(0, 0, 1)

        z = camera.GetPosition()[2]
        alpha = 1
        if z < 0:

            dz = camera.GetDirectionOfProjection()[2]

            # alpha = (z + 10)/10
            alpha = 1 - (10 * dz)
            if alpha < 0:
                alpha = 0
        self.global_visual.actors["sea"].alpha(ALPHA_SEA * alpha)

    def keyPressFunction(self, obj, event):
        key = obj.GetKeySym()
        if key == "Escape":
            if self.onEscapeKey is not None:
                self.onEscapeKey()

    def refresh_embeded_view(self):
        self.vtkWidget.update()

    def update_painting(self, v):
        """Updates the painting for this visual

        Painting depends on the node type of this visual.
        The properties for the individual actors of this visual are
        stored in

        """

        ps = self.settings.painter_settings  # alias
        if ps is None:
            print("No painter settings, ugly world :(")
            return

        if v.node is not None:
            if not v.node.visible:
                for a in v.actors.values():
                    a.off()
                    a.xray = False
                return

        if v.node is None:
            node_class = "global"
        else:
            if isinstance(v.node, dn.ContactBall):
                node_class = f"ContactBall:{v.paint_state}"
            elif isinstance(v.node, dn.Tank):
                node_class = f"Tank:{v.paint_state}"
            else:
                node_class = v.node.class_name

        if node_class in ps:
            node_painter_settings = ps[node_class]
        else:
            print(f"No paint for {node_class}")
            return  # no settings available

        for key, actor in v.actors.items():

            if key in node_painter_settings:
                actor_settings = node_painter_settings[key]
            else:
                print(f"No paint for actor {node_class} {key}")
                continue

            # set the "xray" property of the actor
            actor.xray = actor_settings.xray

            # on or off
            if actor_settings.surfaceShow or actor_settings.lineWidth > 0:
                actor.on()
            else:
                actor.off()
                continue

            if actor_settings.surfaceShow:

                props = actor.GetProperty()
                props.SetInterpolationToPBR()
                props.SetRepresentationToSurface()
                props.SetColor(
                    (
                        actor_settings.surfaceColor[0] / 255,
                        actor_settings.surfaceColor[1] / 255,
                        actor_settings.surfaceColor[2] / 255,
                    )
                )
                props.SetOpacity(actor_settings.alpha)
                props.SetMetallic(actor_settings.metallic)
                props.SetRoughness(actor_settings.roughness)
            else:
                actor.GetProperty().SetRepresentationToWireframe()

            actor.lineWidth(actor_settings.lineWidth)

            if actor_settings.lineWidth > 0:
                actor.lineColor(
                    (
                        actor_settings.lineColor[0] / 255,
                        actor_settings.lineColor[1] / 255,
                        actor_settings.lineColor[2] / 255,
                    )
                )
            else:
                actor.GetProperty().SetLineWidth(0)

    def update_visibility(self):
        """Updates the settings of the viewport to reflect the settings in self.settings.painter_settings"""

        for v in self.visuals:
            if not (v._is_selected or v._is_sub_selected):
                self.update_painting(v)

        self.update_outlines()


class WaveField:
    def __init__(self):
        self.actor = None
        self.pts = None
        self.nt = 0
        self.elevation = None

        self.texture = vtk.vtkTexture()
        input = vtk.vtkJPEGReader()
        input.SetFileName(TEXTURE_SEA)
        self.texture.SetInputConnection(input.GetOutputPort())
        self.ttp = vtk.vtkTextureMapToPlane()

    def update(self, t):
        t = np.mod(t, self.period)
        i = int(self.nt * t / self.period)

        count = 0
        for ix, xx in enumerate(self.x):
            for iy, yy in enumerate(self.y):
                self.pts.SetPoint(count, xx, yy, self.elevation[iy, ix, i])
                count += 1
        self.pts.Modified()

    def create_waveplane(
        self,
        wave_direction,
        wave_amplitude,
        wave_length,
        wave_period,
        nt,
        nx,
        ny,
        dx,
        dy,
    ):

        x = np.linspace(-dx, dx, nx)
        y = np.linspace(-dy, dy, ny)
        xv, yv = np.meshgrid(x, y)

        u = np.array(
            (np.cos(np.deg2rad(wave_direction)), np.sin(np.deg2rad(wave_direction)))
        )

        dist_phasor = np.exp(1j * (xv * u[0] + yv * u[1]) * (2 * np.pi / wave_length))

        t = np.linspace(0, wave_period, nt)
        time_phasor = np.exp(-1j * (2 * np.pi * t / wave_period))

        elevation = np.zeros((*xv.shape, nt))

        for i in range(nt):
            elevation[:, :, i] = wave_amplitude * np.real(time_phasor[i] * dist_phasor)

        # the vtk stuff

        # make grid
        pts = vtk.vtkPoints()
        for ix, xx in enumerate(x):
            for iy, yy in enumerate(y):
                pts.InsertNextPoint(yy, xx, elevation[iy, ix, 1])

        grid = vtk.vtkStructuredGrid()
        grid.SetDimensions(ny, nx, 1)
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
        #
        #
        actor.GetProperty().SetAmbient(1.0)
        actor.GetProperty().SetDiffuse(0.0)
        actor.GetProperty().SetSpecular(0.0)
        actor.SetTexture(self.texture)

        # alternative: use PBR
        #
        # Does not render nicely: wave grid clearly visible
        #
        # props = actor.GetProperty()
        # props.SetInterpolationToPBR()
        # props.SetMetallic(0.8)
        # props.SetRoughness(0.1)

        self.pts = pts
        self.actor = actor
        self.elevation = elevation
        self.nt = nt
        self.period = wave_period
        self.x = x
        self.y = y
