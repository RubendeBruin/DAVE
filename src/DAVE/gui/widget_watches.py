"""
This is an example/template of how to setup a new dockwidget
"""
from PySide2.QtCore import Qt
from PySide2.QtGui import QIcon
from PySide2.QtWidgets import QCompleter

from DAVE.gui.helpers.flow_layout import FlowLayout

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
from DAVE.gui.forms.dialog_edit_watch import Ui_DialigEditWatch

class WidgetWatches(guiDockWidget):

    def guiCreate(self):
        """
        Add gui components to self.contents

        Do not fill the controls with actual values here. This is executed
        upon creation and guiScene etc are not yet available.

        """

        # manual:

        self.flow_layout = FlowLayout()
        self.contents.setLayout(self.flow_layout)

        self.slider = QtWidgets.QSlider()
        self.slider.setOrientation(Qt.Horizontal)
        self.slider.setValue(8)
        self.slider.setMinimum(6)
        self.slider.setMaximum(32)
        self.slider.valueChanged.connect(self.changeFontSize)

        self.btnNew = QtWidgets.QPushButton('Add watch')
        self.btnNew.pressed.connect(self.new_watch)

        self.flow_layout.addWidget(self.slider)
        self.flow_layout.addWidget(self.btnNew)

        self.active_w = []
        self._labels = []


    def changeFontSize(self):
        size = self.slider.value()
        for l in self._labels:
            l.setStyleSheet(f'font: {size}pt;')

    def guiProcessEvent(self, event):
        """
        Add processing that needs to be done.

        After creation of the widget this event is called with guiEventType.FULL_UPDATE
        """

        if event in [guiEventType.FULL_UPDATE,
                     guiEventType.MODEL_STATE_CHANGED,
                     guiEventType.SELECTED_NODE_MODIFIED]:
            self.fill()

        if event in [guiEventType.SELECTION_CHANGED, guiEventType.FULL_UPDATE]:
            if self.guiSelection:
                self.btnNew.setText(f'Add watch on {self.guiSelection[0].name}')
                self.btnNew.setEnabled(True)
            else:
                self.btnNew.setText(f'Select a node to add a watch')
                self.btnNew.setEnabled(False)

    def guiDefaultLocation(self):
        return QtCore.Qt.DockWidgetArea.RightDockWidgetArea

    def fill(self):

        w = []

        for n in self.guiScene._nodes:
            r = n.run_watches()
            if r:
                w.extend([(*result, n) for result in r] ) # add the referring node to the list

        if self.active_w == w:
            print('Nothing changed')
            return

        self.setUpdatesEnabled(False)

        self.active_w = w

        for l in self._labels:
            l.deleteLater()
        self._labels.clear()

        i = 0
        for desc, value, node in w:
            l = QtWidgets.QLabel(f'{desc} : {value}')
            self.flow_layout.addWidget(l)

            l.mousePressEvent = lambda *args, i=len(self._labels) : self.clickWatch(i, *args)
            self._labels.append(l)


        self.changeFontSize()

        self.setUpdatesEnabled(True)

    def new_watch(self):
        if self.guiSelection:
            node = self.guiSelection[0]

            # select the first available name
            i = 1
            while True:
                name = f'new watch {i}'
                if name not in node.watches:
                    break
                i+=1

            node.watches[name] = Watch()

            if not self.edit_watch(node.watches[name], node, key=name):
                node.watches.pop(name) # remove if cancelled

    def edit_watch(self, watch, node, key):
        dialog = QtWidgets.QDialog()
        dialog.setWindowTitle(f'Edit watch on {node.name}')

        dialog.setWindowFlag(Qt.WindowCloseButtonHint, False)
        dialog.setWindowFlag(Qt.WindowContextHelpButtonHint, False)
        dialog.setWindowIcon(QIcon(":/icons/cube.png"))

        ui = Ui_DialigEditWatch()
        ui.setupUi(dialog)

        ui.tbName.setText(key)

        # Add all possible properties as suggestion
        #
        items = [f'self.{prop}' for prop in self.guiScene.give_properties_for_node(node)]
        completer = QCompleter(items)
        completer.setCaseSensitivity(Qt.CaseInsensitive)
        completer.setModelSorting(QCompleter.UnsortedModel)
        completer.setFilterMode(Qt.MatchContains)
        ui.tbEvaluate.setCompleter(completer)

        ui.tbEvaluate.setCurrentText(watch.evaluate)
        ui.tbCondition.setText(watch.condition)
        ui.sbDecimals.setValue(watch.decimals)



        def run_watch():
            evaluate = ui.tbEvaluate.currentText()
            condition = ui.tbCondition.text()

            try:
                evResult = eval(evaluate, None, {'self': node, 's': self.guiScene, 'np': np})

                try:
                    if condition:
                        conResult = eval(condition, None,
                                         {'self': node, 's': self.guiScene, 'np': np, 'value': evResult})
                    else:
                        conResult = True
                except Exception as M:
                    conResult = f'Failed with {str(M)}'


            except Exception as M:
                evResult = f'Failed with {str(M)}'
                conResult = f'not evaluated'

            ui.lblConditionResult.setText(str(conResult))
            ui.lblEvaluationResult.setText(str(evResult))

        ui.tbEvaluate.currentTextChanged.connect(run_watch)
        ui.tbCondition.textChanged.connect(run_watch)
        run_watch()

        result = dialog.exec_()  # 1 or 0 (cancel)
        if result:
            new_key = ui.tbName.text()
            if new_key != key:
                node.watches[new_key] = node.watches.pop(key)

            w = node.watches[new_key]
            w.evaluate = ui.tbEvaluate.currentText()
            w.condition = ui.tbCondition.text()
            w.decimals = ui.sbDecimals.value()

            self.fill()

        return result


    def clickWatch(self, nr, *args):

        event = args[0]
        print(event)

        if event.button() == Qt.MouseButton.LeftButton:

            # get the node and the watch
            data = self.active_w[nr]
            node = data[2]
            key = data[0]
            watch = node.watches[key]

            self.edit_watch(watch,node,key)


        else:
            print('Remove watch')
            pass # TODO: remove watch

