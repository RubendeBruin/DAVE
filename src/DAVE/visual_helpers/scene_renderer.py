"""Scene renderer

provides a class to render a scene using VTK
"""
import logging

import numpy as np
from vtkmodules.vtkCommonDataModel import vtkPolyData
from vtkmodules.vtkCommonTransforms import vtkTransform
from vtkmodules.vtkFiltersCore import vtkCleanPolyData, vtkFeatureEdges
from vtkmodules.vtkFiltersGeneral import vtkTransformPolyDataFilter
from vtkmodules.vtkFiltersHybrid import vtkPolyDataSilhouette
from vtkmodules.vtkFiltersSources import vtkSphereSource
from vtkmodules.vtkIOImage import vtkImageReader2Factory, vtkHDRReader
from vtkmodules.vtkInteractionWidgets import vtkOrientationMarkerWidget
from vtkmodules.vtkRenderingAnnotation import vtkAxesActor
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkRenderWindow,
    vtkProperty2D,
    vtkActor2D,
    vtkRenderer,
    vtkCamera,
    vtkPolyDataMapper,
    vtkProperty,
    vtkTexture,
    vtkSkybox,
    vtkCoordinate,
)


from DAVE.settings_visuals import ViewportSettings, PAINTERS
from DAVE.visual_helpers.actors import VisualActor
from DAVE.visual_helpers.constants import *
from DAVE.visual_helpers.outlines import VisualOutline

from DAVE.visual_helpers.vtkActorMakers import (
    Mesh,
    Dummy,
    Cube,
    Sphere,
    vp_actor_from_file,
    Line,
    Arrow,
    ArrowHead,
    PlaneXY,
    actor_from_trimesh,
    Cylinder,
    Circle, actors_from_gltf,
)
from DAVE.visual_helpers.vtkHelpers import (
    transform_from_direction,
    ApplyTexture,
    transform_to_mat4x4,
    SetMatrixIfDifferent,
    create_tube_data,
    SetTransformIfDifferent,
)

import DAVE.nodes as dn


def visual_actors_from_file(file,
                            actors_dict: dict,
                            N : dn.Visual):

    actors = actors_dict # alias


    if str(file).lower().endswith('glb'):

        gltf_actors = actors_from_gltf(file)

        if not gltf_actors:
            raise ValueError(f"No actors were created from GLTF file {file}")

        actors.clear()
        actors["main"] = gltf_actors[0]
        for i, a in enumerate(gltf_actors[1:]):
            actors[f"extra_{i}"] = a

    else:

        visual = vp_actor_from_file(file)
        actors.clear()
        actors["main"] = visual

    for actor in actors.values():

        actor.loaded_obj = file
        actor.actor_type = ActorType.VISUAL

        if N.visual_outline == dn.VisualOutlineType.NONE:
            actor.no_outline = True
            actor.do_silhouette = False
        elif N.visual_outline == dn.VisualOutlineType.FEATURE:
            actor.do_silhouette = False
            actor.no_outline = False
        else:
            actor.do_silhouette = True
            actor.no_outline = False

        actor._original_color = actor.GetProperty().GetColor()


