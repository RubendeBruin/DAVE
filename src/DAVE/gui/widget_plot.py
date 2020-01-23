"""
This is an example/template of how to setup a new dockwidget
"""

"""
  This Source Code Form is subject to the terms of the Mozilla Public
  License, v. 2.0. If a copy of the MPL was not distributed with this
  file, You can obtain one at http://mozilla.org/MPL/2.0/.

  Ruben de Bruin - 2019
"""

from DAVE.gui.dockwidget import *
from PySide2 import QtGui, QtCore, QtWidgets
from PySide2.QtWidgets import QApplication, QVBoxLayout, QWidget
import DAVE.scene as nodes
import DAVE.settings as ds

import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure

class MatplotlibWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.fig = Figure()
        self.canvas = FigureCanvas(self.fig)
        self.toolbar = NavigationToolbar(self.canvas, self)
        lay = QVBoxLayout(self)
        lay.addWidget(self.toolbar)
        lay.addWidget(self.canvas)

        self.ax = self.fig.add_subplot(111)

        self.ax.text(0,0,"Graph")
        self.ax.cla()

        self.canvas.draw()


class WidgetExample(guiDockWidget):

    def guiCreate(self):
        """
        Add gui components to self.contents

        Do not fill the controls with actual values here. This is executed
        upon creation and guiScene etc are not yet available.

        """

        # manual:

        self.plot = MatplotlibWidget(self.contents)
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.plot)
        self.contents.setLayout(layout)



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
        return QtCore.Qt.DockWidgetArea.RightDockWidgetArea

    # ======

    def fill(self):
        pass
        # # display the name of the selected node
        # if self.guiSelection:
        #     self.label.setText(self.guiSelection[0].name)  # access to selected nodes

    def action(self):
        pass
        # # never executed in the example
        # self.guiRunCodeCallback("print('Hi, I am an exampe')", guiEventType.SELECTED_NODE_MODIFIED)   # call the callback to execute code
        # self.guiSelectNode('Node-name') # to globally select a node


if __name__ == '__main__':

    import sys

    app = QApplication(sys.argv)
    matplotlib_widget = MatplotlibWidget()
    matplotlib_widget.show()
    sys.exit(app.exec_())