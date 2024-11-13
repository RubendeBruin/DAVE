from abc import ABC, abstractmethod

from PySide6.QtWidgets import (
    QDoubleSpinBox,
    QCheckBox,
)

from PySide6 import QtWidgets
from DAVE import Scene, Node, Frame
from DAVE.gui.dock_system.dockwidget import guiEventType


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

    nodetypes_for_parent = Frame
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
