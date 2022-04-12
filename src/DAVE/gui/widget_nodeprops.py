from abc import ABC, abstractmethod
import vedo as vp
from PySide2.QtGui import QColor

from DAVE.gui.dockwidget import *
from PySide2.QtCore import Qt
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
import DAVE.gui.forms.widget_sling
import DAVE.gui.forms.widget_tank
import DAVE.gui.forms.widget_shackle
import DAVE.gui.forms.widget_area
import DAVE.gui.forms.widget_component
import DAVE.gui.forms.widget_spmt

from DAVE.visual import transform_from_node
from DAVE.gui.helpers.my_qt_helpers import BlockSigs
import numpy as np

from PySide2.QtWidgets import QListWidgetItem, QMessageBox, QDoubleSpinBox, QCompleter, QDesktopWidget, QColorDialog
from PySide2 import QtWidgets

DAVE_GUI_NODE_EDITORS = dict() # Key: node-class, value: editor-class

def svinf(spinbox: QDoubleSpinBox, value: float, do_block = True):
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

def cvinf(combobox: QtWidgets.QComboBox,value : str):
    """Updates the value in the combobox IF it does not have focus"""
    if combobox.hasFocus():
        return
    combobox.setCurrentText(value)

def update_combobox_items_with_completer(comboBox: QtWidgets.QComboBox, items):
    """Updates the possible items of the combobox and adds a completer
    Suppresses signals and preserves the current text
    """
    with BlockSigs(comboBox):
        ct = comboBox.currentText()
        comboBox.clear()
        comboBox.addItems(items)

        # set QCompleter
        completer = QCompleter(items)
        completer.setCaseSensitivity(Qt.CaseInsensitive)
        completer.setModelSorting(QCompleter.UnsortedModel)
        completer.setFilterMode(Qt.MatchContains)
        comboBox.setCompleter(completer)
        comboBox.setCurrentText(ct)


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
        return f"\ns['{node.name}'].{ref} = {value}"
    else:
        return ""


def code_if_changed_path(node, value, ref):
    """Returns code to change value of property "ref" to "value" - applicable for paths (r'')

    Args:
        node: node
        value: value to check and set
        ref: name of the property

    Returns:
        str

    """
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


# Singleton decorator, obtained from: https://betterprogramming.pub/singleton-in-python-5eaa66618e3d


class Singleton:
    def __init__(self, cls):
        self._cls = cls

    def Instance(self):
        try:
            return self._instance
        except AttributeError:
            self._instance = self._cls()
            return self._instance

    def __call__(self):
        raise TypeError("Singletons must be accessed through `Instance()`.")

    def __instancecheck__(self, inst):
        return isinstance(inst, self._cls)


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

    def connect(self, node, scene, run_code, guiEmitEvent,gui_solve_func):
        self.node = node
        self.scene = scene
        self._run_code = run_code
        self.guiEmitEvent = guiEmitEvent
        self.gui_solve_func = gui_solve_func

        self.post_update_event()

        return self.widget

    @property
    def widget(self) -> QtWidgets.QWidget:
        return self._widget

    def run_code(self, code, event=None):

        if code == "":
            return

        if event is None:
            self._run_code(code)
        else:
            self._run_code(code, event)

    @abstractmethod
    def post_update_event(self):
        """Populates the controls to reflect the current state of the node"""
        pass


@Singleton
class EditNode(NodeEditor):
    """The basic settings of every node: Name and Visible"""

    def __init__(self):
        widget = QtWidgets.QWidget()
        ui = DAVE.gui.forms.widget_name.Ui_NameWidget()
        ui.setupUi(widget)
        self.ui = ui
        self._widget = widget

        ui.tbName.textChanged.connect(self.name_changed)
        ui.cbVisible.toggled.connect(self.visible_changed)
        ui.lbColor.mousePressEvent = self.color_clicked

    def post_update_event(self):

        self.ui.tbName.blockSignals(True)
        self.ui.cbVisible.blockSignals(True)

        self.ui.tbName.setText(self.node.name)
        self.ui.cbVisible.setChecked(self.node.visible)

        self.ui.tbName.blockSignals(False)
        self.ui.cbVisible.blockSignals(False)

        if self.node.color is None:
            self.ui.lbColor.setStyleSheet('')
            self.ui.lbColor.setText('default')
        else:
            self.ui.lbColor.setStyleSheet("background-color: rgb({}, {}, {});".format(*self.node.color))
            self.ui.lbColor.setText(str(self.node.color))

    def name_changed(self):
        node = self.node
        element = "\ns['{}']".format(node.name)

        new_name = self.ui.tbName.text()

        if new_name:
            if not new_name == node.name:
                code = element + ".name = '{}'".format(new_name)
                self.run_code(code)

    def visible_changed(self):
        node = self.node
        element = "\ns['{}']".format(node.name)
        new_visible = self.ui.cbVisible.isChecked()
        if not new_visible == node.visible:
            code = element + ".visible = {}".format(new_visible)
            self.run_code(code, guiEventType.VIEWER_SETTINGS_UPDATE)

    def color_clicked(self, mouseEvent, **kwargs):

        if mouseEvent.button() == QtCore.Qt.MouseButton.RightButton:
            code = f"s['{self.node.name}'].color = None"
            self.run_code(code, guiEventType.VIEWER_SETTINGS_UPDATE)
            self.ui.lbColor.setStyleSheet('')
            self.ui.lbColor.setText(str('default'))
            return


        if self.node.color is not None:
            qcolor = QColor(*self.node.color)
            result = QColorDialog().getColor(initial=qcolor)
        else:
            result = QColorDialog().getColor()

        if result.isValid():
            code = f"s['{self.node.name}'].color = ({result.red()},{result.green()},{result.blue()})"
            self.run_code(code, guiEventType.VIEWER_SETTINGS_UPDATE)
            self.ui.lbColor.setStyleSheet("background-color: rgb({}, {}, {});".format(*self.node.color))
            self.ui.lbColor.setText(str(self.node.color))


