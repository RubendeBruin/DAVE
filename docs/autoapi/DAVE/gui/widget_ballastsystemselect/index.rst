:mod:`DAVE.gui.widget_ballastsystemselect`
==========================================

.. py:module:: DAVE.gui.widget_ballastsystemselect

.. autoapi-nested-parse::

   WidgetBallastSystemSelect



Module Contents
---------------

.. py:class:: WidgetBallastSystemSelect

   Bases: :class:`DAVE.gui.dockwidget.guiDockWidget`

   .. method:: guiCreate(self)


      Add gui components to self.contents

      Do not fill the controls with actual values here. This is executed
      upon creation and guiScene etc are not yet available.


   .. method:: guiProcessEvent(self, event)


      Add processing that needs to be done.

      After creation of the widget this event is called with guiEventType.FULL_UPDATE


   .. method:: guiDefaultLocation(self)



   .. method:: updateRPD(self)



   .. method:: fill(self)



   .. method:: ballast_system_selected(self)




