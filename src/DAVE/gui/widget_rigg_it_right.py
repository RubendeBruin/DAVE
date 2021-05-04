"""
  This Source Code Form is subject to the terms of the Mozilla Public
  License, v. 2.0. If a copy of the MPL was not distributed with this
  file, You can obtain one at http://mozilla.org/MPL/2.0/.

  Ruben de Bruin - 2019
"""

from DAVE.gui.dockwidget import *
from PySide2 import QtGui, QtCore, QtWidgets
from PySide2.QtWidgets import QPushButton
from PySide2.QtCore import QPoint
import DAVE.scene as nodes
import DAVE.settings as ds
from DAVE.gui.forms.widget_selection_actions import Ui_SelectionActions
from DAVE.gui.helpers.popup_textbox import get_text

class WidgetRiggItRight(guiDockWidget):

    def guiCreate(self):
        """
        Add gui components to self.contents

        Do not fill the controls with actual values here. This is executed
        upon creation and guiScene etc are not yet available.

        """

        # # or from a generated file
        self.ui = Ui_SelectionActions()
        self.ui.setupUi(self.contents)

        layout = QtWidgets.QVBoxLayout()
        self.ui.frame.setLayout(layout)


        self.buttons = []



    def guiProcessEvent(self, event):
        """
        Add processing that needs to be done.

        After creation of the widget this event is called with guiEventType.FULL_UPDATE
        """

        if event in [guiEventType.SELECTION_CHANGED, guiEventType.FULL_UPDATE]:
            self.fill()

    def guiDefaultLocation(self):
        return QtCore.Qt.DockWidgetArea.RightDockWidgetArea

    # ======

    def find_nodes(self, types):
        """Returns nodes of given types. Only the first node per given type is returned and no duplicates.

        Returns None if not all types could be found
        """
        r = []
        source = self.guiSelection.copy()

        for t in types:
            for s in source:
                if isinstance(s, t):
                    r.append(s)
                    source.remove(s)
                    break

        if len(r) == len(types):
            return r
        else:
            return None

    def all_of_type(self, types):
        source = self.guiSelection.copy()

        types = tuple(types)

        if np.all( [isinstance(e, types) for e in source] ):
            return source
        else:
            return None




    def fill(self):

        # display the name of the selected node
        text = ''
        for node in self.guiSelection:
            text += ' ' + node.name

        self.ui.label.setText(text)

        for button in self.buttons:
            button.deleteLater()

        self.buttons.clear()

        style_warning = "color: darkred"

        # Here we manually define all the possible quick-actions
        #
        # each quick-action defines its own button

        def valid_name(text):
            return self.guiScene.name_available(text)

        # At least two sheaves connected
        p2 = self.find_nodes([nodes.Circle, nodes.Circle])
        if p2:

            p0 = p2[0]
            p1 = p2[1]

            # Geometric contact between p0 -> p1
            if p0.parent.parent is not None:

                button = QPushButton(f'Connection using {p1.name} as master', self.ui.frame)
                def geometric_contact1():
                    pos = self.mapToGlobal(QPoint(0,0))
                    name = get_text(pos = pos, suggestion=self.guiScene.available_name_like("contact"), input_valid_callback=valid_name)
                    pin_hole_code_p0p1 = f's.new_geometriccontact("{name}", "{p0.name}", "{p1.name}")'
                    self.guiRunCodeCallback(pin_hole_code_p0p1, guiEventType.MODEL_STRUCTURE_CHANGED)

                button.clicked.connect(geometric_contact1)

                #  sheave poi   axis
                if p0.parent.parent.parent is not None:
                    button.setStyleSheet(style_warning)
                    button.setToolTip(f"Warning: {p0.parent.parent.parent.name} will be disconnected from its parent")

                self.buttons.append(button)

            # Geometric contact between p1 -> p0
            if p1.parent.parent is not None:

                button = QPushButton(f'Connect using {p0.name} as master', self.ui.frame)

                def geometric_contact2():
                    pos = self.mapToGlobal(QPoint(0,0))
                    name = get_text(pos = pos, suggestion=self.guiScene.available_name_like("contact"), input_valid_callback=valid_name)
                    pin_hole_codep1p0 = f's.new_geometriccontact("{name}", "{p1.name}", "{p0.name}")'
                    self.guiRunCodeCallback(pin_hole_codep1p0, guiEventType.MODEL_STRUCTURE_CHANGED)

                button.clicked.connect(geometric_contact2)

                #  sheave poi   axis
                if p1.parent.parent.parent is not None:
                    button.setStyleSheet(style_warning)
                    button.setToolTip(
                        f"Warning: {p1.parent.parent.parent.name} will be disconnected from its parent")

                self.buttons.append(button)

        # Multiple points/sheaves selected
        poi_and_sheave = self.all_of_type([Point, Circle])
        if poi_and_sheave:

            if len(poi_and_sheave) > 1:
                if len(poi_and_sheave) > 2:
                    names = ''.join([f'"{e.name}",' for e in poi_and_sheave[1:-1]])
                    sheaves = f', sheaves = [{names[:-1]}]'
                    button = QPushButton('Create cable with sheaves', self.ui.frame)
                else:
                    sheaves = ''
                    button = QPushButton('Create cable', self.ui.frame)

                def create_cable():
                    pos = self.mapToGlobal(QPoint(0,0))
                    name = get_text(pos = pos, suggestion=self.guiScene.available_name_like("cable"), input_valid_callback=valid_name)
                    cable_code = f's.new_cable("{name}", endA="{poi_and_sheave[0].name}", endB = "{poi_and_sheave[-1].name}"{sheaves})'
                    self.guiRunCodeCallback(cable_code, guiEventType.MODEL_STRUCTURE_CHANGED)

                button.clicked.connect(create_cable)
                self.buttons.append(button)

        # creating sling between points and sheaves
        poi_and_sheave = self.all_of_type([Point, Circle])
        if poi_and_sheave:

            if len(poi_and_sheave) > 1:
                if len(poi_and_sheave) > 2:
                    names = ''.join([f'"{e.name}",' for e in poi_and_sheave[1:-1]])
                    sheaves = f', sheaves = [{names[:-1]}]'
                    button = QPushButton('Create sling over sheaves', self.ui.frame)
                else:
                    sheaves = ''
                    button = QPushButton('Create sling', self.ui.frame)

                def create_sling():
                    pos = self.mapToGlobal(QPoint(0, 0))
                    name = get_text(pos=pos, suggestion=self.guiScene.available_name_like("sling"),
                                    input_valid_callback=valid_name)
                    sling_code = f's.new_sling("{name}", endA="{poi_and_sheave[0].name}", endB = "{poi_and_sheave[-1].name}"{sheaves})'
                    self.guiRunCodeCallback(sling_code, guiEventType.MODEL_STRUCTURE_CHANGED)

                button.clicked.connect(create_sling)
                self.buttons.append(button)

        # a single sheave selected
        if len(self.guiSelection)==1:
            if isinstance(self.guiSelection[0], Circle):
                sheave = self.guiSelection[0]

                # def create_shackle_gphd(s, name, wll):
                sizes = (120, 150, 200, 250, 300, 400, 500, 600, 700, 800, 900, 1000, 1250, 1500)

                def insert_gp(wll):
                    pos = self.mapToGlobal(QPoint(0, 0))
                    name = get_text(pos=pos, suggestion=self.guiScene.available_name_like(f"GP{wll}"),
                                    input_valid_callback=valid_name)
                    code = f's.new_shackle(name="{name}", kind = "GP{wll}")'
                    pin_name = name + '_pin'
                    code += f'\ns.new_geometriccontact("{name}" + "_connection", "{pin_name}", "{sheave.name}", inside=True)'
                    self.guiRunCodeCallback(code, guiEventType.MODEL_STRUCTURE_CHANGED)

                for size in sizes:
                    button = QPushButton(f'insert GP {size} in {sheave.name}', self.ui.frame)
                    button.clicked.connect(lambda wll = size : insert_gp(wll=wll))
                    self.buttons.append(button)

        # nothing selected
        if len(self.guiSelection) == 0:

            def create_sling():
                pos = self.mapToGlobal(QPoint(0, 0))
                name = get_text(pos=pos, suggestion=self.guiScene.available_name_like("sling"),
                                input_valid_callback=valid_name)
                sling_code = f's.new_sling("{name}", length=1)'
                self.guiRunCodeCallback(sling_code, guiEventType.MODEL_STRUCTURE_CHANGED)

            button = QPushButton('Create sling', self.ui.frame)
            button.clicked.connect(create_sling)
            self.buttons.append(button)

            # def create_shackle_gphd(s, name, wll):
            sizes = (120, 150, 200, 250, 300, 400, 500, 600, 700, 800, 900, 1000, 1250, 1500)

            def insert_gp(wll):
                pos = self.mapToGlobal(QPoint(0, 0))
                name = get_text(pos=pos, suggestion=self.guiScene.available_name_like(f"GP{wll}"),
                                input_valid_callback=valid_name)
                code = f's.new_shackle(name="{name}", kind = "GP{wll}")'
                self.guiRunCodeCallback(code, guiEventType.MODEL_STRUCTURE_CHANGED)

            for size in sizes:
                button = QPushButton(f'Create GP {size}', self.ui.frame)
                button.clicked.connect(lambda wll=size: insert_gp(wll=wll))
                self.buttons.append(button)






        # add all buttons to the layout

        for button in self.buttons:
            self.ui.frame.layout().addWidget(button)