@Singleton
class EditAxis(NodeEditor):
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

        self._widget = widget

    def post_update_event(self):

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
class EditVisual(NodeEditor):
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

        self.ui.pbRescan.pressed.connect(self.update_resource_list)
        self.ui.pbReloadFile.pressed.connect(self.reload_visual)

        self.ui.comboBox.editTextChanged.connect(self.generate_code)
        self.resources_loaded = False

    def reload_visual(self):
        # Reload the visual
        # find the actor in the viewport and re-set its  va.actors["main"].loaded_obj property

        store = self.node.path
        self.node.path = 'res: cube_with_bevel.obj'
        self.guiEmitEvent(guiEventType.SELECTED_NODE_MODIFIED)
        self.node.path = store
        self.guiEmitEvent(guiEventType.SELECTED_NODE_MODIFIED)
        self.guiEmitEvent(guiEventType.VIEWER_SETTINGS_UPDATE)

        print('Visual refreshed')



    def update_resource_list(self):

        stl = self.scene.get_resource_list("stl", include_subdirs=True)
        obj = self.scene.get_resource_list("obj", include_subdirs=True)

        names = (*stl, *obj)

        update_combobox_items_with_completer(self.ui.comboBox, names)


    def post_update_event(self):

        if not self.resources_loaded:
            self.update_resource_list()
            self.resources_loaded = True

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
            self.ui.comboBox,
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

        cvinf(self.ui.comboBox, str(self.node.path))
        # self.ui.comboBox.setCurrentText(str(self.node.path))

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

        new_path = self.ui.comboBox.currentText()

        if not new_path == self.node.path:
            code += element + ".path = r'{}'".format(new_path)

        if not np.all(new_position == self.node.offset):
            code += element + ".offset = ({}, {}, {})".format(*new_position)

        if not np.all(new_rotation == self.node.rotation):
            code += element + ".rotation = ({}, {}, {})".format(*new_rotation)

        if not np.all(new_scale == self.node.scale):
            code += element + ".scale = ({}, {}, {})".format(*new_scale)

        self.run_code(code)


