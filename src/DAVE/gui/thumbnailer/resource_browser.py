from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QScrollArea, QVBoxLayout, QFrame, QDialog
from PySide6.QtGui import QPixmap, QImage

from DAVE import *
from DAVE.gui.helpers.flow_layout import FlowLayout
from DAVE.gui.thumbnailer.thumbnail_provider import ThumbnailProvider

from DAVE.gui.forms.resource_browser import Ui_ResourceBrowser


class FileWidget(QFrame):
    def __init__(self, file_path, s : Scene):
        super().__init__()
        layout = QVBoxLayout()

        tumbs = ThumbnailProvider.Instance()

        # Create a label for the thumbnail
        thumbnail = QLabel()
        filename = s.resource_provider.get_resource_path(file_path)

        pixmap = tumbs.get_thumbnail(filename)

        # Create a label for the file name
        file_name = QLabel(file_path)

        # Add the labels to the layout
        layout.addWidget(thumbnail)
        layout.addWidget(file_name)

        self.pixmap = pixmap
        self.thumbnail = thumbnail

        self.setLayout(layout)

    def scale(self, pixels):
        self.thumbnail.setPixmap(self.pixmap.scaled(pixels, pixels, Qt.KeepAspectRatio, Qt.SmoothTransformation))

    def mousePressEvent(self, event):
        print("Mouse pressed")
        self.scale(300)
        self.setFrameStyle(QFrame.Box)


class ResourceBrowserDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.ui = Ui_ResourceBrowser()
        self.ui.setupUi(self)

        self.ui.hsZoom.valueChanged.connect(self.zoom_changed)

    def open_dialog(self, s: Scene, resource_type : str, model_maker_callback = None):
        """Open a dialog to select a resource

        Arguments:
            s {Scene} -- The scene to use, used to get the resource provider
            resource_type {str} -- The type of resource to select
            model_maker_callback {function} -- A function to call to create a DAVE model from a
                resource - used by the thumbnailer to show the resource

        """

        # Set the scene
        self.scene = s

        # Set the resource type
        self.resource_type = resource_type

        # Set the model maker callback
        self.model_maker_callback = model_maker_callback

        # Get the resource provider
        self.resource_provider = s.resource_provider

        # Get the resources
        self.resources = self.resource_provider.get_resource_list(extension=resource_type)

        # Fill the files panel
        self.fill_files_panel(self.resources)


    def fill_files_panel(self, resources):
        # Create the files panel
        main_widget = QWidget()
        flow_layout = FlowLayout()

        # Create a scroll area
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(main_widget)

        file_tiles = []
        for file in resources:
            file_widget = FileWidget(file, self.scene)
            file_widget.scale(self.ui.hsZoom.value())
            flow_layout.addWidget(file_widget)
            file_tiles.append(file_widget)

        main_widget.setLayout(flow_layout)

        # Add the scroll area to the layout
        self.ui.TumbnailArea.setLayout(QVBoxLayout())
        self.ui.TumbnailArea.layout().addWidget(scroll_area)

        self.exec()

    def zoom_changed(self, value):
        for file_widget in self.findChildren(FileWidget):
            file_widget.scale(value)






app = QApplication.instance()

s = Scene()
dialog = ResourceBrowserDialog()
dialog.open_dialog(s, 'obj')

# app.exec()
#
# s.add_resources_paths(r"C:\Users\MS12H\Jottacloud\RdBr\Klanten\Jumbo\DAVE company resources\Library\Visuals")
# file_list = s.resource_provider.get_resource_list(extension='glb')
# file_list.extend(s.resource_provider.get_resource_list(extension='obj'))
# file_list.extend(s.resource_provider.get_resource_list(extension='stl'))
# file_list.extend(s.resource_provider.get_resource_list(extension='dave'))
#
# # Create the main widget and layout
#
#
#

#
# # Add file widgets to the flow layout

#
# # Show the scroll area
# scroll_area.show()
#
# app.exec()