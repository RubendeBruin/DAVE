from dataclasses import dataclass

from PySide6 import QtWidgets
from PySide6.QtCore import QSize, Qt
from PySide6.QtWidgets import QSizePolicy, QTreeWidgetItem, QComboBox

from DAVE.gui.dialog_advanced_cable_settings import AdvancedCableSettings
from DAVE.gui.dock_system.dockwidget import guiEventType
from DAVE.helpers.singleton_class import Singleton
from DAVE.nodes import *
from .forms.widget_connections import Ui_ConnectionForm
from .helpers.nodelist_drag_drop_move import call_from_dragEnter_or_Move_Event
from .widget_nodeprops_abstracts_and_helpers import NodeEditor
from ..nds.core import DEFAULT_WINDING_ANGLE

"""
This module contains the code for the connections editor

This editor is primarily used for editing the connections of a cable,
but is also used for editing the connections of SlingGrommet as defined in
the rigging package.

"""

ERROR_STYLESHEET = "QTreeWidget {\n    border-width: 2px;\n    border-style: solid;\n    border-color: red;\n}"

"""
This module contains the editor for connections of a cable.

Connections, and associated friction properties, are inter-connected. It is quite
common to temporarily create invalid conditions while editing the connections.

We have three "layers"

1.- The ui with the treeview
2.- A model of the connections with data
3.- The node

The model is filled from the node when the editor is opened.
The model is used to fill the ui
Changes in the ui are used to update the model and then update the ui again
if the model is valid, then the code is generated and sent to the node

The model holds data for EACH connection and is aligned with the connections.
In the node the data is stored as vectors and only where relevant. So there is a 
conversion with indices between the two.

"""


@dataclass
class CableConnection:
    connection_node: [Circle, Point]
    reversed: bool
    offset: float
    max_winding_angle: float
    friction_type: FrictionType
    friction_force_factor: float or None
    friction_point_cable: float or None
    friction_point_connection: float or None


def set_disabled(item, indices):
    for i in indices:
        item.setForeground(i, Qt.lightGray)
        item.setBackground(i, Qt.lightGray)


def float_or_none(s):
    try:
        return float(s)
    except ValueError:
        return None