@Singleton
class EditWaveInteraction(NodeEditor):
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

        new_position = np.array(
            (
                self.ui.doubleSpinBox_1.value(),
                self.ui.doubleSpinBox_2.value(),
                self.ui.doubleSpinBox_3.value(),
            )
        )
        new_path = self.ui.comboBox.currentText()

        if not new_path == self.node.path:
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

        self.ui.cbPath.currentTextChanged.connect(self.generate_code)
        self.ui.pbReScan.clicked.connect(self.rescan)

        self.fileextension = "dave"

    def rescan(self):
        self.post_update_event()

        text = (
            f"Rescan completed for files ending with {self.fileextension} in folders:"
        )
        for p in self.scene.resources_paths:
            text += f"\n - {str(p)}"
        text += "\n\nlist updated"

        QMessageBox.information(self.widget, "Done", text, QMessageBox.Ok)

    def reload(self):
        code = f"\ns['{self.node.name}'].path = r'{self.node.path}'"
        self.run_code(code, guiEventType.MODEL_STRUCTURE_CHANGED)

    def post_update_event(self):
        """Sync the properties of the node to the gui"""
        self.ui.cbPath.blockSignals(True)
        self.ui.cbPath.clear()
        self.ui.cbPath.addItems(
            self.scene.get_resource_list(self.fileextension, include_subdirs=True)
        )
        # self.ui.cbPath.setCurrentText(str(self.node.path))
        cvinf(self.ui.cbPath, str(self.node.path))
        self.ui.cbPath.blockSignals(False)

    def barge_changed(self):
        self.guiEmitEvent(guiEventType.SELECTED_NODE_MODIFIED)

    def generate_code(self):
        """Generate code to update the node, then run it"""

        code = ""
        code += code_if_changed_path(self.node, self.ui.cbPath.currentText(), "path")

        if code:
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
class EditBuoyancyOrContactMesh(NodeEditor):
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

        ui.comboBox.editTextChanged.connect(self.generate_code)
        ui.cbInvertNormals.toggled.connect(self.generate_code)

        self.ui.pbRescan.pressed.connect(self.update_resource_list)
        self.ui.pbReloadFile.pressed.connect(self.reload_file)
        self.resources_loaded = False

    def update_resource_list(self):

        stl = self.scene.get_resource_list("stl", include_subdirs=True)
        obj = self.scene.get_resource_list("obj", include_subdirs=True)

        names = (*stl, *obj)

        update_combobox_items_with_completer(self.ui.comboBox, names)


    def reload_file(self):
        self.node.trimesh._load_from_privates()
        print('Mesh reloaded')

    def post_update_event(self):

        if not self.resources_loaded:
            self.update_resource_list()
            self.resources_loaded = True

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
            self.ui.comboBox,
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

        cvinf(self.ui.comboBox, str(self.node.trimesh._path))
        # self.ui.comboBox.setCurrentText(self.node.trimesh._path)

        for widget in widgets:
            widget.blockSignals(False)

    def generate_code(self):

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

        new_path = self.ui.comboBox.currentText()

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
class EditPoi(NodeEditor):
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
class EditCable(NodeEditor):
    def __init__(self):

        widget = QtWidgets.QWidget()
        ui = DAVE.gui.forms.widget_cable.Ui_Cable_form()
        ui.setupUi(widget)

        self.ui = ui
        self._widget = widget
        self.additional_pois = list()

        # Set events
        ui.pbRemoveSelected.clicked.connect(self.delete_selected)

        ui.doubleSpinBox.valueChanged.connect(self.generate_code)
        ui.doubleSpinBox_1.valueChanged.connect(self.generate_code)
        ui.doubleSpinBox_2.valueChanged.connect(self.generate_code)
        ui.doubleSpinBox_3.valueChanged.connect(self.generate_code)
        ui.doubleSpinBox_4.valueChanged.connect(self.generate_code)

        self.ui.pushButton.clicked.connect(self.add_item)

        # ------- setup the drag-and-drop code ---------

        ui.list.dropEvent = self.dropEvent
        ui.list.dragEnterEvent = self.dragEnterEvent
        ui.list.dragMoveEvent = self.dragEnterEvent
        ui.list.itemChanged.connect(self.itemChanged)

        ui.list.setDragEnabled(True)
        ui.list.setAcceptDrops(True)
        ui.list.setDragEnabled(True)

    def itemChanged(self, *args):
        self.generate_code()

    def add_item(self):
        name = self.ui.cbPointsAndCircles.currentText()
        if self.scene.node_exists(name):

            # get a selected node
            index = self.ui.list.count()
            for i in range(index):
                if self.ui.list.item(i).isSelected():
                    index=i
                    break

            node_names = [node.name for node in self.node.connections]
            node_names.insert(index, name)

            code = f"s['{self.node.name}'].connections = ("
            for name in node_names:
                code += "'{}',".format(name)
            code = code[:-1] + ")"
            self.run_code(code)
        else:
            self.run_code(f"raise ValueError(f'No node with name {name}')")




    def post_update_event(self):

        svinf(self.ui.doubleSpinBox_1, self.node.length)
        svinf(self.ui.doubleSpinBox_2, self.node.EA)
        svinf(self.ui.doubleSpinBox, self.node.diameter)
        svinf(self.ui.doubleSpinBox_3, self.node.mass_per_length)
        svinf(self.ui.doubleSpinBox_4, self.node.mass)

        # update the combombox with points and circles

        points_and_circles = [node.name for node in self.scene.nodes_of_type((Point, Circle))]
        current_contents = [self.ui.cbPointsAndCircles.itemText(i) for i in range(self.ui.cbPointsAndCircles.count())]
        if points_and_circles != current_contents:
            update_combobox_items_with_completer(self.ui.cbPointsAndCircles, points_and_circles)

        # update_combobox_items_with_completer

        self.ui.list.blockSignals(True)  # update the list

        self.ui.list.clear()
        labelVisible = False

        for connection, reversed in zip(self.node.connections, self.node.reversed):
            item = QtWidgets.QListWidgetItem(connection.name)

            if isinstance(connection, Circle):
                item.setCheckState(Qt.CheckState.Checked if reversed else Qt.CheckState.Unchecked)
                labelVisible = True

            self.ui.list.addItem(item)

        self.ui.lbDirection.setVisible(labelVisible)

        self.set_colors()
        self.ui.list.blockSignals(False)

    def set_colors(self):
        if self.ui.doubleSpinBox_2.value() == 0:
            self.ui.doubleSpinBox_2.setStyleSheet("background: orange")
        else:
            self.ui.doubleSpinBox_2.setStyleSheet("background: white")

    def dropEvent(self, event):

        list = self.ui.list

        # dropping onto something?
        point = event.pos()
        drop_onto = list.itemAt(point)

        if drop_onto:
            row = list.row(drop_onto)
        else:
            row = -1

        if event.source() == list:
            item = list.currentItem()
            name = item.text()
            delrow = list.row(item)
            list.takeItem(delrow)
        else:
            name = event.mimeData().text()

        if row >= 0:
            list.insertItem(row, name)
        else:
            list.addItem(name)

        self.generate_code()

    def dragEnterEvent(self, event):
        if event.source() == self.ui.list:
            event.accept()
        else:
            try:
                name = event.mimeData().text()
                node = self.scene[name]
                if isinstance(node, Circle) or isinstance(node, Point):
                    event.accept()
            except:
                return


    def delete_selected(self):
        row = self.ui.list.currentRow()
        if row > -1:
            self.ui.list.takeItem(row)
        self.generate_code()

    def generate_code(self):

        self.set_colors()

        code = ""
        element = "\ns['{}']".format(self.node.name)

        new_length = self.ui.doubleSpinBox_1.value()
        new_EA = self.ui.doubleSpinBox_2.value()
        new_diameter = self.ui.doubleSpinBox.value()
        new_mass_per_length = self.ui.doubleSpinBox_3.value()

        code += code_if_changed_d(self.node, new_length, 'length')
        code += code_if_changed_d(self.node, new_EA, 'EA')
        code += code_if_changed_d(self.node, new_diameter, 'diameter')
        code += code_if_changed_d(self.node, new_mass_per_length, 'mass_per_length')
        code += code_if_changed_d(self.node, self.ui.doubleSpinBox_4.value(), 'mass')

        # connection names
        new_names = []
        for i in range(self.ui.list.count()):
            new_names.append(self.ui.list.item(i).text())

        old_names = [node.name for node in self.node.connections]

        if not (new_names == old_names):
            code += element + ".connections = ("
            for name in new_names:
                code += "'{}',".format(name)
            code = code[:-1] + ")"

        # reversed
        reversed = tuple([self.ui.list.item(irow).checkState() == Qt.CheckState.Checked for irow in range(self.ui.list.count())])

        if reversed != self.node.reversed:
            code += f'{element}.reversed = {reversed}'


        self.run_code(code)


