"""
  This Source Code Form is subject to the terms of the Mozilla Public
  License, v. 2.0. If a copy of the MPL was not distributed with this
  file, You can obtain one at http://mozilla.org/MPL/2.0/.

  Ruben de Bruin - 2019

"""
import logging
from copy import copy
from warnings import warn

from enum import Enum

from scipy.spatial import ConvexHull

# enforce PySide6
import vtkmodules.qt
vtkmodules.qt.PyQtImpl = "PySide6"


from vtkmodules.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
from vtkmodules.vtkRenderingCore import vtkActor2D, vtkRenderer, vtkCamera, vtkRenderWindowInteractor
from vtkmodules.vtkRenderingOpenGL2 import vtkOpenGLFXAAPass, vtkSSAOPass


from DAVE.visual_helpers.vtkBlenderLikeInteractionStyle import BlenderStyle
from DAVE.visual_helpers.vtkHelpers import (
    create_shearline_actors,
    create_momentline_actors,
)

from DAVE.visual_helpers.vtkActorMakers import Mesh, Dummy, Cube, Sphere, vp_actor_from_file

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
    TEXTURE_WAVEPLANE,
    COLOR_SELECT_255,
    UC_CMAP,
    OUTLINE_WIDTH,
    COLOR_OUTLINE,
    COLOR_BG1_GUI,
    COLOR_BG2_GUI,
)

import DAVE.scene as vf
import DAVE.scene as dn
import DAVE.settings_visuals


"""
visual visualizes a scene using vtk and vedo helpers

Basic data structure:

Viewport
 - node_visuals (VisualActors)
    - [node] -> reference to corresponding node 
    - actors [dict]
        - [ActorType]
        
        <the appearance of these visuals is determined by painters which are activated by update_visibility>
        
 - temporary_visuals (VisualActors)
    These are visuals that are temporary added to the viewport. For example a moment-line or boundary edges of a mesh
    these are automatically deleted when the viewport is updated (position_visuals) 
        
 - private visuals (wave-plane, etc)
 
       <the appearance of these visuals is determined by Viewport>
       <set by update_global_visibility which is called bt update_visibility>




Viewport
============

Viewport is the main class which handles the viewport (ie: Plotter).
It supports embedded plotting (in a qt application) as well as stand-alone or via Jupyter or Renders (offscreen renderer)

A viewport contains VisualActors.


Visual-Actors
------------------

this class contains a reference to a Node (optional) and a dict of actors

Dict of actors: On of them is always called "main". This is used, among others, to determine the position of the label (if any) 
    

a visual actor can be hidden by setting visible to False

each of the individual vtk-plotter actors has a "actor_type" property which is a enum ActorType.

ActorType is used for general control of these actors. At the moment this is only Scaling which is implemented in "position visuals"


VISUALS FOR NODES
==================



     each actor:
       - may have an ActorType property. This is yet another way to tell what kind of feature the visual represents
    - has a property "node"
   


- A visual representing a Node has its node property set to a node (not None).
  appearance of these nodes is controlled by Painters.
- The visibility of these nodes may be overridden by the .visible setting of the node.
  
  
   
    Updates the visibility settings for all of the actors
    A visual can be hidden completely by setting visible to false
    An actor can be hidden depending on the actor-type using ????  <-- obsolete
        
        


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
                     Hides outlines for invisible actors, except if they are xray

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
  
Temporary actors
-----------------
Actors (anything derived from vtkActor) can be added to the viewport by calling
add_temporary_actor. Temporary actors are automatically removed when the viewport
is updated or can be removed manually be calling remove_temporary_actors


Outlines
=========
Outlines are individual actors. They attach to a actor and do not have a reference to the node or the other actors
of the node.
They copy the data of the actor that they outline when they are created. They update based on the global-transform of
the referenced actor.

If the geometry of the referenced actor (ie the vertices) have changed then the outline needs to be re-created.
In that case the ._vertices_changed = True flag of the outlined actor should be set. 

"""

from DAVE.visual_helpers.vtkHelpers import *