@Singleton
class EditConnections(NodeEditor):
    def __init__(self):
        self.node: Cable  # type hint only
        self.connections_model: list[CableConnection] = []
        self._filling = True

        # support for SlingGrommet
        self.endAFr = False
        self.endAMaxWind = False
        self.endBFr = False
        self.endBMaxWind = False
        self.is_grommet_in_line_mode = False

        widget = QtWidgets.QWidget()
        ui = Ui_ConnectionForm()
        ui.setupUi(widget)

        self.ui = ui
        self._widget = widget

        self._widget.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        self.additional_pois = list()

        self.ui.tree.sizeHint = lambda: QSize(0, 0)  # disable the size-hint

        self.ui.tree.setHeaderLabels(
            [
                "⭮/⭯",
                "Connection",
                "Offset",
                "Max winding",
                "Use Friction",
                "Friction Force [-]",
                "Pin pos. Cable [-]",
                "Pin pos. Surface [deg]",
            ]
        )

        # noinspection PyUnresolvedReferences
        self.ui.tree.header().setSectionResizeMode(
            QtWidgets.QHeaderView.ResizeToContents
        )

        # Set events
        ui.pbRemoveSelected.clicked.connect(self.delete_selected)
        self.ui.pushButton.clicked.connect(self.add_item)
        ui.pbSetShortestRoute.clicked.connect(self.set_shortest_route)
        ui.pbPinLocations.clicked.connect(self.set_pin_locations)
        ui.tree.keyPressEvent = self.deleteKeyPressEvent  # delete

        # ------- setup the drag-and-drop code ---------

        ui.tree.dragMoveEvent = self.dragEnterEvent
        ui.tree.dragEnterEvent = self.dragEnterEvent
        ui.tree.dropEvent = self.dropEvent

        ui.pbRemoveSelected.dragEnterEvent = self.dragOntoDeleteButtonEvent
        ui.pbRemoveSelected.dropEvent = self.dropOnDeleteButtonEvent

        ui.tree.itemChanged.connect(self.ui_changed)

        ui.pbRemoveSelected.setAcceptDrops(True)
        ui.tree.setDragEnabled(True)
        ui.tree.setAcceptDrops(True)

        ui.checkBox.toggled.connect(self._update_column_visibility)
        ui.cbGeometryTweaking.toggled.connect(self._update_column_visibility)

        self._update_column_visibility()

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

    def post_update_event(self):
        """Model has changed and we need to update the ui"""
        # update the combobox with points and circles
        self.ui.widgetPicker.fill("keep")
        self.hide_error()

        self.node: Cable  # type hint only

        (
            self.endAFr,
            self.endAMaxWind,
            self.endBFr,
            self.endBMaxWind,
            self.is_grommet_in_line_mode,
        ) = self.node._get_advanced_settings_dialog_settings()

        self.ui.pbSetShortestRoute.setVisible(
            hasattr(self.node, "set_optimum_connection_directions")
        )

        self._update_model_from_node()
        self._update_ui_from_model()

        self._update_column_visibility()

    def _update_model_from_node(self):
        """Update the model from the node"""
        self.node: Cable  # type hint

        # get the data from the node, aligned with connections
        a_friction_type = self.node._make_connection_aligned_copy_of_friction_vector(
            self.node.friction_type, insert_value=FrictionType.No
        )
        a_friction_factor = self.node._make_connection_aligned_copy_of_friction_vector(
            self.node.friction_force_factor, insert_value=None
        )
        a_friction_cable_point = (
            self.node._make_connection_aligned_copy_of_friction_vector(
                self.node.friction_point_cable, insert_value=None
            )
        )
        a_friction_connector_point = (
            self.node._make_connection_aligned_copy_of_friction_vector(
                self.node.friction_point_connection, insert_value=None
            )
        )

        self.connections_model.clear()

        for (
            connection,
            reversed,
            offs,
            friction_type,
            friction_factor,
            friction_cable_point,
            friction_connector_point,
            max_winding,
        ) in zip(
            self.node.connections,
            self.node.reversed,
            self.node.offsets,
            a_friction_type,
            a_friction_factor,
            a_friction_cable_point,
            a_friction_connector_point,
            self.node.max_winding_angles,
        ):
            self.connections_model.append(
                CableConnection(
                    connection,
                    reversed,
                    offs,
                    max_winding,
                    friction_type,
                    friction_factor,
                    friction_cable_point,
                    friction_connector_point,
                )
            )

    def _update_ui_from_model(self):
        """Update the ui from the model"""
        self._filling = True
        self.ui.tree.blockSignals(True)

        N = len(self.connections_model)
        is_loop = (
            self.connections_model[0].connection_node
            == self.connections_model[-1].connection_node
        )

        # friction for the first and last connections?
        # This is dictated by the endAFr, endBFr, endAMaxWind, endBMaxWind
        # but these depend on whether or not the cable is a loop, which is determined by the connections which
        # we are changing. So for a Cable these values should not be used.
        #
        # For a SlingGrommet the values CAN be used.

        """
        Depending on what "cable" really is, the following settings are exposed:
        
        endA friction
        endA max winding angle
        endB friction
        endB max winding angle
        
                                  Cable          Cable    SlingGrommet*     SlingGrommet          SlingGrommet
                                  line           loop       sling           Grommet/circle        Grommet/line
                                  
        endA friction              no             yes        no              yes                       yes
        endA max winding angle     no             yes        no              yes                       yes
        endB friction              no             no         no              yes                       yes
        endB max winding angle     no             no         no              yes                       yes
        """

        endAFr = self.endAFr
        endBFr = self.endBFr

        if isinstance(self.node, Cable):
            endAFr = is_loop

        self.ui.tree.clear()

        # flag that position properties are not required
        friction_types = [c.friction_type for c in self.connections_model]
        loop_with_one_fixed_position = (
            endAFr
            and friction_types.count(FrictionType.Position) == 1
            and (
                friction_types[0] == FrictionType.Position
                or (endBFr and (friction_types[-1] == FrictionType.Position))
            )
        )

        # columns:
        # 0 : reversed
        # 1 : connection
        # 2 : offset
        # 3 : max winding angle
        # 4 : friction type
        # 5 : friction factor
        # 6 : friction cable point
        # 7 : friction connector point

        for i, connection in enumerate(self.connections_model):
            item = QTreeWidgetItem(self.ui.tree)
            item.setText(0, " ")
            item.setText(1, connection.connection_node.label)
            item.setToolTip(
                1, connection.connection_node.name
            )  # store the node name as tooltop
            item.setText(2, str(connection.offset))
            item.setText(3, str(connection.max_winding_angle))

            # make item editable by user
            item.setFlags(item.flags() | Qt.ItemIsEditable)

            # column # 0 : reversed
            if isinstance(connection.connection_node, (Circle)):
                item.setCheckState(
                    0,
                    (
                        Qt.CheckState.Checked
                        if connection.reversed
                        else Qt.CheckState.Unchecked
                    ),
                )

            # 4 : friction type

            if (
                i == 0 and not endAFr and not is_loop or i == N - 1 and not endBFr
            ):  # see above for reasoning
                # no friction to be set
                set_disabled(item, [5, 6, 7])

            else:
                friction_kind_combo = QComboBox()
                friction_kind_combo.setSizeAdjustPolicy(
                    QComboBox.SizeAdjustPolicy.AdjustToMinimumContentsLengthWithIcon
                )
                friction_kind_combo.addItems(["No", "Force", "Position"])

                self.ui.tree.setItemWidget(item, 4, friction_kind_combo)

                if connection.friction_type == FrictionType.No:
                    friction_kind_combo.setCurrentIndex(0)
                    set_disabled(item, [5, 6, 7])

                elif connection.friction_type == FrictionType.Force:
                    friction_kind_combo.setCurrentIndex(1)
                    value = connection.friction_force_factor
                    item.setText(5, f"{value:.3g}" if value else "0")
                    set_disabled(item, [6, 7])

                elif connection.friction_type == FrictionType.Position:
                    friction_kind_combo.setCurrentIndex(2)

                    if loop_with_one_fixed_position:
                        set_disabled(item, [5, 6, 7])
                    else:
                        set_disabled(item, [5])
                        value = connection.friction_point_cable
                        item.setText(6, f"{value:.6g}" if value or value == 0 else "")
                        if isinstance(connection.connection_node, Point):
                            set_disabled(item, [7])
                        else:
                            value = connection.friction_point_connection
                            item.setText(
                                7, f"{value:.3g}" if value or value == 0 else ""
                            )

                friction_kind_combo.currentIndexChanged.connect(self.ui_changed)

        # formatting
        # get the model-index of the first item
        index = self.ui.tree.indexFromItem(self.ui.tree.topLevelItem(0))
        rowheight = self.ui.tree.rowHeight(index)

        n_rows = max(6, N + 3)
        self.ui.tree.setMinimumHeight(n_rows * rowheight)

        self._filling = False
        self.ui.tree.blockSignals(False)

    def ui_changed(self, *args):
        try:
            self._update_model_from_ui()
        except ValueError as e:
            self.show_error(str(e))
            return

        if (
            not self._update_node_from_model()
        ):  # --> will automatically trigger a post_update_event which reloads the model and ui
            self._update_ui_from_model()

    def _update_model_from_ui(self):
        """Update the model from the ui"""

        self.connections_model.clear()
        for i in range(self.ui.tree.topLevelItemCount()):
            item = self.ui.tree.topLevelItem(i)
            connection = self.scene[item.toolTip(1)]  # note: from tooltip!
            reversed = item.checkState(0) == Qt.CheckState.Checked
            offset = float(item.text(2))
            max_winding = float(item.text(3))

            friction_type = FrictionType.No  # default
            widget = self.ui.tree.itemWidget(item, 4)
            if widget:
                friction_type_string = widget.currentText()

                if friction_type_string == "No":
                    friction_type = FrictionType.No
                elif friction_type_string == "Force":
                    friction_type = FrictionType.Force
                elif friction_type_string == "Position":
                    friction_type = FrictionType.Position

            friction_factor = float_or_none(item.text(5))
            friction_cable_point = float_or_none(item.text(6))
            friction_connector_point = float_or_none(item.text(7))

            self.connections_model.append(
                CableConnection(
                    connection,
                    reversed,
                    offset,
                    max_winding,
                    friction_type,
                    friction_factor,
                    friction_cable_point,
                    friction_connector_point,
                )
            )

    def _update_node_from_model(self) -> bool:
        """Checks the model, if valid then generates the code to update the node
        and executes it.
        If the model is not valid, then the ui is updated with errors and no code is executed

        Returns True if the model is valid, False otherwise
        """

        is_loop = (
            self.connections_model[0].connection_node
            == self.connections_model[-1].connection_node
        )

        # loop over the connections in the model and fill the vectors accordingly
        connection_names = [n.connection_node.name for n in self.connections_model]
        reversed = [n.reversed for n in self.connections_model]
        offsets = [n.offset for n in self.connections_model]
        max_winding_angles = [n.max_winding_angle for n in self.connections_model]

        # friction vectors

        # for Cable nodes the endAFr depends on the connections, so we need to check and overrule
        endAFr = self.endAFr
        if isinstance(self.node, Cable):
            endAFr = is_loop

        if not self.endBFr:
            cons = self.connections_model[
                :-1
            ]  # no friction info for the last connection
        else:
            cons = self.connections_model

        if not endAFr:  # note, the local variable
            cons = cons[1:]  # and also not the first connection if not a loop

        friction_types = [n.friction_type for n in cons]
        friction_factors = [n.friction_force_factor for n in cons]
        friction_cable_points = [n.friction_point_cable for n in cons]
        friction_connector_points = [n.friction_point_connection for n in cons]

        # check the values
        self.node: Cable  # type hint only
        errors = self.node._check_friction_vectors(
            connections=connection_names,
            friction_force_factor=friction_factors,
            friction_point_cable=friction_cable_points,
            friction_point_connection=friction_connector_points,
            friction_type=friction_types,
            max_winding_angles=max_winding_angles,
            offsets=offsets,
            reversed=reversed,
        )

        if errors:
            errors = self.node._check_friction_vectors(
                connections=connection_names,
                friction_force_factor=friction_factors,
                friction_point_cable=friction_cable_points,
                friction_point_connection=friction_connector_points,
                friction_type=friction_types,
                max_winding_angles=max_winding_angles,
                offsets=offsets,
                reversed=reversed,
            )
            self.show_error("\n".join(errors))
            return False

        # generate the code

        code = f"connections = {connection_names}\n"
        code += f"reversed = {reversed}\n"
        code += f"offsets = {offsets}\n"
        code += f"max_winding_angles = {max_winding_angles}\n"
        code += f"friction_type = {friction_types}\n"
        code += f"friction_force_factor = {friction_factors}\n"
        code += f"friction_point_cable = {friction_cable_points}\n"
        code += f"friction_point_connection = {friction_connector_points}\n"

        element = f"\ns['{self.node.name}']"
        code += (
            f"{element}.update_connections(connections=connections,\n"
            "                             reversed=reversed,\n"
            "                             offsets=offsets,\n"
            "                             max_winding_angles=max_winding_angles,\n"
            "                             friction_type=friction_type,\n"
            "                             friction_force_factor=friction_force_factor,\n"
            "                             friction_point_cable=friction_point_cable,\n"
            "                             friction_point_connection=friction_point_connection)\n"
        )

        self.run_code(code, guiEventType.SELECTED_NODE_MODIFIED, sender=self)

        return True

    # ---- ui code ----

    def show_error(self, message):
        self.ui.tree.setStyleSheet(ERROR_STYLESHEET)
        self.ui.lblError.setText(message)
        self.ui.lblError.setVisible(True)

    def hide_error(self):
        self.ui.tree.setStyleSheet("")
        self.ui.lblError.setVisible(False)

    def _update_column_visibility(self):
        # hide the friction and max winding angle columns if not applicable
        basic = not self.ui.checkBox.isChecked()
        self.ui.tree.setColumnHidden(4, basic)
        self.ui.tree.setColumnHidden(5, basic)
        self.ui.tree.setColumnHidden(6, basic)
        self.ui.tree.setColumnHidden(7, basic)
        self.ui.pbPinLocations.setHidden(basic)

        # hide the geometry tweaking column if not applicable
        geo = not self.ui.cbGeometryTweaking.isChecked()
        self.ui.tree.setColumnHidden(2, geo)
        self.ui.tree.setColumnHidden(3, geo)

    # ---- drag / drop / reoreder / insert / delete code -----

    def _active_table_row(self):
        if self.ui.tree.selectedItems():
            return self.ui.tree.indexOfTopLevelItem(self.ui.tree.selectedItems()[0])
        return -1

    def delete_selected(self):
        if not self.ui.tree.selectedItems():
            return

        row = self._active_table_row()
        self.connections_model.pop(row)

        self._update_node_from_model()
        self._update_ui_from_model()

    # three ways to call delete_selected
    def deleteKeyPressEvent(self, event):
        if event.key() == Qt.Key_Delete:
            self.delete_selected()

    def dropOnDeleteButtonEvent(self, event):
        if event.source() == self.ui.tree:
            self.delete_selected()

    def dragOntoDeleteButtonEvent(self, event):
        if event.source() == self.ui.tree:
            event.accept()

    # adding an item via the picker/button, added at the end

    def add_item(self):
        name = self.ui.widgetPicker.value
        if self.scene.node_exists(name):

            self.connections_model.append(
                CableConnection(
                    self.scene[name], False, 0, 0, FrictionType.No, None, None, None
                )
            )

            self._update_ui_from_model()
            self._update_node_from_model()
        else:
            self.show_error(f"No node with name {name}")

    # drag/drop in the tree

    def dragEnterEvent(self, event):
        call_from_dragEnter_or_Move_Event(
            self.ui.tree, self.scene, (Circle, Point), event
        )

    def dropEvent(self, event):
        self._filling = True
        tree = self.ui.tree  # alias

        # where are we dropping?

        to_row = -1  # place at end by default
        to_item = self.ui.tree.itemAt(event.pos())
        if to_item:
            to_row = tree.indexOfTopLevelItem(to_item)

        # what item are we dropping or moving
        if event.source() == tree:  # internal move
            from_row = tree.indexOfTopLevelItem(tree.selectedItems()[0])

            if to_row >= 0:
                self.connections_model.insert(
                    to_row, self.connections_model.pop(from_row)
                )
            else:
                self.connections_model.append(self.connections_model.pop(from_row))

        else:
            if event.mimeData().hasText():
                node_name = event.mimeData().text()

                # Node exists and is of the correct type (else drop is not accepted)
                # but check anyways

                if not self.scene.node_exists(node_name):
                    self.show_error(f"No node with name {node_name}")
                    return

                node = self.scene[node_name]
                if not isinstance(node, (Circle, Point)):
                    self.show_error(f"Node {node_name} is not a Circle or Point")
                    return

                # add the node to the model

                # connection_node: [Circle, Point]
                # reversed: bool
                # offset: float
                # max_winding_angle: float
                # friction_type: FrictionType
                # friction_force_factor: float or None
                # friction_point_cable: float or None
                # friction_point_connection: float or None

                new_connection = CableConnection(
                    connection_node=node,
                    reversed=False,
                    offset=0,
                    max_winding_angle=DEFAULT_WINDING_ANGLE,
                    friction_type=FrictionType.No,
                    friction_force_factor=None,
                    friction_point_cable=None,
                    friction_point_connection=None,
                )
                if to_row > 0:
                    self.connections_model.insert(to_row, new_connection)
                else:
                    self.connections_model.append(new_connection)

        self._update_ui_from_model()
        self._update_node_from_model()

    # ---- for SlingGrommet support -----

    def set_shortest_route(self, *args):
        self.run_code(
            f's["{self.node.name}"].set_optimum_connection_directions()',
            guiEventType.SELECTED_NODE_MODIFIED,
        )

    def set_pin_locations(self, *args):
        # update the model

        if isinstance(self.node, Cable):
            self.node.set_sticky_data_from_current_geometry()

        self.guiEmitEvent(guiEventType.SELECTED_NODE_MODIFIED)
        #
        # self._update_model_from_node()
        # self._update_ui_from_model()





    # def show_advanced_settings(self):
    #     dialog = AdvancedCableSettings(cable=self.node)
    #     dialog.exec()
    #     if dialog.code:
    #         self.run_code(dialog.code, guiEventType.SELECTED_NODE_MODIFIED)
