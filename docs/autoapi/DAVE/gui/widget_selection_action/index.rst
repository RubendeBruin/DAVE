:mod:`DAVE.gui.widget_selection_action`
=======================================

.. py:module:: DAVE.gui.widget_selection_action

.. autoapi-nested-parse::

   This Source Code Form is subject to the terms of the Mozilla Public
   License, v. 2.0. If a copy of the MPL was not distributed with this
   file, You can obtain one at http://mozilla.org/MPL/2.0/.

   Ruben de Bruin - 2019



Module Contents
---------------

.. py:class:: WidgetSelectionActions

   Bases: :class:`DAVE.gui.dockwidget.guiDockWidget`

   .. method:: guiCreate(self)


      Add gui components to self.contents

      Do not fill the controls with actual values here. This is executed
      upon creation and guiScene etc are not yet available.


   .. method:: guiProcessEvent(self, event)


      Add processing that needs to be done.

      After creation of the widget this event is called with guiEventType.FULL_UPDATE


   .. method:: guiDefaultLocation(self)



   .. method:: find_nodes(self, types)


      Returns nodes of given types. Only the first node per given type is returned and no duplicates.

      Returns None if not all types could be found


   .. method:: all_of_type(self, types)



   .. method:: fill(self)




