from PySide6 import QtWidgets
from PySide6.QtCore import QSize, Qt
from PySide6.QtWidgets import QSizePolicy, QTreeWidgetItem, QComboBox

from DAVE.helpers.singleton_class import Singleton
from DAVE.nodes import *
from DAVE.gui.dialog_advanced_cable_settings import AdvancedCableSettings
from DAVE.gui.dock_system.dockwidget import guiEventType

from .forms.widget_connections import Ui_ConnectionForm
from .helpers.nodelist_drag_drop_move import call_from_dragEnter_or_Move_Event
from .widget_nodeprops_abstracts_and_helpers import NodeEditor

"""
This module contains the code for the connections editor

This editor is primarily used for editing the connections of a cable,
but is also used for editing the connections of SlingGrommet as defined in
the rigging package.

"""


def set_disabled(item, i):
    item.setForeground(i, Qt.lightGray)
    item.setBackground(i, Qt.lightGray)

def set_enabled(item, i):
    item.setForeground(i, Qt.black)
    item.setBackground(i, Qt.white)

@Singleton
class EditConnections(NodeEditor):
    def __init__(self):
        self.node: Cable  # type hint only

        widget = QtWidgets.QWidget()
        ui = Ui_ConnectionForm()
        ui.setupUi(widget)

        self.ui = ui
        self._widget = widget

        self._widget.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        self.additional_pois = list()

        self.ui.tree.sizeHint = lambda: QSize(0, 0)  # disable the size-hint

        self.ui.tree.setHeaderLabels(
            ["⭮/⭯", "Connection", "Offset",  "Max winding", "Use Friction", "Force Factor", "Cable point", "Circle point"]
        )

        # Set events
        ui.pbRemoveSelected.clicked.connect(self.delete_selected)
        self.ui.pushButton.clicked.connect(self.add_item)
        ui.pbSetShortestRoute.clicked.connect(self.set_shortest_route)

        ui.tree.keyPressEvent = self.listKeyPressEvent

        # ------- setup the drag-and-drop code ---------

        ui.tree.dropEvent = self.dropEvent
        ui.tree.dragEnterEvent = self.dragEnterEvent
        ui.tree.dragMoveEvent = self.dragEnterEvent

        ui.pbRemoveSelected.dragEnterEvent = self.dragOntoDeleteButtonEvent
        ui.pbRemoveSelected.dropEvent = self.dropOnDeleteButtonEvent

        ui.tree.itemChanged.connect(self.itemChanged)

        ui.pbRemoveSelected.setAcceptDrops(True)
        ui.tree.setDragEnabled(True)
        ui.tree.setAcceptDrops(True)

        ui.checkBox.toggled.connect(self.post_update_event)

        # ui.tree.editItem = self.editItem

    def connect(
            self,
            node,
            scene,
            run_code,
            guiEmitEvent,
            gui_solve_func,
            node_picker_register_func,
    ):
        self.ui.widgetPicker.initialize(
            scene=scene,
            nodetypes=(Point, Circle),
            callback=None,
            register_func=node_picker_register_func,
            NoneAllowed=True,
            node=node,
        )
        return super().connect(
            node,
            scene,
            run_code,
            guiEmitEvent,
            gui_solve_func,
            node_picker_register_func,
        )

    def itemChanged(self, *args):
        self.generate_code()

    def add_item(self):
        name = self.ui.widgetPicker.value
        if self.scene.node_exists(name):
            node_names = [node.name for node in self.node.connections]

            # See if any of the items in the tree is selected,
            # if so, insert the new item before the selected item
            selected = self.ui.tree.selectedItems()
            if selected:
                index = self.ui.tree.indexOfTopLevelItem(selected[0])
                node_names.insert(index, name)
            else:
                node_names.append(name)

            code = f"s['{self.node.name}'].connections = ("
            for name in node_names:
                code += "'{}',".format(name)
            code = code[:-1] + ")"
            self.run_code(code)
        else:
            self.run_code(f"raise ValueError(f'No node with name {name}')")

    def _update_grid_colors_to_friction_type_in_treeview(self):

        # loop over the items in the treeview
        for i in range(self.ui.tree.topLevelItemCount()):
            item = self.ui.tree.topLevelItem(i)
            friction_kind_combo = self.ui.tree.itemWidget(item, 4).currentText()

            if friction_kind_combo == 'Force':
                set_enabled(item,5)
                set_disabled(item,6)
                set_disabled(item,7)

            elif friction_kind_combo == 'Position':
                set_disabled(item,5)
                set_enabled(item, 6)

                if isinstance(self.node.connections[i], Circle):
                    set_enabled(item, 7)
                else:
                    set_disabled(item, 7)
            else:
                set_disabled(item,5)
                set_disabled(item,6)
                set_disabled(item,7)



    def post_update_event(self):
        # update the combobox with points and circles
        self.ui.widgetPicker.fill("keep")

        labelVisible = False

        # make data of all properties
        # and align with connections
        (
            endAFr,
            endAMaxWind,
            endBFr,
            endBMaxWind,
            is_grommet_in_line_mode,
        ) = self.node._get_advanced_settings_dialog_settings()

        # # frictions
        # frictions = []
        # if not endAFr:  # friction at endA not definable
        #     frictions.append("-")  # first item
        # for friction in self.node.friction:
        #     if friction is not None:
        #         frictions.append(str(friction))
        #     else:
        #         frictions.append("?")  # NONE
        #
        # if not endBFr:
        #     frictions.append("-")  # last item

        self.node : Cable # type hint

        friction_types = self.node._make_connection_aligned_copy_of_friction_vector(self.node.friction_type, insert_value=FrictionType.No)
        friction_factors = self.node._make_connection_aligned_copy_of_friction_vector(self.node.friction, insert_value=None)
        friction_cable_points = self.node._make_connection_aligned_copy_of_friction_vector(self.node.friction_point_cable, insert_value=None)
        friction_connector_points = self.node._make_connection_aligned_copy_of_friction_vector(self.node.friction_point_connection, insert_value=None)

        # convert to string
        friction_factors = [f'{friction:.3g}' if friction is not None else "?" for friction in friction_factors]
        friction_cable_points = [f'{friction:.3g}' if friction is not None else "" for friction in friction_cable_points]
        friction_connector_points = [f'{friction:.3g}' if friction is not None else "" for friction in friction_connector_points]


        # maximum winding angles
        mas = [f'{ma:.3g}' if ma>0 else '' for ma in self.node.max_winding_angles]

        # offsets
        offsets = [f'{offset:.3g}' for offset in self.node.offsets]

        N = len(self.node.connections)

        self.ui.tree.blockSignals(True)  # update the list
        self.ui.tree.clear()

        for i, (connection, reversed, offs, friction_type, friction_factor, friction_cable_point, friction_connector_point, max_winding) in enumerate(
                zip(self.node.connections,
                    self.node.reversed,
                    offsets,
                    friction_types,
                    friction_factors,
                    friction_cable_points,
                    friction_connector_points,
                    mas)):

            item = QTreeWidgetItem(self.ui.tree)
            item.setText(0, " ")
            item.setText(1, connection.name)
            item.setText(2, offs)

            # max winding
            item.setText(3, max_winding)
            if (i==0 and not endAMaxWind) or (i==N-1 and not endBMaxWind):
                set_disabled(item,3)

            # 4 : friction type

            item.setText(5, friction_factor)
            item.setText(6, friction_cable_point)
            item.setText(7, friction_connector_point)

            # set reversed using the checkbox

            if isinstance(connection, Circle):
                item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
                item.setCheckState(
                    0,
                    Qt.CheckState.Checked if reversed else Qt.CheckState.Unchecked,
                )
                labelVisible = True

            item.setFlags(item.flags() | Qt.ItemIsEditable)

            # set the friction kind
            friction_kind_combo = QComboBox()  # memory handled by treeview
            friction_kind_combo.setSizeAdjustPolicy(QComboBox.SizeAdjustPolicy.AdjustToMinimumContentsLengthWithIcon)

            if (i==0 and not endAFr) or (i==N-1 and not endBFr):
                friction_kind_combo.addItems(["-","-- Can not set for this connection --"])
                friction_kind_combo.setCurrentIndex(0)
            else:
                friction_kind_combo.addItems(["No", "Force", "Position"])

                if friction_type == FrictionType.No:
                    friction_kind_combo.setCurrentIndex(0)
                elif friction_type == FrictionType.Force:
                    friction_kind_combo.setCurrentIndex(1)
                elif friction_type == FrictionType.Position:
                    friction_kind_combo.setCurrentIndex(2)

            friction_kind_combo.currentIndexChanged.connect(self.itemChanged)
            self.ui.tree.setItemWidget(item, 4, friction_kind_combo)
            self.ui.tree.addTopLevelItem(item)  # add to tree

        self._update_grid_colors_to_friction_type_in_treeview()

        # get the model-index of the first item
        index = self.ui.tree.indexFromItem(self.ui.tree.topLevelItem(0))
        rowheight = self.ui.tree.rowHeight(index)

        n_rows = max(6, N + 3)
        self.ui.tree.setMinimumHeight(n_rows * rowheight)
        self.ui.tree.blockSignals(False)
        self.ui.lbDirection.setVisible(labelVisible)

        # before this
        self.ui.lblError.setVisible(False)
        self.ui.pbSetShortestRoute.setVisible(not isinstance(self.node, (Cable)))
        self.ui.tree.setStyleSheet("")

        self.ui.tree.header().setSectionResizeMode(
            QtWidgets.QHeaderView.ResizeToContents
        )

        # hide the friction and max winding angle columns if not applicable
        basic = not self.ui.checkBox.isChecked()
        self.ui.tree.setColumnHidden(4, basic)
        self.ui.tree.setColumnHidden(5, basic)
        self.ui.tree.setColumnHidden(6, basic)
        self.ui.tree.setColumnHidden(7, basic)
        if not basic:
            self.ui.tree.setToolTip(
                "Friction:"
                "\n`-` indicates that friction can not be prescribed for that connection\n"
                "`?` indicates that the friction is auto determined for that connection\n"
            )
        else:
            self.ui.tree.setToolTip(
                "Check the `advanced setttings` box for more options"
            )

    def which_row(self, item):
        for i in range(self.ui.tree.topLevelItemCount()):
            if self.ui.tree.topLevelItem(i) == item:
                return i
        return -1

    def dropEvent(self, event):
        tree = self.ui.tree  # alias

        try:
            connections = list(self.node.connections)

            # what item are we dropping or moving

            if event.source() == tree:
                moved_item = tree.selectedItems()[0].text(1)
            else:
                if event.mimeData().hasText():
                    moved_item = event.mimeData().text()
                else:
                    event.accept()  # do nothing
                    return

            # Where to place?
            to_item = self.ui.tree.itemAt(event.pos())

            if to_item:
                row_to = self.which_row(to_item)
            else:
                row_to = -1

            if row_to >= 0:
                connections.insert(row_to, moved_item)
            else:
                connections.append(moved_item)

            # anything to remove?
            if event.source() == tree:  # moving, remove old item
                delrow = self.which_row(tree.selectedItems()[0])
                if delrow > row_to and row_to > -1:
                    connections.pop(delrow + 1)
                else:
                    connections.pop(delrow)

            # update the connections
            code = f"s['{self.node.name}'].connections = ("
            for name in connections:
                code += "'{}',".format(name)
            code = code[:-1] + ")"
            self.run_code(code, event=guiEventType.SELECTED_NODE_MODIFIED, sender=self)
            self.post_update_event()

        finally:
            event.accept()

    def dragEnterEvent(self, event):
        call_from_dragEnter_or_Move_Event(
            self.ui.tree, self.scene, (Circle, Point), event
        )

    def dropOnDeleteButtonEvent(self, event):
        if event.source() == self.ui.tree:
            self.ui.pbRemoveSelected.click()
            event.accept()

    def dragOntoDeleteButtonEvent(self, event):
        if event.source() == self.ui.tree:
            event.accept()

    def delete_selected(self):
        if not self.ui.tree.selectedItems():
            return

        item = self.ui.tree.selectedItems()[0]
        row = self.which_row(item)
        connections = list(self.node.connections)
        connections.pop(row)
        code = f"s['{self.node.name}'].connections = ("
        for name in connections:
            code += "'{}',".format(name)
        code = code[:-1] + ")"
        self.run_code(code, event=guiEventType.SELECTED_NODE_MODIFIED, sender=self)
        self.post_update_event()

    def listKeyPressEvent(self, event):
        if event.key() == Qt.Key_Delete:
            self.delete_selected()

    def generate_code(self):

        code = ""
        element = "\ns['{}']".format(self.node.name)

        N = self.ui.tree.invisibleRootItem().childCount()

        a_connections = []
        a_reversed = []
        a_offsets = []
        a_maw = []
        a_friction_type = []
        a_friction_factor = []
        a_friction_cable_point = []
        a_friction_connector_point = []

        try:  # catch value errors in float / str conversions
            for i in range(N):
                item = self.ui.tree.invisibleRootItem().child(i)

                reversed = item.checkState(0) == Qt.CheckState.Checked
                connection = item.text(1)
                offset = item.text(2)
                max_winding = item.text(3)
                friction_type_string = self.ui.tree.itemWidget(item, 4).currentText()
                friction_factor = item.text(5)
                friction_cable_point = item.text(6)
                friction_connector_point = item.text(7)


                a_connections.append(connection)
                a_reversed.append(reversed)
                a_offsets.append(float(offset))

                if max_winding:
                    a_maw.append(float(max_winding))
                else:
                    a_maw.append(0) # no max winding angle

                # friction type

                if friction_type_string == "No":
                    a_friction_type.append(FrictionType.No)
                elif friction_type_string == "Force":
                    a_friction_type.append(FrictionType.Force)
                elif friction_type_string == "Position":
                    a_friction_type.append(FrictionType.Position)
                else:
                    a_friction_type.append(None) # really doesn't matter, will be removed later

                # friction factor

                if friction_factor == "-":
                    pass
                elif friction_factor.strip() == "?":
                    a_friction_factor.append(None)
                else:
                    a_friction_factor.append(float(friction_factor))

                # friction cable point
                if friction_cable_point:
                    a_friction_cable_point.append(float(friction_cable_point))
                else:
                    a_friction_cable_point.append(None)

                # friction connector point
                if friction_connector_point:
                    a_friction_connector_point.append(float(friction_connector_point))
                else:
                    a_friction_connector_point.append(None)

        except ValueError as e:
            self.ui.tree.setStyleSheet("background-color: rgb(251, 220, 255)")
            self.ui.lblError.setText(str(e))
            self.ui.lblError.setVisible(True)
            self._update_grid_colors_to_friction_type_in_treeview()

            return

        else:
            self.ui.tree.setStyleSheet("") # ok
            self.ui.lblError.setVisible(False)

        # cut friction vectors to the correct length
        # from the gui they are defined for all connections

        self.node : Cable
        a_friction_type = self.node._make_friction_vector_from_connection_aligned_vector(a_friction_type)
        a_friction_factor = self.node._make_friction_vector_from_connection_aligned_vector(a_friction_factor)
        a_friction_cable_point = self.node._make_friction_vector_from_connection_aligned_vector(a_friction_cable_point)
        a_friction_connector_point = self.node._make_friction_vector_from_connection_aligned_vector(a_friction_connector_point)

        # check for differences



        # dry-run to see if what we want is valid,
        # if not then do not execute the code to give the user the
        # opportunity to fix the errors

        try:
            if a_connections != [node.name for node in self.node.connections]:
                code += f"{element}.connections = ("
                for name in a_connections:
                    code += "'{}',".format(name)
                code = code[:-1] + ")"
                self.node.connections = a_connections

            if tuple(a_reversed) != tuple(self.node.reversed):
                code += f"{element}.reversed = {a_reversed}"
                self.node.reversed = a_reversed

            if tuple(a_offsets) != tuple(self.node.offsets):
                code += f"{element}.offsets = {a_offsets}"
                self.node.offsets = a_offsets

            if tuple(a_maw) != tuple(self.node.max_winding_angles):
                code += f"{element}.max_winding_angles = {a_maw}"
                self.node.max_winding_angles = a_maw

            if a_friction_factor != self.node.friction:
                code += f"{element}.friction = {a_friction_factor}"
                self.node.friction = a_friction_factor

            if a_friction_cable_point != self.node.friction_point_cable:
                code += f"{element}.friction_point_cable = {a_friction_cable_point}"
                self.node.friction_point_cable = a_friction_cable_point

            if a_friction_connector_point != self.node.friction_point_connection:
                code += f"{element}.friction_point_connection = {a_friction_connector_point}"
                self.node.friction_point_connection = a_friction_connector_point


            # Apply type last !!!
            if tuple(a_friction_type) != tuple(self.node.friction_type):
                code += f"{element}.friction_type = {a_friction_type}"
                self.node.friction_type = a_friction_type


        except Exception as e:
            self.ui.tree.setStyleSheet("background-color: rgb(251, 220, 255)")
            self.ui.lblError.setText(str(e))
            self.ui.lblError.setVisible(True)
            self._update_grid_colors_to_friction_type_in_treeview()

            return

        self.run_code(
            code, guiEventType.SELECTED_NODE_MODIFIED, sender=self
        )  # we will not receive the event

        # check if the connections are valid to see if the code did run correctly
        reversed_ok = a_reversed == list(self.node.reversed)
        names_ok = a_connections == [node.name for node in self.node.connections]

        if reversed_ok and names_ok:
            self.ui.tree.setStyleSheet("")
        else:
            self.ui.tree.setStyleSheet(
                "background-color: rgb(251, 220, 255)"
            )  # echt heel lelijk

    def set_shortest_route(self, *args):
        self.run_code(
            f's["{self.node.name}"].set_optimum_connection_directions()',
            guiEventType.SELECTED_NODE_MODIFIED,
        )

    def show_advanced_settings(self):
        dialog = AdvancedCableSettings(cable=self.node)
        dialog.exec()
        if dialog.code:
            self.run_code(dialog.code, guiEventType.SELECTED_NODE_MODIFIED)
