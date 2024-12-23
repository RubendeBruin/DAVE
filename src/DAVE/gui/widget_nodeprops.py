from abc import ABC, abstractmethod


from PySide6.QtGui import QColor

from DAVE import Point, Circle, Buoyancy, Frame
from DAVE.gui.forms.widget_grid_edit_controls import Ui_widgetGridEditControls
from DAVE.gui.helpers.info_message import InfoMessage
from DAVE.gui.widget_gridedit import GriddedNodeEditor
from DAVE.visual_helpers.vtkActorMakers import Line, Lines
from DAVE.gui.dialog_advanced_cable_settings import AdvancedCableSettings
from DAVE.gui.dock_system.dockwidget import *
from PySide6.QtCore import Qt, QSize, QModelIndex
import DAVE.scene as vfs

import DAVE.gui.forms.widget_axis
import DAVE.gui.forms.widget_body
import DAVE.gui.forms.widget_poi
import DAVE.gui.forms.widget_cable
import DAVE.gui.forms.widget_name
import DAVE.gui.forms.widget_visual
import DAVE.gui.forms.widget_force
import DAVE.gui.forms.widget_lincon6
import DAVE.gui.forms.widget_linhyd
import DAVE.gui.forms.widget_beam
import DAVE.gui.forms.widget_con2d
import DAVE.gui.forms.widget_sheave
import DAVE.gui.forms.widget_waveinteraction
import DAVE.gui.forms.widget_contactball
import DAVE.gui.forms.widget_geometricconnection

from DAVE.gui.forms.widget_measurement import Ui_MeasurementWidget
from DAVE.gui.forms.widget_supportpoint import Ui_SupportPointWidget

# import DAVE.gui.forms.widget_sling
import DAVE.gui.forms.widget_tank
import DAVE.gui.forms.widget_area
import DAVE.gui.forms.widget_component
import DAVE.gui.forms.widget_spmt
import DAVE.gui.forms.widget_connections
from DAVE.gui.helpers.nodelist_drag_drop_move import (
    call_from_drop_Event,
    call_from_dragEnter_or_Move_Event,
)
from DAVE.gui.helpers.property_editor import PropertyEditorDialog

from DAVE.visual_helpers.vtkHelpers import transform_from_node
from DAVE.gui.helpers.my_qt_helpers import (
    update_combobox_items_with_completer,
    EnterKeyPressFilter,
    RightClickEventFilter,
)
import numpy as np

from PySide6.QtWidgets import (
    QListWidgetItem,
    QMessageBox,
    QDoubleSpinBox,
    QColorDialog,
    QSizePolicy,
    QCheckBox,
    QTreeWidgetItem,
    QSpacerItem,
    QWidget,
)
from PySide6 import QtWidgets

DAVE_GUI_NODE_EDITORS = dict()  # Key: node-class, value: editor-class

from DAVE.helpers.singleton_class import Singleton


def cbvinf(checkbox: QCheckBox, value: bool, do_block=True):
    """Updates the value in the checkbox IF it does not have focus. Blocks signals during change if do_block is true (default)"""
    if checkbox.hasFocus():
        return

    if do_block:
        remember = checkbox.signalsBlocked()
        checkbox.blockSignals(True)
        checkbox.setChecked(value)
        checkbox.blockSignals(remember)
    else:
        checkbox.setChecked(value)


def svinf(spinbox: QDoubleSpinBox, value: float, do_block=True):
    """Updates the value in the spinbox IF it does not have focus. Blocks signals during change if do_block is true (default)"""
    if spinbox.hasFocus():
        return

    if do_block:
        remember = spinbox.signalsBlocked()
        spinbox.blockSignals(True)
        spinbox.setValue(value)
        spinbox.blockSignals(remember)
    else:
        spinbox.setValue(value)


def tvinf(edit_text, value: str, do_block=True):
    """Updates the value in the spinbox IF it does not have focus. Blocks signals during change if do_block is true (default)"""
    if edit_text.hasFocus():
        return

    if do_block:
        remember = edit_text.signalsBlocked()
        edit_text.blockSignals(True)
        edit_text.setText(value)
        edit_text.blockSignals(remember)
    else:
        edit_text.setText(value)


def cvinf(combobox: QtWidgets.QComboBox, value: str):
    """Updates the value in the combobox IF it does not have focus"""
    if combobox.hasFocus():
        return
    combobox.setCurrentText(value)


def code_if_user_focus(node, control, ref, dec=3):
    """Returns the code to update property "ref" of node "node" with the value in the control if the control has the current focus"""

    if not control.hasFocus():
        return ""

    try:  # try value
        value = control.value()  # for spinboxes and sliders

        if isinstance(value, (int, float)):  # it is a number?
            return code_if_changed_d(node, value, ref, dec=dec)
        else:
            raise ValueError("Not a number")
    except:
        pass

    try:  # try bool
        value = control.isChecked()
        return code_if_changed_b(node, value, ref)
    except:
        pass

    try:  # try text  ; carefull with this one, gives false positives for checkboxes etc that also have a "text" method
        value = control.text()
        return code_if_changed_text(node, value, ref)
    except:
        pass

    raise ValueError("Can not get value from this control")


def code_if_changed_b(node, value, ref):
    """Returns code to change value of property "ref" to "value" if different from target value

    Args:
        node: node
        value: value to check and set
        ref: name of the property

    Returns:
        str

    """
    current = getattr(node, ref)

    if value != current:
        return f"\ns['{node.name}'].{ref} = {value}"
    else:
        return ""


def code_if_changed_d(node, value, ref, dec=3):
    """Returns code to change value of property "ref" to "value" if difference between current and target value
    exceeds tolerance (dec)

    Args:
        node: node
        value: value to check and set
        ref: name of the property
        dec: decimals (3)

    Returns:
        str

    """
    current = getattr(node, ref)

    if abs(value - current) > 10 ** (-dec):
        value = round(value, dec)
        return f"\ns['{node.name}'].{ref} = {value}"
    else:
        return ""


def code_if_changed_text(node, value, ref):
    """Returns code to change value of property "ref" to "value" - applicable for text properties

    Args:
        node: node
        value: value to check and set
        ref: name of the property

    Returns:
        str

    """
    return code_if_changed_path(node, value, ref, accept_empty=True)


def code_if_changed_path(node, value, ref, accept_empty=False) -> str:
    """Returns code to change value of property "ref" to "value" - applicable for paths (r'')

    Does not accept empty paths

    Args:
        node: node
        value: value to check and set
        ref: name of the property

    Returns:
        str

    """
    if not value and not accept_empty:
        return ""

    current = getattr(node, ref)

    if value != current:
        return f"\ns['{node.name}'].{ref} = r'{value}'"
    else:
        return ""


def code_if_changed_v3(node, value, ref, dec=3):
    """Returns code to change value of property "ref" to "value" if difference between current and target value
    exceeds tolerance (dec)

    Args:
        node: node
        value: value to check and set
        ref: name of the property
        dec: decimals (3)

    Returns:
        str

    """
    current = getattr(node, ref)

    # compare components of current to components of value
    if (
        abs(value[0] - current[0]) > 10 ** (-dec)
        or abs(value[1] - current[1]) > 10 ** (-dec)
        or abs(value[2] - current[2]) > 10 ** (-dec)
    ):
        return f"\ns['{node.name}'].{ref} = ({value[0]}, {value[1]},{value[2]})"
    else:
        return ""


"""
In singleton:

    e = Editor.Instance() 
    - runs __init__() which creates the gui
    
    property widget : returns the main widget
    
    e.connect(node, callback, scene, run_code) --> returns widget"""


class NodeEditor(ABC):
    """NodeEditor implements a "singleton" instance of NodeEditor-derived widget.


    __init__ : creates the gui, connects the events  --> typically sets self._widget for the widget property
    connect  : links the widget to the actual model and node
    post_update_event : fill the contents




    properties:
    - node : the node being edited
    - run_code : function to run code - running this function triggers the post_update event on all open editors
    - gui_solve_func : function to the 'solve' button in the gui. Gives the user the possibility to terminate

    """

    @abstractmethod
    def __init__(self):
        """Creates the gui and connects signals"""
        pass

    def connect(
        self,
        node,
        scene,
        run_code,
        guiEmitEvent,
        gui_solve_func,
        node_picker_register_func,
    ):
        """NOTE, overriding this method and then calling super() malfunctions when cythonized."""

        self.node: Node = node
        self.scene: Scene = scene
        self._run_code = run_code
        self.guiEmitEvent = guiEmitEvent
        self.gui_solve_func = gui_solve_func
        self.node_picker_register_func = node_picker_register_func

        self.post_update_event()

        return self.widget

    @property
    def widget(self) -> QtWidgets.QWidget:
        return self._widget

    def run_code(self, code, event=None, sender=None, store_undo=True):
        assert (
            self.node.is_valid
        ), f"Nodeprop attempted to run code while node is not valid. Code was {code}"

        if code == "":
            return

        if event is None:
            return self._run_code(code, sender=sender, store_undo=store_undo)
        else:
            return self._run_code(code, event, sender=sender, store_undo=store_undo)

    @abstractmethod
    def post_update_event(self):
        """Populates the controls to reflect the current state of the node"""
        pass