@Singleton
class EditForce(NodeEditor):
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

    def post_update_event(self):

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

        svinf(self.ui.doubleSpinBox_1, self.node.force[0])
        svinf(self.ui.doubleSpinBox_2, self.node.force[1])
        svinf(self.ui.doubleSpinBox_3, self.node.force[2])
        svinf(self.ui.doubleSpinBox_4, self.node.moment[0])
        svinf(self.ui.doubleSpinBox_5, self.node.moment[1])
        svinf(self.ui.doubleSpinBox_6, self.node.moment[2])

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

        if not np.all(new_force == self.node.force):
            code += element + ".force = ({}, {}, {})".format(*new_force)
        if not np.all(new_moment == self.node.moment):
            code += element + ".moment = ({}, {}, {})".format(*new_moment)

        self.run_code(code)


# =================


@Singleton
class EditArea(NodeEditor):
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
class EditSheave(NodeEditor):
    def __init__(self):

        widget = QtWidgets.QWidget()
        ui = DAVE.gui.forms.widget_sheave.Ui_widget_sheave()
        ui.setupUi(widget)
        self.ui = ui
        self._widget = widget

        self.ui.sbAX.valueChanged.connect(self.generate_code)
        self.ui.sbAY.valueChanged.connect(self.generate_code)
        self.ui.sbAZ.valueChanged.connect(self.generate_code)

        self.ui.sbRadius.valueChanged.connect(self.generate_code)

    def post_update_event(self):

        widgets = [self.ui.sbAX, self.ui.sbAY, self.ui.sbAZ, self.ui.sbRadius]

        for widget in widgets:
            widget.blockSignals(True)

        svinf(self.ui.sbAX, self.node.axis[0])
        svinf(self.ui.sbAY, self.node.axis[1])
        svinf(self.ui.sbAZ, self.node.axis[2])
        svinf(self.ui.sbRadius, self.node.radius)

        for widget in widgets:
            widget.blockSignals(False)

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

        self.run_code(code)


