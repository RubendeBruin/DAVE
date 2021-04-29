"""
This is the widget that calculates the mode-shapes and activates or terminates the animation

If strucutre of model changes:
 - terminate animation

If button pressed:
 - calculate mode-shapes
 - start animation


"""

"""
  This Source Code Form is subject to the terms of the Mozilla Public
  License, v. 2.0. If a copy of the MPL was not distributed with this
  file, You can obtain one at http://mozilla.org/MPL/2.0/.

  Ruben de Bruin - 2019
"""

from DAVE.gui.dockwidget import *
from PySide2 import QtCore, QtWidgets
from PySide2.QtGui import QBrush, QColor
from DAVE.gui.forms.widgetUI_modeshapes import Ui_ModeShapesWidget
import DAVE.frequency_domain
import numpy as np

class WidgetModeShapes(guiDockWidget):

    def guiCreate(self):
        """
        Add gui components to self.contents

        Do not fill the controls with actual values here. This is executed
        upon creation and guiScene etc are not yet available.

        """

        # or from a generated file
        self.ui = Ui_ModeShapesWidget()
        self.ui.setupUi(self.contents)
        self.ui.btnCalc.clicked.connect(self.calc_modeshapes)
        self.ui.horizontalSlider.actionTriggered.connect(self.activate_modeshape)
        self.ui.sliderSize.actionTriggered.connect(self.activate_modeshape)
        self.ui.lblError.setText('')
        self.ui.pushButton_2.clicked.connect(self.quickfix)
        self._shapes_calculated = False

    def guiProcessEvent(self, event):
        """
        Add processing that needs to be done.

        After creation of the widget this event is called with guiEventType.FULL_UPDATE
        """

        # do not update is state changed due to an animation
        if self.gui.animation_running() and event == guiEventType.MODEL_STATE_CHANGED:
            pass


        if event in [guiEventType.FULL_UPDATE,
                     guiEventType.MODEL_STRUCTURE_CHANGED,
                     guiEventType.SELECTED_NODE_MODIFIED]:

            self.gui.animation_terminate()
            if self.guiScene.verify_equilibrium():
                self.d0 = self.guiScene._vfc.get_dofs()
            else:
                self.d0 = None
            self.fill_result_table()
            self._shapes_calculated = False
            self.ui.btnCalc.setStyleSheet("background-color: lightgreen;")
            self.ui.lblError.setText("")

            # self.autocalc()

    def guiDefaultLocation(self):
        return QtCore.Qt.DockWidgetArea.TopDockWidgetArea

    # ======

    # def autocalc(self):
    #     if self.ui.btnCalc.isChecked():
    #         self.calc_modeshapes()

    def calc_modeshapes(self):

        self.gui.animation_terminate()

        if self.d0 is None:
            if not self.guiScene.verify_equilibrium():
                self.gui.solve_statics()
            self.d0 = self.guiScene._vfc.get_dofs()

        try:
            V, D = DAVE.frequency_domain.mode_shapes(self.guiScene)
        except ArithmeticError as me:
            print('Could not calculate mode-shapes because:')
            print(me)
            self.ui.lblError.setText(str(me))
            return


        if V is not None:
            self.n_shapes = len(V)
        else:
            self.n_shapes = 0

        warnings = ''

        if np.any(np.iscomplex(V)):
            warnings += 'MASSLESS '
        else:
            V = np.real(V)

        if np.any(np.isnan(V)):
            warnings += ' UNCONTRAINED'

        self.ui.lblError.setText(warnings)
        self.ui.btnCalc.setStyleSheet("")

        self.ui.horizontalSlider.setMaximum(self.n_shapes - 1)
        self.omega = np.sqrt(V)  # omega is sqrt(eigenvalues)
        self.shapes = D
        self._shapes_calculated = True
        self.activate_modeshape()

    def quickfix(self):
        self.gui.animation_terminate()
        summary = DAVE.frequency_domain.dynamics_quickfix(self.guiScene)
        self.guiEmitEvent(guiEventType.MODEL_STRUCTURE_CHANGED)
        self.fill_results_table_with(summary)  # do this after emitting the event

    def activate_modeshape(self):

        if not self._shapes_calculated:
            return

        i = self.ui.horizontalSlider.sliderPosition()
        scale = self.ui.sliderSize.sliderPosition() + 1
        scale = 1.05 ** (scale - 30)
        # print('Activating mode-shape {} with scale {}'.format(i, scale))

        omega = self.omega[i]
        self.ui.lblPeriod.setText('{:.2f} s'.format(2 * np.pi / omega))
        self.ui.lblRads.setText('{:.2f} rad/s'.format(omega))

        shape = self.shapes[:,i]

        n_frames = 100
        t_modeshape = 5

        dofs = DAVE.frequency_domain.generate_modeshape_dofs(self.d0,shape,scale,n_frames,scene=self.guiScene)
        t = np.linspace(0,t_modeshape, n_frames)
        self.gui.animation_start(t,dofs,True, self.d0, do_not_reset_time=True)


        # update exitation row in table
        for i, d in enumerate(shape):
            self.ui.tableWidget.setItem(i, 0, QtWidgets.QTableWidgetItem('{:.2f}'.format(d)))
            cell = self.ui.tableWidget.item(i, 0)
            if cell is None:
                continue
            m = np.max(np.abs(shape))
            if m > 0 and abs(d) > 0:
                factor = 0.5 + 0.5 * abs(d) / m
            else:
                factor = 0
            color = QColor.fromRgb(255 - 100 * factor, 255 - 100 * factor, 255)
            cell.setBackground(QBrush(color))




    def fill_result_table(self):
        self.gui.animation_terminate()
        summary = DAVE.frequency_domain.dynamics_summary_data(self.guiScene)
        self.fill_results_table_with(summary)

    def fill_results_table_with(self, summary):
        rows = -1
        factor = 0.3
        color = QColor.fromRgb(255 - 100 * factor, 255 - 100 * factor, 255)

        for b in summary:
            mode = b['mode']
            name = b['node'] + ' mode:' + str(mode)
            try:
                node = self.guiScene[b['node']]
            except:
                continue

            rows += 1
            self.ui.tableWidget.setRowCount(rows+1)
            self.ui.tableWidget.setVerticalHeaderItem(rows, QtWidgets.QTableWidgetItem(name))
            self.ui.tableWidget.setItem(rows, 1, QtWidgets.QTableWidgetItem('{:e}'.format(node.inertia)))

            if mode>2:
                self.ui.tableWidget.setItem(rows, 2, QtWidgets.QTableWidgetItem('{:e}'.format(node.inertia_radii[mode-3])))
                self.ui.tableWidget.item(rows, 2).setBackground(QBrush(color))
            else:
                self.ui.tableWidget.item(rows, 1).setBackground(QBrush(color))
                self.ui.tableWidget.setItem(rows, 2,
                                            QtWidgets.QTableWidgetItem('n/a'))

            self.ui.tableWidget.setItem(rows, 3, QtWidgets.QTableWidgetItem('{:.3e}'.format(b['total_inertia'])))
            self.ui.tableWidget.setItem(rows, 4, QtWidgets.QTableWidgetItem('{:.3e}'.format(b['stiffness'])))
            self.ui.tableWidget.setItem(rows, 5, QtWidgets.QTableWidgetItem(b['unconstrained']))
            self.ui.tableWidget.setItem(rows, 6, QtWidgets.QTableWidgetItem(b['noinertia']))



