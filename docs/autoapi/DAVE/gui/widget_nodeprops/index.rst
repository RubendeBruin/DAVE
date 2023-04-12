:mod:`DAVE.gui.widget_nodeprops`
================================

.. py:module:: DAVE.gui.widget_nodeprops


Module Contents
---------------

.. py:class:: NodeEditor(node, callback, scene, run_code)

   NodeEditor implements a "singleton" instance of NodeEditor-derived widget.

   This widget is shown in target_layout, which is a QtLayout

   properties:
   - node : the node being edited
   - callback : a callback function being called when python code need to be executed

   A create_widget() method shall be implemented. This function creates the widget and returns it. When th

   .. method:: create_widget(self)


      Creates and returns the widget



.. py:class:: EditNode

   Bases: :class:`DAVE.gui.widget_nodeprops.NodeEditor`

   .. attribute:: _ui
      

      

   .. method:: create_widget(self)




.. py:class:: EditAxis

   Bases: :class:`DAVE.gui.widget_nodeprops.NodeEditor`

   .. attribute:: _ui
      

      

   .. method:: create_widget(self)



   .. method:: generate_code(self)




.. py:class:: EditVisual

   Bases: :class:`DAVE.gui.widget_nodeprops.NodeEditor`

   .. attribute:: _ui
      

      

   .. method:: create_widget(self)



   .. method:: generate_code(self)




.. py:class:: EditWaveInteraction

   Bases: :class:`DAVE.gui.widget_nodeprops.NodeEditor`

   .. attribute:: _ui
      

      

   .. method:: create_widget(self)



   .. method:: generate_code(self)




.. py:class:: EditBuoyancyOrContactMesh

   Bases: :class:`DAVE.gui.widget_nodeprops.NodeEditor`

   .. attribute:: _ui
      

      

   .. method:: create_widget(self)



   .. method:: generate_code(self)




.. py:class:: EditBody

   Bases: :class:`DAVE.gui.widget_nodeprops.EditAxis`

   .. attribute:: _ui
      

      

   .. method:: create_widget(self)



   .. method:: generate_code(self)




.. py:class:: EditPoi

   Bases: :class:`DAVE.gui.widget_nodeprops.NodeEditor`

   .. attribute:: _ui
      

      

   .. method:: create_widget(self)



   .. method:: generate_code(self)




.. py:class:: EditCable

   Bases: :class:`DAVE.gui.widget_nodeprops.NodeEditor`

   .. attribute:: _ui
      

      

   .. method:: create_widget(self)



   .. method:: dropEvent(self, event)



   .. method:: dragEnterEvent(self, event)



   .. method:: delete_selected(self)



   .. method:: generate_code(self)




.. py:class:: EditForce

   Bases: :class:`DAVE.gui.widget_nodeprops.NodeEditor`

   .. attribute:: _ui
      

      

   .. method:: create_widget(self)



   .. method:: generate_code(self)




.. py:class:: EditSheave

   Bases: :class:`DAVE.gui.widget_nodeprops.NodeEditor`

   .. attribute:: _ui
      

      

   .. method:: create_widget(self)



   .. method:: generate_code(self)




.. py:class:: EditHydSpring

   Bases: :class:`DAVE.gui.widget_nodeprops.NodeEditor`

   .. attribute:: _ui
      

      

   .. method:: create_widget(self)



   .. method:: generate_code(self)




.. py:class:: EditLC6d

   Bases: :class:`DAVE.gui.widget_nodeprops.NodeEditor`

   .. attribute:: _ui
      

      

   .. method:: create_widget(self)



   .. method:: generate_code(self)




.. py:class:: EditConnector2d

   Bases: :class:`DAVE.gui.widget_nodeprops.NodeEditor`

   .. attribute:: _ui
      

      

   .. method:: create_widget(self)



   .. method:: generate_code(self)




.. py:class:: EditBeam

   Bases: :class:`DAVE.gui.widget_nodeprops.NodeEditor`

   .. attribute:: _ui
      

      

   .. method:: create_widget(self)



   .. method:: generate_code(self)




.. py:class:: EditGeometricContact

   Bases: :class:`DAVE.gui.widget_nodeprops.NodeEditor`

   .. attribute:: _ui
      

      

   .. method:: create_widget(self)



   .. method:: flip(self)



   .. method:: change_side(self)



   .. method:: change_type(self)



   .. method:: generate_code(self)




.. py:class:: EditContactBall

   Bases: :class:`DAVE.gui.widget_nodeprops.NodeEditor`

   .. attribute:: _ui
      

      

   .. method:: create_widget(self)



   .. method:: dragEnter(self, event)



   .. method:: onDrop(self, event)



   .. method:: update_meshes_list(self)



   .. method:: generate_code(self)




.. py:class:: EditSling

   Bases: :class:`DAVE.gui.widget_nodeprops.NodeEditor`

   .. attribute:: _ui
      

      

   .. method:: create_widget(self)



   .. method:: dropEvent(self, event)



   .. method:: dragEnterEvent(self, event)



   .. method:: delete_selected(self)



   .. method:: generate_code(self)




.. py:class:: WidgetNodeProps

   Bases: :class:`DAVE.gui.dockwidget.guiDockWidget`

   .. method:: guiDefaultLocation(self)



   .. method:: guiCreate(self)



   .. method:: select_manager(self)



   .. method:: guiProcessEvent(self, event)



   .. method:: node_name_changed(self)


      Triggered by changing the text in the node-name widget


   .. method:: node_property_changed(self)



   .. method:: run_code(self, code)



   .. method:: select_node(self, node)