@Singleton
class EditHydSpring(NodeEditor):
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

        ui.cbMasterAxis.currentIndexChanged.connect(self.generate_code)
        ui.cbSlaveAxis.currentIndexChanged.connect(self.generate_code)

    def post_update_event(self):

        widgets = [
            self.ui.doubleSpinBox_1,
            self.ui.doubleSpinBox_2,
            self.ui.doubleSpinBox_3,
            self.ui.doubleSpinBox_4,
            self.ui.doubleSpinBox_5,
            self.ui.doubleSpinBox_6,
            self.ui.cbMasterAxis,
            self.ui.cbSlaveAxis,
        ]

        for widget in widgets:
            widget.blockSignals(True)

        self.alist = list()
        for axis in self.scene.nodes_of_type(vfs.Frame):
            self.alist.append(axis.name)

        self.ui.cbMasterAxis.clear()
        self.ui.cbSlaveAxis.clear()

        self.ui.cbMasterAxis.addItems(self.alist)
        self.ui.cbSlaveAxis.addItems(self.alist)

        # self.ui.cbMasterAxis.setCurrentText(self.node.main.name)
        cvinf(self.ui.cbMasterAxis, self.node.main.name)
        # self.ui.cbSlaveAxis.setCurrentText(self.node.secondary.name)
        cvinf(self.ui.cbSlaveAxis, self.node.secondary.name)

        svinf(self.ui.doubleSpinBox_1, self.node.stiffness[0])
        svinf(self.ui.doubleSpinBox_2, self.node.stiffness[1])
        svinf(self.ui.doubleSpinBox_3, self.node.stiffness[2])

        svinf(self.ui.doubleSpinBox_4, self.node.stiffness[3])
        svinf(self.ui.doubleSpinBox_5, self.node.stiffness[4])
        svinf(self.ui.doubleSpinBox_6, self.node.stiffness[5])

        for widget in widgets:
            widget.blockSignals(False)

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

        new_master = self.ui.cbMasterAxis.currentText()
        new_slave = self.ui.cbSlaveAxis.currentText()

        if not np.all(new_stiffness == self.node.stiffness):
            code += element + ".stiffness = ({}, {}, {},".format(*new_stiffness[:3])
            code += "                  {}, {}, {})".format(*new_stiffness[3:])

        if not new_master == self.node.main.name:
            code += element + '.main = s["{}"]'.format(new_master)

        if not new_slave == self.node.secondary.name:
            code += element + '.secondary = s["{}"]'.format(new_slave)

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

        ui.cbMasterAxis.currentIndexChanged.connect(self.generate_code)
        ui.cbSlaveAxis.currentIndexChanged.connect(self.generate_code)

    def post_update_event(self):

        widgets = [
            self.ui.cbMasterAxis,
            self.ui.cbSlaveAxis,
            self.ui.doubleSpinBox_1,
            self.ui.doubleSpinBox_4,
        ]

        for widget in widgets:
            widget.blockSignals(True)

        self.alist = list()
        for axis in self.scene.nodes_of_type(vfs.Frame):
            self.alist.append(axis.name)

        self.ui.cbMasterAxis.clear()
        self.ui.cbSlaveAxis.clear()

        self.ui.cbMasterAxis.addItems(self.alist)
        self.ui.cbSlaveAxis.addItems(self.alist)

        # self.ui.cbMasterAxis.setCurrentText(self.node.nodeA.name)
        cvinf(self.ui.cbMasterAxis, self.node.nodeA.name)

        # self.ui.cbSlaveAxis.setCurrentText(self.node.nodeB.name)
        cvinf(self.ui.cbSlaveAxis, self.node.nodeB.name)

        svinf(self.ui.doubleSpinBox_1, self.node.k_linear)
        svinf(self.ui.doubleSpinBox_4, self.node.k_angular)

        for widget in widgets:
            widget.blockSignals(False)

    def generate_code(self):

        code = ""
        element = "\ns['{}']".format(self.node.name)

        new_k_lin = self.ui.doubleSpinBox_1.value()
        new_k_ang = self.ui.doubleSpinBox_4.value()
        new_master = self.ui.cbMasterAxis.currentText()
        new_slave = self.ui.cbSlaveAxis.currentText()

        if not new_master == self.node.nodeA.name:
            code += element + '.nodeA = s["{}"]'.format(new_master)

        if not new_slave == self.node.nodeB.name:
            code += element + '.nodeB = s["{}"]'.format(new_slave)

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

        ui.cbMasterAxis.currentIndexChanged.connect(self.generate_code)
        ui.cbSlaveAxis.currentIndexChanged.connect(self.generate_code)
        ui.sbnSegments.valueChanged.connect(self.generate_code)

    def post_update_event(self):

        widgets = [
            self.ui.sbnSegments,
            self.ui.doubleSpinBox_1,
            self.ui.doubleSpinBox_2,
            self.ui.doubleSpinBox_3,
            self.ui.doubleSpinBox_4,
            self.ui.doubleSpinBox_5,
            self.ui.sbMass,
            self.ui.cbTensionOnly,
            self.ui.cbMasterAxis,
            self.ui.cbSlaveAxis,
        ]

        for widget in widgets:
            widget.blockSignals(True)

        self.alist = list()
        for axis in self.scene.nodes_of_type(vfs.Frame):
            self.alist.append(axis.name)

        self.ui.cbMasterAxis.clear()
        self.ui.cbSlaveAxis.clear()

        self.ui.cbMasterAxis.addItems(self.alist)
        self.ui.cbSlaveAxis.addItems(self.alist)

        self.ui.cbMasterAxis.setCurrentText(self.node.nodeA.name)
        self.ui.cbSlaveAxis.setCurrentText(self.node.nodeB.name)

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

        new_master = self.ui.cbMasterAxis.currentText()
        new_slave = self.ui.cbSlaveAxis.currentText()

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

        if not new_master == self.node.nodeA.name:
            code += element + '.nodeA = s["{}"]'.format(new_master)

        if not new_slave == self.node.nodeB.name:
            code += element + '.nodeB = s["{}"]'.format(new_slave)

        if not new_n == self.node.n_segments:
            code += element + ".n_segments = {}".format(new_n)

        if not new_tensiononly == self.node.tension_only:
            code += element + ".tension_only = {}".format(new_tensiononly)

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

    def flip(self):
        code = "\ns['{}'].flip()".format(self.node.name)
        self.run_code(code)

        self.post_update_event()

    def change_side(self):
        code = "\ns['{}'].change_side()".format(self.node.name)
        self.run_code(code)

        self.post_update_event()  # no need, done automatically by run_code
        #
        # self.ui.sbSlaveRotation.valueChanged.disconnect()
        # self.ui.sbMasterRotation.valueChanged.disconnect()
        # self.ui.sbMasterRotation.setValue(self.node.rotation_on_parent)
        # self.ui.sbSlaveRotation.setValue(self.node.child_rotation)
        # self.ui.sbSlaveRotation.valueChanged.connect(self.callback)
        # self.ui.sbMasterRotation.valueChanged.connect(self.callback)

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
class EditContactBall(NodeEditor):
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


