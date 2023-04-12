:mod:`DAVE.gui.widget_modeshapes`
=================================

.. py:module:: DAVE.gui.widget_modeshapes

.. autoapi-nested-parse::

   This is the widget that calculates the mode-shapes and activates or terminates the animation

   If strucutre of model changes:
    - terminate animation

   If button pressed:
    - calculate mode-shapes
    - start animation



Module Contents
---------------

.. py:class:: WidgetModeShapes

   Bases: :class:`DAVE.gui.dockwidget.guiDockWidget`

   .. method:: guiCreate(self)


      Add gui components to self.contents

      Do not fill the controls with actual values here. This is executed
      upon creation and guiScene etc are not yet available.


   .. method:: guiProcessEvent(self, event)


      Add processing that needs to be done.

      After creation of the widget this event is called with guiEventType.FULL_UPDATE


   .. method:: guiDefaultLocation(self)



   .. method:: calc_modeshapes(self)



   .. method:: quickfix(self)



   .. method:: activate_modeshape(self)



   .. method:: fill_result_table(self)



   .. method:: fill_results_table_with(self, summary)