class AbstractNodeEditorWithParent(NodeEditor):
    """Extended version of NodeEditor featuring a node-picker for the parent of the node.

    - required the ui to have a `widgetParent` of type QNodePicker
    - post_update_event shall call self.ui.widgetParent.fill()
    - if needed, override generate_parent_code
    """

    nodetypes_for_parent = DAVE.nodes.Frame
    NoneAllowedAsParent = True

    def generate_parent_code(self):
        code = ""
        element = "\ns['{}']".format(self.node.name)

        new_parent = self.ui.widgetParent.value
        if new_parent == "":
            new_parent = None
        else:
            new_parent = self.scene[new_parent]

        if new_parent != self.node.parent:
            if new_parent is None:
                code += element + f".parent = None"
            else:
                code += element + f".parent = s['{new_parent.name}']"

        self.run_code(code, guiEventType.MODEL_STRUCTURE_CHANGED)

    def connect(
        self,
        node,
        scene,
        run_code,
        guiEmitEvent,
        gui_solve_func,
        node_picker_register_func,
    ):
        self.ui.widgetParent.initialize(
            scene=scene,
            nodetypes=self.nodetypes_for_parent,
            callback=self.generate_parent_code,
            register_func=node_picker_register_func,
            NoneAllowed=self.NoneAllowedAsParent,
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


class EditNode(NodeEditor):
    """The basic settings of every node: Name and Visible"""

    def __init__(self):
        widget = QtWidgets.QWidget()
        ui = DAVE.gui.forms.widget_name.Ui_NameWidget()
        ui.setupUi(widget)
        self.ui = ui
        self._widget = widget
        self.filling = False
        self._editing = ""

        ui.cbVisible.toggled.connect(self.visible_changed)
        ui.lbColor.mousePressEvent = self.color_clicked

        self.ui.tbName.editingFinished.connect(self.nameChangedEnter)

        self.rightclickfilter = RightClickEventFilter()
        self.rightclickfilter.callback = self.mouse_event_on_tbName
        self.ui.tbName.installEventFilter(self.rightclickfilter)

        self.ui.pbEditAll.clicked.connect(self.edit_all)

    def post_update_event(self):
        self.filling = True
        self.ui.tbName.blockSignals(True)
        self.ui.cbVisible.blockSignals(True)

        self.ui.tbName.setText(self.node.name)
        self._editing = self.node.name
        self.ui.cbVisible.setChecked(self.node.visible)

        self.ui.tbName.blockSignals(False)
        self.ui.cbVisible.blockSignals(False)

        if self.node.color is None:
            self.ui.lbColor.setStyleSheet("")
            self.ui.lbColor.setText("default")
        else:
            self.ui.lbColor.setStyleSheet(
                "background-color: rgb({}, {}, {});".format(*self.node.color)
            )
            self.ui.lbColor.setText(str(self.node.color))

        self.filling = False

    def nameChangedEnter(self):
        if self.filling:
            return

        if self.node.is_valid:
            node = self.node

            if node.name != self._editing:
                return

            element = "\ns['{}']".format(node.name)

            new_name = self.ui.tbName.text()

            if new_name:
                if not new_name == node.name:
                    code = element + ".name = '{}'".format(new_name)
                    self.run_code(code, guiEventType.SELECTED_NODE_MODIFIED)

    def visible_changed(self):
        node = self.node
        element = "\ns['{}']".format(node.name)
        new_visible = self.ui.cbVisible.isChecked()
        if not new_visible == node.visible:
            code = element + ".visible = {}".format(new_visible)
            self.run_code(code, guiEventType.VIEWER_SETTINGS_UPDATE)

    def mouse_event_on_tbName(self, mouseEvent, **kwargs):
        if mouseEvent.button() == QtCore.Qt.MouseButton.RightButton:
            self.name_right_clicked(mouseEvent.pos())
            mouseEvent.setAccepted(True)

    def name_right_clicked(self, point, **kwargs):
        globLoc = self.ui.tbName.mapToGlobal(point)

        menu = QtWidgets.QMenu()

        def copy():
            QApplication.instance().clipboard().setText(self.ui.tbName.text())

        def copys():
            QApplication.instance().clipboard().setText(f"s['{self.ui.tbName.text()}']")

        menu.addAction("copy name", copy)
        menu.addAction("copy s['name']", copys)
        menu.exec_(globLoc)

    def color_clicked(self, mouseEvent, **kwargs):
        if mouseEvent.button() == QtCore.Qt.MouseButton.RightButton:
            code = f"s['{self.node.name}'].color = None"
            self.run_code(code, guiEventType.VIEWER_SETTINGS_UPDATE)
            self.ui.lbColor.setStyleSheet("")
            self.ui.lbColor.setText(str("default"))
            return

        if self.node.color is not None:
            qcolor = QColor(*self.node.color)
            result = QColorDialog().getColor(initial=qcolor)
        else:
            result = QColorDialog().getColor()

        if result.isValid():
            code = f"s['{self.node.name}'].color = ({result.red()},{result.green()},{result.blue()})"
            self.run_code(code, guiEventType.VIEWER_SETTINGS_UPDATE)
            self.ui.lbColor.setStyleSheet(
                "background-color: rgb({}, {}, {});".format(*self.node.color)
            )
            self.ui.lbColor.setText(str(self.node.color))

    def edit_all(self):
        node = self.node  # alias
        all_of_this_type = self.scene.nodes_where(kind=type(node))
        self.select_nodes_callback(all_of_this_type)


@Singleton
class EditAxis(AbstractNodeEditorWithParent):
    nodetypes_for_parent = DAVE.nodes.Frame
    NoneAllowedAsParent = True

    def __init__(self):
        widget = QtWidgets.QWidget()
        ui = DAVE.gui.forms.widget_axis.Ui_widget_axis()
        ui.setupUi(widget)

        self.ui = ui

        self.ui.checkBox_1.stateChanged.connect(self.generate_code)
        self.ui.checkBox_2.stateChanged.connect(self.generate_code)
        self.ui.checkBox_3.stateChanged.connect(self.generate_code)
        self.ui.checkBox_4.stateChanged.connect(self.generate_code)
        self.ui.checkBox_5.stateChanged.connect(self.generate_code)
        self.ui.checkBox_6.stateChanged.connect(self.generate_code)

        self.ui.doubleSpinBox_1.valueChanged.connect(self.generate_code)
        self.ui.doubleSpinBox_2.valueChanged.connect(self.generate_code)
        self.ui.doubleSpinBox_3.valueChanged.connect(self.generate_code)
        self.ui.doubleSpinBox_4.valueChanged.connect(self.generate_code)
        self.ui.doubleSpinBox_5.valueChanged.connect(self.generate_code)
        self.ui.doubleSpinBox_6.valueChanged.connect(self.generate_code)

        # self.ui.pbToggleAllFixes.clicked.connect(self.toggle_fixes)
        self.ui.setFree.clicked.connect(self.set_free)
        self.ui.setFixed.clicked.connect(self.set_fixed)
        self.ui.setFixedPosition.clicked.connect(self.set_fixed_position)
        self.ui.setFixedOrientation.clicked.connect(self.set_fixed_orientation)

        self._widget = widget

    def toggle_fixes(self, states):
        for cb, state in zip(
            [
                self.ui.checkBox_1,
                self.ui.checkBox_2,
                self.ui.checkBox_3,
                self.ui.checkBox_4,
                self.ui.checkBox_5,
                self.ui.checkBox_6,
            ],
            states,
        ):
            cb.blockSignals(True)
            cb.setChecked(state)
            cb.blockSignals(False)

        self.generate_code()

    def set_free(self):
        self.toggle_fixes([False, False, False, False, False, False])

    def set_fixed(self):
        self.toggle_fixes([True, True, True, True, True, True])

    def set_fixed_position(self):
        self.toggle_fixes([True, True, True, False, False, False])

    def set_fixed_orientation(self):
        self.toggle_fixes([False, False, False, True, True, True])

    def post_update_event(self):
        self.ui.widgetParent.fill()

        if self.node.parent is not None:
            self.ui.widgetParent.setValue(self.node.parent.name)
        else:
            self.ui.widgetParent.setValue("")

        widgets = [
            self.ui.checkBox_1,
            self.ui.checkBox_2,
            self.ui.checkBox_3,
            self.ui.checkBox_4,
            self.ui.checkBox_5,
            self.ui.checkBox_6,
            self.ui.doubleSpinBox_1,
            self.ui.doubleSpinBox_2,
            self.ui.doubleSpinBox_3,
            self.ui.doubleSpinBox_4,
            self.ui.doubleSpinBox_5,
            self.ui.doubleSpinBox_6,
        ]

        for widget in widgets:
            widget.blockSignals(True)

        svinf(self.ui.doubleSpinBox_1, self.node.position[0])
        svinf(self.ui.doubleSpinBox_2, self.node.position[1])
        svinf(self.ui.doubleSpinBox_3, self.node.position[2])
        svinf(self.ui.doubleSpinBox_4, self.node.rotation[0])
        svinf(self.ui.doubleSpinBox_5, self.node.rotation[1])
        svinf(self.ui.doubleSpinBox_6, self.node.rotation[2])

        self.ui.checkBox_1.setChecked(self.node.fixed[0])
        self.ui.checkBox_2.setChecked(self.node.fixed[1])
        self.ui.checkBox_3.setChecked(self.node.fixed[2])
        self.ui.checkBox_4.setChecked(self.node.fixed[3])
        self.ui.checkBox_5.setChecked(self.node.fixed[4])
        self.ui.checkBox_6.setChecked(self.node.fixed[5])

        self.check_fixities()

        for widget in widgets:
            widget.blockSignals(False)

    def check_fixities(self):
        """Verifies that the dof fixities in the gui are allowed and displays a warning in the gui if not"""

        # 4,5 and 6 are the checkboxes for the rotations
        freeRX = not self.ui.checkBox_4.isChecked()
        freeRY = not self.ui.checkBox_5.isChecked()
        freeRZ = not self.ui.checkBox_6.isChecked()

        count = [freeRX, freeRY, freeRZ].count(True)

        # set all fine:

        self.ui.lblRotationsWarning.setVisible(False)
        self.ui.doubleSpinBox_4.setEnabled(True)
        self.ui.doubleSpinBox_5.setEnabled(True)
        self.ui.doubleSpinBox_6.setEnabled(True)

        if count == 2:
            self.ui.lblRotationsWarning.setVisible(True)

        if count == 1 or count == 2:
            if not freeRX:
                self.ui.doubleSpinBox_4.setValue(0)
                self.ui.doubleSpinBox_4.setEnabled(False)
            if not freeRY:
                self.ui.doubleSpinBox_5.setValue(0)
                self.ui.doubleSpinBox_5.setEnabled(False)
            if not freeRZ:
                self.ui.doubleSpinBox_6.setValue(0)
                self.ui.doubleSpinBox_6.setEnabled(False)

    def generate_code(self):
        code = ""
        element = "\ns['{}']".format(self.node.name)

        new_position = np.array(
            (
                self.ui.doubleSpinBox_1.value(),
                self.ui.doubleSpinBox_2.value(),
                self.ui.doubleSpinBox_3.value(),
            )
        )
        new_rotation = np.array(
            (
                self.ui.doubleSpinBox_4.value(),
                self.ui.doubleSpinBox_5.value(),
                self.ui.doubleSpinBox_6.value(),
            )
        )
        new_fixed = np.array(
            (
                self.ui.checkBox_1.isChecked(),
                self.ui.checkBox_2.isChecked(),
                self.ui.checkBox_3.isChecked(),
                self.ui.checkBox_4.isChecked(),
                self.ui.checkBox_5.isChecked(),
                self.ui.checkBox_6.isChecked(),
            )
        )

        if not np.all(round3d(new_position) == round3d(self.node.position)):
            code += element + ".position = ({}, {}, {})".format(*new_position)

        if not np.all(round3d(new_rotation) == round3d(self.node.rotation)):
            code += element + ".rotation = ({}, {}, {})".format(*new_rotation)

        if not np.all(new_fixed == self.node.fixed):
            code += element + ".fixed = ({}, {}, {}, {}, {}, {})".format(*new_fixed)

        self.run_code(code)


@Singleton
class EditVisual(AbstractNodeEditorWithParent):
    nodetypes_for_parent = DAVE.nodes.Frame
    NoneAllowedAsParent = True

    def __init__(self):
        widget = QtWidgets.QWidget()
        ui = DAVE.gui.forms.widget_visual.Ui_widget_axis()
        ui.setupUi(widget)
        ui.cbInvertNormals.setVisible(False)
        self.ui = ui
        self._widget = widget

        self.ui.doubleSpinBox_1.valueChanged.connect(self.generate_code)
        self.ui.doubleSpinBox_2.valueChanged.connect(self.generate_code)
        self.ui.doubleSpinBox_3.valueChanged.connect(self.generate_code)
        self.ui.doubleSpinBox_4.valueChanged.connect(self.generate_code)
        self.ui.doubleSpinBox_5.valueChanged.connect(self.generate_code)
        self.ui.doubleSpinBox_6.valueChanged.connect(self.generate_code)
        self.ui.doubleSpinBox_7.valueChanged.connect(self.generate_code)
        self.ui.doubleSpinBox_8.valueChanged.connect(self.generate_code)
        self.ui.doubleSpinBox_9.valueChanged.connect(self.generate_code)

    def connect(
        self,
        node,
        scene,
        run_code,
        guiEmitEvent,
        gui_solve_func,
        node_picker_register_func,
    ):

        self.ui.resource_selector.initialize(
            scene=scene,
            resource_types=["stl", "obj", "glb", "gltf"],
            callback=self.generate_code,
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
        self.ui.widgetParent.fill()

        widgets = [
            self.ui.doubleSpinBox_1,
            self.ui.doubleSpinBox_2,
            self.ui.doubleSpinBox_3,
            self.ui.doubleSpinBox_4,
            self.ui.doubleSpinBox_5,
            self.ui.doubleSpinBox_6,
            self.ui.doubleSpinBox_7,
            self.ui.doubleSpinBox_8,
            self.ui.doubleSpinBox_9,
        ]

        for widget in widgets:
            widget.blockSignals(True)

        svinf(self.ui.doubleSpinBox_1, self.node.offset[0])
        svinf(self.ui.doubleSpinBox_2, self.node.offset[1])
        svinf(self.ui.doubleSpinBox_3, self.node.offset[2])
        svinf(self.ui.doubleSpinBox_4, self.node.rotation[0])
        svinf(self.ui.doubleSpinBox_5, self.node.rotation[1])
        svinf(self.ui.doubleSpinBox_6, self.node.rotation[2])
        svinf(self.ui.doubleSpinBox_7, self.node.scale[0])
        svinf(self.ui.doubleSpinBox_8, self.node.scale[1])
        svinf(self.ui.doubleSpinBox_9, self.node.scale[2])

        self.ui.resource_selector.setValue(self.node.path)

        for widget in widgets:
            widget.blockSignals(False)

    def generate_code(self):

        if not self.ui.resource_selector._check_value():
            return

        code = ""
        element = "\ns['{}']".format(self.node.name)

        new_position = np.array(
            (
                self.ui.doubleSpinBox_1.value(),
                self.ui.doubleSpinBox_2.value(),
                self.ui.doubleSpinBox_3.value(),
            )
        )
        new_rotation = np.array(
            (
                self.ui.doubleSpinBox_4.value(),
                self.ui.doubleSpinBox_5.value(),
                self.ui.doubleSpinBox_6.value(),
            )
        )
        new_scale = np.array(
            (
                self.ui.doubleSpinBox_7.value(),
                self.ui.doubleSpinBox_8.value(),
                self.ui.doubleSpinBox_9.value(),
            )
        )

        new_path = self.ui.resource_selector.value

        if not new_path == self.node.path:
            # check if path is valid
            if self.scene.is_valid_resource_path(new_path):
                code += element + ".path = r'{}'".format(new_path)
        if not np.all(new_position == self.node.offset):
            code += element + ".offset = ({}, {}, {})".format(*new_position)

        if not np.all(new_rotation == self.node.rotation):
            code += element + ".rotation = ({}, {}, {})".format(*new_rotation)

        if not np.all(new_scale == self.node.scale):
            code += element + ".scale = ({}, {}, {})".format(*new_scale)

        self.run_code(code)


@Singleton
class EditWaveInteraction(AbstractNodeEditorWithParent):
    nodetypes_for_parent = DAVE.nodes.Frame
    NoneAllowedAsParent = False

    def __init__(self):
        widget = QtWidgets.QWidget()
        ui = DAVE.gui.forms.widget_waveinteraction.Ui_widget_waveinteraction()
        ui.setupUi(widget)
        self._widget = widget

        ui.doubleSpinBox_1.valueChanged.connect(self.generate_code)
        ui.doubleSpinBox_2.valueChanged.connect(self.generate_code)
        ui.doubleSpinBox_3.valueChanged.connect(self.generate_code)
        ui.comboBox.editTextChanged.connect(self.generate_code)
        ui.pbRescan.clicked.connect(self.update_resource_list)

        self.resources_loaded = False

        self.ui = ui

    def update_resource_list(self):
        dhyd = self.scene.get_resource_list("dhyd", include_subdirs=True)
        hyd = self.scene.get_resource_list("hyd", include_subdirs=True)

        names = (*dhyd, *hyd)

        update_combobox_items_with_completer(self.ui.comboBox, names)

    def post_update_event(self):
        self.ui.widgetParent.fill()

        if not self.resources_loaded:
            self.update_resource_list()
            self.resources_loaded = True

        widgets = [
            self.ui.doubleSpinBox_1,
            self.ui.doubleSpinBox_2,
            self.ui.doubleSpinBox_3,
            self.ui.comboBox,
        ]

        for widget in widgets:
            widget.blockSignals(True)

        svinf(self.ui.doubleSpinBox_1, self.node.offset[0])
        svinf(self.ui.doubleSpinBox_2, self.node.offset[1])
        svinf(self.ui.doubleSpinBox_3, self.node.offset[2])

        cvinf(self.ui.comboBox, str(self.node.path))

        for widget in widgets:
            widget.blockSignals(False)

    def generate_code(self):
        code = ""
        element = "\ns['{}']".format(self.node.name)

        if self.scene.is_valid_resource_path(self.ui.comboBox.currentText()):
            self.ui.comboBox.setStyleSheet("")
        else:
            self.ui.comboBox.setStyleSheet("background: orange")

        new_position = np.array(
            (
                self.ui.doubleSpinBox_1.value(),
                self.ui.doubleSpinBox_2.value(),
                self.ui.doubleSpinBox_3.value(),
            )
        )
        new_path = self.ui.comboBox.currentText()

        if not new_path == self.node.path:
            if self.scene.is_valid_resource_path(new_path):
                code += element + ".path = r'{}'".format(new_path)

        if not np.all(new_position == self.node.offset):
            code += element + ".offset = ({}, {}, {})".format(*new_position)

        self.run_code(code)


@Singleton
class EditComponent(NodeEditor):
    def __init__(self):
        """Create the gui, store the main widget as self._widget"""

        widget = QtWidgets.QWidget()
        ui = DAVE.gui.forms.widget_component.Ui_component()
        ui.setupUi(widget)
        self.ui = ui
        self._widget = widget

        self.fileextension = "dave"
        self.resources_loaded = False

        self.ui.pbEditExposedProperties.clicked.connect(self.edit_exposed)

    def connect(
        self,
        node,
        scene,
        run_code,
        guiEmitEvent,
        gui_solve_func,
        node_picker_register_func,
    ):

        self.ui.resource_selector.initialize(
            scene=scene, resource_types=".dave", callback=self.generate_code
        )
        self.ui.resource_selector.callback_reload = self.reload

        return super().connect(
            node,
            scene,
            run_code,
            guiEmitEvent,
            gui_solve_func,
            node_picker_register_func,
        )

    def reload(self):
        code = f"\ns['{self.node.name}'].path = r'{self.node.path}'"
        self.run_code(code, guiEventType.MODEL_STRUCTURE_CHANGED)

    def post_update_event(self):
        """Sync the properties of the node to the gui"""

        self.ui.resource_selector.setValue(self.node.path)

        if self.node.exposed_properties:
            self.ui.pbEditExposedProperties.setEnabled(True)
        else:
            self.ui.pbEditExposedProperties.setEnabled(False)

    def edit_exposed(self):
        """Edit the exposed properties"""

        def getter(name):
            return self.node.get_exposed(name)

        def setter(name, value):
            self.node.set_exposed(name, value)
            self.guiEmitEvent(guiEventType.SELECTED_NODE_MODIFIED)

        names = self.node.exposed_properties
        types = [self.node.get_exposed_type(name) for name in names]

        pe = PropertyEditorDialog(
            prop_names=names,
            prop_types=types,
            getter_callback=getter,
            setter_callback=setter,
            parent=self.widget,
        )
        pe.exec_()

    def generate_code(self):
        """Generate code to update the node, then run it"""

        if not self.ui.resource_selector._check_value():
            return

        if self.ui.resource_selector.value == self.node.path:
            return

        code = f"\ns['{self.node.name}'].path = r'{self.ui.resource_selector.value}'"
        self.run_code(code, guiEventType.MODEL_STRUCTURE_CHANGED)


# ======================================


@Singleton
class EditTank(NodeEditor):
    def __init__(self):
        widget = QtWidgets.QWidget()
        ui = DAVE.gui.forms.widget_tank.Ui_Form()
        ui.setupUi(widget)
        self.ui = ui
        self._widget = widget

        self.ui.sbPermeability.valueChanged.connect(self.generate_code)
        self.ui.sbDenstiy.valueChanged.connect(self.generate_code)
        self.ui.sbVolume.valueChanged.connect(self.generate_code)
        self.ui.sbPercentage.valueChanged.connect(self.generate_code)
        self.ui.sbElevation.valueChanged.connect(self.generate_code)
        self.ui.cbFreeFlooding.toggled.connect(self.generate_code)
        self.ui.cbUseOutsideDensity.toggled.connect(self.generate_code)

    def post_update_event(self):
        widgets = [
            self.ui.sbDenstiy,
            self.ui.sbVolume,
            self.ui.sbPercentage,
            self.ui.sbElevation,
            self.ui.cbFreeFlooding,
            self.ui.sbPermeability,
        ]

        for widget in widgets:
            widget.blockSignals(True)

        svinf(self.ui.sbPermeability, self.node.permeability)
        svinf(self.ui.sbDenstiy, self.node.density)
        svinf(self.ui.sbVolume, self.node.volume)
        svinf(self.ui.sbPercentage, self.node.fill_pct)
        svinf(self.ui.sbElevation, self.node.level_global)

        self.ui.cbFreeFlooding.setChecked(self.node.free_flooding)

        self.ui.cbUseOutsideDensity.setChecked(self.node.density < 0)

        if self.node.density < 0:
            svinf(self.ui.sbDenstiy, self.scene.rho_water)

        for widget in widgets:
            widget.blockSignals(False)

        self.ui.sbDenstiy.setEnabled(self.node.density >= 0)
        self.ui.widgetContents.setEnabled(not self.node.free_flooding)
        self.ui.lblCapacity.setText(f"{self.node.capacity:.3f} m3")
        self.ui.lbUllage.setText(f"{self.node.ullage:.3f} m")
        self.ui.lbSounding.setText(f"{self.node.sounding:.3f} m")

    def generate_code(self):
        new_density = self.ui.sbDenstiy.value()
        new_permeability = self.ui.sbPermeability.value()
        new_volume = self.ui.sbVolume.value()
        new_pct = self.ui.sbPercentage.value()
        new_elev = self.ui.sbElevation.value()
        new_free_flooding = self.ui.cbFreeFlooding.isChecked()

        if self.ui.cbUseOutsideDensity.isChecked():
            new_density = -1

        def add(name, value, ref, dec=3):
            current = getattr(self.node, ref)

            if abs(value - current) > 10 ** (-dec):
                return f"\ns['{name}'].{ref} = {value}"
            else:
                return ""

        name = self.node.name
        code = ""

        code += add(name, new_permeability, "permeability", dec=8)
        code += add(name, new_free_flooding, "free_flooding")
        code += add(name, new_density, "density")
        code += add(name, new_volume, "volume")
        code += add(name, new_pct, "fill_pct")
        code += add(name, new_elev, "level_global")

        self.run_code(code)


@Singleton
class EditMeasurement(NodeEditor):

    def __init__(self):
        widget = QtWidgets.QWidget()
        ui = Ui_MeasurementWidget()
        ui.setupUi(widget)
        self.ui = ui
        self._widget = widget

        # fill cbDirection with the possible values
        # get all names of MeasurementDirection enum
        options = [d.name for d in MeasurementDirection]
        self.ui.cbDirection.addItems(options)

        # connect signals
        self.ui.rbDistance.toggled.connect(self.changed)
        self.ui.rbAngle.toggled.connect(self.changed)
        self.ui.cbDirection.currentIndexChanged.connect(self.changed)
        self.ui.cbFlipAngleDirection.toggled.connect(self.changed)

        self.ui.pbUpdatePos.clicked.connect(self.update_pos)
        self.ui.pbUpdateInverted.clicked.connect(self.update_inverted)

    # override connect to initialize the pickers
    def connect(
        self,
        node,
        scene,
        run_code,
        guiEmitEvent,
        gui_solve_func,
        node_picker_register_func,
    ):
        self.ui.npFrame.initialize(
            scene=scene,
            nodetypes=(Frame),
            callback=self.changed,
            register_func=node_picker_register_func,
            NoneAllowed=True,
            node=node,
        )

        self.ui.npPoint1.initialize(
            scene=scene,
            nodetypes=(Point, Frame, Circle),
            callback=self.changed,
            register_func=node_picker_register_func,
            NoneAllowed=False,
            node=node,
        )

        self.ui.npPoint2.initialize(
            scene=scene,
            nodetypes=(Point, Frame, Circle),
            callback=self.changed,
            register_func=node_picker_register_func,
            NoneAllowed=False,
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

    def update_pos(self):
        self._update_reference(False)

    def update_inverted(self):
        self._update_reference(True)

    def _update_reference(self, inverted):
        code = (
            f"s['{self.node.name}'].update_positive_direction_guide(invert={inverted})"
        )
        self.run_code(code)

    def post_update_event(self):

        # update properties
        try:
            self.filling = True

            self.ui.npFrame.fill(property_name="reference_frame")
            self.ui.npPoint1.fill(property_name="point1")
            self.ui.npPoint2.fill(property_name="point2")

            # noinspection PyTypeChecker
            node: Measurement = self.node  # alias and type hint

            if node.kind == MeasurementType.Distance:
                self.ui.rbDistance.setChecked(True)
            elif node.kind == MeasurementType.Angle:
                self.ui.rbAngle.setChecked(True)
            else:
                raise ValueError(
                    f"Unknown measurement type {node.kind} for node {node.name}"
                )

            self.ui.cbDirection.setCurrentText(node.reference.name)
            self.ui.cbFlipAngleDirection.setChecked(node.flip_angle_direction)

            self.apply_gui_values_based_view()

        finally:
            self.filling = False

    def apply_gui_values_based_view(self):
        # Apply formatting based on the measurement type
        if self.ui.rbDistance.isChecked():
            self.ui.label.setText("Direction")
            self.ui.pbUpdateInverted.setText("Update direction as -")
            self.ui.pbUpdatePos.setText("Update direction as +")
            self.ui.cbFlipAngleDirection.setVisible(False)
        else:
            self.ui.label.setText("Reference")
            self.ui.pbUpdateInverted.setText("Update angle as > 90")
            self.ui.pbUpdatePos.setText("Update angle as < 90")
            self.ui.cbFlipAngleDirection.setVisible(True)

        if self.ui.cbDirection.currentText() == "Total":
            self.ui.widget_advanced.setVisible(False)
            self.ui.npFrame.setVisible(False)
            self.ui.label_5.setVisible(False)
        else:
            self.ui.widget_advanced.setVisible(True)
            self.ui.npFrame.setVisible(True)
            self.ui.label_5.setVisible(True)

    def changed(self):
        if self.filling:
            return

        # get the current values and generate code
        self.apply_gui_values_based_view()

        # see if what we try to do makes sense
        if self.ui.cbDirection.currentText() == "Total" and self.ui.rbAngle.isChecked():
            self.ui.cbDirection.setCurrentIndex(
                0
            )  # forces another changed() event which is ok!
            return

        code = ""
        element = "\ns['{}']".format(self.node.name)

        # noinspection PyTypeChecker
        node: Measurement = self.node  # alias and type hint

        # change in kind?
        if self.ui.rbDistance.isChecked() and node.kind != MeasurementType.Distance:
            code += element + ".kind = MeasurementType.Distance"

        if self.ui.rbAngle.isChecked() and node.kind != MeasurementType.Angle:
            code += element + ".kind = MeasurementType.Angle"

        # change in direction?
        if self.ui.cbDirection.currentText() != node.reference.name:
            code += (
                element
                + f".reference = MeasurementDirection.{self.ui.cbDirection.currentText()}"
            )

        # change in flip angle direction?
        if self.ui.cbFlipAngleDirection.isChecked() != node.flip_angle_direction:
            code += (
                element
                + f".flip_angle_direction = {self.ui.cbFlipAngleDirection.isChecked()}"
            )

        # change in point1?
        if self.ui.npPoint1.value != node.point1.name:
            code += element + f".point1 = s['{self.ui.npPoint1.value}']"

        # change in point2?
        if self.ui.npPoint2.value != node.point2.name:
            code += element + f".point2 = s['{self.ui.npPoint2.value}']"

        # change in reference frame?
        frameValue = self.ui.npFrame.value
        if frameValue == "":
            frameValue = None

        if frameValue != node.reference_frame:
            if self.ui.npFrame.value:
                code += element + f".reference_frame = s['{self.ui.npFrame.value}']"
            else:
                code += element + f".reference_frame = None"

        self.run_code(code)


@Singleton
class EditSupportPoint(NodeEditor):

    def __init__(self):
        widget = QtWidgets.QWidget()
        ui = Ui_SupportPointWidget()
        ui.setupUi(widget)
        self.ui = ui
        self._widget = widget

        # connect signals
        self.ui.dsKx.valueChanged.connect(self.changed)
        self.ui.dsKy.valueChanged.connect(self.changed)
        self.ui.dsKz.valueChanged.connect(self.changed)
        self.ui.dsDeltaZ.valueChanged.connect(self.changed)

    # override connect to initialize the pickers
    def connect(
        self,
        node,
        scene,
        run_code,
        guiEmitEvent,
        gui_solve_func,
        node_picker_register_func,
    ):
        self.ui.npFrame.initialize(
            scene=scene,
            nodetypes=(Frame),
            callback=self.changed,
            register_func=node_picker_register_func,
            NoneAllowed=False,
            node=node,
        )

        self.ui.npPoint.initialize(
            scene=scene,
            nodetypes=(Point),
            callback=self.changed,
            register_func=node_picker_register_func,
            NoneAllowed=False,
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

        # update properties
        try:
            self.filling = True

            self.ui.npFrame.fill(property_name="frame")
            self.ui.npPoint.fill(property_name="point")

            # noinspection PyTypeChecker
            node: SupportPoint = self.node  # alias and type hint

            self.ui.dsKx.setValue(node.kx)
            self.ui.dsKy.setValue(node.ky)
            self.ui.dsKz.setValue(node.kz)
            self.ui.dsDeltaZ.setValue(node.delta_z)
        finally:
            self.filling = False

    def changed(self):
        if self.filling:
            return

        code = ""
        element = "\ns['{}']".format(self.node.name)

        # noinspection PyTypeChecker
        node: SupportPoint = self.node  # alias and type hint

        # change in point?
        if self.ui.npPoint.value != node.point.name:
            code += element + f".point = s['{self.ui.npPoint.value}']"

        # change in frame?
        if self.ui.npFrame.value != node.frame.name:
            code += element + f".frame = s['{self.ui.npFrame.value}']"

        code += code_if_changed_d(node, self.ui.dsKz.value(), "kz", 3)
        code += code_if_changed_d(node, self.ui.dsDeltaZ.value(), "delta_z", 3)
        code += code_if_changed_d(node, self.ui.dsKx.value(), "kx", 3)
        code += code_if_changed_d(node, self.ui.dsKy.value(), "ky", 3)

        self.run_code(code)


@Singleton
class EditBuoyancyOrContactMesh(AbstractNodeEditorWithParent):
    nodetypes_for_parent = DAVE.nodes.Frame
    NoneAllowedAsParent = False

    def __init__(self):
        widget = QtWidgets.QWidget()
        ui = DAVE.gui.forms.widget_visual.Ui_widget_axis()  # same as visual widget!
        ui.setupUi(widget)
        self.ui = ui
        self._widget = widget

        ui.doubleSpinBox_1.valueChanged.connect(self.generate_code)
        ui.doubleSpinBox_2.valueChanged.connect(self.generate_code)
        ui.doubleSpinBox_3.valueChanged.connect(self.generate_code)
        ui.doubleSpinBox_4.valueChanged.connect(self.generate_code)
        ui.doubleSpinBox_5.valueChanged.connect(self.generate_code)
        ui.doubleSpinBox_6.valueChanged.connect(self.generate_code)
        ui.doubleSpinBox_7.valueChanged.connect(self.generate_code)
        ui.doubleSpinBox_8.valueChanged.connect(self.generate_code)
        ui.doubleSpinBox_9.valueChanged.connect(self.generate_code)

        ui.cbInvertNormals.toggled.connect(self.generate_code)

    def connect(
        self,
        node,
        scene,
        run_code,
        guiEmitEvent,
        gui_solve_func,
        node_picker_register_func,
    ):

        self.ui.resource_selector.initialize(
            scene=scene, resource_types=["stl", "obj"], callback=self.generate_code
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
        self.ui.widgetParent.fill()

        widgets = [
            self.ui.doubleSpinBox_1,
            self.ui.doubleSpinBox_2,
            self.ui.doubleSpinBox_3,
            self.ui.doubleSpinBox_4,
            self.ui.doubleSpinBox_5,
            self.ui.doubleSpinBox_6,
            self.ui.doubleSpinBox_7,
            self.ui.doubleSpinBox_8,
            self.ui.doubleSpinBox_9,
            self.ui.cbInvertNormals,
        ]

        for widget in widgets:
            widget.blockSignals(True)

        svinf(self.ui.doubleSpinBox_1, self.node.trimesh._offset[0])
        svinf(self.ui.doubleSpinBox_2, self.node.trimesh._offset[1])
        svinf(self.ui.doubleSpinBox_3, self.node.trimesh._offset[2])
        svinf(self.ui.doubleSpinBox_4, self.node.trimesh._rotation[0])
        svinf(self.ui.doubleSpinBox_5, self.node.trimesh._rotation[1])
        svinf(self.ui.doubleSpinBox_6, self.node.trimesh._rotation[2])
        svinf(self.ui.doubleSpinBox_7, self.node.trimesh._scale[0])
        svinf(self.ui.doubleSpinBox_8, self.node.trimesh._scale[1])
        svinf(self.ui.doubleSpinBox_9, self.node.trimesh._scale[2])

        self.ui.cbInvertNormals.setChecked(self.node.trimesh._invert_normals)

        self.ui.resource_selector.setValue(self.node.trimesh._path)

        for widget in widgets:
            widget.blockSignals(False)

    def generate_code(self):

        # do not generate code if the resource is not valid
        if not self.ui.resource_selector._check_value():
            return

        code = ""
        element = "\ns['{}']".format(self.node.name)

        offset = np.array(
            (
                self.ui.doubleSpinBox_1.value(),
                self.ui.doubleSpinBox_2.value(),
                self.ui.doubleSpinBox_3.value(),
            )
        )
        rotation = np.array(
            (
                self.ui.doubleSpinBox_4.value(),
                self.ui.doubleSpinBox_5.value(),
                self.ui.doubleSpinBox_6.value(),
            )
        )
        scale = np.array(
            (
                self.ui.doubleSpinBox_7.value(),
                self.ui.doubleSpinBox_8.value(),
                self.ui.doubleSpinBox_9.value(),
            )
        )
        invert_normals = self.ui.cbInvertNormals.isChecked()

        new_path = self.ui.resource_selector.value

        # check if we need to reload the mesh
        if (
            np.any(offset != self.node.trimesh._offset)
            or np.any(rotation != self.node.trimesh._rotation)
            or np.any(scale != self.node.trimesh._scale)
            or invert_normals != self.node.trimesh._invert_normals
            or self.node.trimesh._path != new_path
        ):
            if invert_normals:
                code = (
                    element
                    + ".trimesh.load_file(r'{}', scale = ({},{},{}), rotation = ({},{},{}), offset = ({},{},{}), invert_normals=True)".format(
                        new_path, *scale, *rotation, *offset
                    )
                )
            else:
                code = (
                    element
                    + ".trimesh.load_file(r'{}', scale = ({},{},{}), rotation = ({},{},{}), offset = ({},{},{}))".format(
                        new_path, *scale, *rotation, *offset
                    )
                )

        self.run_code(code)


@Singleton
class EditBody(NodeEditor):
    def __init__(self):
        widget = QtWidgets.QWidget()
        ui = DAVE.gui.forms.widget_body.Ui_Form()
        ui.setupUi(widget)
        self.ui = ui
        self._widget = widget

        ui.doubleSpinBox_1.valueChanged.connect(self.generate_code)
        ui.doubleSpinBox_2.valueChanged.connect(self.generate_code)
        ui.doubleSpinBox_3.valueChanged.connect(self.generate_code)
        ui.doubleSpinBox_mass.valueChanged.connect(self.generate_code)

    def post_update_event(self):
        widgets = [
            self.ui.doubleSpinBox_1,
            self.ui.doubleSpinBox_2,
            self.ui.doubleSpinBox_3,
            self.ui.doubleSpinBox_mass,
        ]

        for widget in widgets:
            widget.blockSignals(True)

        svinf(self.ui.doubleSpinBox_1, self.node.cog[0])
        svinf(self.ui.doubleSpinBox_2, self.node.cog[1])
        svinf(self.ui.doubleSpinBox_3, self.node.cog[2])
        svinf(self.ui.doubleSpinBox_mass, self.node.mass)

        for widget in widgets:
            widget.blockSignals(False)

    def generate_code(self):
        code = ""
        element = "\ns['{}']".format(self.node.name)

        new_mass = self.ui.doubleSpinBox_mass.value()
        new_cog = np.array(
            (
                self.ui.doubleSpinBox_1.value(),
                self.ui.doubleSpinBox_2.value(),
                self.ui.doubleSpinBox_3.value(),
            )
        )

        if new_mass != self.node.mass:
            code += element + ".mass = {}".format(new_mass)

        if not np.all(new_cog == self.node.cog):
            code += element + ".cog = ({}, {}, {})".format(*new_cog)

        self.run_code(code)


@Singleton
class EditPoi(AbstractNodeEditorWithParent):
    nodetypes_for_parent = DAVE.nodes.Frame
    NoneAllowedAsParent = True

    def __init__(self):
        widget = QtWidgets.QWidget()
        ui = DAVE.gui.forms.widget_poi.Ui_Poi()
        ui.setupUi(widget)
        self.ui = ui
        self._widget = widget

        ui.doubleSpinBox_1.valueChanged.connect(self.generate_code)
        ui.doubleSpinBox_2.valueChanged.connect(self.generate_code)
        ui.doubleSpinBox_3.valueChanged.connect(self.generate_code)

    def post_update_event(self):
        self.ui.widgetParent.fill()

        widgets = [
            self.ui.doubleSpinBox_1,
            self.ui.doubleSpinBox_2,
            self.ui.doubleSpinBox_3,
        ]

        for widget in widgets:
            widget.blockSignals(True)

        svinf(self.ui.doubleSpinBox_1, self.node.position[0])
        svinf(self.ui.doubleSpinBox_2, self.node.position[1])
        svinf(self.ui.doubleSpinBox_3, self.node.position[2])

        for widget in widgets:
            widget.blockSignals(False)

    def generate_code(self):
        code = ""
        element = "\ns['{}']".format(self.node.name)

        new_position = np.array(
            (
                self.ui.doubleSpinBox_1.value(),
                self.ui.doubleSpinBox_2.value(),
                self.ui.doubleSpinBox_3.value(),
            )
        )

        if not np.all(new_position == self.node.position):
            code += element + ".position = ({}, {}, {})".format(*new_position)

        self.run_code(code)


@Singleton
class EditConnections(NodeEditor):
    def __init__(self):
        self.node: Cable  # type hint only

        widget = QtWidgets.QWidget()
        ui = DAVE.gui.forms.widget_connections.Ui_ConnectionForm()
        ui.setupUi(widget)

        self.ui = ui
        self._widget = widget

        self._widget.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        self.additional_pois = list()

        self.ui.tree.sizeHint = lambda: QSize(0, 0)  # disable the size-hint

        self.ui.tree.setHeaderLabels(
            ["⭮/⭯", "Connection", "Offset", "Friction", "Max winding"]
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

    def post_update_event(self):
        # update the combobox with points and circles
        self.ui.widgetPicker.fill("keep")

        labelVisible = False

        # make strings of all properties
        # and align with connections

        (
            endAFr,
            endAMaxWind,
            endBFr,
            endBMaxWind,
            is_grommet_in_line_mode,
        ) = self.node._get_advanced_settings_dialog_settings()

        # frictions
        frictions = []
        if not endAFr:  # friction at endA not definable
            frictions.append("-")  # first item
        for friction in self.node.friction:
            if friction is not None:
                frictions.append(str(friction))
            else:
                frictions.append("?")  # NONE

        if not endBFr:
            frictions.append("-")  # last item

        # maximum winding angles
        mas = [str(ma) for ma in self.node.max_winding_angles]

        # offsets
        offsets = [str(offset) for offset in self.node.offsets]

        N = len(self.node.connections)

        self.ui.tree.blockSignals(True)  # update the list
        self.ui.tree.clear()

        for i, (connection, reversed, friction_s, maxa_s, offs) in enumerate(
            zip(self.node.connections, self.node.reversed, frictions, mas, offsets)
        ):
            item = QTreeWidgetItem(self.ui.tree)
            item.setText(0, " ")
            item.setText(1, connection.name)
            item.setText(2, offs)
            item.setText(3, friction_s)
            item.setText(4, maxa_s)

            self.ui.tree.addTopLevelItem(item)

            if isinstance(connection, Circle):
                item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
                item.setCheckState(
                    0,
                    Qt.CheckState.Checked if reversed else Qt.CheckState.Unchecked,
                )
                labelVisible = True

            item.setFlags(item.flags() | Qt.ItemIsEditable)

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
        self.ui.tree.setColumnHidden(2, basic)
        self.ui.tree.setColumnHidden(3, basic)
        self.ui.tree.setColumnHidden(4, basic)
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
        a_friction = []
        a_maw = []

        try:  # catch value errors in float / str conversions
            for i in range(N):
                item = self.ui.tree.invisibleRootItem().child(i)

                reversed = item.checkState(0) == Qt.CheckState.Checked
                connection = item.text(1)
                offset = item.text(2)
                friction = item.text(3)
                max_winding = item.text(4)

                a_connections.append(connection)
                a_reversed.append(reversed)
                a_offsets.append(float(offset))

                if friction == "-":
                    pass
                elif friction.strip() == "?":
                    a_friction.append(None)
                else:
                    a_friction.append(float(friction))
                a_maw.append(float(max_winding))
        except ValueError:
            self.ui.tree.setStyleSheet("background-color: rgb(251, 220, 255)")
            return

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

            if a_reversed != self.node.reversed:
                code += f"{element}.reversed = {a_reversed}"

                self.node.reversed = a_reversed

            if a_offsets != self.node.offsets:
                code += f"{element}.offsets = {a_offsets}"

                self.node.offsets = a_offsets

            if a_friction != self.node.friction:
                code += f"{element}.friction = {a_friction}"

                self.node.friction = a_friction

            if a_maw != self.node.max_winding_angles:
                code += f"{element}.max_winding_angles = {a_maw}"

                self.node.max_winding_angles = a_maw

        except Exception as e:
            self.ui.tree.setStyleSheet("background-color: rgb(251, 220, 255)")
            self.ui.lblError.setText(str(e))
            self.ui.lblError.setVisible(True)
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


@Singleton
class EditCable(NodeEditor):
    def __init__(self):
        widget = QtWidgets.QWidget()
        ui = DAVE.gui.forms.widget_cable.Ui_Cable_form()
        ui.setupUi(widget)

        self.ui = ui
        self._widget = widget

        # Set events

        ui.doubleSpinBox.valueChanged.connect(self.generate_code)
        ui.doubleSpinBox_1.valueChanged.connect(self.generate_code)
        ui.doubleSpinBox_2.valueChanged.connect(self.generate_code)
        ui.doubleSpinBox_3.valueChanged.connect(self.generate_code)
        ui.doubleSpinBox_4.valueChanged.connect(self.generate_code)
        ui.cbSolveSegmentLengths.toggled.connect(self.generate_code)

    def post_update_event(self):
        svinf(self.ui.doubleSpinBox_1, self.node.length)
        svinf(self.ui.doubleSpinBox_2, self.node.EA)
        svinf(self.ui.doubleSpinBox, self.node.diameter)
        svinf(self.ui.doubleSpinBox_3, self.node.mass_per_length)
        svinf(self.ui.doubleSpinBox_4, self.node.mass)
        cbvinf(self.ui.cbSolveSegmentLengths, self.node.solve_segment_lengths)
        self.set_colors()

    def set_colors(self):
        if self.ui.doubleSpinBox_2.value() == 0 and self.ui.doubleSpinBox_1.value() > 0:
            self.ui.doubleSpinBox_2.setStyleSheet("background: orange")
        else:
            self.ui.doubleSpinBox_2.setStyleSheet("background: white")

    def generate_code(self):
        self.set_colors()

        code = ""
        element = "\ns['{}']".format(self.node.name)

        new_EA = self.ui.doubleSpinBox_2.value()
        new_length = self.ui.doubleSpinBox_1.value()
        new_diameter = self.ui.doubleSpinBox.value()
        new_mass_per_length = self.ui.doubleSpinBox_3.value()

        code += code_if_changed_d(self.node, new_EA, "EA")  # ea before length
        code += code_if_changed_d(self.node, new_length, "length")
        code += code_if_changed_d(self.node, new_diameter, "diameter", dec=6)
        code += code_if_changed_d(self.node, new_mass_per_length, "mass_per_length")
        code += code_if_changed_d(self.node, self.ui.doubleSpinBox_4.value(), "mass")
        code += code_if_changed_b(
            self.node,
            self.ui.cbSolveSegmentLengths.isChecked(),
            "solve_segment_lengths",
        )

        self.run_code(code)


@Singleton
class EditForce(AbstractNodeEditorWithParent):
    nodetypes_for_parent = DAVE.nodes.Point
    NoneAllowedAsParent = False

    def __init__(self):
        widget = QtWidgets.QWidget()
        ui = DAVE.gui.forms.widget_force.Ui_widget_force()
        ui.setupUi(widget)
        self.ui = ui
        self._widget = widget

        ui.doubleSpinBox_1.valueChanged.connect(self.generate_code)
        ui.doubleSpinBox_2.valueChanged.connect(self.generate_code)
        ui.doubleSpinBox_3.valueChanged.connect(self.generate_code)

        ui.doubleSpinBox_4.valueChanged.connect(self.generate_code)
        ui.doubleSpinBox_5.valueChanged.connect(self.generate_code)
        ui.doubleSpinBox_6.valueChanged.connect(self.generate_code)

        ui.cbDefinition.currentIndexChanged.connect(
            self.generate_code
        )  # index 0 --> global, index 1 --> local

    def post_update_event(self):
        self.ui.widgetParent.fill()

        widgets = [
            self.ui.doubleSpinBox_1,
            self.ui.doubleSpinBox_2,
            self.ui.doubleSpinBox_3,
            self.ui.doubleSpinBox_4,
            self.ui.doubleSpinBox_5,
            self.ui.doubleSpinBox_6,
            self.ui.cbDefinition,
        ]

        for widget in widgets:
            widget.blockSignals(True)

        svinf(self.ui.doubleSpinBox_1, self.node.force[0])
        svinf(self.ui.doubleSpinBox_2, self.node.force[1])
        svinf(self.ui.doubleSpinBox_3, self.node.force[2])
        svinf(self.ui.doubleSpinBox_4, self.node.moment[0])
        svinf(self.ui.doubleSpinBox_5, self.node.moment[1])
        svinf(self.ui.doubleSpinBox_6, self.node.moment[2])

        if not self.ui.cbDefinition.hasFocus():
            self.ui.cbDefinition.setCurrentIndex(0 if self.node.is_global else 1)

        for widget in widgets:
            widget.blockSignals(False)

    def generate_code(self):
        code = ""
        element = "\ns['{}']".format(self.node.name)

        new_force = np.array(
            (
                self.ui.doubleSpinBox_1.value(),
                self.ui.doubleSpinBox_2.value(),
                self.ui.doubleSpinBox_3.value(),
            )
        )
        new_moment = np.array(
            (
                self.ui.doubleSpinBox_4.value(),
                self.ui.doubleSpinBox_5.value(),
                self.ui.doubleSpinBox_6.value(),
            )
        )

        new_force_is_global = self.ui.cbDefinition.currentIndex() == 0

        if not np.all(new_force == self.node.force):
            code += element + ".force = ({}, {}, {})".format(*new_force)
        if not np.all(new_moment == self.node.moment):
            code += element + ".moment = ({}, {}, {})".format(*new_moment)

        if not (new_force_is_global == self.node.is_global):
            code += element + ".is_global = {}".format(new_force_is_global)

        self.run_code(code)


# =================


@Singleton
class EditArea(AbstractNodeEditorWithParent):
    nodetypes_for_parent = DAVE.nodes.Point
    NoneAllowedAsParent = False

    def __init__(self):
        widget = QtWidgets.QWidget()
        ui = DAVE.gui.forms.widget_area.Ui_frmArea()
        ui.setupUi(widget)
        self.ui = ui
        self._widget = widget

        ui.Area.valueChanged.connect(self.generate_code)
        ui.Cd.valueChanged.connect(self.generate_code)
        ui.X.valueChanged.connect(self.generate_code)
        ui.Y.valueChanged.connect(self.generate_code)
        ui.Z.valueChanged.connect(self.generate_code)
        ui.X_2.valueChanged.connect(self.generate_code)
        ui.Y_2.valueChanged.connect(self.generate_code)
        ui.Z_2.valueChanged.connect(self.generate_code)
        ui.rbPlane.toggled.connect(self.generate_code)
        ui.rbCylinder.toggled.connect(self.generate_code)
        ui.rbNoOrientation.toggled.connect(self.generate_code)

    def post_update_event(self):
        self.ui.widgetParent.fill()

        widgets = [
            self.ui.Area,
            self.ui.Cd,
            self.ui.X,
            self.ui.Y,
            self.ui.Z,
            self.ui.X_2,
            self.ui.Y_2,
            self.ui.Z_2,
            self.ui.rbPlane,
            self.ui.rbCylinder,
            self.ui.rbNoOrientation,
        ]

        for widget in widgets:
            widget.blockSignals(True)

        svinf(self.ui.Area, self.node.A)
        svinf(self.ui.Cd, self.node.Cd)
        svinf(self.ui.X, self.node.direction[0])
        svinf(self.ui.Y, self.node.direction[1])
        svinf(self.ui.Z, self.node.direction[2])
        svinf(self.ui.X_2, self.node.direction[0])
        svinf(self.ui.Y_2, self.node.direction[1])
        svinf(self.ui.Z_2, self.node.direction[2])

        if isinstance(self.node, WindArea):
            self.ui.windcurrent.setText("Wind area")
        elif isinstance(self.node, CurrentArea):
            self.ui.windcurrent.setText("Current area")

        if self.node.areakind == AreaKind.SPHERE:
            self.ui.rbNoOrientation.setChecked(True)
            self.ui.widget.setEnabled(False)
            self.ui.widget_2.setEnabled(False)
        elif self.node.areakind == AreaKind.PLANE:
            self.ui.rbPlane.setChecked(True)
            self.ui.widget.setEnabled(True)
            self.ui.widget_2.setEnabled(False)
        else:
            self.ui.rbCylinder.setChecked(True)
            self.ui.widget.setEnabled(False)
            self.ui.widget_2.setEnabled(True)

        for widget in widgets:
            widget.blockSignals(False)

    def generate_code(self):
        code = ""
        element = "\ns['{}']".format(self.node.name)

        code += code_if_changed_d(self.node, self.ui.Cd.value(), "Cd")
        code += code_if_changed_d(self.node, self.ui.Area.value(), "A")

        if self.ui.rbNoOrientation.isChecked():
            if self.node.areakind != AreaKind.SPHERE:
                code += element + ".areakind = AreaKind.SPHERE"
        elif self.ui.rbPlane.isChecked():
            if self.node.areakind != AreaKind.PLANE:
                code += element + ".areakind = AreaKind.PLANE"

            new_direction = (self.ui.X.value(), self.ui.Y.value(), self.ui.Z.value())
            code += code_if_changed_v3(self.node, new_direction, "direction")

        elif self.ui.rbCylinder.isChecked():
            if self.node.areakind != AreaKind.CYLINDER:
                code += element + ".areakind = AreaKind.CYLINDER"

            new_direction = (
                self.ui.X_2.value(),
                self.ui.Y_2.value(),
                self.ui.Z_2.value(),
            )
            code += code_if_changed_v3(self.node, new_direction, "direction")

        if code:
            self.run_code(code)


# ===========================


@Singleton
class EditSheave(AbstractNodeEditorWithParent):
    nodetypes_for_parent = DAVE.nodes.Point
    NoneAllowedAsParent = False

    def __init__(self):
        widget = QtWidgets.QWidget()
        ui = DAVE.gui.forms.widget_sheave.Ui_widget_sheave()
        ui.setupUi(widget)
        self.ui = ui
        self._widget = widget

        self.ui.sbAX.valueChanged.connect(self.generate_code)
        self.ui.sbAY.valueChanged.connect(self.generate_code)
        self.ui.sbAZ.valueChanged.connect(self.generate_code)

        self.ui.cbIsRoundBar.toggled.connect(self.generate_code)
        self.ui.sbStart.valueChanged.connect(self.generate_code)
        self.ui.sbStop.valueChanged.connect(self.generate_code)

        self.ui.sbRadius.valueChanged.connect(self.generate_code)

    def post_update_event(self):
        self.ui.widgetParent.fill()

        self.ui.widgetParent.setValue(self.node.parent.name)

        widgets = [
            self.ui.sbAX,
            self.ui.sbAY,
            self.ui.sbAZ,
            self.ui.sbRadius,
            self.ui.sbStop,
            self.ui.sbStart,
            self.ui.cbIsRoundBar,
        ]

        for widget in widgets:
            widget.blockSignals(True)

        # only update axis if none of the boxes is selected
        # this has to do with the normalization which should only
        # be applied to the gui once editing is done

        if (
            not self.ui.sbAX.hasFocus()
            and not self.ui.sbAY.hasFocus()
            and not self.ui.sbAZ.hasFocus()
        ):
            svinf(self.ui.sbAX, self.node.axis[0])
            svinf(self.ui.sbAY, self.node.axis[1])
            svinf(self.ui.sbAZ, self.node.axis[2])

        cbvinf(self.ui.cbIsRoundBar, self.node.is_roundbar)

        svinf(self.ui.sbRadius, self.node.radius)
        svinf(self.ui.sbStop, self.node.draw_stop)
        svinf(self.ui.sbStart, self.node.draw_start)

        for widget in widgets:
            widget.blockSignals(False)

        self.ui.rbWidget.setVisible(self.node.is_roundbar)

    def generate_code(self):
        code = ""
        element = "\ns['{}']".format(self.node.name)

        new_axis = np.array(
            (self.ui.sbAX.value(), self.ui.sbAY.value(), self.ui.sbAZ.value())
        )
        new_radius = self.ui.sbRadius.value()

        if not np.all(new_axis == self.node.axis):
            code += element + ".axis = ({}, {}, {})".format(*new_axis)
        if not new_radius == self.node.radius:
            code += element + ".radius = {}".format(new_radius)

        code += code_if_changed_b(
            self.node, self.ui.cbIsRoundBar.isChecked(), "is_roundbar"
        )
        code += code_if_changed_d(self.node, self.ui.sbStart.value(), "draw_start")
        code += code_if_changed_d(self.node, self.ui.sbStop.value(), "draw_stop")

        if code:
            self.run_code(code)


@Singleton
class EditHydSpring(AbstractNodeEditorWithParent):
    nodetypes_for_parent = DAVE.nodes.Frame
    NoneAllowedAsParent = False

    def __init__(self):
        widget = QtWidgets.QWidget()
        ui = DAVE.gui.forms.widget_linhyd.Ui_widget_linhyd()
        ui.setupUi(widget)
        self.ui = ui
        self._widget = widget

        ui.doubleSpinBox_1.valueChanged.connect(self.generate_code)
        ui.doubleSpinBox_2.valueChanged.connect(self.generate_code)
        ui.doubleSpinBox_3.valueChanged.connect(self.generate_code)
        ui.BMT.valueChanged.connect(self.generate_code)
        ui.BML.valueChanged.connect(self.generate_code)
        ui.COFX.valueChanged.connect(self.generate_code)
        ui.COFY.valueChanged.connect(self.generate_code)
        ui.kHeave.valueChanged.connect(self.generate_code)
        ui.waterline.valueChanged.connect(self.generate_code)
        ui.disp.valueChanged.connect(self.generate_code)

    def post_update_event(self):
        self.ui.widgetParent.fill()

        widgets = [
            self.ui.doubleSpinBox_1,
            self.ui.doubleSpinBox_2,
            self.ui.doubleSpinBox_3,
            self.ui.BMT,
            self.ui.BML,
            self.ui.COFX,
            self.ui.COFY,
            self.ui.kHeave,
            self.ui.waterline,
            self.ui.disp,
        ]

        for widget in widgets:
            widget.blockSignals(True)

        svinf(self.ui.doubleSpinBox_1, self.node.cob[0])
        svinf(self.ui.doubleSpinBox_2, self.node.cob[1])
        svinf(self.ui.doubleSpinBox_3, self.node.cob[2])
        svinf(self.ui.BMT, self.node.BMT)
        svinf(self.ui.BML, self.node.BML)
        svinf(self.ui.COFX, self.node.COFX)
        svinf(self.ui.COFY, self.node.COFY)
        svinf(self.ui.kHeave, self.node.kHeave)
        svinf(self.ui.waterline, self.node.waterline)
        svinf(self.ui.disp, self.node.displacement_kN)

        for widget in widgets:
            widget.blockSignals(False)

    def generate_code(self):
        code = ""
        element = "\ns['{}']".format(self.node.name)

        new_cob = np.array(
            (
                self.ui.doubleSpinBox_1.value(),
                self.ui.doubleSpinBox_2.value(),
                self.ui.doubleSpinBox_3.value(),
            )
        )
        new_bmt = self.ui.BMT.value()
        new_bml = self.ui.BML.value()
        new_cofx = self.ui.COFX.value()
        new_cofy = self.ui.COFY.value()
        new_kHeave = self.ui.kHeave.value()
        new_waterline = self.ui.waterline.value()
        new_dipl = self.ui.disp.value()

        if not np.all(new_cob == self.node.cob):
            code += element + ".cob = ({}, {}, {})".format(*new_cob)

        if not new_bmt == self.node.BMT:
            code += element + ".BMT = {}".format(new_bmt)

        if not new_bml == self.node.BML:
            code += element + ".BML = {}".format(new_bml)

        if not new_cofx == self.node.COFX:
            code += element + ".COFX = {}".format(new_cofx)

        if not new_cofy == self.node.COFY:
            code += element + ".COFY = {}".format(new_cofy)

        if not new_kHeave == self.node.kHeave:
            code += element + ".kHeave = {}".format(new_kHeave)

        if not new_waterline == self.node.waterline:
            code += element + ".waterline = {}".format(new_waterline)

        if not new_dipl == self.node.displacement_kN:
            code += element + ".displacement_kN = {}".format(new_dipl)

        self.run_code(code)


@Singleton
class EditLC6d(NodeEditor):
    def __init__(self):
        widget = QtWidgets.QWidget()
        ui = DAVE.gui.forms.widget_lincon6.Ui_widget_lincon6()
        ui.setupUi(widget)
        self.ui = ui
        self._widget = widget

        ui.doubleSpinBox_1.valueChanged.connect(self.generate_code)
        ui.doubleSpinBox_2.valueChanged.connect(self.generate_code)
        ui.doubleSpinBox_3.valueChanged.connect(self.generate_code)
        ui.doubleSpinBox_4.valueChanged.connect(self.generate_code)
        ui.doubleSpinBox_5.valueChanged.connect(self.generate_code)
        ui.doubleSpinBox_6.valueChanged.connect(self.generate_code)

        # ui.cbMasterAxis.currentIndexChanged.connect(self.generate_code)
        # ui.cbSlaveAxis.currentIndexChanged.connect(self.generate_code)

        self.ui.widgetMain.initialize(
            None,
            nodetypes=DAVE.Frame,
            callback=self.main_changed,
            register_func=None,
            NoneAllowed=False,
            node=None,
        )

        self.ui.widgetSecondary.initialize(
            None,
            nodetypes=DAVE.Frame,
            callback=self.secondary_changed,
            register_func=None,
            NoneAllowed=False,
            node=None,
        )

    def post_update_event(self):
        self.ui.widgetMain.scene = self.scene
        self.ui.widgetMain.register_func = self.node_picker_register_func
        self.ui.widgetMain.node = self.node

        self.ui.widgetSecondary.scene = self.scene
        self.ui.widgetSecondary.register_func = self.node_picker_register_func
        self.ui.widgetSecondary.node = self.node

        self.ui.widgetMain.fill("main")
        self.ui.widgetSecondary.fill("secondary")

        widgets = [
            self.ui.doubleSpinBox_1,
            self.ui.doubleSpinBox_2,
            self.ui.doubleSpinBox_3,
            self.ui.doubleSpinBox_4,
            self.ui.doubleSpinBox_5,
            self.ui.doubleSpinBox_6,
        ]

        for widget in widgets:
            widget.blockSignals(True)

        svinf(self.ui.doubleSpinBox_1, self.node.stiffness[0])
        svinf(self.ui.doubleSpinBox_2, self.node.stiffness[1])
        svinf(self.ui.doubleSpinBox_3, self.node.stiffness[2])

        svinf(self.ui.doubleSpinBox_4, self.node.stiffness[3])
        svinf(self.ui.doubleSpinBox_5, self.node.stiffness[4])
        svinf(self.ui.doubleSpinBox_6, self.node.stiffness[5])

        for widget in widgets:
            widget.blockSignals(False)

    def main_changed(self):
        code = ""
        element = "\ns['{}']".format(self.node.name)

        new_master = self.ui.widgetMain.value
        if not new_master == self.node.main.name:
            code += element + '.main = s["{}"]'.format(new_master)

        self.run_code(code)

    def secondary_changed(self):
        code = ""
        element = "\ns['{}']".format(self.node.name)

        new_secondary = self.ui.widgetSecondary.value
        if not new_secondary == self.node.secondary.name:
            code += element + '.secondary = s["{}"]'.format(new_secondary)

        self.run_code(code)

    def generate_code(self):
        code = ""
        element = "\ns['{}']".format(self.node.name)

        new_stiffness = np.array(
            (
                self.ui.doubleSpinBox_1.value(),
                self.ui.doubleSpinBox_2.value(),
                self.ui.doubleSpinBox_3.value(),
                self.ui.doubleSpinBox_4.value(),
                self.ui.doubleSpinBox_5.value(),
                self.ui.doubleSpinBox_6.value(),
            )
        )

        if not np.all(new_stiffness == self.node.stiffness):
            code += element + ".stiffness = ({}, {}, {},".format(*new_stiffness[:3])
            code += "                  {}, {}, {})".format(*new_stiffness[3:])

        self.run_code(code)


@Singleton
class EditConnector2d(NodeEditor):
    def __init__(self):
        widget = QtWidgets.QWidget()
        ui = DAVE.gui.forms.widget_con2d.Ui_widget_con2d()
        ui.setupUi(widget)
        self.ui = ui
        self._widget = widget

        ui.doubleSpinBox_1.valueChanged.connect(self.generate_code)
        ui.doubleSpinBox_4.valueChanged.connect(self.generate_code)

        # Partial initialization
        # remaining properties are set during post-update-event

        self.ui.widgetMain.initialize(
            None,
            nodetypes=DAVE.Frame,
            callback=self.main_changed,
            register_func=None,
            NoneAllowed=False,
            node=None,
        )

        self.ui.widgetSecondary.initialize(
            None,
            nodetypes=DAVE.Frame,
            callback=self.secondary_changed,
            register_func=None,
            NoneAllowed=False,
            node=None,
        )

    def post_update_event(self):
        self.ui.widgetMain.scene = self.scene
        self.ui.widgetMain.register_func = self.node_picker_register_func
        self.ui.widgetMain.node = self.node

        self.ui.widgetSecondary.scene = self.scene
        self.ui.widgetSecondary.register_func = self.node_picker_register_func
        self.ui.widgetSecondary.node = self.node

        self.ui.widgetMain.fill("nodeA")
        self.ui.widgetSecondary.fill("nodeB")

        widgets = [
            self.ui.doubleSpinBox_1,
            self.ui.doubleSpinBox_4,
        ]

        for widget in widgets:
            widget.blockSignals(True)

        svinf(self.ui.doubleSpinBox_1, self.node.k_linear)
        svinf(self.ui.doubleSpinBox_4, self.node.k_angular)

        for widget in widgets:
            widget.blockSignals(False)

    def main_changed(self):
        code = ""
        element = "\ns['{}']".format(self.node.name)

        new_master = self.ui.widgetMain.value
        if not new_master == self.node.nodeA.name:
            code += element + '.nodeA = s["{}"]'.format(new_master)

        self.run_code(code)

    def secondary_changed(self):
        code = ""
        element = "\ns['{}']".format(self.node.name)

        new_secondary = self.ui.widgetSecondary.value
        if not new_secondary == self.node.nodeB.name:
            code += element + '.nodeB = s["{}"]'.format(new_secondary)

        self.run_code(code)

    def generate_code(self):
        code = ""
        element = "\ns['{}']".format(self.node.name)

        new_k_lin = self.ui.doubleSpinBox_1.value()
        new_k_ang = self.ui.doubleSpinBox_4.value()

        if not new_k_lin == self.node.k_linear:
            code += element + ".k_linear = {}".format(new_k_lin)

        if not new_k_ang == self.node.k_angular:
            code += element + ".k_angular = {}".format(new_k_ang)

        self.run_code(code)


@Singleton
class EditBeam(NodeEditor):
    def __init__(self):
        widget = QtWidgets.QWidget()
        ui = DAVE.gui.forms.widget_beam.Ui_widget_beam()
        ui.setupUi(widget)
        self.ui = ui
        self._widget = widget

        ui.doubleSpinBox_1.valueChanged.connect(self.generate_code)
        ui.doubleSpinBox_2.valueChanged.connect(self.generate_code)
        ui.doubleSpinBox_3.valueChanged.connect(self.generate_code)
        ui.doubleSpinBox_4.valueChanged.connect(self.generate_code)
        ui.doubleSpinBox_5.valueChanged.connect(self.generate_code)
        ui.sbMass.valueChanged.connect(self.generate_code)
        ui.cbTensionOnly.stateChanged.connect(self.generate_code)
        ui.sbnSegments.valueChanged.connect(self.generate_code)

        # Partial initialization
        # remaining properties are set during post-update-event

        self.ui.widgetMain.initialize(
            None,
            nodetypes=DAVE.Frame,
            callback=self.main_changed,
            register_func=None,
            NoneAllowed=False,
            node=None,
        )

        self.ui.widgetSecondary.initialize(
            None,
            nodetypes=DAVE.Frame,
            callback=self.secondary_changed,
            register_func=None,
            NoneAllowed=False,
            node=None,
        )

    def post_update_event(self):
        self.ui.widgetMain.scene = self.scene
        self.ui.widgetMain.register_func = self.node_picker_register_func
        self.ui.widgetMain.node = self.node

        self.ui.widgetSecondary.scene = self.scene
        self.ui.widgetSecondary.register_func = self.node_picker_register_func
        self.ui.widgetSecondary.node = self.node

        self.ui.widgetMain.fill("nodeA")
        self.ui.widgetSecondary.fill("nodeB")

        widgets = [
            self.ui.sbnSegments,
            self.ui.doubleSpinBox_1,
            self.ui.doubleSpinBox_2,
            self.ui.doubleSpinBox_3,
            self.ui.doubleSpinBox_4,
            self.ui.doubleSpinBox_5,
            self.ui.sbMass,
            self.ui.cbTensionOnly,
        ]

        for widget in widgets:
            widget.blockSignals(True)

        self.ui.sbnSegments.setValue(self.node.n_segments)

        svinf(self.ui.doubleSpinBox_1, self.node.L)
        svinf(self.ui.doubleSpinBox_2, self.node.EIy)
        svinf(self.ui.doubleSpinBox_3, self.node.EIz)

        svinf(self.ui.doubleSpinBox_4, self.node.GIp)
        svinf(self.ui.doubleSpinBox_5, self.node.EA)

        self.ui.cbTensionOnly.setChecked(self.node.tension_only)

        svinf(self.ui.sbMass, self.node.mass)

        for widget in widgets:
            widget.blockSignals(False)

    def generate_code(self):
        code = ""
        element = "\ns['{}']".format(self.node.name)

        new_L = self.ui.doubleSpinBox_1.value()
        new_EIy = self.ui.doubleSpinBox_2.value()
        new_EIz = self.ui.doubleSpinBox_3.value()
        new_GIp = self.ui.doubleSpinBox_4.value()
        new_EA = self.ui.doubleSpinBox_5.value()
        new_mass = self.ui.sbMass.value()
        new_n = self.ui.sbnSegments.value()
        new_tensiononly = self.ui.cbTensionOnly.isChecked()

        if not new_L == self.node.L:
            code += element + ".L = {}".format(new_L)

        if not new_EIy == self.node.EIy:
            code += element + ".EIy = {}".format(new_EIy)

        if not new_EIz == self.node.EIz:
            code += element + ".EIz = {}".format(new_EIz)

        if not new_GIp == self.node.GIp:
            code += element + ".GIp = {}".format(new_GIp)

        if not new_EA == self.node.EA:
            code += element + ".EA = {}".format(new_EA)

        if not new_mass == self.node.mass:
            code += element + ".mass = {}".format(new_mass)

        if not new_n == self.node.n_segments:
            code += element + ".n_segments = {}".format(new_n)

        if not new_tensiononly == self.node.tension_only:
            code += element + ".tension_only = {}".format(new_tensiononly)

        self.run_code(code)

    def main_changed(self):
        code = ""
        element = "\ns['{}']".format(self.node.name)

        new_master = self.ui.widgetMain.value
        if not new_master == self.node.nodeA.name:
            code += element + '.nodeA = s["{}"]'.format(new_master)

        self.run_code(code)

    def secondary_changed(self):
        code = ""
        element = "\ns['{}']".format(self.node.name)

        new_secondary = self.ui.widgetSecondary.value
        if not new_secondary == self.node.nodeB.name:
            code += element + '.nodeB = s["{}"]'.format(new_secondary)

        self.run_code(code)


@Singleton
class EditGeometricContact(NodeEditor):
    def __init__(self):
        widget = QtWidgets.QWidget()
        ui = DAVE.gui.forms.widget_geometricconnection.Ui_GeometricConnection()
        ui.setupUi(widget)
        self.ui = ui
        self._widget = widget

        ui.rbPinHole.toggled.connect(self.change_type)

        ui.cbMFix.toggled.connect(self.generate_code)
        ui.cbSFix.toggled.connect(self.generate_code)
        ui.cbSwivelFix.toggled.connect(self.generate_code)

        ui.sbMasterRotation.valueChanged.connect(self.generate_code)
        ui.sbSlaveRotation.valueChanged.connect(self.generate_code)
        ui.sbSwivel.valueChanged.connect(self.generate_code)

        ui.pbFlip.clicked.connect(self.flip)
        ui.pbChangeSide.clicked.connect(self.change_side)

    def post_update_event(self):
        widgets = [
            self.ui.lblParent,
            self.ui.lblChild,
            self.ui.rbPinHole,
            self.ui.rbPinPin,
            self.ui.cbMFix,
            self.ui.cbSFix,
            self.ui.cbSwivelFix,
            self.ui.sbMasterRotation,
            self.ui.sbSlaveRotation,
            self.ui.sbSwivel,
        ]

        for widget in widgets:
            widget.blockSignals(True)

        self.ui.lblParent.setText(self.node.parent.name)
        self.ui.lblChild.setText(self.node.child.name)

        self.ui.rbPinHole.setChecked(self.node.inside)
        self.ui.rbPinPin.setChecked(not self.node.inside)

        self.ui.cbMFix.setChecked(self.node.fixed_to_parent)
        self.ui.cbSFix.setChecked(self.node.child_fixed)
        self.ui.cbSwivelFix.setChecked(self.node.swivel_fixed)

        svinf(self.ui.sbMasterRotation, self.node.rotation_on_parent)
        svinf(self.ui.sbSlaveRotation, self.node.child_rotation)
        svinf(self.ui.sbSwivel, self.node.swivel)

        for widget in widgets:
            widget.blockSignals(False)

        self.ui.lbWarningInsideLagerThanOutside.setVisible(
            not self.node.inside_child_is_smaller_than_parent()
        )

        warnings.warn(
            "Parent circle is smaller than child circle, this is allowed but may lead to unexpected results if this is not what you intended to do"
        )

    def flip(self):
        code = "\ns['{}'].flip()".format(self.node.name)
        self.run_code(code)

        self.post_update_event()

    def change_side(self):
        code = "\ns['{}'].change_side()".format(self.node.name)
        self.run_code(code)

        self.post_update_event()  # no need, done automatically by run_code

    def change_type(self):
        new_inside = self.ui.rbPinHole.isChecked()
        if not new_inside == self.node.inside:
            code = "\ns['{}']".format(self.node.name) + ".inside = " + str(new_inside)
            self.run_code(code)
            # self.post_update_event() # no need, done automatically by run_code

    def generate_code(self):
        code = ""
        element = "\ns['{}']".format(self.node.name)

        new_swivel = self.ui.sbSwivel.value()
        new_master = self.ui.sbMasterRotation.value()
        new_slave = self.ui.sbSlaveRotation.value()

        new_swivel_fixed = self.ui.cbSwivelFix.isChecked()
        new_master_fixed = self.ui.cbMFix.isChecked()
        new_slave_fixed = self.ui.cbSFix.isChecked()

        if not new_swivel == self.node.swivel:
            code += element + ".swivel = " + str(new_swivel)
        if not new_master == self.node.rotation_on_parent:
            code += element + ".rotation_on_parent = " + str(new_master)
        if not new_slave == self.node.child_rotation:
            code += element + ".child_rotation = " + str(new_slave)

        if not new_swivel_fixed == self.node.swivel_fixed:
            code += element + ".swivel_fixed = " + str(new_swivel_fixed)
        if not new_master_fixed == self.node.fixed_to_parent:
            code += element + ".fixed_to_parent = " + str(new_master_fixed)
        if not new_slave_fixed == self.node.child_fixed:
            code += element + ".child_fixed = " + str(new_slave_fixed)

        # if not new_inside == self.node.inside:
        #     code += element + '.inside = ' + str(new_inside)

        self.run_code(code)


@Singleton
class EditContactBall(AbstractNodeEditorWithParent):
    nodetypes_for_parent = DAVE.nodes.Point
    NoneAllowedAsParent = False

    def __init__(self):
        widget = QtWidgets.QWidget()
        ui = DAVE.gui.forms.widget_contactball.Ui_widget_contactball()
        ui.setupUi(widget)
        self.ui = ui
        self._widget = widget

        ui.lwMeshes.dropEvent = self.onDrop
        ui.lwMeshes.dragEnterEvent = self.dragEnter
        ui.lwMeshes.dragMoveEvent = self.dragEnter

        ui.pbRemoveSelected.clicked.connect(self.delete_selected)
        ui.sbR.valueChanged.connect(self.generate_code)
        ui.sbK.valueChanged.connect(self.generate_code)

    def post_update_event(self):
        self.ui.widgetParent.fill()

        self.ui.sbR.blockSignals(True)
        self.ui.sbK.blockSignals(True)

        svinf(self.ui.sbR, self.node.radius)
        svinf(self.ui.sbK, self.node.k)

        self.update_meshes_list()

        self.ui.sbR.blockSignals(False)
        self.ui.sbK.blockSignals(False)

    def dragEnter(self, event):
        dragged_name = event.mimeData().text()

        try:
            a = self.scene[dragged_name]
            if isinstance(a, vfs.ContactMesh):
                event.accept()
        except:
            return

    def onDrop(self, event):
        try:
            dragged_name = event.mimeData().text()
        except:
            event.ignore()
            return

        try:
            dropped_node = self.scene[dragged_name]
        except:
            dropped_node = None

        if not isinstance(dropped_node, ContactMesh):
            event.ignore()
            return

        self.ui.lwMeshes.addItem(QListWidgetItem(dragged_name))
        self.generate_code()

    def delete_selected(self):
        row = self.ui.lwMeshes.currentRow()
        if row > -1:
            self.ui.lwMeshes.takeItem(row)
        self.generate_code()

    def update_meshes_list(self):
        self.ui.lwMeshes.clear()
        for name in self.node.meshes_names:
            self.ui.lwMeshes.addItem(QListWidgetItem(name))

    def generate_code(self):
        code = ""
        element = "\ns['{}']".format(self.node.name)

        new_r = self.ui.sbR.value()
        new_k = self.ui.sbK.value()

        if new_r != self.node.radius:
            code += element + ".radius = {}".format(new_r)
        if new_k != self.node.k:
            code += element + ".k = {}".format(new_k)

        new_names = []
        for i in range(self.ui.lwMeshes.count()):
            new_names.append(self.ui.lwMeshes.item(i).text())

        if not (new_names == self.node.meshes_names):
            if new_names:
                code += element + ".meshes = ["
                for name in new_names:
                    code += "'{}',".format(name)
                code = code[:-1] + "]"
            else:
                code += element + ".meshes = []"

        self.run_code(code)


# @Singleton
# class EditSling(NodeEditor):
#     def __init__(self):
#         widget = QtWidgets.QWidget()
#         ui = DAVE.gui.forms.widget_sling.Ui_Form()
#         ui.setupUi(widget)
#
#         self.ui = ui
#         self._widget = widget
#         # Set events
#
#         ui.sbLength.valueChanged.connect(self.generate_code)
#         ui.sbEA.valueChanged.connect(self.generate_code)
#         ui.sbDiameter.valueChanged.connect(self.generate_code)
#         ui.sbMass.valueChanged.connect(self.generate_code)
#         ui.sbLEyeA.valueChanged.connect(self.generate_code)
#         ui.sbLEyeB.valueChanged.connect(self.generate_code)
#         ui.sbLSpliceA.valueChanged.connect(self.generate_code)
#         ui.sbLSpliceB.valueChanged.connect(self.generate_code)
#         ui.sbK.valueChanged.connect(self.generate_code)
#
#     def post_update_event(self):
#         widgets = [
#             self.ui.sbLength,
#             self.ui.sbEA,
#             self.ui.sbDiameter,
#             self.ui.sbMass,
#             self.ui.sbLEyeA,
#             self.ui.sbLEyeB,
#             self.ui.sbLSpliceA,
#             self.ui.sbLSpliceB,
#             self.ui.sbK,
#         ]
#
#         for widget in widgets:
#             widget.blockSignals(True)
#
#         svinf(self.ui.sbLength, self.node.length)
#         svinf(self.ui.sbEA, self.node.EA)
#         svinf(self.ui.sbDiameter, self.node.diameter)
#         svinf(self.ui.sbMass, self.node.mass)
#         svinf(self.ui.sbLEyeA, self.node.LeyeA)
#         svinf(self.ui.sbLEyeB, self.node.LeyeB)
#         svinf(self.ui.sbLSpliceA, self.node.LspliceA)
#         svinf(self.ui.sbLSpliceB, self.node.LspliceB)
#         svinf(self.ui.sbK, self.node.k_total)
#
#         for widget in widgets:
#             widget.blockSignals(False)
#
#     def generate_code(self):
#         code = ""
#         element = "\ns['{}']".format(self.node.name)
#
#         node = self.node
#
#         new_length = self.ui.sbLength.value()
#         new_EA = self.ui.sbEA.value()
#         new_diameter = self.ui.sbDiameter.value()
#         new_mass = self.ui.sbMass.value()
#         new_LeyeA = self.ui.sbLEyeA.value()
#         new_LeyeB = self.ui.sbLEyeB.value()
#         new_LspliceA = self.ui.sbLSpliceA.value()
#         new_LspliceB = self.ui.sbLSpliceB.value()
#         new_k = self.ui.sbK.value()
#
#         code += code_if_changed_d(
#             node, new_length, "length", 3
#         )  # Need to change the length before changing the length of
#         # the components beause the length of the components is checked against the total length
#
#         code += code_if_changed_d(node, new_k, "k_total", 1)
#         code += code_if_changed_d(node, new_EA, "EA", 1)
#         code += code_if_changed_d(node, new_diameter, "diameter", 1)
#
#         code += code_if_changed_d(node, new_mass, "mass", 1)
#         code += code_if_changed_d(node, new_LeyeA, "LeyeA", 3)
#         code += code_if_changed_d(node, new_LeyeB, "LeyeB", 3)
#         code += code_if_changed_d(node, new_LspliceA, "LspliceA", 3)
#         code += code_if_changed_d(node, new_LspliceB, "LspliceB", 3)
#
#         self.run_code(code)


@Singleton
class EditSPMT(AbstractNodeEditorWithParent):
    nodetypes_for_parent = DAVE.nodes.Frame
    NoneAllowedAsParent = False

    def __init__(self):
        widget = QtWidgets.QWidget()
        ui = DAVE.gui.forms.widget_spmt.Ui_SPMTwidget()
        ui.setupUi(widget)
        self.ui = ui
        self._widget = widget

        self.ui.rbPerpendicular.toggled.connect(self.generate_code)
        self.ui.rbVertical.toggled.connect(self.generate_code)

        self.ui.sbDX.valueChanged.connect(self.generate_code)
        self.ui.sbDY.valueChanged.connect(self.generate_code)
        self.ui.sbNX.valueChanged.connect(self.generate_code)
        self.ui.sbNY.valueChanged.connect(self.generate_code)

        self.ui.sbRefExtension.valueChanged.connect(self.generate_code)
        self.ui.sbRefForce.valueChanged.connect(self.generate_code)
        self.ui.sbStiffness.valueChanged.connect(self.generate_code)

    def post_update_event(self):
        # self.ui.comboBox.blockSignals(True)
        self.ui.widgetParent.fill()

        self.ui.rbPerpendicular.blockSignals(True)
        self.ui.rbVertical.blockSignals(True)
        self.ui.rbPerpendicular.setChecked(not self.node.use_friction)
        self.ui.rbVertical.setChecked(self.node.use_friction)
        self.ui.rbPerpendicular.blockSignals(False)
        self.ui.rbVertical.blockSignals(False)

        svinf(self.ui.sbDX, self.node.spacing_length)
        svinf(self.ui.sbDY, self.node.spacing_width)
        svinf(self.ui.sbNX, self.node.n_length)
        svinf(self.ui.sbNY, self.node.n_width)

        svinf(self.ui.sbRefExtension, self.node.reference_extension)
        svinf(self.ui.sbRefForce, self.node.reference_force)
        svinf(self.ui.sbStiffness, self.node.k)

    def generate_code(self):
        code = ""
        if self.ui.rbVertical.isChecked() and not self.node.use_friction:
            code = f"s['{self.node.name}'].use_friction = True"
        if self.ui.rbPerpendicular.isChecked() and self.node.use_friction:
            code = f"s['{self.node.name}'].use_friction = False"

        code += code_if_changed_d(self.node, self.ui.sbDX.value(), "spacing_length")
        code += code_if_changed_d(self.node, self.ui.sbDY.value(), "spacing_width")
        code += code_if_changed_d(self.node, self.ui.sbNX.value(), "n_length")
        code += code_if_changed_d(self.node, self.ui.sbNY.value(), "n_width")
        code += code_if_changed_d(
            self.node, self.ui.sbRefExtension.value(), "reference_extension"
        )
        code += code_if_changed_d(
            self.node, self.ui.sbRefForce.value(), "reference_force"
        )
        code += code_if_changed_d(self.node, self.ui.sbStiffness.value(), "k")

        self.run_code(code, self)


@Singleton
class EditVisualOutline(NodeEditor):
    def __init__(self):
        widget = QtWidgets.QWidget()
        self._widget = widget

        layout = QtWidgets.QHBoxLayout()

        label = QtWidgets.QLabel("Edges in viewport")

        widget.setLayout(layout)
        self.cbOutline = QtWidgets.QComboBox()
        self.cbOutline.addItems(("None", "Feature", "Feature and Silhouette"))
        spacerItem = QtWidgets.QSpacerItem(
            8, 8, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum
        )
        layout.addItem(spacerItem)
        layout.setContentsMargins(9, 0, 9, 0)

        layout.addWidget(label)
        layout.addWidget(self.cbOutline)

        self.cbOutline.currentTextChanged.connect(self.generate_code)

    def post_update_event(self):
        self.cbOutline.blockSignals(True)
        if self.node.visual_outline == VisualOutlineType.NONE:
            text = "None"
        elif self.node.visual_outline == VisualOutlineType.FEATURE_AND_SILHOUETTE:
            text = "Feature and Silhouette"
        else:
            text = "Feature"
        self.cbOutline.setCurrentText(text)

        self.cbOutline.blockSignals(False)

    def generate_code(self):
        q = dict()
        q["None"] = VisualOutlineType.NONE
        q["Feature"] = VisualOutlineType.FEATURE
        q["Feature and Silhouette"] = VisualOutlineType.FEATURE_AND_SILHOUETTE

        value = q[self.cbOutline.currentText()]

        if self.node.visual_outline != value:
            code = f"s['{self.node.name}'].visual_outline = {value}"
            self.run_code(code, self)

            # Enforce reload
            store = self.node.path
            self.node.path = "res: cube_with_bevel.obj"
            self.guiEmitEvent(guiEventType.SELECTED_NODE_MODIFIED)
            self.node.path = store
            self.guiEmitEvent(guiEventType.SELECTED_NODE_MODIFIED)
            self.guiEmitEvent(guiEventType.VIEWER_SETTINGS_UPDATE)


# ===========================================


class WidgetNodeProps(guiDockWidget):
    def guiDefaultLocation(self):
        return PySide6QtAds.DockWidgetArea.RightDockWidgetArea

    def guiCreate(self):
        self.node_picker = None

        # self.setMinimumWidth(442)
        self.setVisible(False)
        # self.setAllowedAreas(
        #     QtCore.Qt.LeftDockWidgetArea | QtCore.Qt.RightDockWidgetArea
        # )

        self._open_edit_widgets = list()
        self._node_editors = list()

        # self.scroll_area = QtWidgets.QWidget()
        # scroll_area_layout = QtWidgets.QVBoxLayout()
        # scroll_area_layout.setSpacing(0)
        # scroll_area_layout.setContentsMargins(0, 0, 0, 0)
        # self.scroll_area.setLayout(scroll_area_layout)

        # self.scroll_area.setWidget(self.contents)
        # scroll_area_layout.addWidget(self.contents)
        self.setWidget(self.contents)

        # self.scroll_area.setStyleSheet('background-color: rgb(255, 255, 0);')

        # self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.no_node_layout = QtWidgets.QVBoxLayout()
        self.no_node_message = QtWidgets.QLabel()
        self.no_node_message.setText("Select a node to edit its properties")
        self.no_node_message.setAlignment(QtCore.Qt.AlignCenter)
        self.no_node_layout.addWidget(self.no_node_message)

        # contents (main layout)
        #   manager_widget ( manager_layout )
        #   props_widget ( layout )

        self.main_layout = QtWidgets.QVBoxLayout()

        self.manager_widget = QtWidgets.QWidget()
        self.manager_layout = QtWidgets.QVBoxLayout()
        self.manager_widget.setLayout(self.manager_layout)

        self.managed_label = QtWidgets.QLabel(self.manager_widget)
        self.managed_label.setWordWrap(True)
        self.managed_label.setFrameShape(QtWidgets.QFrame.Box)
        self.managed_label.setStyleSheet("background: gold;")
        self.manager_layout.addWidget(self.managed_label)

        self.manager_link_label = QtWidgets.QPushButton(self.contents)
        self.manager_link_label.setText("Select manager")
        self.manager_link_label.clicked.connect(self.select_manager)
        self.manager_layout.addWidget(self.manager_link_label)

        self.warning_label = QtWidgets.QLabel()
        self.warning_label.setFrameShape(QtWidgets.QFrame.Box)
        self.warning_label.setText("WARNING")
        self.warning_label.setStyleSheet(
            "background-color: rgb(255, 255, 185);\ncolor: rgb(200, 0, 127);"
        )

        self.props_widget = QtWidgets.QWidget()

        self.main_layout.addWidget(self.warning_label)
        self.main_layout.addWidget(self.manager_widget)
        self.main_layout.addWidget(self.props_widget)
        self.main_layout.setContentsMargins(0, 6, 6, 6)

        self.contents.setLayout(self.main_layout)

        self.layout = QtWidgets.QVBoxLayout()

        self._node_name_editor = EditNode()

        self._name_widget = self._node_name_editor.widget
        self.layout.addWidget(self._name_widget)

        self.layout.setContentsMargins(0, 0, 0, 0)
        self.props_widget.setLayout(self.layout)

        self._Vspacer = QtWidgets.QSpacerItem(
            20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding
        )
        self.layout.addSpacerItem(self._Vspacer)

        self.positioned = False
        self.node = "This will be a node"
        self.node_type = (
            "This will be the type of the node at the time that is was assigned"
        )

        # create the multi-layout
        self.multi_layout = QtWidgets.QVBoxLayout()
        self.multi_layout.setContentsMargins(0, 0, 0, 0)

        self.widget_grid_edit_controls = Ui_widgetGridEditControls()
        target = QWidget()

        self.widget_grid_edit_controls.setupUi(target)

        self.widget_grid_edit_controls.cbSortByName.toggled.connect(
            self.multi_sort_toggled
        )
        self.widget_grid_edit_controls.rbCommon.toggled.connect(
            self.multi_common_toggled
        )

        self.multi_layout.addWidget(target)
        self.grid = None  # created during first update

        self.multi_active = False

        self.layout_storage_multi = (
            QWidget()
        )  # used to store the current layout to keep it from being deleted
        self.layout_storage_main = (
            QWidget()
        )  # used to store the current layout to keep it from being deleted

    def set_single_layout(self):
        self.multi_active = False
        if self.contents.layout() == self.main_layout:
            return

        self.layout_storage_multi.setLayout(
            self.multi_layout
        )  # remove the current layout
        self.contents.setLayout(self.main_layout)

    def set_multi_layout(self):
        self.multi_active = True
        if self.contents.layout() == self.multi_layout:
            return

        self.layout_storage_main.setLayout(
            self.main_layout
        )  # remove the current layout
        self.contents.setLayout(self.multi_layout)

    def multi_exec(self, code):
        self.run_code(code)

    def multi_sort_toggled(self, *args, **kwargs):
        self.grid.set_sorted(self.widget_grid_edit_controls.cbSortByName.isChecked())

    def multi_common_toggled(self, *args, **kwargs):
        self.grid.set_common(self.widget_grid_edit_controls.rbCommon.isChecked())

    def node_picker_register(self, node_picker):
        self.node_picker = node_picker

    def select_manager(self):
        node = self.guiSelection[0]
        manager = node._manager
        self.guiSelectNode(manager)

    def guiProcessEvent(self, event):
        # structure changed is emitted when a node is moved in the tree.
        # if the moved node is the active node then it needs to be updated as its local-position may have changed

        if self.grid is None:  # first use final initialization
            self.grid = GriddedNodeEditor(
                scene=self.guiScene,
                parent=self,
                execute_func=self.multi_exec,
                select_single_node_callback=self.guiSelectNode,
            )
            self.multi_layout.addWidget(self.grid)
            self._node_name_editor.select_nodes_callback = self.guiSelectNode

        if event is guiEventType.SELECTION_CHANGED:
            if self.node_picker is not None:
                _old_node = (
                    self.node
                )  # make a copy because the function below may execute "STRUCTURE CHANGED" or something
                # which changes self.node

                if self.guiSelection:
                    if not self.node_picker.nodesSelected(
                        self.guiSelection
                    ):  # if nothing was done with the selection
                        return  # then keep it this way

                # clear node_picker and re-select current node
                self.node_picker.unregister()
                self.node_picker = None
                self.guiSelectNode(_old_node)
                return

        if event in [
            guiEventType.SELECTION_CHANGED,
            guiEventType.FULL_UPDATE,
            guiEventType.MODEL_STRUCTURE_CHANGED,
            guiEventType.MODEL_STEP_ACTIVATED,
        ]:
            # check if we have a selection
            if self.guiSelection:
                if len(self.guiSelection) > 1:
                    self.set_multi_layout()
                    self.grid.set_nodes(self.guiSelection)

                    return
                else:
                    self.set_single_layout()
                    self.select_node(self.guiSelection[0])

        if event in [guiEventType.MODEL_STATE_CHANGED]:
            if self.guiSelection:
                if self.multi_layout:
                    self.grid.fill()
                    return
                else:
                    self.select_node(self.guiSelection[0])

        # does the current node still exist?
        if self.node not in self.guiScene._nodes:
            self.select_node(None)
            return

        if event in [
            guiEventType.SELECTED_NODE_MODIFIED,
            guiEventType.MODEL_STRUCTURE_CHANGED,
            guiEventType.MODEL_STATE_CHANGED,
            guiEventType.MODEL_STEP_ACTIVATED,
            guiEventType.FULL_UPDATE,
        ]:  # reloaded component emit model structure changed instead of selected node modified
            for w in self._node_editors:
                w.post_update_event()
            self._node_name_editor.post_update_event()
            self.check_for_warnings()

    def run_code(self, code, event=None, sender=None, store_undo=True):
        if event is None:
            return self.guiRunCodeCallback(
                code,
                guiEventType.SELECTED_NODE_MODIFIED,
                sender=sender,
                store_undo=store_undo,
            )
        else:
            return self.guiRunCodeCallback(
                code, event, sender=sender, store_undo=store_undo
            )

        self.check_for_warnings()

    def check_for_warnings(self):
        """Controls the warning-label on top of the node-editor

        Args:
            node:

        Returns:

        """
        node = self.node

        self.warning_label.setVisible(False)
        if isinstance(node, (Buoyancy, Tank)):
            # check mesh

            self.gui.visual.remove_temporary_actors()
            messages = node.trimesh.messages
            if messages:
                self.warning_label.setText("\n".join(messages))
                self.warning_label.setVisible(True)

                if node.trimesh.boundary_edges:
                    actor = Lines(node.trimesh.boundary_edges, lw=5, color=(1, 0, 0))
                    actor.SetUserTransform(transform_from_node(node.parent))
                    self.gui.visual.add_temporary_actor(actor)
                if node.trimesh.non_manifold_edges:
                    actor = Lines(
                        node.trimesh.non_manifold_edges, lw=5, color=(1, 0, 1)
                    )
                    actor.SetUserTransform(transform_from_node(node.parent))
                    self.gui.visual.add_temporary_actor(actor)

    def select_node(self, node):
        if self.node == node:
            if (
                type(node) == self.node_type
            ):  # node can have changed type if it was dissolved
                return

        self.node = node
        self.node_type = type(self.node)

        self.setUpdatesEnabled(False)
        to_be_removed = self._open_edit_widgets.copy()

        if node is None:
            # remove all widgets and add a message
            self.setWidget(self.no_node_message)
            self.update()
            self.setUpdatesEnabled(True)
            return

        self.setWidget(self.contents)

        self.contents.setVisible(True)
        self.contents.setLayout(self.main_layout)  # default

        manager_workaround = None
        self._name_widget.setEnabled(
            True
        )  # default, disabled for partially managed nodes
        if node._manager:
            self.managed_label.setText(
                f"This node is controlled by node '{node._manager.name}' and can not be changed directly. Select the manager to make changes indirectly."
            )
            self.managed_label.setStyleSheet("background: gold;")
            self.manager_widget.setVisible(True)

            manager_workaround = getattr(
                node, "_editor_widget_types_when_managed", None
            )
            if manager_workaround is None:
                self.props_widget.setEnabled(self.guiScene._godmode)
            else:
                self._name_widget.setEnabled(False)
                self.props_widget.setEnabled(True)
                self.managed_label.setText(
                    f"Some of the properties of this node are controlled by '{node._manager.name}'. Select that (manager) node to change change those."
                )
                self.managed_label.setStyleSheet("background: lightyellow;")

        else:
            self.manager_widget.setVisible(False)
            self.props_widget.setEnabled(True)

        #
        no_name_editor = getattr(node, "_no_name_editor", False)

        self._name_widget.setVisible(not no_name_editor)

        suppressed_editors = getattr(node, "_suppressed_node_editors", [])

        self._node_editors.clear()
        self._open_edit_widgets.clear()

        # self._node_name_editor = EditNode.Instance()
        self._node_name_editor.connect(
            node,
            self.guiScene,
            self.run_code,
            self.guiEmitEvent,
            self.guiPressSolveButton,
            self.node_picker_register,
        )
        #
        # # add to layout if not already in
        # name_widget = getattr(self, "_name_widget", None)
        # if name_widget is None:
        #     self._name_widget = self._node_name_editor.widget
        #     self.layout.addWidget(self._name_widget)

        try:
            self.layout.removeItem(self._Vspacer)
        except:
            pass  # _Vspacer is not always in

        # # check the plugins
        # for plugin in self.gui.plugins_editor:
        #     cls = plugin(node)
        #     if cls is not None:
        #         self._node_editors.append(cls.Instance())

        if isinstance(node, vfs.Visual) and (vfs.Visual not in suppressed_editors):
            self._node_editors.append(EditVisualOutline.Instance())
            self._node_editors.append(EditVisual.Instance())

        if isinstance(node, vfs.WaveInteraction1) and (
            vfs.WaveInteraction1 not in suppressed_editors
        ):
            self._node_editors.append(EditWaveInteraction.Instance())

        if isinstance(node, vfs.Component) and (
            vfs.Component not in suppressed_editors
        ):
            self._node_editors.append(EditComponent.Instance())

        if isinstance(node, vfs.Frame) and (vfs.Frame not in suppressed_editors):
            self._node_editors.append(EditAxis.Instance())

        if isinstance(node, vfs.RigidBody) and (
            vfs.RigidBody not in suppressed_editors
        ):
            self._node_editors.append(EditBody.Instance())

        if isinstance(node, vfs.Point) and (vfs.Point not in suppressed_editors):
            self._node_editors.append(EditPoi.Instance())

        if isinstance(node, vfs.Cable) and (vfs.Cable not in suppressed_editors):
            self._node_editors.append(EditCable.Instance())
            self._node_editors.append(EditConnections.Instance())

        if isinstance(node, vfs.Force) and (vfs.Force not in suppressed_editors):
            self._node_editors.append(EditForce.Instance())

        if isinstance(node, vfs.Circle) and (vfs.Circle not in suppressed_editors):
            self._node_editors.append(EditSheave.Instance())

        if isinstance(node, vfs.HydSpring) and (
            vfs.HydSpring not in suppressed_editors
        ):
            self._node_editors.append(EditHydSpring.Instance())

        if isinstance(node, vfs.LC6d) and (vfs.LC6d not in suppressed_editors):
            self._node_editors.append(EditLC6d.Instance())

        if isinstance(node, vfs.Connector2d) and (
            vfs.Connector2d not in suppressed_editors
        ):
            self._node_editors.append(EditConnector2d.Instance())

        if isinstance(node, vfs.Beam) and (vfs.Beam not in suppressed_editors):
            self._node_editors.append(EditBeam.Instance())

        if isinstance(node, vfs.ContactBall) and (
            vfs.ContactBall not in suppressed_editors
        ):
            self._node_editors.append(EditContactBall.Instance())

        if isinstance(node, vfs.GeometricContact) and (
            vfs.GeometricContact not in suppressed_editors
        ):
            self._node_editors.append(EditGeometricContact.Instance())

        # if isinstance(node, vfs.Sling) and (vfs.Sling not in suppressed_editors):
        #     self._node_editors.append(EditSling.Instance())
        #     self._node_editors.append(EditConnections.Instance())

        if isinstance(node, vfs.SPMT) and (vfs.SPMT not in suppressed_editors):
            self._node_editors.append(EditSPMT.Instance())

        if isinstance(node, vfs.WindOrCurrentArea) and (
            vfs.WindOrCurrentArea not in suppressed_editors
        ):
            self._node_editors.append(EditArea.Instance())

        if (
            (
                isinstance(node, vfs.Buoyancy)
                or isinstance(node, vfs.ContactMesh)
                or isinstance(node, vfs.Tank)
            )
            and (vfs.Buoyancy not in suppressed_editors)
            and (vfs.ContactMesh not in suppressed_editors)
            and (vfs.Tank not in suppressed_editors)
        ):
            self._node_editors.append(EditBuoyancyOrContactMesh.Instance())

        if isinstance(node, vfs.Tank) and (vfs.Tank not in suppressed_editors):
            self._node_editors.append(EditTank.Instance())

        if isinstance(node, vfs.Measurement) and (
            vfs.Measurement not in suppressed_editors
        ):
            self._node_editors.append(EditMeasurement.Instance())

        if isinstance(node, vfs.SupportPoint) and (
            vfs.SupportPoint not in suppressed_editors
        ):
            self._node_editors.append(EditSupportPoint.Instance())

        for key, value in DAVE_GUI_NODE_EDITORS.items():
            if isinstance(node, key):
                if isinstance(value, (list, tuple)):
                    for v in value:
                        if v not in suppressed_editors:
                            self._node_editors.append(v.Instance())
                else:
                    if value not in suppressed_editors:
                        self._node_editors.append(value.Instance())

        # print("Node editor created!", flush=True)

        # Remove suppressed editors
        if manager_workaround:
            self._node_editors = [
                editor
                for editor in self._node_editors
                if isinstance(editor, manager_workaround)
            ]

        to_be_added = []
        for editor in self._node_editors:
            # add a check for the return value of connect because the program will hard-crash if the return value is None
            # this function returns the widget
            widget = editor.connect(
                node,
                self.guiScene,
                self.run_code,
                self.guiEmitEvent,
                self.guiPressSolveButton,
                self.node_picker_register,
            )
            assert (
                widget is not None
            ), f"Editor {editor} returned None when connecting to node {node}"
            to_be_added.append(widget)

            print(f"Editor {editor} {widget.sizeHint()}")

        for widget in to_be_removed:
            if widget in to_be_added:
                to_be_added.remove(widget)
                self._open_edit_widgets.append(widget)
            else:
                self.layout.removeWidget(widget)
                widget.setVisible(False)

        for widget in to_be_added:
            self.layout.addWidget(widget)
            self._open_edit_widgets.append(widget)
            widget.setVisible(True)

        # Check for warnings

        self.check_for_warnings()

        # check if one of the widgets is "expanding"
        # if not, then add a spacer
        expanding = False
        for widget in self._open_edit_widgets:
            if widget.sizePolicy().verticalPolicy() == QSizePolicy.Expanding:
                expanding = True

                # move expanding widget to the end
                self.layout.removeWidget(widget)
                self.layout.addWidget(widget)

                break

        if not expanding:
            self.layout.addSpacerItem(self._Vspacer)  # add a spacer at the bottom

        self.setUpdatesEnabled(True)
        self.update()


from DAVE.gui.settings import DAVE_GUI_DOCKS

DAVE_GUI_DOCKS["Properties"] = WidgetNodeProps