@Singleton
class EditSling(NodeEditor):
    def __init__(self):

        widget = QtWidgets.QWidget()
        ui = DAVE.gui.forms.widget_sling.Ui_Form()
        ui.setupUi(widget)

        self.ui = ui
        self._widget = widget
        self.additional_pois = list()

        # Set events
        ui.pbRemoveSelected.clicked.connect(self.delete_selected)

        ui.sbLength.valueChanged.connect(self.generate_code)
        ui.sbEA.valueChanged.connect(self.generate_code)
        ui.sbDiameter.valueChanged.connect(self.generate_code)
        ui.sbMass.valueChanged.connect(self.generate_code)
        ui.sbLEyeA.valueChanged.connect(self.generate_code)
        ui.sbLEyeB.valueChanged.connect(self.generate_code)
        ui.sbLSpliceA.valueChanged.connect(self.generate_code)
        ui.sbLSpliceB.valueChanged.connect(self.generate_code)
        ui.sbK.valueChanged.connect(self.generate_code)

        # ------- setup the drag-and-drop code ---------

        ui.list.dropEvent = self.dropEvent
        ui.list.dragEnterEvent = self.dragEnterEvent
        ui.list.dragMoveEvent = self.dragEnterEvent

        ui.list.setDragEnabled(True)
        ui.list.setAcceptDrops(True)
        ui.list.setDragEnabled(True)

    def post_update_event(self):

        widgets = [
            self.ui.sbLength,
            self.ui.sbEA,
            self.ui.sbDiameter,
            self.ui.sbMass,
            self.ui.sbLEyeA,
            self.ui.sbLEyeB,
            self.ui.sbLSpliceA,
            self.ui.sbLSpliceB,
            self.ui.sbK,
        ]

        for widget in widgets:
            widget.blockSignals(True)

        for ddb in self.additional_pois:
            self.poiLayout.removeWidget(ddb)
            ddb.deleteLater()

        svinf(self.ui.sbLength, self.node.length)
        svinf(self.ui.sbEA, self.node.EA)
        svinf(self.ui.sbDiameter, self.node.diameter)
        svinf(self.ui.sbMass, self.node.mass)
        svinf(self.ui.sbLEyeA, self.node.LeyeA)
        svinf(self.ui.sbLEyeB, self.node.LeyeB)
        svinf(self.ui.sbLSpliceA, self.node.LspliceA)
        svinf(self.ui.sbLSpliceB, self.node.LspliceB)
        svinf(self.ui.sbK, self.node.k_total)

        self.ui.list.clear()

        if self.node.endA is not None:
            self.ui.list.addItem(self.node.endA.name)

        for s in self.node.sheaves:
            self.ui.list.addItem(s.name)

        if self.node.endB is not None:
            self.ui.list.addItem(self.node.endB.name)

        for widget in widgets:
            widget.blockSignals(False)

    def dropEvent(self, event):

        list = self.ui.list

        # dropping onto something?
        point = event.pos()
        drop_onto = list.itemAt(point)

        if drop_onto:
            row = list.row(drop_onto)
        else:
            row = -1

        if event.source() == list:
            item = list.currentItem()
            name = item.text()
            delrow = list.row(item)
            list.takeItem(delrow)
        else:
            name = event.mimeData().text()

        if row >= 0:
            list.insertItem(row, name)
        else:
            list.addItem(name)

        self.generate_code()

    def dragEnterEvent(self, event):
        if event.source() == self.ui.list:
            event.accept()
        else:
            try:
                name = event.mimeData().text()
                node = self.scene[name]
                if isinstance(node, Circle) or isinstance(node, Point):
                    event.accept()
            except:
                return

    # def dragMoveEvent(self, event):
    #     event.accept()

    def delete_selected(self):
        row = self.ui.list.currentRow()
        if row > -1:
            self.ui.list.takeItem(row)
        self.generate_code()

    def generate_code(self):
        code = ""
        element = "\ns['{}']".format(self.node.name)

        node = self.node

        new_length = self.ui.sbLength.value()
        new_EA = self.ui.sbEA.value()
        new_diameter = self.ui.sbDiameter.value()
        new_mass = self.ui.sbMass.value()
        new_LeyeA = self.ui.sbLEyeA.value()
        new_LeyeB = self.ui.sbLEyeB.value()
        new_LspliceA = self.ui.sbLSpliceA.value()
        new_LspliceB = self.ui.sbLSpliceB.value()
        new_k = self.ui.sbK.value()

        code += code_if_changed_d(
            node, new_length, "length", 3
        )  # Need to change the length before changing the length of
        # the components beause the length of the components is checked against the total length

        code += code_if_changed_d(node, new_k, "k_total", 1)
        code += code_if_changed_d(node, new_EA, "EA", 1)
        code += code_if_changed_d(node, new_diameter, "diameter", 1)

        code += code_if_changed_d(node, new_mass, "mass", 1)
        code += code_if_changed_d(node, new_LeyeA, "LeyeA", 3)
        code += code_if_changed_d(node, new_LeyeB, "LeyeB", 3)
        code += code_if_changed_d(node, new_LspliceA, "LspliceA", 3)
        code += code_if_changed_d(node, new_LspliceB, "LspliceB", 3)

        # get the poi names
        new_names = []
        for i in range(self.ui.list.count()):
            new_names.append(self.ui.list.item(i).text())

        new_endA = None
        new_endB = None
        new_circles = []

        if len(new_names) > 0:
            new_endA = new_names[0]

        if len(new_names) > 1:
            new_endB = new_names[-1]

        if len(new_names) > 2:
            new_circles = new_names[1:-1]

        if node.endA is not None:
            if not node.endA.name == new_endA:
                code += element + '.endA = "{}"'.format(new_endA)
        else:
            code += element + '.endA = "{}"'.format(new_endA)

        if node.endB is not None:
            if not node.endB.name == new_endB:
                code += element + '.endB = "{}"'.format(new_endB)
        else:
            code += element + '.endB = "{}"'.format(new_endB)

        sheave_names = [n.name for n in node.sheaves]

        if not sheave_names == new_circles:

            if new_circles:
                code += element + ".sheaves = ["
                for s in new_circles:
                    code += f'"{s}", '
                code = code[:-2] + "]"
            else:
                code += element + ".sheaves = []"

        self.run_code(code)


@Singleton
class EditShackle(NodeEditor):
    def __init__(self):
        widget = QtWidgets.QWidget()
        ui = DAVE.gui.forms.widget_shackle.Ui_widgetShackle()
        ui.setupUi(widget)
        self.ui = ui
        self._widget = widget

        self.ui.comboBox.currentTextChanged.connect(self.generate_code)

    def post_update_event(self):

        self.ui.comboBox.blockSignals(True)

        self.ui.comboBox.clear()
        self.ui.comboBox.addItems(self.node.defined_kinds())

        self.ui.comboBox.setCurrentText(self.node.kind)

        self.ui.comboBox.blockSignals(False)

    def generate_code(self):

        code = ""

        kind = self.ui.comboBox.currentText()
        if kind != self.node.kind:
            element = "\ns['{}']".format(self.node.name)
            code = element + f".kind = '{kind}'"

        self.run_code(code)


