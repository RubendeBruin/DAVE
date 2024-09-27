from pathlib import Path

from PySide6.QtWidgets import QFileDialog
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QVBoxLayout,
    QScrollArea,
    QVBoxLayout,
    QFrame,
    QDialog,
)
from PySide6.QtGui import QKeySequence, QShortcut

from DAVE import *
from DAVE.gui.helpers.flow_layout import FlowLayout
from DAVE.gui.thumbnailer.thumbnail_provider import ThumbnailProvider

from DAVE.gui.forms.resource_browser import Ui_ResourceBrowser


class FileWidget(QFrame):
    def __init__(self, file_path, s: Scene):
        super().__init__()


        layout = QVBoxLayout(self)

        tumbs = ThumbnailProvider.Instance()

        # Create a label for the thumbnail
        thumbnail = QLabel(self)
        filename = s.resource_provider.get_resource_path(file_path)

        pixmap = tumbs.get_thumbnail(filename)

        # Create a label for the file name
        file_name = QLabel(file_path, parent=self)

        # Add the labels to the layout
        layout.addWidget(thumbnail)
        layout.addWidget(file_name)

        self.pixmap = pixmap
        self.thumbnail = thumbnail

        self.setLayout(layout)

        self.browser = None # will be set to filebrowser instance
        self.resource_path = file_path

    def scale(self, pixels):
        self.thumbnail.setPixmap(
            self.pixmap.scaled(
                pixels, pixels, Qt.KeepAspectRatio, Qt.SmoothTransformation
            )
        )

    def mousePressEvent(self, event):
        self.browser.select(self)


    def mouseDoubleClickEvent(self, event):
        self.browser.select_and_ok(self)



