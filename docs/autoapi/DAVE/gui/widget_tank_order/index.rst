:mod:`DAVE.gui.widget_tank_order`
=================================

.. py:module:: DAVE.gui.widget_tank_order

.. autoapi-nested-parse::

   This is an example/template of how to setup a new dockwidget



Module Contents
---------------

.. py:class:: WidgetTankOrder

   Bases: :class:`DAVE.gui.dockwidget.guiDockWidget`

   .. method:: guiCreate(self)


      Add gui components to self.contents

      Do not fill the controls with actual values here. This is executed
      upon creation and guiScene etc are not yet available.


   .. method:: guiProcessEvent(self, event)


      Add processing that needs to be done.

      After creation of the widget this event is called with guiEventType.FULL_UPDATE


   .. method:: guiDefaultLocation(self)



   .. method:: run_action(self, action)



   .. method:: point(self, additional='')



   .. method:: fill(self)




