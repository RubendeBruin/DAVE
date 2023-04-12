:mod:`DAVE.gui.widget_plot`
===========================

.. py:module:: DAVE.gui.widget_plot

.. autoapi-nested-parse::

   This is an example/template of how to setup a new dockwidget



Module Contents
---------------

.. py:class:: MatplotlibWidget(parent=None)

   Bases: :class:`PySide2.QtWidgets.QWidget`


.. py:class:: WidgetExample

   Bases: :class:`DAVE.gui.dockwidget.guiDockWidget`

   .. method:: guiCreate(self)


      Add gui components to self.contents

      Do not fill the controls with actual values here. This is executed
      upon creation and guiScene etc are not yet available.


   .. method:: guiProcessEvent(self, event)


      Add processing that needs to be done.

      After creation of the widget this event is called with guiEventType.FULL_UPDATE


   .. method:: guiDefaultLocation(self)



   .. method:: fill(self)



   .. method:: action(self)




.. data:: app
   

   