class AbstractSceneRenderer:
    """Scene renderer

    This class is used to render a scene using VTK

    Typical workflow:

    - Create a renderer
    - Create window and camera

    - Create actors (visuals) for the nodes in the scene
    - Create global actors (sea, origin)

    - Add actors to renderer

    - Create additional actors (for example a colorbar)
    - Add additional actors to renderer



    """

    def __init__(self, scene, settings: ViewportSettings = None):
        # set properties
        self.scene = scene

        self.layers: list["AnnotationLayer"] = []  # list of layers

        # define attributes
        """These are the visuals for the nodes"""
        self.node_visuals: list[VisualActor] = list()
        self.node_outlines: list[VisualOutline] = list()

        self.temporary_actors: list[vtkActor] = list()

        """These are all non-node-bound visuals , visuals for the global environment"""
        self.sea_visuals = dict()
        self.origin_visuals = dict()

        """background and environment"""
        self._skybox: vtkSkybox or None = None

        if settings is None:
            self.settings = ViewportSettings()
            self.settings.painter_settings = PAINTERS["Construction"]

        """If true, only quick updates are performed"""
        self.quick_updates_only = False

        # set up the rendering pipeline
        (
            self.renderer,
            self.renderers,
            self.camera,
            self.window,
        ) = self.create_rendering_pipeline()

        # set the default camera position
        self.set_startup_camera_position()

        self.setup_lighting_and_rendering()  # do this before creating the actors

        self.create_node_visuals(
            recreate=True
        )  # create actors for nodes, also if they already exist (in another viewport)
        self.create_world_actors()
        self.add_new_node_actors_to_screen()
        self.position_visuals()


    def create_rendering_pipeline(
        self,
    ) -> tuple[vtkRenderer, list[vtkRenderer], vtkCamera, vtkRenderWindow]:
        """Creates the rendering pipeline"""

        raise NotImplementedError("This method must be implemented in a subclass")

    def render_layers(self, *args):
        """Renders all layers"""
        for layer in self.layers:
            layer.render()

    def to_screenspace(self, pos3d):
        """Converts a 3d position to screen space [0..1 , 0..1]"""

        coo = vtkCoordinate()
        coo.SetCoordinateSystemToWorld()
        coo.SetValue(pos3d[0], pos3d[1], pos3d[2])
        display_point = coo.GetComputedViewportValue(self.renderer)

        return display_point[0], display_point[1]

    def set_startup_camera_position(self):
        """Sets the camera position at startup"""
        self.camera.SetPosition(10, -10, 5)
        self.camera.SetFocalPoint(0, 0, 0)
        self.camera.SetViewUp(0, 0, 1)

    @property
    def node_actors(self):
        """Returns all actors that are bound to nodes"""
        r = []
        for a in self.node_visuals:
            r.extend(a.actors.values())
        return r

    def add(self, actor):
        """Add an actor to the viewport"""
        self.renderer.AddActor(actor)

    def remove(self, actor: vtkActor or list[vtkActor]):
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
            # if v.label_actor == actor:
            #     return v.node

        return None

    def actor_from_node(self, node, guess=None) -> VisualActor or None:
        """Finds the VisualActor belonging to node"""

        if guess is not None:
            if guess.node == node:
                return guess

        for v in self.node_visuals:
            if v.node is node:
                return v
        return None

    def outline_from_actor(self, actor):
        """Return the actor that outlines actor if any, else returns None"""
        for a in self.node_outlines:
            if a.outlined_actor == actor:
                return a.outline_actor
        return None

    def set_painters(self, painters):
        self.settings.painter_settings = painters
        self.position_visuals()
        self.update_visibility()

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
            if getattr(outline.outlined_actor, "xray", False):
                outline.outline_actor.SetVisibility(True)
            else:
                if outline.outlined_actor.GetVisibility():
                    outline.outline_actor.SetVisibility(True)
                else:
                    outline.outline_actor.SetVisibility(False)

        # t.elapsed("Control outline visibility")


        # remove the outlines of actors that are no longer present
        # ol.outlined actor is not in buffered actors

        outlined_actors = set([ol.outlined_actor for ol in self.node_outlines])
        actors_in_scene = set(self.actors)

        obsolete_outlined_actors = outlined_actors - actors_in_scene

        if obsolete_outlined_actors:
            for obsolete_outlined in obsolete_outlined_actors:
                ol = obsolete_outlined._outline  # Note: the outlined actor has already been removed from the scene, yet it still exists (or at least the _outline prop still exists)
                self.node_outlines.remove(ol)
                self.remove(ol.outline_actor)


        # list actors that already have an outline
        _outlines = [a.outlined_actor for a in self.node_outlines]

        # Remove outlines of nodes for which the input data has changed
        # such that they can be re-created

        # buffered_actors = self.actors

        for ol in tuple(self.node_outlines):
            remove = False
            if getattr(ol.outlined_actor, "_vertices_changed", False):
                logging.info(
                    "Force-recreating outline due to vertices_changed flag on outlined actor"
                )
                remove = True


            elif getattr(ol.outlined_actor, "do_silhouette", True) != ol.is_silhouette:
                logging.info(
                    "Force-recreating outline due to silhouette/feature egde change"
                )
                remove = True

            if remove:
                self.node_outlines.remove(ol)
                self.remove(ol.outline_actor)
                _outlines.remove(ol.outlined_actor)
                ol.outlined_actor._vertices_changed = False

        # loop over actors, add outlines if needed
        for actor in self.node_actors:
            if actor in _outlines:
                continue

            if not VisualOutline.actor_needs_outline(actor):
                continue

            outline = VisualOutline(actor, camera, self.settings.outline_width)
            self.node_outlines.append(outline)
            self.add(outline.outline_actor)

            actor._outline = outline

        # Update transforms for outlines
        for outline in self.node_outlines:
            # is the parent actor still present?
            # assert (
            #     outline.outlined_actor in buffered_actors
            # ), "Parent actor not present in actors list"    # this can be really slow!
            outline.update()

    def save_to_gtlf(self, filename):
        """Exports the current scene to a gltf file"""
        from vtkmodules.vtkIOExport import vtkGLTFExporter

        self.quick_updates_only = True
        self.update_visibility()

        exporter = vtkGLTFExporter()
        exporter.SetFileName(filename)  # Set the output file name
        exporter.SetRenderWindow(self.window)  # Set the render window to export
        exporter.SetInlineData(True)  # Export data instead of external files
        exporter.Write()  # Write the render window to the file

    def save_to_obj(self, filename):
        """Exports the current scene to a obj file"""
        from vtkmodules.vtkIOExport import vtkOBJExporter

        exporter = vtkOBJExporter()
        exporter.SetFilePrefix(filename)  # Set the output prefix file name
        exporter.SetRenderWindow(self.window)  # Set the render window to export
        exporter.Write()

    def create_world_actors(self):
        """Creates the sea and global axes"""

        if "sea" in self.sea_visuals:
            raise ValueError("Global visuals already created - can not create again")

        plane = PlaneXY(size=1000)  # .c(COLOR_WATER)
        ApplyTexture(plane, TEXTURE_SEA)
        plane.SetPickable(False)
        plane.GetProperty().SetOpacity(ALPHA_SEA)
        plane.GetProperty().SetRoughness(0)

        self.sea_visuals["sea"] = plane
        self.sea_visuals["sea"].actor_type = ActorType.GLOBAL
        self.sea_visuals[
            "sea"
        ].no_outline = False  # If outlines are used, then they need to be disabled
        # when performing a zoom-fit (see zoom-all)

        self.origin_visuals["main"] = Line([(0, 0, 0), (10, 0, 0)], color=(1, 0, 0))
        self.origin_visuals["main"].actor_type = ActorType.GEOMETRY

        self.origin_visuals["y"] = Line([(0, 0, 0), (0, 10, 0)], color=(0, 1, 0))
        self.origin_visuals["y"].actor_type = ActorType.GEOMETRY

        self.origin_visuals["z"] = Line([(0, 0, 0), (0, 0, 10)], color=(0, 0, 1))
        self.origin_visuals["z"].actor_type = ActorType.GEOMETRY

        for actor in self.sea_visuals.values():
            self.renderer.AddActor(actor)
        for actor in self.origin_visuals.values():
            self.renderer.AddActor(actor)

        wind_actor = Line(
            [(-0.5, 1, 0), (0, 0, 0), (10, 0, 0)], color=[c / 255 for c in DARK_GRAY]
        )

        points = [(3 + 4 * i / 36, 0.4 * np.cos(i / 4), 0) for i in range(36)]

        current_actor = Line(
            [*points[:-1], (10, 0, 0), (9, 0.3, 0), (10, 0, 0), (9, -0.3, 0)],
            color=[c / 255 for c in BLUE_DARK],
        )

        self.current_actor = current_actor
        self.wind_actor = wind_actor

        # self.renderer.AddActor(self.colorbar_actor)

    def create_node_visuals(self, recreate=True):
        """Creates actors for nodes in the scene that do not yet have one

        Visuals are created in their parent axis system


        Attributes:
            recreate : re-create already exisiting visuals
        """

        for N in self.scene._nodes:
            #
            if not recreate:
                if getattr(N, "_visualObject", None) is not None:
                    continue

            actors = dict()
            info = None

            if isinstance(N, dn.Buoyancy):
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

                p = Mesh(
                    vertices=vertices, faces=faces
                )  # waterplane, ok to create like this

                p.actor_type = ActorType.NOT_GLOBAL
                actors["waterplane"] = p

            if isinstance(N, dn.Tank):
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

                # fluid
                actors["fluid"] = Dummy()
                actors["fluid"].SetVisibility(False)
                actors["fluid"].no_outline = True

            if isinstance(N, dn.ContactMesh):
                # 0 : source-mesh

                # This is the source-mesh. Connect it to the parent

                vis = actor_from_trimesh(N.trimesh._TriMesh)
                if not vis:
                    vis = Dummy()

                vis.actor_type = ActorType.MESH_OR_CONNECTOR
                vis.loaded_obj = True

                # disable backface
                backProp = vtkProperty()
                backProp.SetOpacity(0)
                vis.SetBackfaceProperty(backProp)

                actors["main"] = vis

            if isinstance(N, dn.Visual):
                file = self.scene.get_resource_path(N.path)
                visual_actors_from_file(file,
                                        actors_dict=actors,
                                        N=N)


            if isinstance(N, dn.Frame):
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

            if isinstance(N, dn.WindOrCurrentArea):  # wind or current area
                # circle with area 1m2
                # and then scale with sqrt(A)
                # A = pi * r**2 --> r = sqrt(1/pi)
                actors["main"] = Circle(res=36, r=np.sqrt(1 / np.pi))
                actors["main"].SetScale(np.sqrt(N.A))

            if isinstance(N, dn.RigidBody):
                # a rigidbody is also an axis

                cog = vp_actor_from_file(self.scene.get_resource_path("res: cog.obj"))
                cog.actor_type = ActorType.COG

                # switch the CoG to be the main actor
                actors["x"] = actors["main"]
                actors["main"] = cog

            if isinstance(N, dn.Point):
                size = 0.5
                p = Sphere(r=size / 2, res=RESOLUTION_SPHERE)
                p.actor_type = ActorType.GEOMETRY
                actors["main"] = p

                # footprint
                actors["footprint"] = Dummy()  # dummy

            if isinstance(N, dn.ContactBall):
                p = Sphere(r=N.radius, res=RESOLUTION_SPHERE)
                p.actor_type = ActorType.MESH_OR_CONNECTOR
                p._r = N.radius
                actors["main"] = p

                point1 = (0, 0, 0)
                a = Line([point1, point1], lw=5)
                a.actor_type = ActorType.MESH_OR_CONNECTOR

                actors["contact"] = a

            if isinstance(N, dn.WaveInteraction1):
                size = 2
                p = Sphere(r=size / 2, res=RESOLUTION_SPHERE)
                p.actor_type = ActorType.FORCE
                actors["main"] = p

            if isinstance(N, dn.Force):
                endpoint = self._scaled_force_vector(N.global_force)
                p = Arrow(startPoint=(0, 0, 0), endPoint=endpoint, res=RESOLUTION_ARROW)
                p.SetPickable(True)
                p.actor_type = ActorType.FORCE
                p._force = endpoint

                actors["main"] = p

                endpoint = self._scaled_force_vector(N.global_moment)
                p = Arrow(startPoint=(0, 0, 0), endPoint=endpoint, res=RESOLUTION_ARROW)
                p.SetPickable(True)
                p.actor_type = ActorType.FORCE
                p._moment = endpoint
                actors["moment1"] = p

                p = ArrowHead(
                    startPoint=0.96 * endpoint,
                    endPoint=1.36 * endpoint,
                    res=RESOLUTION_ARROW,
                )
                p.SetPickable(True)
                p.actor_type = ActorType.FORCE
                actors["moment2"] = p

            if isinstance(N, dn.Circle):
                axis = np.array(N.axis)
                axis /= np.linalg.norm(axis)
                p = Cylinder(r=1)
                p.actor_type = ActorType.GEOMETRY

                actors["main"] = p

            if isinstance(N, dn.Cable):
                cable_gpoints = N.get_points_for_visual()
                if cable_gpoints:
                    if N._render_as_tube:
                        # Ref: vedo / shapes.py :: Tube
                        # mapper = vtkPolyDataMapper()
                        # mapper.SetInputData(
                        #     create_tube_data(cable_gpoints, N._vfNode.diameter)
                        # )
                        #
                        # a = vtkActor()
                        # a.SetMapper(mapper)
                        #
                        # info = {"mapper": mapper}
                        a = Dummy()

                    else:
                        a = Line(cable_gpoints)
                else:
                    a = Line([(0, 0, 0), (0, 0, 0.1), (0, 0, 0)])

                a.PickableOn()

                a.actor_type = ActorType.CABLE
                actors["main"] = a

            if isinstance(N, dn.Measurement):
                a = Line([(0, 0, 0), (0, 0, 0.1), (0, 0, 0)])
                a.actor_type = ActorType.MEASUREMENT
                a.PickableOn()
                a.GetProperty().SetColor(0.5,0.5, 0.5)
                actors["main"] = a

            if isinstance(N, dn.SupportPoint):
                a = Line([(0, 0, 0), (0, 0, 0.1), (0, 0, 0)])
                a.actor_type = ActorType.MESH_OR_CONNECTOR
                a.PickableOn()
                a.GetProperty().SetColor(1, 0.5, 0)
                actors["main"] = a

                b = Sphere(r=0.25, res=RESOLUTION_SPHERE)
                actors["sphere"] = b

            if isinstance(N, dn.SPMT):
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

            if isinstance(N, dn.Beam):
                gp = N.global_positions

                if len(gp) > 0:
                    a = Line(gp)
                else:
                    a = Line([(0, 0, 0), (0, 0, 0.1), (0, 0, 0)])

                a.SetPickable(True)

                a.actor_type = ActorType.CABLE
                actors["main"] = a

            if isinstance(N, dn.Connector2d):
                points = list()

                for i in range(2):
                    points.append((0, 0, 0))

                a = Line(points)
                a.actor_type = ActorType.CABLE

                a.SetPickable(True)

                actors["main"] = a

            if isinstance(N, dn.LC6d):
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

            # va.labelUpdate(N.name)

            N._visualObject = va
            N._visualObject.__just_created = True

            self.node_visuals.append(va)

    def remove_visuals_for_deleted_nodes(self):
        """Removes visuals for nodes that have been deleted"""

        set_of_scene_nodes = set(self.scene._nodes)

        to_be_removed = []

        for V in self.node_visuals:
            if V.node not in set_of_scene_nodes:
                to_be_removed.append(V)

        for V in to_be_removed:
            self.node_visuals.remove(V)

            # remove actors
            for a in V.actors.values():
                self.renderer.RemoveActor(a)

    def position_visuals(self):
        """When the nodes in the scene have moved:
        Updates the positions of existing visuals
        Removes visuals for which the node is no longer present in the scene
        Applies scaling for non-physical actors
        Updates the geometry for visuals where needed (meshes)
        Updates the "paint_state" property for tanks and contact nodes (see paint)"""

        # self.remove_visuals_for_deleted_nodes()

        for V in self.node_visuals:
            V.update_geometry(viewport=self)

        self.update_outlines()

        for L in self.layers:
            L.update()

    def add_temporary_actor(self, actor: vtkActor):
        self.temporary_actors.append(actor)
        if self.renderer:
            self.renderer.AddActor(actor)

    def remove_temporary_actors(self):
        if self.temporary_actors:
            if self.renderer:
                for actor in self.temporary_actors:
                    self.renderer.RemoveActor(actor)
        self.temporary_actors.clear()

    def add_wind_and_current_actors(self):
        # TODO
        # self.screen.add_icon(self.wind_actor, pos=2, size=0.06)
        # self.screen.add_icon(self.current_actor, pos=4, size=0.06)
        pass

    def update_wind_and_current_actors(self):
        # update wind and current actors
        transform = vtkTransform()
        transform.Identity()
        transform.RotateZ(self.scene.wind_direction)

        SetTransformIfDifferent(self.wind_actor, transform)

        transform = vtkTransform()
        transform.Identity()
        transform.RotateZ(self.scene.current_direction)

        SetTransformIfDifferent(self.current_actor, transform)

        if self.scene.wind_velocity > 0:
            self.wind_actor.SetVisibility(True)
        else:
            self.wind_actor.SetVisibility(False)

        if self.scene.current_velocity > 0:
            self.current_actor.SetVisibility(True)
        else:
            self.current_actor.SetVisibility(False)

    def add_new_node_actors_to_screen(self):
        """Updates the screen with added actors"""



        if self.renderer:

            # t = TimeElapsed()

            actors_in_renderer = set(self.actors)
            actors_required = list()
            for va in self.node_visuals:
                actors_required.extend(va.actors.values())
            actors_required = set(actors_required)

            # difference between actors and actors_present
            to_be_added = actors_required - actors_in_renderer

            # t.elapsed("Invesigated to be added")


            if to_be_added:
                for add_me in to_be_added:
                    self.renderer.AddActor(add_me)

            # check if objs or meshes need to be re-loaded
            for va in self.node_visuals:
                if isinstance(va.node, dn.Visual):
                    try:
                        file = self.scene.get_resource_path(va.node.path)
                    except FileExistsError:
                        continue

                    if file == va.actors["main"].loaded_obj:
                        continue

                    # self.renderer.RemoveActor(va.actors["main"])
                    for A in va.actors.values():
                        self.renderer.RemoveActor(A)

                    visual_actors_from_file(file, actors_dict=va.actors, N = va.node)


                    for A in va.actors.values():
                        self.renderer.AddActor(A)

                    # self.add(va.actors["main"])

                if (
                    isinstance(va.node, dn.Buoyancy)
                    or isinstance(va.node, dn.ContactMesh)
                    or isinstance(va.node, dn.Tank)
                ):
                    if va.node.trimesh._new_mesh:
                        # va.node.update() # the whole scene is already updated when executing code

                        new_mesh = actor_from_trimesh(va.node.trimesh._TriMesh)
                        new_mesh.no_outline = True

                        if isinstance(va.node, dn.ContactMesh):
                            backProp = vtkProperty()
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
                                va.actors["main"].SetVisibility(False)

                            self.add(va.actors["main"])  # add after positioning

    def load_hdr(self, filename):
        """Loads an HDR file as environment texture"""
        texture = vtkTexture()

        reader = vtkHDRReader()
        reader.SetFileName(filename)

        texture.SetColorModeToDirectScalars()
        texture.SetInputConnection(reader.GetOutputPort())

        texture.MipmapOn()
        texture.InterpolateOn()

        ren = self.renderer  # alias

        ren.UseImageBasedLightingOn()
        ren.UseSphericalHarmonicsOn()

        ren.SetEnvironmentUp(0, 0, 1)
        ren.SetEnvironmentRight(1, 0, 0)

        ren.SetEnvironmentTexture(texture, False)

        # irradiance = ren.GetEnvMapIrradiance()
        # irradiance.SetIrradianceStep(0.3)
        if self._skybox is not None:
            self._skybox.SetTexture(texture)

    def _create_skybox_actor(self):
        if self._skybox is None:
            skybox = vtkSkybox()
            skybox.SetProjection(vtkSkybox.Sphere)
            skybox.SetFloorPlane(0, 0, 1, 0)
            skybox.SetFloorRight(1, 0, 0)

            self._skybox = skybox
        else:
            raise ValueError("Skybox already exists")

    def SkyBoxOn(self):
        """Turns on the skybox"""
        if self._skybox is not None:
            return

        self._create_skybox_actor()

        texture = self.renderer.GetEnvironmentTexture()

        if texture is None:
            raise ValueError(
                "No background texture on renderer, load a background texture before turning on the skybox"
            )

        self._skybox.SetTexture(texture)
        self.renderer.AddActor(self._skybox)

    def SkyBoxOff(self):
        """Turns off the skybox"""
        if self._skybox is None:
            return

        self.renderer.RemoveActor(self._skybox)
        self._skybox = None

    def background_color(self, color):
        """Sets the background color"""

        ren = self.renderer  # alias

        if self._skybox is not None:
            self.SkyBoxOff()
        ren.SetBackground(color)

    def setup_lighting_and_rendering(self):
        ren = self.renderer  # alias
        ren.SetAutomaticLightCreation(False)

        self.load_hdr(DEFAULT_HDR)

        ren.SetEnvironmentUp(0, 0, 1)
        ren.SetEnvironmentRight(1, 0, 0)

        ren.UseDepthPeelingOn()

        self.background_color(COLOR_BG1)

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

    def zoom_all(self):
        """Set camera to view the whole scene (ignoring the sea)"""
        sea_actor = self.sea_visuals["sea"]
        sea_actor.SetUseBounds(False)

        # find outline actor for sea
        outline_node = self.outline_from_actor(sea_actor)
        if outline_node is not None:
            outline_node.SetUseBounds(False)  # and keep at False

        # check if style can be used
        try:
            self.Style.ZoomFit()
        except AttributeError:
            try:
                self.renderer.ResetCamera()  # try to use the current renderer
            except:
                logging.warn("Can not perform zoom-all, no active renderer/camera")

        sea_actor.SetUseBounds(True)

    def update_global_visibility(self):
        """Syncs the visibility of the global actors to Viewport-settings"""

        for actor in self.sea_visuals.values():
            actor.SetVisibility(self.settings.show_sea)

        for actor in self.origin_visuals.values():
            actor.SetVisibility(self.settings.show_origin)

        # self.colorbar_actor.SetVisibility(self.settings.paint_uc)

    def update_visibility(self):
        """Updates the settings of the viewport to reflect the settings in self.settings.painter_settings"""

        for v in self.node_visuals:
            # on-off from node overrides everything
            if v.node is not None:
                for a in v.actors.values():
                    a.SetVisibility(v.node.visible)
                    if not v.node.visible:  # only disable xray, never enable
                        a.xray = False

                # v.label_actor.SetVisibility(v.node.visible)

                if not v.node.visible:
                    continue  # no need to update paint on invisible actor

            v.update_paint(self.settings)

        self.update_global_visibility()
        self.update_outlines()
