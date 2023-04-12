:mod:`DAVE.gui.widget_ballastconfiguration`
===========================================

.. py:module:: DAVE.gui.widget_ballastconfiguration

.. autoapi-nested-parse::

   WidgetBallastConfiguration



Module Contents
---------------

.. py:class:: WidgetBallastConfiguration

   Bases: :class:`DAVE.gui.dockwidget.guiDockWidget`

   .. method:: guiCreate(self)


      Add gui components to self.contents

      Do not fill the controls with actual values here. This is executed
      upon creation and guiScene etc are not yet available.


   .. method:: guiProcessEvent(self, event)


      Add processing that needs to be done.

      After creation of the widget this event is called with guiEventType.FULL_UPDATE


   .. method:: guiDefaultLocation(self)



   .. method:: selection_changed(self, cur_row, cur_col, prev_row, prev_col)



   .. method:: update_outlines(self, name='')



   .. method:: freeze_all(self)



   .. method:: unfreeze_all(self)



   .. method:: toggle_freeze(self)



   .. method:: fill_all_to(self, pct)



   .. method:: fill(self)



   .. method:: reorder_rows(self, a, b, c)



   .. method:: tankfillchanged(self, a, b)



   .. method:: tankFrozenChanged(self)



   .. method:: report_python(self)


      Runs the current tank fillings in python