class ResourceBrowserDialog(QDialog):
    def __init__(self, s: Scene, resource_type: str or list[str] or tuple[str]):
        super().__init__()
        self.ui = Ui_ResourceBrowser()
        self.ui.setupUi(self)


        self.setWindowTitle("Select resource")

        # Create a shortcut for Ctrl + F
        self.shortcut = QShortcut(QKeySequence("Ctrl+F"), self)
        self.shortcut.activated.connect(self.ui.teFilter.setFocus)

        self.file_tiles = []
        self.selected_file = None

        self.ui.hsZoom.valueChanged.connect(self.zoom_changed)
        self.ui.lwWhere.itemSelectionChanged.connect(self.select_where)
        self.ui.lwResourcePaths.itemSelectionChanged.connect(self.select_where)

        self.ui.pushButton.setAutoDefault(True)
        self.ui.pushButton.pressed.connect(self.accept)
        self.ui.pushButton_2.pressed.connect(self.reject)

        # make resizable
        self.setSizeGripEnabled(True)


        # Set the scene
        self.scene = s

        self.selected_file = None

        # Get the resource provider
        self.resource_provider = s.resource_provider

        if isinstance(resource_type, str):
            self.resource_type = [resource_type]
        else:
            self.resource_type = tuple(resource_type)

        self.resources = []

        # scan res including subdirs
        self.resources.extend(self.resource_provider.get_resource_list(extension=self.resource_type, include_subdirs=True, include_current_dir=False))

        # scan cd excluding subdirs
        self.resources.extend(self.resource_provider.get_resource_list(extension=self.resource_type, include_subdirs=False,
                                                     include_current_dir=True))
        # Fill the files panel
        self.create_files_panel()

        # fill the lwResourcesPaths list widget
        self.ui.lwResourcePaths.clear()
        self.ui.lwResourcePaths.addItem("All Resources")
        for r in self.resource_provider.resources_paths:
            self.ui.lwResourcePaths.addItem(str(r))

        self.ui.lwResourcePaths.blockSignals(True)
        self.ui.lwResourcePaths.setCurrentRow(0)
        self.ui.lwResourcePaths.blockSignals(False)

        # select  the first item in the where list
        # create a single-shot timer
        self.ui.lwWhere.setCurrentRow(0)

        self.ui.teFilter.textChanged.connect(self.hide_tiles_on_filter)




    def open_dialog(self, ):
        """Open a dialog to select a resource

        Arguments:
            s {Scene} -- The scene to use, used to get the resource provider
            resource_type {str} -- The type of resource to select


        """
        self.ui.teFilter.setFocus()

        return self.exec()

    def select_where(self):
        row = self.ui.lwWhere.selectedIndexes()[0].row()
        self.selected_file = None

        if row==0:
            self.select_res()
            self.hide_tiles_on_filter()
        elif row == 1:
            self.select_cd()
            self.hide_tiles_on_filter()
        else:
            self.select_local()
            self.ui.teFilter.clear()



    def select_res(self):
        selection = [res for res in self.resources if res.startswith('res')]
        self.clear_files_panel()
        self.ui.lbInfo.setText("Files in resources system")
        self.ui.lbInfo.setVisible(False)

        # apply local filter if any
        if self.ui.lwResourcePaths.currentItem():
            location = self.ui.lwResourcePaths.currentItem().text()
            if location != "All Resources":
                selection = [res for res in selection if str(self.resource_provider.get_resource_path(res)).startswith(location)]

        self.fill_files_panel(selection)
        self.ui.widget_RES.setVisible(True)

    def select_cd(self):
        selection = [res for res in self.resources if res.startswith('cd')]
        self.clear_files_panel()
        self.ui.lbInfo.setText(f"Files in [{self.resource_provider.cd}]")
        self.ui.lbInfo.setVisible(True)
        self.fill_files_panel(selection)
        self.ui.widget_RES.setVisible(False)

    def select_local(self):
        # select a file using a file dialog
        # use the resources-types as filter

        dialog = QFileDialog()

        filter_str = "Resources ("
        for r in self.resource_type:
            filter_str += " *" + r
        filter_str += ')'

        dialog.setNameFilter(filter_str)
        dialog.setDirectory(str(self.resource_provider.cd))

        if dialog.exec():
            selected_file = dialog.selectedFiles()[0]
            self.clear_files_panel()
            self.ui.lbInfo.setText(f"Selected local file: {selected_file}")
            self.ui.lbInfo.setVisible(True)
            self.fill_files_panel([selected_file])
            self.ui.widget_RES.setVisible(False)


    def create_files_panel(self):
        # Create the files panel
        self.main_widget = QWidget()
        self.flow_layout = FlowLayout()

        # Create a scroll area
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(self.main_widget)
        self.main_widget.setStyleSheet("background-color: white")

        self.main_widget.setLayout(self.flow_layout)

        # Add the scroll area to the layout
        layout = QVBoxLayout()
        layout.setContentsMargins(0,0,0,0)
        self.ui.TumbnailArea.setLayout(layout)
        self.ui.TumbnailArea.layout().addWidget(scroll_area)

        self.scroll_area = scroll_area


    def fill_files_panel(self, resources):

        # delay any gui updates while adding widgets
        self.scroll_area.setVisible(False)


        file_tiles = []

        print('creating tiles')
        for file in resources:
            file_widget = FileWidget(file, self.scene)
            file_widget.scale(self.ui.hsZoom.value())
            file_tiles.append(file_widget)
            file_widget.browser = self

        print('adding widgets')
        for w in file_tiles:
            self.flow_layout.addWidget(w)

        self.file_tiles = file_tiles

        if file_tiles:
            self.select(file_tiles[0])

        self.scroll_area.setVisible(True)


    def clear_files_panel(self):
        # remove all file_tiles from the file_panel
        self.scroll_area.setVisible(False)
        for fp in self.file_tiles:
            self.flow_layout.removeWidget(fp)
            fp.deleteLater()

        self.scroll_area.setVisible(True)

        self.file_tiles.clear()

    def hide_tiles_on_filter(self):
        filter_str = self.ui.teFilter.text()

        first_tile = None

        self.scroll_area.setVisible(False)

        if not filter_str:
            for file_tile in self.file_tiles:
                file_tile.show()
                if not first_tile:
                    first_tile = file_tile
        else:
            for file_tile in self.file_tiles:
                if filter_str.lower() not in file_tile.resource_path.lower():
                    file_tile.hide()
                else:
                    file_tile.show()
                    if not first_tile:
                        first_tile = file_tile

        if first_tile:
            self.select(first_tile)

        self.scroll_area.setVisible(True)


    def zoom_changed(self, value):
        self.scroll_area.setVisible(False)
        for file_widget in self.findChildren(FileWidget):
            file_widget.scale(value)

        self.scroll_area.setVisible(True)

    def select_none(self):
        for ft in self.file_tiles:
            ft.setFrameStyle(QFrame.NoFrame)


    def select(self, file_tile):
        self.select_none()
        file_tile.setFrameStyle(QFrame.Box)

        self.selected_file = file_tile.resource_path

    def select_and_ok(self, file_tile):
        self.select(file_tile)
        self.accept()


if __name__ == "__main__":

    app = QApplication.instance() or QApplication([])

    s = Scene()
    s.resource_provider.cd = Path(r'c:\data')
    s.resource_provider.addPath(Path(r"h:\assets"))

    tumbs = ThumbnailProvider.Instance()

    try:
        from DAVE_rigging import Crane

        s.resource_provider.addPath(
            Path(r"C:\data\DAVE\modules\DAVE_rigging\resources")
        )

        crane = True
    except ImportError:
        crane = False

    if crane:

        def loader_func(s, file_path):
            print(f"Loading {file_path}")
            c = Crane(s, "demo_crane")
            c.path = file_path

        tumbs.register_loader_plugin(".crane.csv", loader_func)

        dialog = ResourceBrowserDialog(s, ".crane.csv")
        dialog.open_dialog()

    else:
        dialog = ResourceBrowserDialog(s, ["demo", "obj", "glb"])

        def loader_func(s, file_path):
            print(f"Loading {file_path}")
            s.new_frame("origin")
            s.new_visual("visual", parent="origin", path="res: cube.obj")

        tumbs.register_loader_plugin(".demo", loader_func)

        if dialog.open_dialog():
            print(dialog.selected_file)

