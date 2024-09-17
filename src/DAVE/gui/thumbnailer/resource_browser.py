from PySide6.QtGui import QPixmap, QImage
import numpy as np
from vtkmodules.vtkIOGeometry import vtkOBJReader, vtkSTLReader
from vtkmodules.vtkIOImport import vtkGLTFImporter
from vtkmodules.vtkRenderingCore import vtkRenderer, vtkRenderWindow, vtkPolyDataMapper, vtkActor, vtkCamera, \
    vtkWindowToImageFilter
from vtkmodules.util.numpy_support import vtk_to_numpy

from DAVE import *
import PySide6
from PySide6.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QScrollArea, QVBoxLayout, QFrame
from PySide6.QtGui import QPixmap
from DAVE.gui.helpers.flow_layout import FlowLayout


from PySide6.QtGui import QPixmap, QImage

from DAVE.gui.thumbnailer.thumbnail_provider import ThumbnailProvider


class FileWidget(QFrame):
    def __init__(self, file_path):
        super().__init__()
        layout = QVBoxLayout()

        tumbs = ThumbnailProvider.Instance()

        # Create a label for the thumbnail
        thumbnail = QLabel()
        filename = s.resource_provider.get_resource_path(file_path)
        print(filename)

        pixmap = tumbs.get_thumbnail(filename)

        # Create a label for the file name
        file_name = QLabel(file_path)

        # Add the labels to the layout
        layout.addWidget(thumbnail)
        layout.addWidget(file_name)

        self.pixmap = pixmap
        self.thumbnail = thumbnail

        self.scale(50)

        self.setLayout(layout)

    def scale(self, pixels):
        self.thumbnail.setPixmap(self.pixmap.scaled(pixels, pixels, PySide6.QtCore.Qt.KeepAspectRatio, PySide6.QtCore.Qt.SmoothTransformation))

    def mousePressEvent(self, event):
        print("Mouse pressed")
        self.scale(300)
        self.setFrameStyle(QFrame.Box)


app = QApplication.instance()

s = Scene()
s.add_resources_paths(r"C:\Users\MS12H\Jottacloud\RdBr\Klanten\Jumbo\DAVE company resources\Library\Visuals")
file_list = s.resource_provider.get_resource_list(extension='glb')
file_list.extend(s.resource_provider.get_resource_list(extension='obj'))
file_list.extend(s.resource_provider.get_resource_list(extension='stl'))
file_list.extend(s.resource_provider.get_resource_list(extension='dave'))

# Create the main widget and layout


main_widget = QWidget()
flow_layout = FlowLayout()

# Create a scroll area
scroll_area = QScrollArea()
scroll_area.setWidgetResizable(True)
scroll_area.setWidget(main_widget)

# Add file widgets to the flow layout
file_tiles = []
for file in file_list:
    file_widget = FileWidget(file)
    flow_layout.addWidget(file_widget)
    file_tiles.append(file_widget)

main_widget.setLayout(flow_layout)

# Show the scroll area
scroll_area.show()

app.exec()