@Singleton
class EditSPMT(NodeEditor):
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

        code += code_if_changed_d(self.node, self.ui.sbDX.value(), 'spacing_length')
        code += code_if_changed_d(self.node, self.ui.sbDY.value(), 'spacing_width')
        code += code_if_changed_d(self.node, self.ui.sbNX.value(), 'n_length')
        code += code_if_changed_d(self.node, self.ui.sbNY.value(), 'n_width')
        code += code_if_changed_d(self.node, self.ui.sbRefExtension.value(), 'reference_extension')
        code += code_if_changed_d(self.node, self.ui.sbRefForce.value(), 'reference_force')
        code += code_if_changed_d(self.node, self.ui.sbStiffness.value(), 'k')

        self.run_code(code, self)


@Singleton
class EditVisualOutline(NodeEditor):
    def __init__(self):
        widget = QtWidgets.QWidget()
        self._widget = widget

        layout = QtWidgets.QVBoxLayout()
        widget.setLayout(layout)
        self.cbOutline = QtWidgets.QComboBox()
        self.cbOutline.addItems(('None','Feature','Feature and Silhouette'))
        layout.addWidget(self.cbOutline)

        self.cbOutline.currentTextChanged.connect(self.generate_code)


    def post_update_event(self):
        self.cbOutline.blockSignals(True)
        if self.node.visual_outline == VisualOutlineType.NONE:
            text = 'None'
        elif self.node.visual_outline == VisualOutlineType.FEATURE_AND_SILHOUETTE:
            text = 'Feature and Silhouette'
        else:
            text = 'Feature'
        self.cbOutline.setCurrentText(text)

        self.cbOutline.blockSignals(False)

    def generate_code(self):

        q = dict()
        q['None']=VisualOutlineType.NONE
        q['Feature']=VisualOutlineType.FEATURE
        q['Feature and Silhouette']=VisualOutlineType.FEATURE_AND_SILHOUETTE

        value = q[self.cbOutline.currentText()]

        if self.node.visual_outline != value:
            code = f"s['{self.node.name}'].visual_outline = {value}"
            self.run_code(code, self)

            # Enforce reload
            store = self.node.path
            self.node.path = 'res: cube_with_bevel.obj'
            self.guiEmitEvent(guiEventType.SELECTED_NODE_MODIFIED)
            self.node.path = store
            self.guiEmitEvent(guiEventType.SELECTED_NODE_MODIFIED)
            self.guiEmitEvent(guiEventType.VIEWER_SETTINGS_UPDATE)


# ===========================================


