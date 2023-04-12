:mod:`DAVE.gui.widget_ballastsolver`
====================================

.. py:module:: DAVE.gui.widget_ballastsolver

.. autoapi-nested-parse::

   Ballastsolver



Module Contents
---------------

.. py:class:: WidgetBallastSolver

   Bases: :class:`DAVE.gui.dockwidget.guiDockWidget`

   .. method:: guiCreate(self)


      Add gui components to self.contents

      Do not fill the controls with actual values here. This is executed
      upon creation and guiScene etc are not yet available.


   .. method:: guiProcessEvent(self, event)


      Add processing that needs to be done.

      After creation of the widget this event is called with guiEventType.FULL_UPDATE


   .. method:: guiDefaultLocation(self)



   .. method:: assert_selection_valid(self)



   .. method:: ballast_system_selected(self)



   .. method:: determineRequiredBallast(self)



   .. method:: solveBallast(self)



   .. method:: draftChanged(self)




