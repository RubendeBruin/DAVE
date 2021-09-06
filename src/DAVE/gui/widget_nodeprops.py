from abc import ABC, abstractmethod
import vedo as vp

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

from DAVE.visual import transform_from_node

import numpy as np

from PySide2.QtWidgets import QListWidgetItem
from PySide2 import QtWidgets


def code_if_changed(node, value, ref, dec=3):
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
    if abs(value[0] - current[0]) > 10 ** (-dec) or \
            abs(value[1] - current[1]) > 10 ** (-dec) or \
            abs(value[2] - current[2]) > 10 ** (-dec) :

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

    """

    @abstractmethod
    def __init__(self):
        """Creates the gui and connects signals"""
        pass

    def connect(self, node, scene, run_code):
        self.node = node
        self.scene = scene
        self._run_code = run_code

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

    def post_update_event(self):

        self.ui.tbName.blockSignals(True)
        self.ui.cbVisible.blockSignals(True)

        self.ui.tbName.setText(self.node.name)
        self.ui.cbVisible.setChecked(self.node.visible)

        self.ui.tbName.blockSignals(False)
        self.ui.cbVisible.blockSignals(False)

    def name_changed(self):
        node = self.node
        element = "\ns['{}']".format(node.name)

        new_name = self.ui.tbName.text()
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

        self.ui.doubleSpinBox_1.setValue(self.node.position[0])
        self.ui.doubleSpinBox_2.setValue(self.node.position[1])
        self.ui.doubleSpinBox_3.setValue(self.node.position[2])

        self.ui.doubleSpinBox_4.setValue(self.node.rotation[0])
        self.ui.doubleSpinBox_5.setValue(self.node.rotation[1])
        self.ui.doubleSpinBox_6.setValue(self.node.rotation[2])

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
        self.ui.comboBox.editTextChanged.connect(self.generate_code)

    def post_update_event(self):

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

        self.ui.doubleSpinBox_1.setValue(self.node.offset[0])
        self.ui.doubleSpinBox_2.setValue(self.node.offset[1])
        self.ui.doubleSpinBox_3.setValue(self.node.offset[2])

        self.ui.doubleSpinBox_4.setValue(self.node.rotation[0])
        self.ui.doubleSpinBox_5.setValue(self.node.rotation[1])
        self.ui.doubleSpinBox_6.setValue(self.node.rotation[2])

        self.ui.doubleSpinBox_7.setValue(self.node.scale[0])
        self.ui.doubleSpinBox_8.setValue(self.node.scale[1])
        self.ui.doubleSpinBox_9.setValue(self.node.scale[2])

        self.ui.comboBox.clear()
        self.ui.comboBox.addItems(self.scene.get_resource_list("stl"))
        self.ui.comboBox.addItems(self.scene.get_resource_list("obj"))

        self.ui.comboBox.setCurrentText(str(self.node.path))

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

        self.ui = ui

    def post_update_event(self):

        widgets = [
            self.ui.doubleSpinBox_1,
            self.ui.doubleSpinBox_2,
            self.ui.doubleSpinBox_3,
            self.ui.comboBox,
        ]

        for widget in widgets:
            widget.blockSignals(True)

        self.ui.doubleSpinBox_1.setValue(self.node.offset[0])
        self.ui.doubleSpinBox_2.setValue(self.node.offset[1])
        self.ui.doubleSpinBox_3.setValue(self.node.offset[2])

        self.ui.comboBox.clear()
        self.ui.comboBox.addItems(self.scene.get_resource_list("dhyd"))
        self.ui.comboBox.setCurrentText(
            str(self.node.path)
        )  # str because path may be a Path

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

        self.ui.sbPermeability.setValue(self.node.permeability)
        self.ui.sbDenstiy.setValue(self.node.density)
        self.ui.sbVolume.setValue(self.node.volume)
        self.ui.sbPercentage.setValue(self.node.fill_pct)
        self.ui.sbElevation.setValue(self.node.level_global)
        self.ui.cbFreeFlooding.setChecked(self.node.free_flooding)

        self.ui.cbUseOutsideDensity.setChecked(self.node.density < 0)

        if self.node.density < 0:
            self.ui.sbDenstiy.setValue(self.scene.rho_water)

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

    def post_update_event(self):

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

        self.ui.doubleSpinBox_1.setValue(self.node.trimesh._offset[0])
        self.ui.doubleSpinBox_2.setValue(self.node.trimesh._offset[1])
        self.ui.doubleSpinBox_3.setValue(self.node.trimesh._offset[2])

        self.ui.doubleSpinBox_4.setValue(self.node.trimesh._rotation[0])
        self.ui.doubleSpinBox_5.setValue(self.node.trimesh._rotation[1])
        self.ui.doubleSpinBox_6.setValue(self.node.trimesh._rotation[2])

        self.ui.doubleSpinBox_7.setValue(self.node.trimesh._scale[0])
        self.ui.doubleSpinBox_8.setValue(self.node.trimesh._scale[1])
        self.ui.doubleSpinBox_9.setValue(self.node.trimesh._scale[2])

        self.ui.cbInvertNormals.setChecked(self.node.trimesh._invert_normals)

        self.ui.comboBox.clear()
        self.ui.comboBox.addItems(self.scene.get_resource_list("stl"))
        self.ui.comboBox.addItems(self.scene.get_resource_list("obj"))

        self.ui.comboBox.setCurrentText(self.node.trimesh._path)

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

        self.ui.doubleSpinBox_1.setValue(self.node.cog[0])
        self.ui.doubleSpinBox_2.setValue(self.node.cog[1])
        self.ui.doubleSpinBox_3.setValue(self.node.cog[2])
        self.ui.doubleSpinBox_mass.setValue(self.node.mass)

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

        self.ui.doubleSpinBox_1.setValue(self.node.position[0])
        self.ui.doubleSpinBox_2.setValue(self.node.position[1])
        self.ui.doubleSpinBox_3.setValue(self.node.position[2])

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

        ui.doubleSpinBox_1.valueChanged.connect(self.generate_code)
        ui.doubleSpinBox_2.valueChanged.connect(self.generate_code)
        ui.doubleSpinBox.valueChanged.connect(self.generate_code)

        # ------- setup the drag-and-drop code ---------

        ui.list.dropEvent = self.dropEvent
        ui.list.dragEnterEvent = self.dragEnterEvent
        ui.list.dragMoveEvent = self.dragEnterEvent

        ui.list.setDragEnabled(True)
        ui.list.setAcceptDrops(True)
        ui.list.setDragEnabled(True)

    def post_update_event(self):

        widgets = [
            self.ui.doubleSpinBox_1,
            self.ui.doubleSpinBox_2,
            self.ui.doubleSpinBox,
        ]

        for widget in widgets:
            widget.blockSignals(True)

        for ddb in self.additional_pois:
            self.ui.poiLayout.removeWidget(ddb)
            ddb.deleteLater()

        self.ui.doubleSpinBox_1.setValue(self.node.length)
        self.ui.doubleSpinBox_2.setValue(self.node.EA)
        self.ui.doubleSpinBox.setValue(self.node.diameter)

        for widget in widgets:
            widget.blockSignals(False)

        self.ui.list.clear()
        for item in self.node._give_poi_names():
            self.ui.list.addItem(item)

        self.set_colors()

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

    # def dragMoveEvent(self, event):
    #     event.accept()

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

        if not new_length == self.node.length:
            code += element + ".length = {}".format(new_length)

        if not new_EA == self.node.EA:
            code += element + ".EA = {}".format(new_EA)

        if not new_diameter == self.node.diameter:
            code += element + ".diameter = {}".format(new_diameter)

        # get the poi names
        # new_names = [self.ui.comboBox.currentText(),self.ui.comboBox_2.currentText()]
        new_names = []
        for i in range(self.ui.list.count()):
            new_names.append(self.ui.list.item(i).text())

        if not (new_names == self.node._give_poi_names):
            code += element + ".connections = ("
            for name in new_names:
                code += "'{}',".format(name)
            code = code[:-1] + ")"

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

        self.ui.doubleSpinBox_1.setValue(self.node.force[0])
        self.ui.doubleSpinBox_2.setValue(self.node.force[1])
        self.ui.doubleSpinBox_3.setValue(self.node.force[2])

        self.ui.doubleSpinBox_4.setValue(self.node.moment[0])
        self.ui.doubleSpinBox_5.setValue(self.node.moment[1])
        self.ui.doubleSpinBox_6.setValue(self.node.moment[2])

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

        self.ui.Area.setValue(self.node.A)
        self.ui.Cd.setValue(self.node.Cd)
        self.ui.X.setValue(self.node.direction[0])
        self.ui.Y.setValue(self.node.direction[1])
        self.ui.Z.setValue(self.node.direction[2])
        self.ui.X_2.setValue(self.node.direction[0])
        self.ui.Y_2.setValue(self.node.direction[1])
        self.ui.Z_2.setValue(self.node.direction[2])

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

        code += code_if_changed(self.node, self.ui.Cd.value(), 'Cd')
        code += code_if_changed(self.node, self.ui.Area.value(), 'A')

        if self.ui.rbNoOrientation.isChecked():
            if self.node.areakind != AreaKind.SPHERE:
                code += element + '.areakind = AreaKind.SPHERE'
        elif self.ui.rbPlane.isChecked():
            if self.node.areakind != AreaKind.PLANE:
                code += element + '.areakind = AreaKind.PLANE'

            new_direction = (self.ui.X.value(), self.ui.Y.value(), self.ui.Z.value())
            code += code_if_changed_v3(self.node, new_direction, 'direction')

        elif self.ui.rbCylinder.isChecked():
            if self.node.areakind != AreaKind.CYLINDER:
                code += element + '.areakind = AreaKind.CYLINDER'

            new_direction = (self.ui.X_2.value(), self.ui.Y_2.value(), self.ui.Z_2.value())
            code += code_if_changed_v3(self.node, new_direction, 'direction')

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

        self.ui.sbAX.setValue(self.node.axis[0])
        self.ui.sbAY.setValue(self.node.axis[1])
        self.ui.sbAZ.setValue(self.node.axis[2])
        self.ui.sbRadius.setValue(self.node.radius)

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

        self.ui.doubleSpinBox_1.setValue(self.node.cob[0])
        self.ui.doubleSpinBox_2.setValue(self.node.cob[1])
        self.ui.doubleSpinBox_3.setValue(self.node.cob[2])
        self.ui.BMT.setValue(self.node.BMT)
        self.ui.BML.setValue(self.node.BML)
        self.ui.COFX.setValue(self.node.COFX)
        self.ui.COFY.setValue(self.node.COFY)
        self.ui.kHeave.setValue(self.node.kHeave)
        self.ui.waterline.setValue(self.node.waterline)
        self.ui.disp.setValue(self.node.displacement_kN)

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

        self.ui.cbMasterAxis.setCurrentText(self.node.main.name)
        self.ui.cbSlaveAxis.setCurrentText(self.node.secondary.name)

        self.ui.doubleSpinBox_1.setValue(self.node.stiffness[0])
        self.ui.doubleSpinBox_2.setValue(self.node.stiffness[1])
        self.ui.doubleSpinBox_3.setValue(self.node.stiffness[2])

        self.ui.doubleSpinBox_4.setValue(self.node.stiffness[3])
        self.ui.doubleSpinBox_5.setValue(self.node.stiffness[4])
        self.ui.doubleSpinBox_6.setValue(self.node.stiffness[5])

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

        self.ui.cbMasterAxis.setCurrentText(self.node.nodeA.name)
        self.ui.cbSlaveAxis.setCurrentText(self.node.nodeB.name)

        self.ui.doubleSpinBox_1.setValue(self.node.k_linear)
        self.ui.doubleSpinBox_4.setValue(self.node.k_angular)

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

        self.ui.doubleSpinBox_1.setValue(self.node.L)
        self.ui.doubleSpinBox_2.setValue(self.node.EIy)
        self.ui.doubleSpinBox_3.setValue(self.node.EIz)

        self.ui.doubleSpinBox_4.setValue(self.node.GIp)
        self.ui.doubleSpinBox_5.setValue(self.node.EA)

        self.ui.cbTensionOnly.setChecked(self.node.tension_only)

        self.ui.sbMass.setValue(self.node.mass)

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

        self.ui.sbMasterRotation.setValue(self.node.rotation_on_parent)
        self.ui.sbSlaveRotation.setValue(self.node.child_rotation)
        self.ui.sbSwivel.setValue(self.node.swivel)

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

        self.ui.sbR.setValue(self.node.radius)
        self.ui.sbK.setValue(self.node.k)

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

        self.ui.sbLength.setValue(self.node.length)
        self.ui.sbEA.setValue(self.node.EA)
        self.ui.sbDiameter.setValue(self.node.diameter)
        self.ui.sbMass.setValue(self.node.mass)
        self.ui.sbLEyeA.setValue(self.node.LeyeA)
        self.ui.sbLEyeB.setValue(self.node.LeyeB)
        self.ui.sbLSpliceA.setValue(self.node.LspliceA)
        self.ui.sbLSpliceB.setValue(self.node.LspliceB)
        self.ui.sbK.setValue(self.node.k_total)

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

        code += code_if_changed(node, new_k, 'k_total', 1)
        code += code_if_changed(node, new_EA, 'EA', 1)
        code += code_if_changed(node, new_diameter, 'diameter', 1)

        code += code_if_changed(node, new_mass, 'mass', 1)
        code += code_if_changed(node, new_LeyeA, 'LeyeA', 3)
        code += code_if_changed(node, new_LeyeB, 'LeyeB', 3)
        code += code_if_changed(node, new_LspliceA, 'LspliceA', 3)
        code += code_if_changed(node, new_LspliceB, 'LspliceB', 3)
        code += code_if_changed(node, new_length, 'length', 3)


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

    def select_manager(self):
        node = self.guiSelection[0]
        manager = node._manager
        self.guiSelectNode(manager)

    def guiProcessEvent(self, event):

        if event in [guiEventType.SELECTION_CHANGED, guiEventType.FULL_UPDATE]:
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
        self._node_name_editor.connect(node, self.guiScene, self.run_code)

        # add to layout if not already in
        name_widget = getattr(self, "_name_widget", None)
        if name_widget is None:
            self._name_widget = self._node_name_editor.widget
            self.layout.addWidget(self._name_widget)

        self.layout.removeItem(self._Vspacer)

        # check the plugins
        for plugin in self.gui.plugins_editor:
            cls = plugin(node)
            if cls is not None:
                self._node_editors.append(cls.Instance())

        if isinstance(node, vfs.Visual):
            self._node_editors.append(EditVisual.Instance())

        if isinstance(node, vfs.WaveInteraction1):
            self._node_editors.append(EditWaveInteraction.Instance())

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

        to_be_added = []
        for editor in self._node_editors:
            to_be_added.append(
                editor.connect(node, self.guiScene, self.run_code)
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

        self.layout.addSpacerItem(self._Vspacer)  # add a spacer at the bottom

        self.resize(
            0, 0
        )  # set the size of the floating dock widget to its minimum size
        self.adjustSize()
