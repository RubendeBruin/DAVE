"""Error interaction

Errors may occur during load or execution of code in the scene.

It may be useful for the user to be informed of the error and given the option to continue or
abort the operation or directly correct the error.

The user may be able to correct the following errors:
- Missing resources
- Missing nodes

The following options are available:

missing resources:
- ignore all missing resources
- ask for each missing resource (default)
- ignore this missing resource
- for visuals: replace with a default visual


Select manually
Accept suggestion
Accept suggestion for all missing resources
Ignore
Ignore all missing resources


missing nodes:
- ignore all missing nodes
- ask for each missing node (default)
- try to select best match from the scene

Select manually
Accept suggestion
Accept suggestion for all missing nodes
Ignore
Ignore all missing nodes

----

Implementation:

an instance of this class can be attached to the scene as ".error_interaction".
By default this is None

when an error occurs, the scene will check if the error_interaction is not None and call the
handle_missing_resource or handle_missing_node method.

The error interaction will then show a dialog to the user and return the result.
Or return None if the user has not made a choice.

These methods are called with a handle to the scene that is calling. This is required for the resource provider and
node trees.

When copying a scene, the created copy may be given a handle to the same error interaction instance. This way the SAME
error interaction can be shared between scenes. This is useful when loading components for example.

"""
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QDialog

from DAVE.gui.forms.dialog_missing_item import Ui_MissingItemDialog
from DAVE.gui.helpers.my_qt_helpers import update_combobox_items_with_completer
from DAVE.gui.new_node_dialog import fill_dropdown_boxes

from DAVE.scene import Scene
from DAVE.tools import MostLikelyMatch


class MissingItemDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MissingItemDialog()
        self.ui.setupUi(self)
        self.ignore_all_clicked = False

        self.ui.pbNever.pressed.connect(self.ignore_all)
        self.ui.pbNo.pressed.connect(self.reject)
        self.ui.pbYes.pressed.connect(self.accept)


    def ignore_all(self):
        self.ignore_all_clicked = True
        self.reject()



    @classmethod
    def run(cls, item_name, suggestions):
        """Run the dialog and return the result

        (None | item name, bool)

        return values:
        [0] None: ignore
            string: name of the selected item
        [1] bool: apply to all


        """
        dialog = cls()

        # remove the close button from the dialog
        dialog.setWindowFlag(Qt.WindowContextHelpButtonHint, False)

        dialog.ui.lbItemName.setText(item_name)

        update_combobox_items_with_completer(dialog.ui.cbReplacement, suggestions)
        dialog.ui.cbReplacement.setCurrentIndex(0)

        result = dialog.exec()

        if result == QDialog.Accepted:
            return dialog.ui.cbReplacement.currentText(), dialog.ui.cbAcceptAll.isChecked()
        elif result == QDialog.Rejected:
            return (None, dialog.ignore_all_clicked)

        raise ValueError("Dialog was closed in an unexpected way")







class ErrorInteraction:

    def __init__(self):
        self.ignore_all_missing_resources = False
        self.ignore_all_missing_nodes = False

        self.accept_all_suggested_resources = False
        self.accept_all_suggested_nodes = False


    def reset(self):
        """Reset the error interaction to defaults"""
        self.__init__()

    def handle_missing_node(self, scene, node_name, req_type= None):
        """Handle a missing node

        scene: the scene that is calling
        node_name: the name of the missing node

        returns: the name of the node to use, or None if the user has not made a choice
        """

        if self.ignore_all_missing_nodes:
            return None

        # See if we can give a good hint using fuzzy
        if req_type is None:
            choices = list(scene.node_names)
        else:
            choices = list(scene.nodes_where(kind = req_type))

        if len(choices) == 0:
            return None

        suggestion = MostLikelyMatch(node_name, choices)
        choices.remove(suggestion)

        if self.accept_all_suggested_nodes:
            return suggestion

        result, all = MissingItemDialog.run(node_name, [suggestion, *choices])

        if result is None:
            if all:
                self.ignore_all_missing_nodes = True
            return None

        else:
            if all:
                self.accept_all_suggested_nodes = True

        return result



        # msg = QMessageBox()
        # msg.setIcon(QMessageBox.Question)
        # msg.setText(
        #     f'Node with name "{node_name}" not found. Did you mean: "{suggestion}"?'
        # )
        # msg.setWindowTitle("DAVE")
        # msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        # if msg.exec() == QMessageBox.Yes:
        #     return self.node_by_name(suggestion)
        #
        #



if __name__ == '__main__':
    s = Scene()
    EI = ErrorInteraction()
    s.error_interaction = EI

    for i in range(100):
        s.new_frame(f'parent{i}')

    for i in range(10):
        s.new_point(f'p{i}', parent = 'no_parent')