class Viewport:
    """
    Viewport provides a view of a Scene.

    Use:
    v = Viewport(scene)
    v.show()


    """

    def __init__(self, scene):
        self.scene = scene
        self.renderer: vtkRenderer or None = None
        self.renderers : list[vtkRenderer] = list()
        self.camera : vtkCamera or None = None
        self.interactor : vtkRenderWindowInteractor or None = None

        """SSAO effect"""
        self._ssao_on = False
        self.SSAO_fxaaP: vtkOpenGLFXAAPass or None = None
        self.SSAO_pass: vtkSSAOPass or None = None

        """These are the visuals for the nodes"""
        self.node_visuals: list[VisualActor] = list()
        self.node_outlines: list[VisualOutline] = list()

        """These are the temporary visuals"""
        self.temporary_actors: list[vtkActor] = list()

        """These are all non-node-bound visuals , visuals for the global environment"""
        self.sea_visuals = dict()
        self.origin_visuals = dict()

        self.vtkWidget = None
        """Qt viewport, if any"""

        self.settings = ViewportSettings()

        self.quick_updates_only = (
            False  # Do not perform slow updates ( make animations quicker)
        )

        self._wavefield = None
        """WaveField object"""

        # colorbar image
        png = vtk.vtkPNGReader()
        png.SetFileName(
            str(Path(__file__).parent / "resources" / "uc_colorbar_smaller.png")
        )
        png.Update()

        imagemapper = vtk.vtkImageMapper()
        imagemapper.SetInputData(png.GetOutput())
        imagemapper.SetColorWindow(255)
        imagemapper.SetColorLevel(127.5)

        image = vtkActor2D()
        image.SetMapper(imagemapper)
        image.SetPosition(0, 0.95)

        self.colorbar_actor = image
        """The colorbar for UCs is a static image"""

        self.cycle_next_painterset = None
        self.cycle_previous_painterset = None

        self.Style = BlenderStyle()
        self.Style.callbackCameraDirectionChanged = self._camera_direction_changed
        self.Style.callbackCameraMoved = self._camera_moved
        self.Style.callbackAnyKey = self.keyPressFunction

    def add(self, actor):
        """Add an actor to the viewport"""
        self.renderer.AddActor(actor)

    def remove(self, actor : vtkActor or list[vtkActor]):
        """Remove an actor from the viewport"""
        if isinstance(actor, vtkActor):
            self.renderer.RemoveActor(actor)
        else:
            for a in actor:
                self.renderer.RemoveActor(a)

    @property
    def actors(self):
        """Returns all actors in the viewport"""
        return self.renderer.GetActors()

    def set_painters(self, painters):
        self.settings.painter_settings = painters
        self.position_visuals()
        self.update_visibility()

    def show_as_qt_app(self, painters=None):
        from PySide6.QtWidgets import QWidget, QApplication

        app = QApplication.instance() or QApplication()

        widget = QWidget()

        if painters is None:
            from DAVE.settings_visuals import PAINTERS

            painters = PAINTERS["Construction"]

        v = self

        v.settings.painter_settings = painters

        v.show_embedded(widget)
        v.quick_updates_only = False

        v.create_node_visuals()

        v.position_visuals()
        v.add_new_node_actors_to_screen()  # position visuals may create new actors
        v.update_visibility()

        v.zoom_all()

        widget.show()

        from PySide6.QtCore import QEventLoop

        if not QEventLoop().isRunning():
            app.exec_()

    def save_to_gtlf(self, filename):
        """Exports the current scene to a gltf file"""
        from vtkmodules.vtkIOExport import vtkGLTFExporter

        self.quick_updates_only = True
        self.update_visibility()

        exporter = vtkGLTFExporter()
        exporter.SetFileName(filename)  # Set the output file name
        exporter.SetRenderWindow(self.screen.window)  # Set the render window to export
        exporter.SetInlineData(True)  # Export data instead of external files
        exporter.Write()  # Write the render window to the file

    def save_to_obj(self, filename):
        """Exports the current scene to a obj file"""
        from vtkmodules.vtkIOExport import vtkOBJExporter

        exporter = vtkOBJExporter()
        exporter.SetFilePrefix(filename)  # Set the output prefix file name
        exporter.SetRenderWindow(self.screen.window)  # Set the render window to export
        exporter.Write()

    def initialize_node_drag(self, nodes, text_info=None):
        # Initialize dragging on selected node

        actors = []
        outlines = []

        for node in nodes:
            node_actor = self.actor_from_node(node)
            if node_actor is not None:
                actors.extend([*node_actor.actors.values()])
                outlines.extend(
                    [
                        ol.outline_actor
                        for ol in self.node_outlines
                        if ol.parent_vp_actor in actors
                    ]
                )

        self.Style.StartDragOnProps([*actors, *outlines], info_text=text_info)

    def add_temporary_actor(self, actor: vtk.vtkActor):
        self.temporary_actors.append(actor)
        if self.renderer:
            self.renderer.AddActor(actor)

    def remove_temporary_actors(self):
        if self.temporary_actors:
            if self.renderer:
                for actor in self.temporary_actors:
                    self.renderer.RemoveActor(actor)
        self.temporary_actors.clear()

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
        if self.renderer is None:
            return

        camera = self.camera
        if camera is None:
            print("No camera")

        # Hide and quit if only doing quick updates
        if self.quick_updates_only:
            for outline in self.node_outlines:
                outline.outline_actor.SetVisibility(False)
            return

        # Control outline visibility
        for outline in self.node_outlines:
            if getattr(outline.parent_vp_actor, "xray", False):
                outline.outline_actor.SetVisibility(True)
            else:
                if outline.parent_vp_actor.GetVisibility():
                    outline.outline_actor.SetVisibility(True)
                else:
                    outline.outline_actor.SetVisibility(False)

        # list of already existing outlines
        _outlines = [a.parent_vp_actor for a in self.node_outlines]

        # Remove outlines of nodes for which the input data has changed
        # such that they can be re-created

        to_be_deleted = []

        for ol in self.node_outlines:
            if getattr(ol.parent_vp_actor, "_vertices_changed", False):
                logging.info(
                    "Force-recreating outline due to vertices_changed flag on outlined actor"
                )
                to_be_deleted.append(ol)
                _outlines.remove(ol.parent_vp_actor)
                ol.parent_vp_actor._vertices_changed = False

        # loop over actors, add outlines if needed
        for vp_actor in self.actors:
            if isinstance(
                vp_actor.GetProperty(), vtkmodules.vtkRenderingCore.vtkProperty2D
            ):  # annotations
                continue

            try:
                if vp_actor.GetProperty().GetRepresentation() == 1:  # wireframe
                    continue
            except:
                continue

            if getattr(vp_actor, "no_outline", False):
                continue

            do_silhouette = getattr(vp_actor, "do_silhouette", True)

            data = vp_actor.GetMapper().GetInputAsDataSet()

            if isinstance(data, vtk.vtkPolyData):
                # this actor can have an outline
                if vp_actor not in _outlines:
                    # create outline and add to self.outlines

                    # clean the input data to ensure continuous faces
                    # # clean the data

                    con = vtk.vtkCleanPolyData()
                    con.SetInputData(data)
                    con.Update()

                    tr = vtk.vtkTransformPolyDataFilter()

                    tr.SetInputData(con.GetOutput())

                    temp = vtk.vtkTransform()
                    temp.Identity()
                    tr.SetTransform(temp)
                    tr.Update()

                    if do_silhouette:
                        ol = vtk.vtkPolyDataSilhouette()
                        ol.SetInputConnection(tr.GetOutputPort())
                        ol.SetEnableFeatureAngle(True)
                        ol.SetCamera(camera)
                        ol.SetBorderEdges(True)
                    else:
                        ol = vtk.vtkFeatureEdges()
                        ol.SetColoring(False)  # does not seem to do anything
                        ol.SetInputConnection(tr.GetOutputPort())

                        ol.ExtractAllEdgeTypesOff()
                        ol.BoundaryEdgesOn()
                        ol.SetFeatureAngle(25)
                        ol.FeatureEdgesOn()

                    mapper = vtk.vtkPolyDataMapper()
                    mapper.SetInputConnection(ol.GetOutputPort())
                    mapper.ScalarVisibilityOff()  # No colors!

                    actor = vtk.vtkActor()
                    actor.SetMapper(mapper)
                    actor.GetProperty().SetColor(0, 0, 0)
                    actor.GetProperty().SetLineWidth(self.settings.outline_width)

                    self.add(actor)  # vtk actor

                    # store
                    record = VisualOutline()
                    record.outline_actor = actor
                    record.outline_transform = tr
                    record.parent_vp_actor = vp_actor
                    vp_actor._outline = record
                    self.node_outlines.append(record)

                    record.outline_actor.outlined_actor = vp_actor  # insert a ref to the original actor, used when clicking

        # Update transforms for outlines

        for record in self.node_outlines:
            # is the parent actor still present?
            if record.parent_vp_actor in self.actors:
                record.update()

            else:
                # mark for deletion
                to_be_deleted.append(record)

        # Remove obsolete outlines
        to_be_deleted_actors = [oa.outline_actor for oa in to_be_deleted]
        self.remove(to_be_deleted_actors)

        for record in to_be_deleted:
            self.node_outlines.remove(record)

    def focus_on(self, position):
        """Places the camera focus on position"""

        c = self.camera

        cur_focus = np.array(c.GetFocalPoint())

        if np.linalg.norm(cur_focus - np.array(position)) < 1e-3:
            # already has focus, zoom in
            distance = np.array(c.GetPosition()) - cur_focus
            c.SetPosition(cur_focus + 0.9 * distance)
            self.renderer.ResetCameraClippingRange()

        else:
            self.camera.SetFocalPoint(position)

    def create_world_actors(self):
        """Creates the sea and global axes"""

        if "sea" in self.sea_visuals:
            raise ValueError("Global visuals already created - can not create again")

        plane = PlaneXY(size=1000) # .c(COLOR_WATER)
        ApplyTexture(plane, TEXTURE_SEA)
        plane.GetProperty().SetAmbient(1.0)
        plane.GetProperty().SetDiffuse(0.0)
        plane.GetProperty().SetSpecular(0.0)
        plane.GetProperty().SetSpecularPower(1e-7)

        self.sea_visuals["sea"] = plane
        self.sea_visuals["sea"].actor_type = ActorType.GLOBAL
        self.sea_visuals[
            "sea"
        ].no_outline = False  # If outlines are used, then they need to be disabled
        # when performing a zoom-fit (see zoom-all)

        self.origin_visuals["main"] = Line([(0, 0, 0), (10, 0, 0)], color=(1,0,0))
        self.origin_visuals["main"].actor_type = ActorType.GEOMETRY

        self.origin_visuals["y"] = Line([(0, 0, 0), (0, 10, 0)], color = (0,1,0))
        self.origin_visuals["y"].actor_type = ActorType.GEOMETRY

        self.origin_visuals["z"] = Line([(0, 0, 0), (0, 0, 10)], color = (0,0,1))
        self.origin_visuals["z"].actor_type = ActorType.GEOMETRY

        for actor in self.sea_visuals.values():
            self.renderer.AddActor(actor)
        for actor in self.origin_visuals.values():
            self.renderer.AddActor(actor)

        wind_actor = Line([ (-0.5, 1, 0),
                            (0, 0, 0),
                            (10, 0, 0)],
                          color = [c/255 for c in DAVE.settings_visuals._DARK_GRAY])

        points = [(3 + 4 * i / 36, 0.4 * np.cos(i / 4), 0) for i in range(36)]

        current_actor = Line([*points[:-1],
                                 (10, 0, 0),
                                 (9, 0.3, 0),
                                 (10, 0, 0),
                                 (9, -0.3, 0)],
                                 color = [c/255 for c in DAVE.settings_visuals._BLUE_DARK])

        self.current_actor = current_actor
        self.wind_actor = wind_actor

        self.renderer.AddActor(self.colorbar_actor)

    def add_wind_and_current_actors(self):
        # TODO
        # self.screen.add_icon(self.wind_actor, pos=2, size=0.06)
        # self.screen.add_icon(self.current_actor, pos=4, size=0.06)
        pass

    def deselect_all(self):
        for v in self.node_visuals:
            if v._is_selected:
                v._is_selected = False
                v.update_paint(self.settings)

    def node_from_vtk_actor(self, actor):
        """
        Given a vkt actor, find the corresponding node
        Args:
            actor: vtkActor

        Returns:

        """
        # print(actor)

        outlined_actor = getattr(actor, "outlined_actor", None)
        if outlined_actor is not None:
            return self.node_from_vtk_actor(outlined_actor)

        for v in self.node_visuals:
            for a in v.actors.values():
                if a == actor:
                    return v.node
            if v.label_actor == actor:
                return v.node

        return None

    def actor_from_node(self, node) -> VisualActor or None:
        """Finds the VisualActor belonging to node"""
        for v in self.node_visuals:
            if v.node is node:
                return v
        return None

    def outline_from_actor(self, actor):
        """Return the actor that outlines actor if any, else returns None"""
        for a in self.node_outlines:
            if a.parent_vp_actor == actor:
                return a.outline_actor
        return None

    def add_dynamic_wave_plane(self, waveplane):
        self.remove_dynamic_wave_plane()
        self.add(waveplane.actor)
        self.add(waveplane.line_actor)
        self._wavefield = waveplane

        self.settings.show_sea = False
        #
        # if self.settings.show_global = False:
        #     self._staticwaveplane = True
        #     self.global_visual.off()
        # else:
        #     self._staticwaveplane = False

    def remove_dynamic_wave_plane(self):
        if self._wavefield is not None:
            self.remove(self._wavefield.actor)
            self.remove(self._wavefield.line_actor)
            self._wavefield = None

            # if self._staticwaveplane:
            #     self.global_visual.on()

    def update_dynamic_waveplane(self, t):
        if self._wavefield is not None:
            self._wavefield.update(t)

    def hide_actors_of_type(self, types):
        for V in self.node_visuals:
            for A in V.actors.values():
                if A.actor_type in types:
                    A.off()

    def show_actors_of_type(self, types):
        for V in self.node_visuals:
            for A in V.actors.values():
                if A.actor_type in types:
                    A.on()

    def set_alpha(self, alpha, exclude_nodes=None):
        """Sets the alpha (transparency) of for ALL actors in all visuals except the GLOBAL actors or visuals belonging to a node in exclude_nodes"""

        if exclude_nodes is None:
            exclude_nodes = []
        for V in self.node_visuals:
            for A in V.actors.values():
                if V.node in exclude_nodes:
                    continue

                if A.actor_type == ActorType.GLOBAL:
                    continue
                A.alpha(alpha)

    def toggle_2D(self):
        """Toggles between 2d and 3d mode. Returns True if mode is 2d after toggling"""
        self.Style.ToggleParallelProjection()
        return bool(self.renderer.GetActiveCamera().GetParallelProjection())

    def _scaled_force_vector(self, vector):
        r = np.array(vector)
        len = np.linalg.norm(r)
        if len == 0:
            return r
        if self.settings.force_do_normalize:
            r *= 1000 / len
        r *= self.settings.force_scale / 1000
        return r

    def create_node_visuals(self, recreate=False):
        """Creates actors for nodes in the scene that do not yet have one

        Visuals are created in their parent axis system


        Attributes:
            recreate : re-create already exisiting visuals
        """

        for N in self.scene._nodes:
            if not recreate:
                try:  # if we already have a visual, then no need to create another one
                    N._visualObject
                    if N._visualObject is not None:
                        continue
                except:
                    pass

            actors = dict()
            info = None

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
                c = Sphere(r=0.5, res=RESOLUTION_SPHERE)
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

                p = Mesh([vertices, faces])  # waterplane, ok to create like this

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
                c = Sphere(r=0.1, res=RESOLUTION_SPHERE)
                c.actor_type = ActorType.MESH_OR_CONNECTOR
                actors["cog"] = c

            if isinstance(N, vf.ContactMesh):
                # 0 : source-mesh

                # This is the source-mesh. Connect it to the parent

                vis = actor_from_trimesh(N.trimesh._TriMesh)
                if not vis:
                    vis = Dummy()

                vis.actor_type = ActorType.MESH_OR_CONNECTOR
                vis.loaded_obj = True

                # disable backface
                backProp = vtk.vtkProperty()
                backProp.SetOpacity(0)
                vis.SetBackfaceProperty(backProp)

                actors["main"] = vis

            if isinstance(N, vf.Visual):
                file = self.scene.get_resource_path(N.path)
                visual = vp_actor_from_file(file)

                if N.visual_outline == dn.VisualOutlineType.NONE:
                    visual.no_outline = True
                    visual.do_silhouette = False
                elif N.visual_outline == dn.VisualOutlineType.FEATURE:
                    visual.do_silhouette = False
                    visual.no_outline = False
                else:
                    visual.do_silhouette = True
                    visual.no_outline = False

                visual.loaded_obj = file
                visual.actor_type = ActorType.VISUAL
                actors["main"] = visual

            if isinstance(N, vf.Frame):
                size = 1
                ar = Arrow((0, 0, 0), (size, 0, 0), res=RESOLUTION_ARROW)
                ag = Arrow((0, 0, 0), (0, size, 0), res=RESOLUTION_ARROW)
                ab = Arrow((0, 0, 0), (0, 0, size), res=RESOLUTION_ARROW)

                ar.actor_type = ActorType.GEOMETRY
                ag.actor_type = ActorType.GEOMETRY
                ab.actor_type = ActorType.GEOMETRY

                ar.SetPickable(True)
                ag.SetPickable(True)
                ab.SetPickable(True)

                actors["main"] = ar
                actors["y"] = ag
                actors["z"] = ab

                # footprint
                actors["footprint"] = Dummy()

            if isinstance(N, vf.WindOrCurrentArea):  # wind or current area
                # circle with area 1m2
                # and then scale with sqrt(A)
                # A = pi * r**2 --> r = sqrt(1/pi)
                actors["main"] = Circle(res=36, r=np.sqrt(1 / np.pi))
                actors["main"].SetScale(np.sqrt(N.A))

            if isinstance(N, vf.RigidBody):
                # a rigidbody is also an axis

                cog = vp_actor_from_file(self.scene.get_resource_path("res: cog.obj"))
                cog.actor_type = ActorType.COG

                # switch the CoG to be the main actor
                actors["x"] = actors["main"]
                actors["main"] = cog

            if isinstance(N, vf.Point):
                size = 0.5
                p = Sphere(r=size / 2, res=RESOLUTION_SPHERE)
                p.actor_type = ActorType.GEOMETRY
                actors["main"] = p

                # footprint
                actors["footprint"] = Dummy()  # dummy

            if isinstance(N, vf.ContactBall):
                p = Sphere(r=N.radius, res=RESOLUTION_SPHERE)
                p.actor_type = ActorType.MESH_OR_CONNECTOR
                p._r = N.radius
                actors["main"] = p

                point1 = (0, 0, 0)
                a = Line([point1, point1], lw=5)
                a.actor_type = ActorType.MESH_OR_CONNECTOR

                actors["contact"] = a

            if isinstance(N, vf.WaveInteraction1):
                size = 2
                p = Sphere(r=size / 2, res=RESOLUTION_SPHERE)
                p.actor_type = ActorType.FORCE
                actors["main"] = p

            if isinstance(N, vf.Force):
                endpoint = self._scaled_force_vector(N.global_force)
                p = Arrow(
                    startPoint=(0, 0, 0), endPoint=endpoint, res=RESOLUTION_ARROW
                )
                p.pickable(True)()
                p.actor_type = ActorType.FORCE
                p._force = endpoint

                actors["main"] = p

                endpoint = self._scaled_force_vector(N.global_moment)
                p = Arrow(
                    startPoint=(0, 0, 0), endPoint=endpoint, res=RESOLUTION_ARROW
                )
                p.pickable(True)()
                p.actor_type = ActorType.FORCE
                p._moment = endpoint
                actors["moment1"] = p

                p = ArrowHead(
                    startPoint=0.96 * endpoint,
                    endPoint=1.36 * endpoint,
                    res=RESOLUTION_ARROW,
                )
                p.pickable(True)()
                p.actor_type = ActorType.FORCE
                actors["moment2"] = p

            if isinstance(N, vf.Circle):
                axis = np.array(N.axis)
                axis /= np.linalg.norm(axis)
                p = Cylinder(r=1)
                p.actor_type = ActorType.GEOMETRY

                actors["main"] = p

            if isinstance(N, vf.Cable):
                if N._vfNode.global_points:
                    if N._render_as_tube:
                        # Ref: vedo / shapes.py :: Tube
                        gp = N._vfNode.global_points  # alias

                        mapper = vtk.vtkPolyDataMapper()
                        mapper.SetInputData(create_tube_data(gp, N._vfNode.diameter))

                        a = vtk.vtkActor()
                        a.SetMapper(mapper)

                        info = {"mapper": mapper}

                    else:
                        a = Line(N._vfNode.global_points)
                else:
                    a = Line([(0, 0, 0), (0, 0, 0.1), (0, 0, 0)])

                a.PickableOn()

                a.actor_type = ActorType.CABLE
                actors["main"] = a

            if isinstance(N, vf.SPMT):
                # SPMT
                #
                # 'main' is a cube spanning the upper surface of the SPMT
                # the center is at the center
                # the length extents half the distance between the axles
                # the width extents half the wheel_width

                WHEEL_WIDTH = 1.0  # [m, a wheel is actually a pair of wheels]
                TOP_THICKNESS = 0.5  # m

                top_length = N.n_length * N.spacing_length
                top_width = (N.n_width - 1) * N.spacing_width + WHEEL_WIDTH

                actors["main"] = Cube(side=1)

                gp = N.get_actual_global_points()
                if gp:
                    a = Line(gp, lw=3)
                else:
                    a = Line([(0, 0, 0), (0, 0, 0.1), (0, 0, 0)], lw=3)

                a.actor_type = ActorType.CABLE
                a.SetPickable(True)
                actors["line"] = a

            if isinstance(N, vf.Beam):
                gp = N.global_positions

                if len(gp) > 0:
                    a = Line(gp)
                else:
                    a = Line([(0, 0, 0), (0, 0, 0.1), (0, 0, 0)])

                a.SetPickable(True)

                a.actor_type = ActorType.CABLE
                actors["main"] = a

            if isinstance(N, vf.Connector2d):
                points = list()

                for i in range(2):
                    points.append((0, 0, 0))

                a = Line(points)
                a.actor_type = ActorType.CABLE

                a.SetPickable(True)

                actors["main"] = a

            if isinstance(N, vf.LC6d):
                points = list()

                for i in range(2):
                    points.append((0, 0, 0))

                a = Line(points)
                a.actor_type = ActorType.CABLE

                a.SetPickable(True)

                actors["main"] = a

            if not actors:  # no actors created
                if not isinstance(N, dn.Manager):
                    print(f"No actors created for node {N.name}")
                continue

            try:
                va = VisualActor(actors, N)
            except ValueError as M:
                raise ValueError(f"Error creating visual for node {N.name} : {M}")


            va.info = info

            va.labelUpdate(N.name)

            N._visualObject = va
            N._visualObject.__just_created = True

            self.node_visuals.append(va)

    def position_visuals(self):
        """When the nodes in the scene have moved:
        Updates the positions of existing visuals
        Removes visuals for which the node is no longer present in the scene
        Applies scaling for non-physical actors
        Updates the geometry for visuals where needed (meshes)
        Updates the "paint_state" property for tanks and contact nodes (see paint)"""

        to_be_removed = []

        for V in self.node_visuals:
            # check if the node still exists
            # if not, then remove the visual

            node = V.node
            if node not in self.scene._nodes:
                if V.actors:  # not all nodes have an actor
                    if (
                        getattr(V.actors["main"], "actor_type", None)
                        != ActorType.GLOBAL
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

            V.update_geometry(viewport=self)

        acs = list()
        for V in to_be_removed:
            self.node_visuals.remove(V)
            acs.extend(list(V.actors.values()))
            if V.label_actor is not None:
                acs.append(V.label_actor)

        acs.extend(self.temporary_actors)

        if acs:
            self.remove(acs)

        self._camera_direction_changed()

        self.update_outlines()

        # update wind and current actors
        transform = vtk.vtkTransform()
        transform.Identity()
        transform.RotateZ(self.scene.wind_direction)

        SetTransformIfDifferent(self.wind_actor, transform)

        transform = vtk.vtkTransform()
        transform.Identity()
        transform.RotateZ(self.scene.current_direction)

        SetTransformIfDifferent(self.current_actor, transform)

        if self.scene.wind_velocity > 0:
            self.wind_actor.SetScale(1.0)
        else:
            self.wind_actor.SetScale(0.0)

        if self.scene.current_velocity > 0:
            self.current_actor.SetScale(1.0)
        else:
            self.current_actor.SetScale(0.0)

    def add_new_node_actors_to_screen(self):
        """Updates the screen with added actors"""

        to_be_added = []

        if self.renderer:
            actors = self.actors
            for va in self.node_visuals:
                for a in va.actors.values():
                    if not (a in actors):
                        to_be_added.append(a)

                if va.label_actor is not None:
                    if va.label_actor not in actors:
                        to_be_added.append(va.label_actor)

            if to_be_added:
                for add_me in to_be_added:
                    self.renderer.AddActor(add_me)

            # check if objs or meshes need to be re-loaded
            for va in self.node_visuals:
                if isinstance(va.node, vf.Visual):
                    try:
                        file = self.scene.get_resource_path(va.node.path)
                    except FileExistsError:
                        continue

                    if file == va.actors["main"].loaded_obj:
                        continue

                    self.renderer.RemoveActor(va.actors["main"])

                    # update the obj
                    va.actors["main"] = vp_actor_from_file(file)
                    va.actors["main"].loaded_obj = file
                    va.actors["main"].actor_type = ActorType.VISUAL

                    # set the outline visibility (copy from "create")

                    if va.node.visual_outline == dn.VisualOutlineType.NONE:
                        va.actors["main"].no_outline = True
                        va.actors["main"].do_silhouette = False
                    elif va.node.visual_outline == dn.VisualOutlineType.FEATURE:
                        va.actors["main"].do_silhouette = False
                        va.actors["main"].no_outline = False
                    else:
                        va.actors["main"].do_silhouette = True
                        va.actors["main"].no_outline = False

                    if not va.node.visible:
                        va.actors["main"].off()

                    self.add(va.actors["main"])

                if (
                    isinstance(va.node, vf.Buoyancy)
                    or isinstance(va.node, vf.ContactMesh)
                    or isinstance(va.node, vf.Tank)
                ):
                    if va.node.trimesh._new_mesh:
                        # va.node.update() # the whole scene is already updated when executing code

                        new_mesh = actor_from_trimesh(va.node.trimesh._TriMesh)
                        new_mesh.no_outline = True

                        if isinstance(va.node, vf.ContactMesh):
                            backProp = vtk.vtkProperty()
                            backProp.SetOpacity(0)
                            new_mesh.SetBackfaceProperty(backProp)

                        if new_mesh is not None:
                            self.remove(va.actors["main"])

                            va.actors["main"] = new_mesh
                            va.actors["main"].actor_type = ActorType.MESH_OR_CONNECTOR

                            if va.node.parent is not None:
                                tr = va.node.parent.global_transform
                                mat4x4 = transform_to_mat4x4(tr)
                                SetMatrixIfDifferent(va.actors["main"], mat4x4)

                            else:
                                print("Trimesh without a parent")

                            if not va.node.visible:
                                va.actors["main"].off()

                            self.add(va.actors["main"])  # add after positioning

                            # va.node.trimesh._new_mesh = False  # is set to False by position_visuals

            # self.set_default_dsa()

    def shutdown_qt(self):
        """Stops the renderer such that the application can close without issues"""

        if self.vtkWidget:
            ren = self.vtkWidget.GetRenderWindow()
            iren = ren.GetInteractor()
            ren.Finalize()
            iren.TerminateApp()


    def setup_lighting_and_rendering(self):

        readerFactory = vtk.vtkImageReader2Factory()

        from pathlib import Path

        if not Path.exists(LIGHT_TEXTURE_SKYBOX):
            raise ValueError(f"No image found here: {LIGHT_TEXTURE_SKYBOX}")

        textureFile = readerFactory.CreateImageReader2(str(LIGHT_TEXTURE_SKYBOX))
        textureFile.SetFileName(str(LIGHT_TEXTURE_SKYBOX))
        textureFile.Update()
        texture = vtk.vtkTexture()
        texture.SetInputDataObject(textureFile.GetOutput())

        self._create_SSAO_pass()

        for r in self.renderers:
            r.ResetCamera()
            # r.AddLight(light)

            r.UseImageBasedLightingOn()
            r.SetEnvironmentTexture(texture)

            r.SetUseDepthPeeling(True)

            # r.SetLightFollowCamera(True)

            r.Modified()

    def show(self, include_outlines=True):
        """Add actors to screen and show

        If purpose is to show embedded, then call show_embedded instead
        """

        if self.screen is None:
            raise Exception("Please call setup_screen first")


        if self.vtkWidget is None:
            # show embedded
            for va in self.node_visuals:
                for a in va.actors.values():
                    # if a.GetVisibility():  # also invisible nodes need to be added because they may be x-rayed
                    self.screen.add(a)

            self.update_visibility()  # needs to be called after actors have been added to screen
            self.update_global_visibility()

            self.screen.resetcam = False

            for outline in self.node_outlines:
                self.screen.add(outline.outline_actor)

            return self.screen

        else:
            screen = self.screen

            for va in self.node_visuals:
                for a in va.actors.values():
                    screen.add(a)

            if include_outlines:
                for outline in self.node_outlines:
                    screen.add(outline.outline_actor)

            screen.resetcam = False

            camera = dict()
            camera["viewup"] = [0, 0, 1]
            camera["pos"] = [10, -10, 5]
            camera["focalPoint"] = [0, 0, 0]

            screen.show(camera=camera)

            return screen

    def _create_SSAO_pass(self):
        """Creates self.ssao and self.SSAO_fxaaP"""

        passes = vtk.vtkRenderPassCollection()
        passes.AddItem(vtk.vtkRenderStepsPass())

        seq = vtk.vtkSequencePass()
        seq.SetPasses(passes)

        self.ssao = vtk.vtkSSAOPass()
        self.ssao.SetDelegatePass(seq)
        self.ssao.SetBlur(True)
        self.SSAO_fxaaP = vtk.vtkOpenGLFXAAPass()  # include Anti-Aliasing

        # options = vtk.vtkFXAAOptions()
        # options.SetSubpixelBlendLimit(0.1)
        # self.SSAO_fxaaP.SetFXAAOptions(options)

        self.SSAO_fxaaP.SetDelegatePass(self.ssao)

        self._update_SSAO_settings()

    def _update_SSAO_settings(self, radius=0.005, bias=0.2, kernel_size=64):
        if self.renderer is None:
            return

        bounds = np.asarray(self.renderer.ComputeVisiblePropBounds())

        b_r = np.linalg.norm(
            [bounds[1] - bounds[0], bounds[3] - bounds[2], bounds[5] - bounds[4]]
        )

        occlusion_radius = b_r * radius
        occlusion_bias = bias

        self.ssao.SetRadius(occlusion_radius)
        self.ssao.SetBias(occlusion_bias)
        self.ssao.SetKernelSize(kernel_size)

    def EnableSSAO(self):
        # from documentation:
        # virtual void 	UseSSAOOn ()
        # virtual void 	UseSSAOOff ()
        #
        # but does not work
        if self._ssao_on:
            return

        for r in self.screen.renderers:
            r.SetPass(self.SSAO_fxaaP)
            self._update_SSAO_settings()
            r.Modified()

        self._ssao_on = True

    def DisableSSAO(self):
        if self._ssao_on == False:
            return

        for r in self.screen.renderers:
            r.SetPass(None)
            r.Modified()

        self._ssao_on = False

    def zoom_all(self):
        """Set camera to view the whole scene (ignoring the sea)"""
        sea_actor = self.sea_visuals["sea"]
        sea_actor.SetUseBounds(False)

        # find outline actor for sea
        outline_node = self.outline_from_actor(sea_actor)
        if outline_node is not None:
            outline_node.SetUseBounds(False)  # and keep at False

        # check if style can be used
        if self.Style.GetCurrentRenderer():
            self.Style.ZoomFit()
        else:
            try:
                self.renderer.ResetCamera()  # try to use the current renderer
            except:
                warn("Can not perform zoom-all, no active renderer/camera")

        sea_actor.SetUseBounds(True)

    def onMouseRight(self, info):
        if self.mouseRightEvent is not None:
            self.mouseRightEvent(info)

    def show_embedded(self, target_frame):
        """target frame : QFrame"""

        from PySide6.QtWidgets import QVBoxLayout

        # add a widget to gui
        vl = QVBoxLayout()
        vl.setContentsMargins(1, 1, 1, 1)
        self.target_frame = target_frame
        self.vtkWidget = QVTKRenderWindowInteractor(target_frame)

        # change the color of the parent widget when the interactor gets/looses focus
        self.vtkWidget.focusInEvent = self.get_focus
        self.vtkWidget.focusOutEvent = self.focus_lost

        vl.addWidget(self.vtkWidget)
        target_frame.setLayout(vl)

        self.renderer = vtkRenderer()
        self.renderer.SetBackground(COLOR_BG1)

        # add all actors
        for va in self.node_visuals:
            for a in va.actors.values():
                self.renderer.AddActor(a)

        self.renwin = self.vtkWidget.GetRenderWindow()

        self.renwin.AddRenderer(self.renderer)

        iren = self.renwin.GetInteractor()
        self.interactor = iren

        style = self.Style

        self.camera = self.renderer.GetActiveCamera()

        self.renderers = [self.renderer]
        iren.SetInteractorStyle(style)
        iren.Initialize()

        iren.SetNumberOfFlyFrames(2)

        for r in self.renderers:
            r.ResetCamera()

        self.setup_lighting_and_rendering()

        self.create_world_actors()
        self.add_wind_and_current_actors()

    def get_focus(self, *args):
        # print('getting focus')
        self.target_frame.setStyleSheet("background-color: gray")

    def focus_lost(self, *args):
        # print('loosing focus')
        self.target_frame.setStyleSheet("")

    def keyPressFunction(self, key):
        """Most key-pressed are handled by the Style,

        here we override some specific ones.

        Returning True make the style ignore the key-press

        """
        KEY = key.upper()

        if KEY == "A":
            self.zoom_all()
            self.refresh_embeded_view()
            return True

        if KEY == "BRACKETLEFT":
            if self.cycle_next_painterset is not None:
                self.cycle_next_painterset()
                return True

        if KEY == "BRACKETRIGHT":
            if self.cycle_previous_painterset is not None:
                self.cycle_previous_painterset()
                return True

    def refresh_embeded_view(self):
        if self.vtkWidget is not None:
            self.vtkWidget.update()

    def update_visibility(self):
        """Updates the settings of the viewport to reflect the settings in self.settings.painter_settings"""

        for v in self.node_visuals:
            # on-off from node overrides everything
            if v.node is not None:
                for a in v.actors.values():
                    a.SetVisibility(v.node.visible)
                    if not v.node.visible:  # only disable xray, never enable
                        a.xray = False

                v.label_actor.SetVisibility(v.node.visible)

                if not v.node.visible:
                    continue  # no need to update paint on invisible actor

            v.update_paint(self.settings)

        self.update_global_visibility()
        self.update_outlines()

    def update_global_visibility(self):
        """Syncs the visibility of the global actors to Viewport-settings"""

        for actor in self.sea_visuals.values():
            actor.SetVisibility(self.settings.show_sea)

        for actor in self.origin_visuals.values():
            actor.SetVisibility(self.settings.show_origin)

        self.colorbar_actor.SetVisibility(self.settings.paint_uc)

    def _camera_direction_changed(self):
        """Gets called when the camera has moved"""

        for V in self.node_visuals:
            node = V.node

            if isinstance(node, dn.WindOrCurrentArea):
                actor = V.actors["main"]

                # calculate scale
                scale = np.sqrt(node.A)

                if node.areakind == dn.AreaKind.SPHERE:
                    direction = self.camera.GetDirectionOfProjection()
                elif node.areakind == dn.AreaKind.PLANE:
                    direction = node.direction
                    if node.parent.parent is not None:
                        direction = node.parent.parent.to_glob_direction(direction)
                else:
                    axis_direction = node.direction
                    if node.parent.parent is not None:
                        axis_direction = node.parent.parent.to_glob_direction(
                            axis_direction
                        )
                    camera_direction = self.camera.GetDirectionOfProjection()

                    # the normal of the plane need to be
                    # 1. perpendicular to "direction"
                    # 2. in the same plane as "camera direction" and "direction"

                    temp = np.cross(axis_direction, camera_direction)
                    if np.linalg.norm(temp) < 1e-6:  # axis and camera are perpendicular
                        direction = self.camera.GetViewUp()
                    else:
                        direction = np.cross(temp, axis_direction)
                        direction = direction / np.linalg.norm(direction)

                transform = transform_from_direction(
                    direction, position=node.parent.global_position, scale=scale
                )

                SetMatrixIfDifferent(actor, transform)
                if hasattr(actor, "_outline"):
                    actor._outline.update()

    def _camera_moved(self):
        if self._ssao_on:
            self._update_SSAO_settings()


class WaveField:
    def __init__(self, texture=None):
        self.actor = None
        self.pts = None
        self.elevation = None

        self.texture = vtk.vtkTexture()
        input = vtk.vtkJPEGReader()

        if texture is None:
            input.SetFileName(TEXTURE_WAVEPLANE)
            input.SetFileName(TEXTURE_WAVEPLANE)
        else:
            input.SetFileName(texture)
        self.texture.SetInputConnection(input.GetOutputPort())

        self.texture.SetRepeat(True)
        self.texture.SetEdgeClamp(True)
        self.texture.Modified()

    @property
    def nt(self):
        if self.elevation is None:
            return 0
        else:
            _, _, nt = self.elevation.shape
            return nt

    def update(self, t):
        nx, ny, nt = self.elevation.shape
        i = int(t / self.dt) % nt

        for ix in range(nx):
            for iy in range(ny):
                count = ix + iy * nx

                x, y, _ = self.pts.GetPoint(count)
                self.pts.SetPoint(count, x, y, self.elevation[ix, iy, i])

        self.pts.Modified()

        pts = getattr(self, "line_pts", None)
        if pts is not None:
            for ix in range(nx):
                x, y, _ = pts.GetPoint(ix)
                pts.SetPoint(ix, x, y, self.elevation[ix, 0, i])
            pts.Modified()

    def make_grid(self, xmin, xmax, ymin, ymax, nx, ny, wave_direction):
        """Constructs the wave-grid and stores the result in
        self.xv and self.yv.

        wave-direction is the direction in which the waves progress. Mathematical angle in [deg]
        """

        # xfactor = np.linspace(-1,1, nx)
        # xg = dx * xfactor * np.sqrt(np.abs(xfactor))
        xg = np.linspace(xmin, xmax, nx)
        yg = np.linspace(ymin, ymax, ny)

        # create a grid in direction of wave-direction
        # xv, yv = np.meshgrid(xg, yg) # pre-allocate the grid
        yv, xv = np.meshgrid(yg, xg)  # pre-allocate the grid

        for iy in range(ny):
            for ix in range(nx):
                x = xg[ix]
                y = yg[iy]

                xr = (
                    np.cos(np.deg2rad(wave_direction)) * x
                    - np.sin(np.deg2rad(wave_direction)) * y
                )
                yr = (
                    np.sin(np.deg2rad(wave_direction)) * x
                    + np.cos(np.deg2rad(wave_direction)) * y
                )

                xv[ix, iy] = xr
                yv[ix, iy] = yr

        self.yv = yv
        self.xv = xv

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
        # create the grid
        self.make_grid(-dx / 2, 1.5 * dx, -dy, dy, nx, 2, wave_direction)

        xv = self.xv  # alias
        yv = self.yv

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
        self.elevation = elevation

        self.dt = wave_period / nt

        self.create_actor()
        self.create_line_actor()

    def create_line_actor(self):
        nx, ny, nt = self.elevation.shape

        # make grid
        pts = vtk.vtkPoints()
        for ix in range(nx):
            x = self.xv[ix, 0]
            y = self.yv[ix, 0]

            pts.InsertNextPoint(x, y, self.elevation[ix, 0, 0])  # use t=0 and y=y[0]

        segments = vtk.vtkCellArray()
        segments.InsertNextCell(nx)
        for i in range(nx):
            segments.InsertCellPoint(i)

        poly = vtk.vtkPolyData()
        poly.SetPoints(pts)
        poly.SetLines(segments)

        # make mapper
        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputData(poly)

        actor = vtk.vtkActor()
        actor.SetMapper(mapper)
        actor.GetProperty().SetColor(0.0, 0.0, 0.0)
        actor.GetProperty().SetLineWidth(2)

        self.line_actor = actor
        self.line_pts = pts

    def create_actor(self):
        ny, nx, nt = self.elevation.shape

        # make grid
        pts = vtk.vtkPoints()
        for ix in range(nx):
            for iy in range(ny):
                pts.InsertNextPoint(
                    self.xv[iy, ix], self.yv[iy, ix], self.elevation[iy, ix, 1]
                )

        grid = vtk.vtkStructuredGrid()
        grid.SetDimensions(ny, nx, 1)
        grid.SetPoints(pts)

        # make mapper
        filter = vtk.vtkStructuredGridGeometryFilter()
        filter.SetInputData(grid)

        # texture stuff
        TextureCooridinates = vtk.vtkFloatArray()
        TextureCooridinates.SetNumberOfComponents(2)
        TextureCooridinates.SetName("TextureCoordinates")

        tex_repeat = 4

        for i in range(0, nx):
            for j in range(0, ny):
                TextureCooridinates.InsertNextTuple2(
                    tex_repeat * i / (nx - 1), tex_repeat * j / (ny - 1)
                )

        grid.GetPointData().SetTCoords(TextureCooridinates)

        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputConnection(filter.GetOutputPort())

        actor = vtk.vtkActor()
        actor.SetMapper(mapper)
        #
        #
        # actor.GetProperty().SetColor(0.0, 0.5, 0.5)
        actor.GetProperty().SetOpacity(0.8)
        actor.GetProperty().SetAmbient(1.0)
        actor.GetProperty().SetDiffuse(0.0)
        actor.GetProperty().SetSpecular(0.0)
        actor.SetTexture(self.texture)

        self.actor = actor
        self.pts = pts
