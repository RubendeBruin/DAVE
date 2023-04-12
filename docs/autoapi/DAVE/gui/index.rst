:mod:`DAVE.gui`
===============

.. py:module:: DAVE.gui


Subpackages
-----------
.. toctree::
   :titlesonly:
   :maxdepth: 3

   forms/index.rst
   helpers/index.rst


Submodules
----------
.. toctree::
   :titlesonly:
   :maxdepth: 1

   dockwidget/index.rst
   element_widgets/index.rst
   main/index.rst
   new_node_dialog/index.rst
   standard_assets/index.rst
   widget_airy/index.rst
   widget_ballastconfiguration/index.rst
   widget_ballastsolver/index.rst
   widget_ballastsystemselect/index.rst
   widget_derivedproperties/index.rst
   widget_dynamic_properties/index.rst
   widget_explore/index.rst
   widget_modeshapes/index.rst
   widget_nodeprops/index.rst
   widget_nodetree/index.rst
   widget_plot/index.rst
   widget_selection_action/index.rst
   widget_stability_disp/index.rst
   widget_tank_order/index.rst
   widget_template_example/index.rst


Package Contents
----------------

.. py:class:: Gui(scene=None, splash=None, app=None, geometry_scale=-1, cog_scale=-1)

   .. attribute:: _animation_start_time
      

      Time at start of the simulation in seconds (system-time)


   .. attribute:: _animation_length
      :annotation: = 0

      The length of the animation in seconds


   .. attribute:: _animation_loop
      :annotation: = False

      Animation is a loop


   .. attribute:: _animation_final_dofs
      

      DOFS at termination of the animation


   .. attribute:: _animation_keyframe_interpolation_object
      

      Object that can be called with a time and yields the dofs at that time. t should be [0..._animation_length]


   .. attribute:: _animation_paused
      :annotation: = False

      Animation paused


   .. attribute:: _animation_available
      :annotation: = False

      Animation available


   .. attribute:: selected_nodes
      :annotation: = []

      A list of selected nodes (if any)


   .. attribute:: scene
      

      Reference to a scene


   .. attribute:: visual
      

      Reference to a viewport


   .. attribute:: guiWidgets
      

      Dictionary of all created guiWidgets (dock-widgets)


   .. method:: copy_screenshot_code(self)



   .. method:: escPressed(self)



   .. method:: savepoint_restore(self)



   .. method:: activate_workspace(self, name)



   .. method:: import_browser(self)



   .. method:: animation_running(self)


      Returns true is an animation is running


   .. method:: timerEvent(self, a, b)



   .. method:: animation_speed_change(self)



   .. method:: animation_activate_time(self, t)



   .. method:: animation_terminate(self, keep_current_dofs=False)



   .. method:: animation_start(self, t, dofs, is_loop, final_dofs=None, do_not_reset_time=False, show_animation_bar=True)


      Start an new animation

      :param t: List of times at keyframes
      :param dofs: List of dofs at keyframes
      :param is_loop: Should animation be played in a loop (bool)
      :param final_dofs: [optional] DOFS to be set when animation is finished or terminated. Defaults to last keyframe
      :param do_not_reset_time: do not reset the time when starting the animation, this means the loop continues where it was.


   .. method:: animation_pause(self)


      Pauses a running animation


   .. method:: animation_continue(self)



   .. method:: animation_pause_or_continue_click(self)


      Pauses or continues the animation


   .. method:: animation_change_time(self)



   .. method:: onClose(self)



   .. method:: show_exception(self, e)



   .. method:: run_code(self, code, event)


      Runs the provided code

      If succesful, add code to history
      If not, set code as current code


   .. method:: stop_solving(self)



   .. method:: solve_statics(self)



   .. method:: animate_change(self, old_dof, new_dof, n_steps)


      Animates from old_dof to new_dofs in n_steps


   .. method:: to_blender(self)



   .. method:: toggle_show_global(self)



   .. method:: toggle_show_global_from_menu(self)



   .. method:: toggle_show_visuals(self)



   .. method:: camera_set_direction(self, vector)



   .. method:: camera_reset(self)



   .. method:: undo_solve_statics(self)



   .. method:: clear(self)



   .. method:: open(self)



   .. method:: menu_import(self)



   .. method:: menu_save(self)



   .. method:: tidy_history(self)



   .. method:: give_clean_history(self)



   .. method:: menu_save_actions(self)



   .. method:: feedback_copy(self)



   .. method:: history_copy(self)



   .. method:: clear_code(self)



   .. method:: generate_scene_code(self)



   .. method:: run_code_in_teCode(self)



   .. method:: rightClickViewport(self, point)



   .. method:: openContextMenyAt(self, node_name, globLoc)



   .. method:: new_axis(self)



   .. method:: new_body(self)



   .. method:: new_poi(self)



   .. method:: new_cable(self)



   .. method:: new_force(self)



   .. method:: new_sheave(self)



   .. method:: new_linear_connector(self)



   .. method:: new_connector2d(self)



   .. method:: new_beam(self)



   .. method:: new_linear_hydrostatics(self)



   .. method:: new_visual(self)



   .. method:: new_buoyancy_mesh(self)



   .. method:: new_contactmesh(self)



   .. method:: new_contactball(self)



   .. method:: new_waveinteraction(self)



   .. method:: new_something(self, what)



   .. method:: view3d_select_element(self, vtkactor)



   .. method:: visual_update_selection(self)



   .. method:: guiEmitEvent(self, event, sender=None)



   .. method:: guiSelectNode(self, node_name)



   .. method:: show_guiWidget(self, name, widgetClass)



   .. method:: refresh_3dview(self)




