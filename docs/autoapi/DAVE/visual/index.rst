:mod:`DAVE.visual`
==================

.. py:module:: DAVE.visual

.. autoapi-nested-parse::

   This Source Code Form is subject to the terms of the Mozilla Public
   License, v. 2.0. If a copy of the MPL was not distributed with this
   file, You can obtain one at http://mozilla.org/MPL/2.0/.

   Ruben de Bruin - 2019


   Some tools



Module Contents
---------------

.. data:: PyQtImpl
   :annotation: = PySide2

   

.. function:: transform_to_mat4x4(transform)


.. function:: transform_from_point(x, y, z)


.. function:: transform_from_direction(axis)

   Creates a transform that rotates the X-axis to the given direction
   :param axis: requested direction

   :returns: vtk.vtkTransform


.. function:: update_line_to_points(line_actor)


.. function:: apply_parent_tranlation_on_transform(parent, t)


.. function:: actor_from_trimesh(trimesh)

   Creates a vtkplotter.Actor from a pyo3d.TriMesh


.. function:: vp_actor_from_obj(filename)


.. py:class:: ActorType

   Bases: :class:`enum.Enum`

   .. attribute:: FORCE
      :annotation: = 1

      

   .. attribute:: VISUAL
      :annotation: = 2

      

   .. attribute:: GEOMETRY
      :annotation: = 3

      

   .. attribute:: GLOBAL
      :annotation: = 4

      

   .. attribute:: CABLE
      :annotation: = 5

      

   .. attribute:: NOT_GLOBAL
      :annotation: = 6

      

   .. attribute:: BALLASTTANK
      :annotation: = 7

      


.. py:class:: VisualOutline

   .. attribute:: parent_vp_actor
      

      

   .. attribute:: outline_actor
      

      

   .. attribute:: outline_transform
      

      


.. py:class:: VisualActor(actors, node)

   .. method:: select(self)



   .. method:: deselect(self)



   .. method:: make_transparent(self)



   .. method:: reset_opacity(self)



   .. method:: set_dsa(self, d, s, a)



   .. method:: on(self)



   .. method:: off(self)



   .. method:: visible(self)
      :property:




.. py:class:: Viewport(scene, jupyter=False)

   .. attribute:: screen
      

      Becomes assigned when a screen is active (or was active...)


   .. attribute:: global_visual
      

      Visuals for the global environment


   .. attribute:: onEscapeKey
      

      Function handles


   .. attribute:: _wavefield
      

      WaveField object


   .. method:: update_outlines(self)



   .. method:: create_world_actors(self)



   .. method:: deselect_all(self)



   .. method:: node_from_vtk_actor(self, actor)


      Given a vkt actor, find the corresponding node
      :param actor: vtkActor

      Returns:


   .. method:: actor_from_node(self, node)


      Finds the VisualActor belonging to node


   .. method:: add_dynamic_wave_plane(self, waveplane)



   .. method:: remove_dynamic_wave_plane(self)



   .. method:: update_dynamic_waveplane(self, t)



   .. method:: hide_actors_of_type(self, types)



   .. method:: show_actors_of_type(self, types)



   .. method:: set_alpha(self, alpha, exclude_nodes=None)


      Sets the alpha (transparency) of for ALL actors in all visuals except the GLOBAL actors or visuals belonging to a node in exclude_nodes


   .. method:: level_camera(self)



   .. method:: camera_reset(self)



   .. method:: toggle_2D(self)



   .. method:: set_camera_direction(self, vector)



   .. method:: _scaled_force_vector(self, vector)



   .. method:: create_visuals(self, recreate=False)


      Visuals are created in their parent axis system

      .. attribute:: recreate

         re-create already exisiting visuals


   .. method:: position_visuals(self)


      All visuals are aligned with their node


   .. method:: add_new_actors_to_screen(self)


      Updates the screen with added actors


   .. method:: shutdown_qt(self)


      Stops the renderer such that the application can close without issues


   .. method:: setup_screen(self, qtWidget=None)


      Creates the plotter instance and stores it in self.screen


   .. method:: show(self, qtWidget=None, camera=None)


      Add actors to screen and show


   .. method:: onMouseLeft(self, info)



   .. method:: zoom_all(self)



   .. method:: onMouseRight(self, info)



   .. method:: show_embedded(self, target_frame)


      target frame : QFrame


   .. method:: _leftmousepress(self, iren, event)


      Implements a "fuzzy" mouse pick function


   .. method:: keep_up_up(self, obj, event_type)


      Force z-axis up


   .. method:: keyPressFunction(self, obj, event)



   .. method:: refresh_embeded_view(self)



   .. method:: update_visibility(self)


      Updates the visibility settings for all of the actors

      A visual can be hidden completely by setting visible to false
      An actor can be hidden depending on the actor-type using

      self.show_geometry = True
      self.show_force = True
      self.show_visual = True
      self.show_global = False


   .. method:: set_dsa(self, d, s, a)



   .. method:: set_default_dsa(self)




.. py:class:: WaveField

   .. method:: update(self, t)



   .. method:: create_waveplane(self, wave_direction, wave_amplitude, wave_length, wave_period, nt, nx, ny, dx, dy)




.. data:: wavefield
   

   

