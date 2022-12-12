"""
This is an example/template of how to setup a new dockwidget
"""
from PySide2.QtCore import QLocale

from DAVE.gui.widget_nodeprops import svinf

"""
  This Source Code Form is subject to the terms of the Mozilla Public
  License, v. 2.0. If a copy of the MPL was not distributed with this
  file, You can obtain one at http://mozilla.org/MPL/2.0/.

  Ruben de Bruin - 2019
"""

from DAVE.gui.dockwidget import *
from PySide2 import QtGui, QtCore, QtWidgets
import DAVE.scene as nodes
import DAVE.settings as ds

MODENAMES = ['x','y','z','rx','ry','rz']

class WidgetDOFEditor(guiDockWidget):



    def guiCreate(self):
        """
        Add gui components to self.contents

        Do not fill the controls with actual values here. This is executed
        upon creation and guiScene etc are not yet available.

        """

        self.setWindowTitle("Edit Degrees of Freedom")

        # manual:
        self._layout = QtWidgets.QGridLayout()
        self.contents.setLayout(self._layout)


        self.dofs = []
        self._widgets = []  # List of QWidget



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
        return None # QtCore.Qt.DockWidgetArea.RightDockWidgetArea

    # ======

    def fill(self):
        """ Get list of dofs,
        if it changed, then update the gui
        and set appropriate values
        """

        s = self.guiScene

        new_dofs = []

        for n in s.nodes_of_type(Frame):
            d = [*n.position, *n.rotation]
            for i,f in  enumerate(n.fixed):
                if f is False: # free dof
                    v = d[i]
                    new_dofs.append({'node':n, 'mode':i, 'value': v})

        # compare to active on Node and mode
        old = [[e['node'], e['mode']] for e in self.dofs]
        new = [[e['node'], e['mode']] for e in new_dofs]

        if old==new:
            pass
        else:
            self.dofs = new_dofs
            self.update_gui()

        # set values
        for d in self.dofs:
            svinf(d['spinbox'], d['value'],do_block=True)


    def update_gui(self):
        """Updates the gui to reflect self.dofs"""

        self.setUpdatesEnabled(False)

        locale = QLocale(QLocale.English, QLocale.UnitedStates)

        # clear existing widgets
        for w in self._widgets:
            w.deleteLater()
        self._widgets.clear()

        nodename = ""

        for irow, dof in enumerate(self.dofs):

            if nodename != dof['node'].name:
                nodename = dof['node'].name
                label = QtWidgets.QLabel(f"{dof['node'].name}")
                self._layout.addWidget(label, irow, 0)
                self._widgets.append(label)

            label = QtWidgets.QLabel(MODENAMES[dof['mode']])
            spinbox = QtWidgets.QDoubleSpinBox()
            spinbox.setDecimals(3)
            spinbox.setMinimum(-1e10)
            spinbox.setMaximum(1e10)
            spinbox.setLocale(locale)

            self._widgets.append(spinbox)
            self._widgets.append(label)

            self._layout.addWidget(label, irow, 1)
            self._layout.addWidget(spinbox, irow, 2)


            dof['spinbox'] = spinbox

            spinbox.valueChanged.connect(lambda *args, i=int(irow), widget=spinbox: self.dof_changed(widget, i, *args))

        self.setUpdatesEnabled(True)

    def dof_changed(self, widget, i, *args):
        if widget.hasFocus():
            value = widget.value()
            dof = self.dofs[i]
            self.guiRunCodeCallback(f"s['{dof['node'].name}'].{MODENAMES[dof['mode']]} = {value}", guiEventType.MODEL_STATE_CHANGED, sender=self)
            if dof['node'] not in self.guiSelection:
                self.guiSelectNode(dof['node'])



DAVE_GUI_DOCKS['DOF Editor'] = WidgetDOFEditor