class WidgetNodeProps(guiDockWidget):
    def guiDefaultLocation(self):
        return None  # QtCore.Qt.DockWidgetArea.RightDockWidgetArea

    def guiCreate(self):

        self.setVisible(False)
        self.setAllowedAreas(
            QtCore.Qt.LeftDockWidgetArea | QtCore.Qt.RightDockWidgetArea
        )

        self._open_edit_widgets = list()
        self._node_editors = list()

        self.scroll_area = QtWidgets.QScrollArea()
        scroll_area_layout = QtWidgets.QVBoxLayout()
        scroll_area_layout.setSpacing(0)
        self.scroll_area.setLayout(scroll_area_layout)
        self.scroll_area.setWidget(self.contents)
        scroll_area_layout.addWidget(self.contents)
        self.setWidget(self.scroll_area)
        self.scroll_area.setWidgetResizable(False)

        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)



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

        self.contents.setLayout(self.main_layout)

        self.layout = QtWidgets.QVBoxLayout()
        self.props_widget.setLayout(self.layout)

        self._Vspacer = QtWidgets.QSpacerItem(
            20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding
        )
        self.layout.addSpacerItem(self._Vspacer)

        self.positioned = False
        self.node = None



    def select_manager(self):
        node = self.guiSelection[0]
        manager = node._manager
        self.guiSelectNode(manager)

    def guiProcessEvent(self, event):

        # structure changed is emitted when a node is moved in the tree.
        # if the moved node is the active node then it needs to be updated as its local-position may have changed

        if event in [guiEventType.SELECTION_CHANGED, guiEventType.FULL_UPDATE, guiEventType.MODEL_STRUCTURE_CHANGED, guiEventType.MODEL_STEP_ACTIVATED, ]:

            # check if we have a selection
            if self.guiSelection:
                self.select_node(self.guiSelection[0])

        if self._open_edit_widgets:

            self.setVisible(True)

            # first time, position the widget at the upper-right corner of the 3d view
            if not self.positioned:
                point = QtCore.QPoint(self.gui.ui.frame3d.width() - self.width(), 0)
                point = self.gui.ui.frame3d.mapToGlobal(point)
                self.move(point)
                self.positioned = True

        else:
            self.setVisible(False)

        if event in [guiEventType.MODEL_STATE_CHANGED]:
            if self.guiSelection:
                self.select_node(self.guiSelection[0])

        # does the current node still exist?
        if self.node not in self.guiScene._nodes:
            self.select_node(None)
            return

        if event in [guiEventType.SELECTED_NODE_MODIFIED]:
            for w in self._node_editors:
                w.post_update_event()

    def run_code(self, code, event=None):
        if event is None:
            self.guiRunCodeCallback(code, guiEventType.SELECTED_NODE_MODIFIED)
        else:
            self.guiRunCodeCallback(code, event)
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
            messages = node.trimesh.check_shape()
            if messages:
                self.warning_label.setText("\n".join(messages))
                self.warning_label.setVisible(True)

                self.gui.visual.remove_temporary_actors()

                if node.trimesh.boundary_edges:
                    actor = vp.Lines(node.trimesh.boundary_edges, lw=5, c=(1, 0, 0))
                    actor.SetUserTransform(transform_from_node(node.parent))
                    self.gui.visual.add_temporary_actor(actor)
                if node.trimesh.non_manifold_edges:
                    actor = vp.Lines(node.trimesh.non_manifold_edges, lw=5, c=(1, 0, 1))
                    actor.SetUserTransform(transform_from_node(node.parent))
                    self.gui.visual.add_temporary_actor(actor)

    def select_node(self, node):

        to_be_removed = self._open_edit_widgets.copy()

        if node is None:
            self.setVisible(False)
            return

        if node._manager and not isinstance(node, vfs.Shackle):
            self.managed_label.setText(
                f"The properties of this node are managed by node '{node._manager.name}' and should not be changed manually"
            )
            self.manager_widget.setVisible(True)
            self.props_widget.setEnabled(self.guiScene._godmode)
        else:
            self.manager_widget.setVisible(False)
            self.props_widget.setEnabled(True)

        self._node_editors.clear()
        self._open_edit_widgets.clear()

        self._node_name_editor = EditNode.Instance()
        self._node_name_editor.connect(
            node, self.guiScene, self.run_code, self.guiEmitEvent, self.guiPressSolveButton
        )

        # add to layout if not already in
        name_widget = getattr(self, "_name_widget", None)
        if name_widget is None:
            self._name_widget = self._node_name_editor.widget
            self.layout.addWidget(self._name_widget)

        self.layout.removeItem(self._Vspacer)

        # # check the plugins
        # for plugin in self.gui.plugins_editor:
        #     cls = plugin(node)
        #     if cls is not None:
        #         self._node_editors.append(cls.Instance())

        if isinstance(node, vfs.Visual):
            self._node_editors.append(EditVisualOutline.Instance())
            self._node_editors.append(EditVisual.Instance())

        if isinstance(node, vfs.WaveInteraction1):
            self._node_editors.append(EditWaveInteraction.Instance())

        if isinstance(node, vfs.Component):
            self._node_editors.append(EditComponent.Instance())

        if isinstance(node, vfs.Frame):
            self._node_editors.append(EditAxis.Instance())

        if isinstance(node, vfs.RigidBody) and not isinstance(node, vfs.Shackle):
            self._node_editors.append(EditBody.Instance())

        if isinstance(node, vfs.Point):
            self._node_editors.append(EditPoi.Instance())

        if isinstance(node, vfs.Cable):
            self._node_editors.append(EditCable.Instance())

        if isinstance(node, vfs.Force):
            self._node_editors.append(EditForce.Instance())

        if isinstance(node, vfs.Circle):
            self._node_editors.append(EditSheave.Instance())

        if isinstance(node, vfs.HydSpring):
            self._node_editors.append(EditHydSpring.Instance())

        if isinstance(node, vfs.LC6d):
            self._node_editors.append(EditLC6d.Instance())

        if isinstance(node, vfs.Connector2d):
            self._node_editors.append(EditConnector2d.Instance())

        if isinstance(node, vfs.Beam):
            self._node_editors.append(EditBeam.Instance())

        if isinstance(node, vfs.ContactBall):
            self._node_editors.append(EditContactBall.Instance())

        if isinstance(node, vfs.GeometricContact):
            self._node_editors.append(EditGeometricContact.Instance())

        if isinstance(node, vfs.Sling):
            self._node_editors.append(EditSling.Instance())

        if isinstance(node, vfs.SPMT):
            self._node_editors.append(EditSPMT.Instance())

        if isinstance(node, vfs._Area):
            self._node_editors.append(EditArea.Instance())

        if (
            isinstance(node, vfs.Buoyancy)
            or isinstance(node, vfs.ContactMesh)
            or isinstance(node, vfs.Tank)
        ):
            self._node_editors.append(EditBuoyancyOrContactMesh.Instance())

        if isinstance(node, vfs.Tank):
            self._node_editors.append(EditTank.Instance())

        if isinstance(node, vfs.Shackle):
            self._node_editors.append(EditShackle.Instance())

        for key, value in DAVE_GUI_NODE_EDITORS.items():
            if isinstance(node, key):
                self._node_editors.append(value.Instance())

        to_be_added = []
        for editor in self._node_editors:
            to_be_added.append(
                editor.connect(node, self.guiScene, self.run_code, self.guiEmitEvent, self.guiPressSolveButton)
            )  # this function returns the widget

        # for item in to_be_added:
        #    print('to be added: ' + str(type(item)))

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

        self.node = node
        self.check_for_warnings()

        # self.layout.sizeHint()

        widgets = [*self._open_edit_widgets, self.manager_widget, self._name_widget]

        ht = sum([w.sizeHint().height() for w in widgets])
        wt = max([w.sizeHint().width() for w in widgets])

        print(ht)

        self.contents.setMinimumSize(QtCore.QSize(wt,ht-5))  # minus 5 to avoid scrollbar to show

        self.layout.addSpacerItem(self._Vspacer)  # add a spacer at the bottom

        # Geometry, resizing and fitting on screen
        target_height = ht

        qdw = QDesktopWidget()
        geo = qdw.screenGeometry(self)

        if target_height > geo.height():
            target_height = geo.height()
            wt = wt + 20 # for scrollbar

        self.resize(
            QtCore.QSize(wt, target_height)
        )  # set the size of the floating dock widget to its minimum size

        top = self.pos().y()

        if top + target_height > geo.height():
            top = geo.height() - target_height
            if top<=0:
                top=5
            self.setGeometry(self.pos().x(), top, wt, target_height)

