"""Error interaction

Errors may occur during load or execution of code in the scene.

It may be useful for the user to be informed of the error and given the option to continue or
abort the operation or directly correct the error.

The user may be able to correct the following errors:
- Missing resources
- Missing nodes

The following options are available:

missing RESOURCES:
- ignore all missing resources
- ask for each missing resource (default)
- ignore this missing resource
- for visuals: replace with a default visual


Select manually + BROWSE
Accept suggestion
Accept suggestion for all missing resources
Ignore
Ignore all missing resources


missing NODES:
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
from PySide6.QtWidgets import QFileDialog, QApplication
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QDialog

from DAVE.gui.forms.dialog_missing_item import Ui_MissingItemDialog
from DAVE.gui.helpers.my_qt_helpers import update_combobox_items_with_completer
from DAVE.gui.new_node_dialog import fill_dropdown_boxes
from DAVE.resource_provider import DaveResourceProvider

from DAVE.scene import Scene
from DAVE.tools import MostLikelyMatch


class MissingItemDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MissingItemDialog()
        self.ui.setupUi(self)
        self.ignore_all_clicked = False

        # only for browse function
        self.item_name = None # the name of the missing item for browsing
        self.extensions = ['All files : *.*']

        self.setWindowTitle("Missing item")

        self.ui.pbNever.pressed.connect(self.ignore_all)
        self.ui.pbNo.pressed.connect(self.reject)
        self.ui.pbYes.pressed.connect(self.accept)

        self.ui.pbBrowse.pressed.connect(self.browse)


    def ignore_all(self):
        self.ignore_all_clicked = True
        self.reject()

    def browse(self):
        # use a file dialog to select a file
        filter = ''

        if self.item_name:
            filter += f"{self.item_name} ({self.item_name})"

        if self.extensions:
            if filter:
                filter += ";;"

            filter += "All similar (*." + '; *.'.join(self.extensions) + ")"

        if filter:
            filter += ";;"

        filter += "All files (*.*)"

        result = QFileDialog.getOpenFileName(None,
                                             'Select a file',
                                             None,
                                             filter)[0]

        if result:
            self.ui.cbReplacement.setCurrentText(result)
            self.accept()



    @classmethod
    def _handle_missing(cls, item_name, suggestions, browse, extensions = None, pure_name = None):

        if pure_name is None:
            pure_name = item_name

        dialog = cls()

        dialog.item_name = pure_name

        dialog.ui.pbBrowse.setVisible(browse)
        dialog.extensions = extensions

        # remove the close button from the dialog
        dialog.setWindowFlag(Qt.WindowContextHelpButtonHint, False)
        dialog.setWindowFlag(Qt.WindowCloseButtonHint, False)

        if browse:
            dialog.ui.label.setText("A resource with this url could not be found:")
            dialog.ui.label_2.setText("Use the following replacement file:")

        dialog.ui.lbItemName.setText(item_name)
        dialog.ui.pbBrowse.setVisible(browse)

        update_combobox_items_with_completer(dialog.ui.cbReplacement, suggestions)
        dialog.ui.cbReplacement.setCurrentIndex(0)

        result = dialog.exec()

        if result == QDialog.Accepted:
            return dialog.ui.cbReplacement.currentText(), dialog.ui.cbAcceptAll.isChecked()
        elif result == QDialog.Rejected:
            return (None, dialog.ignore_all_clicked)

        raise ValueError("Dialog was closed in an unexpected way")

    @classmethod
    def handle_missing_node(cls, item_name, suggestions):
        """Run the dialog and return the result

        (None | item name, bool)

        return values:
        [0] None: ignore
            string: name of the selected item
        [1] bool: apply to all


        """

        return cls._handle_missing(item_name, suggestions, False)



    @classmethod
    def handle_missing_resource(cls, item_name, suggestions, extensions = None):
        """Run the dialog and return the result

        (None | item name, bool)

        return values:
        [0] None: ignore
            string: name of the selected item
        [1] bool: apply to all

        """

        pure_name = item_name.split(":")[-1].strip()  # remove 'res: ' or 'cd: '

        # strip any subfolders
        pure_name = pure_name.split("/")[-1]
        pure_name = pure_name.split("\\")[-1]

        return cls._handle_missing(item_name, suggestions, True, extensions=extensions, pure_name = pure_name)






class ErrorInteraction:

    def __init__(self):
        self.ignore_all_missing_resources = False
        self.ignore_all_missing_nodes = False

        self.accept_all_suggested_resources = False
        self.accept_all_suggested_nodes = False


    def reset(self):
        """Reset the error interaction to defaults (no ignore all, no accept all)"""
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
            nodes = list(scene.nodes_where(kind = req_type))
            choices = [n.name for n in nodes]

        if len(choices) == 0:
            return None

        suggestion = MostLikelyMatch(node_name, choices)
        choices.remove(suggestion)

        if self.accept_all_suggested_nodes:
            return suggestion

        result, all = MissingItemDialog.handle_missing_node(node_name, [suggestion, *choices])

        if result is None:
            if all:
                self.ignore_all_missing_nodes = True
            return None

        else:
            if all:
                self.accept_all_suggested_nodes = True

        return result

    def handle_missing_resource(self, resource_provider : DaveResourceProvider, resource_name : str):
        """Handle a missing resource

        resource_provider: the resource_provider that is calling
        resource_name: the name of the missing resource

        returns: the name of the resource to use, or None if the user has not made a choice
        """

        if self.ignore_all_missing_resources:
            return None

        # check the type of the resource using the extension
        # if the extension is a .csv, then expand to the part before the .csv as well
        # if the extension is a visual , then accept any other visual type as well

        VISUAL_TYPES = ['gltf','glb','obj','stl']

        ext = resource_name.split('.')[-1]
        if ext == 'csv':
            ext = [resource_name.split('.')[-2] + '.csv']
        elif ext in VISUAL_TYPES:
            ext = VISUAL_TYPES
        else:
            ext = [ext]

        choices = resource_provider.get_resource_list(ext)

        if len(choices) == 0:
            return None

        suggestion = MostLikelyMatch(resource_name, choices)
        choices.remove(suggestion)

        if self.accept_all_suggested_resources:
            return suggestion

        result, all = MissingItemDialog.handle_missing_resource(resource_name, [suggestion, *choices], extensions=ext)

        if result is None:
            if all:
                self.ignore_all_missing_resources = True
            return None

        else:
            if all:
                self.accept_all_suggested_resources = True

        return result


if __name__ == '__main__':
    # app = QApplication.instance or QApplication([])
    # print(MissingItemDialog.handle_missing_resource('missing_resource', ['suggestion1', 'suggestion2']))
    s = Scene()
    EI = ErrorInteraction()

    s.error_interaction = EI

    s.resource_provider.get_resource_path(filename='res: unlikely to exist.obj', error_interaction=EI)

    # EI.handle_missing_resource(s, 'missing_resource', ['suggestion1', 'suggestion2'])

    # s.error_interaction = EI
    #
    # for i in range(100):
    #     s.new_frame(f'parent{i}')
    #
    # for i in range(10):
    #     try:
    #         s.new_point(f'p{i}', parent = 'no_parent')
    #     except:
    #         pass

