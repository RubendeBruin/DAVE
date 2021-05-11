
"""
  This Source Code Form is subject to the terms of the Mozilla Public
  License, v. 2.0. If a copy of the MPL was not distributed with this
  file, You can obtain one at http://mozilla.org/MPL/2.0/.

  Ruben de Bruin - 2019
"""

from DAVE.gui.dockwidget import *
from PySide2 import QtGui, QtCore, QtWidgets
from DAVE.gui.helpers.gridedit import GridEdit

class WidgetPainters(guiDockWidget):

    def guiCreate(self):
        """
        Add gui components to self.contents

        Do not fill the controls with actual values here. This is executed
        upon creation and guiScene etc are not yet available.

        """

        # manual:

        self.panel = QtWidgets.QWidget()
        self.buttonExport = QtWidgets.QPushButton()
        self.panelLayout = QtWidgets.QHBoxLayout()
        self.panelLayout.addWidget(self.buttonExport)
        self.panel.setLayout(self.panelLayout)

        self.buttonExport.clicked.connect(self.generate_python_code)


        self.grid = GridEdit(None)

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.panel)
        layout.addWidget(self.grid)
        self.contents.setLayout(layout)

        # create columns

        ge = self.grid # alias

        ge.addColumn('surfaceShow', bool)
        ge.addColumn('lineWidth', float)
        ge.addColumn('xray',bool)
        ge.addColumn('surfaceColor', 'color')
        ge.addColumn('alpha', float)
        ge.addColumn('lineColor', 'color')
        ge.activateColumns()

        ge.onChanged = self.update_display




    def guiProcessEvent(self, event):
        """
        Add processing that needs to be done.

        After creation of the widget this event is called with guiEventType.FULL_UPDATE
        """

        if event in [guiEventType.SELECTION_CHANGED,
                     guiEventType.FULL_UPDATE,
                     guiEventType.MODEL_STATE_CHANGED,
                     guiEventType.SELECTED_NODE_MODIFIED]:
            self.fill()

    def guiDefaultLocation(self):
        return None

    def update_display(self):
        self.gui.visual.update_visibility()
        self.gui.visual.refresh_embeded_view()

    # ======

    def fill(self):

        # Got from nested dicts to a list
        collection = []
        names = []
        keys = []

        for node_name, node_values in self.gui.visual.settings.painter_settings.items():
            for actor_name, actor_value in node_values.items():
                keys.append((node_name, actor_name))
                names.append(f'{node_name} {actor_name}')
                collection.append(actor_value)  # by reference!

        print(collection)

        self.grid.setDataSource(collection, names)

    def generate_python_code(self):

        pc = []
        pc.append('# exported python code for painters')
        pc.append('my_painers = dict()')
        for key, value in self.gui.visual.settings.painter_settings.items():

            pc.append('\n# --- paint for : {value} --- ')

            pc.append('visual = dict()')

            for sub_key, sub_value in value.items():
                pc.append('paint = ActorSettings()')

                for prop, val in sub_value.__dict__.items():
                    pc.append(f'paint.{prop} = {str(val)}')

                pc.append(f"visual['{sub_key}'] = paint")

            pc.append(f"my_painers['{key}'] = visual")

        code = '\n'.join(pc)

        self.gui.ui.teFeedback.append(code)



