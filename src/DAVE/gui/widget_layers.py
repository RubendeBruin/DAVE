import PIL.ImageFont
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QWidget, QListWidgetItem

from DAVE.annotations import AnnotationLayer
from DAVE.gui.forms.widget_viewport_layers import Ui_Widget
from DAVE.settings import DAVE_ANNOTATION_LAYERS
from DAVE.visual_helpers.qt_embedded_renderer import QtEmbeddedSceneRenderer


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
            self.ui.fontSize.setValue(layer.font.size)
            font = QFont(layer.font.getname()[0])
            self.ui.cbFont.setCurrentFont(font)
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

        self.ui.cbFont.currentFontChanged.connect(self.apply_changes)
        self.ui.pbBorderOpacity.valueChanged.connect(self.apply_changes)
        self.ui.fontSize.valueChanged.connect(self.apply_changes)
        self.ui.sbBorderWidth.valueChanged.connect(self.apply_changes)
        self.ui.padTop.valueChanged.connect(self.apply_changes)
        self.ui.padRight.valueChanged.connect(self.apply_changes)
        self.ui.padBottom.valueChanged.connect(self.apply_changes)
        self.ui.padLeft.valueChanged.connect(self.apply_changes)
        self.ui.sbBackgroundOpacity.valueChanged.connect(self.apply_changes)
        self.ui.layerList.itemChanged.connect(self.apply_changes)

    def apply_changes(self):
        # remove all layers from the viewport
        self.viewport.layers.clear()

        # add the layers that are checked
        for i in range(self.ui.layerList.count()):
            item = self.ui.layerList.item(i)
            if item.checkState() == Qt.CheckState.Checked:
                layer = DAVE_ANNOTATION_LAYERS[item.text()](
                    self.viewport.scene,
                    scene_renderer=self.viewport,
                    do_not_update_yet=True,
                )

                # set the properties

                # get the font-file from the font-name
                font: QFont = self.ui.cbFont.currentFont()

                font_name = self.ui.cbFont.currentFont().family()
                font_size = self.ui.fontSize.value()
                font_file = font_name.lower() + ".ttf"

                try:
                    print("Trying to load front from file: " + font_name + ".ttf")
                    layer.font = PIL.ImageFont.truetype(font_file, font_size)
                except:
                    print(
                        "Failed to load font from file: "
                        + font_name
                        + ".ttf, defaulting "
                    )
                    layer.font = PIL.ImageFont.truetype("bahnschrift.ttf", font_size)
                layer.border_width = self.ui.sbBorderWidth.value()
                layer.padding = [
                    self.ui.padTop.value(),
                    self.ui.padRight.value(),
                    self.ui.padBottom.value(),
                    self.ui.padLeft.value(),
                ]

                # layer.border_rgba[3] = self.ui.pbBorderOpacity.value()
                #
                # layer.background_rgba[3] = self.ui.sbBackgroundOpacity.value()

                self.viewport.layers.append(layer)
                layer.enforce_rerender_actors()
                layer.update()

        # self.viewport.renderer.render()

        self.viewport.refresh_embeded_view()
