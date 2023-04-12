:mod:`DAVE.gui.widget_nodetree`
===============================

.. py:module:: DAVE.gui.widget_nodetree


Module Contents
---------------

.. py:class:: NodeTreeWidget

   Bases: :class:`DAVE.gui.dockwidget.QtWidgets.QTreeWidget`

   .. method:: dragEnterEvent(self, event)



   .. method:: dragMoveEvent(self, event)



   .. method:: dropEvent(self, event)



   .. method:: startDrag(self, supportedActions)




.. py:class:: WidgetNodeTree

   Bases: :class:`DAVE.gui.dockwidget.guiDockWidget`

   .. method:: guiCreate(self)



   .. method:: guiProcessEvent(self, event)



   .. method:: dragDropCallback(self, drop, onto, event)



   .. method:: tree_select_node(self, index)



   .. method:: item_clicked(self, data)



   .. method:: rightClickTreeview(self, point)



   .. method:: update_selection(self)



   .. method:: update_node_data_and_tree(self)


      Updates the tree and assembles the node-data

      This data is obtained from scene.nodes and assumes that
      each of the nodes has a visual assigned to it.



