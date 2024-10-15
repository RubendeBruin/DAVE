import PIL.ImageFont
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QWidget, QListWidgetItem, QColorDialog
from pyqtgraph.parametertree.Parameter import SignalBlocker

from DAVE.annotations import AnnotationLayer
from DAVE.annotations.layer import DEFAULT_ANNOTATION_FONT
from DAVE.gui.forms.widget_viewport_layers import Ui_Widget
from DAVE.settings import DAVE_ANNOTATION_LAYERS
from DAVE.visual_helpers.qt_embedded_renderer import QtEmbeddedSceneRenderer


def get_color():
    # color picker
    color = QColorDialog.getColor()
    if color.isValid():
        return color.getRgb()[:3]


class LayersWidget(QWidget):
    def __init__(self, viewport: QtEmbeddedSceneRenderer):
        super().__init__()

        self.viewport = viewport

        self.ui = Ui_Widget()
        self.ui.setupUi(self)

        # Fill the values of the layers
        layers = viewport.layers

        if layers:
            layer: AnnotationLayer = layers[0]
        else:
            layer = AnnotationLayer(viewport.scene, scene_renderer=viewport)

        self.ui.fontSize.setValue(layer.font.size)

        self.ui.sbBorderWidth.setValue(layer.border_width)
        self.ui.pbBorderOpacity.setValue(layer.border_rgba[3])

        self.ui.pbBackgroundColor.setStyleSheet(
            f"background-color: rgba{layer.background_rgba}"
        )

        self.ui.padTop.setValue(layer.padding[0])
        self.ui.padRight.setValue(layer.padding[1])
        self.ui.padBottom.setValue(layer.padding[2])
        self.ui.padLeft.setValue(layer.padding[3])

        self.ui.sbBackgroundOpacity.setValue(layer.background_rgba[3])
        self.ui.pbBackgroundColor.setStyleSheet(
            f"background-color: rgba{layer.background_rgba}"
        )

        self.border_color = layer.border_rgba[:3]
        self.background_color = layer.background_rgba[:3]

        # fill the listbox with all available layers
        self.ui.layerList.clear()

        active_layer_classes = [layer.__class__ for layer in layers]

        for name in DAVE_ANNOTATION_LAYERS.keys():
            item = QListWidgetItem(name)
            if DAVE_ANNOTATION_LAYERS[name] in active_layer_classes:
                item.setCheckState(Qt.CheckState.Checked)
            else:
                item.setCheckState(Qt.CheckState.Unchecked)
            self.ui.layerList.addItem(item)

        # connect all except color signals to apply_changes
        self.ui.pbBackgroundColor.clicked.connect(self.apply_changes)
        self.ui.pbBorderColor.clicked.connect(self.apply_changes)

        self.ui.pbBorderOpacity.valueChanged.connect(self.apply_changes)
        self.ui.fontSize.valueChanged.connect(self.apply_changes)
        self.ui.sbBorderWidth.valueChanged.connect(self.apply_changes)
        self.ui.padTop.valueChanged.connect(self.apply_changes)
        self.ui.padRight.valueChanged.connect(self.apply_changes)
        self.ui.padBottom.valueChanged.connect(self.apply_changes)
        self.ui.padLeft.valueChanged.connect(self.apply_changes)
        self.ui.sbBackgroundOpacity.valueChanged.connect(self.apply_changes)
        self.ui.layerList.itemChanged.connect(self.apply_changes)

        self.ui.pbBackgroundColor.clicked.connect(self.get_background_color)
        self.ui.pbBorderColor.clicked.connect(self.get_border_color)

        rh = self.ui.layerList.sizeHintForRow(0)
        ht = min(rh * (1 + self.ui.layerList.count()), 800)
        self.ui.layerList.setFixedHeight(ht)

    def get_background_color(self):
        color = get_color()
        if color:
            self.ui.pbBackgroundColor.setStyleSheet(f"background-color: rgba{color}")
            self.background_color = color
            self.apply_changes()

    def get_border_color(self):
        color = get_color()
        if color:
            self.ui.pbBorderColor.setStyleSheet(f"background-color: rgb{color}")
            self.border_color = color
            self.apply_changes()

    def apply_changes(self):
        # remove all layers from the viewport
        self.viewport.layers.clear()

        DEFAULT_ANNOTATION_FONT.size = self.ui.fontSize.value()

        # add the layers that are checked
        for i in range(self.ui.layerList.count()):
            item = self.ui.layerList.item(i)
            if item.checkState() == Qt.CheckState.Checked:
                layer = DAVE_ANNOTATION_LAYERS[item.text()](
                    scene = self.viewport.scene,
                    scene_renderer=self.viewport,
                    do_not_update_yet=True,
                )

                layer.border_width = self.ui.sbBorderWidth.value()
                layer.padding = [
                    self.ui.padTop.value(),
                    self.ui.padRight.value(),
                    self.ui.padBottom.value(),
                    self.ui.padLeft.value(),
                ]

                layer.border_rgba = (
                    *self.border_color,
                    self.ui.pbBorderOpacity.value(),
                )
                layer.background_rgba = (
                    *self.background_color,
                    self.ui.sbBackgroundOpacity.value(),
                )

                self.viewport.layers.append(layer)
                layer.enforce_rerender_actors()
                layer.update()

        self.viewport.refresh_embeded_view()
