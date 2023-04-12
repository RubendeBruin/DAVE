:mod:`DAVE.gui.widget_explore`
==============================

.. py:module:: DAVE.gui.widget_explore

.. autoapi-nested-parse::

   Explore widget



Module Contents
---------------

.. py:class:: WidgetExplore

   Bases: :class:`DAVE.gui.dockwidget.guiDockWidget`

   .. method:: guiCreate(self)


      Add gui components to self.contents

      Do not fill the controls with actual values here. This is executed
      upon creation and guiScene etc are not yet available.


   .. method:: guiProcessEvent(self, event)


      Add processing that needs to be done.

      After creation of the widget this event is called with guiEventType.FULL_UPDATE


   .. method:: guiDefaultLocation(self)



   .. method:: test_evaluation(self)



   .. method:: goalseek(self)


      Setup the goal-seek code and run


   .. method:: plot(self)




