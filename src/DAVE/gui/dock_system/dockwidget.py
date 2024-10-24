from PySide6 import QtWidgets, QtCore
from enum import Enum

from PySide6.QtCore import QPoint
from PySide6.QtGui import QCursor
from PySide6.QtWidgets import QApplication

import PySide6QtAds

from DAVE.scene import *


class guiEventType(Enum):
    NOTHING = -1  # no changes, for example model saved
    FULL_UPDATE = 0  # unknown, better update everything
    SELECTED_NODE_MODIFIED = 1  # properties of the currently selected node changed
    MODEL_STRUCTURE_CHANGED = (
        2  # changes in global model structure, for example nodes added or removed
    )
    MODEL_STATE_CHANGED = 3  # only change in dofs
    SELECTION_CHANGED = 4  # a different node is selected
    VIEWER_SETTINGS_UPDATE = 5  # the display settings for the viewer changed
    ENVIRONMENT_CHANGED = (
        6  # one of the scene environment values changed (eg: g, wind_direction, ... )
    )
    TAGS_CHANGED = 7  # whenever a tag is added or removed
    MODEL_STEP_ACTIVATED = 8  # a change in time-step MAY mean
    #    - that the select node is modified,
    #    - model structure is changed
    #    - model state changed
    #    - environment changed
    NEW_NODE_ADDED = 9  # a new node is added to the model -- a selection changed event will typically be submitted as well
    UNLIMITED_ANIMATION_LENGTH_CHANGED = 10  # the animation is started
    ANIMATION_TIME_CHANGED = 11  # the animation time is changed
    WATCHES_CHANGED = 12  # Watches are added or removed


class guiDockWidget(PySide6QtAds.CDockWidget):
    def __init__(self, *args, name, parent, **kwargs):
        super().__init__(name, parent)  # no args *args, **kwargs)
        self.contents = QtWidgets.QWidget(self)
        self.setWidget(self.contents)
        self._active = False
        self.guiCreate()

        self.setMinimumSizeHintMode(
            PySide6QtAds.CDockWidget.MinimumSizeHintFromDockWidget
        )

        self.ui: QtWidgets.QWidget  # type hinting

        # These widgets are created by the main gui -> show_guiWidget. This function sets the following references

        self.gui = None
        """Will be set to a gui object"""

        self.guiRunCodeCallback = None
        """will be set to a function that runs python code with signature func(code, eventype).
        Func returns True if succes, false otherwise"""

        self.guiScene: Scene = None
        """will point to the singleton Scene object"""

        self.guiSelection = list()
        """will point to a list with selected nodes (Node-type)"""

        self.guiEmitEvent = None
        """will point to a function with signature func(event, sender), which emits to event to all widgets except sender"""

        self.guiSelectNode = None
        """will point to a function with signature func(node-name). Call this to select the node with this name"""

        self.guiPressSolveButton = None
        """function reference to the 'solve' button in the gui - call this to solve the current scene while giving the user the option to cancel and some eye-candy"""

    def closeEvent(self, event):  # overrides default
        super().closeEvent(event)  # parent call
        self._active = False
        # self.contents.deleteLater()

    def showEvent(self, event):
        super().showEvent(event)  # parent call
        self._active = True

        self.guiEvent(guiEventType.FULL_UPDATE)

        # self.contents.deleteLater()

    def guiEvent(self, event):
        if self._active:
            self.guiProcessEvent(event)

    def guiDefaultLocation(self):
        """Return the default location, or None for floating"""
        return PySide6QtAds.DockWidgetArea.LeftDockWidgetArea

    def guiCanShareLocation(self):
        """Return True if this widget can share a location with other widgets on the same side"""
        return True

    # ------- these should be overridden in the derived class -----------

    def guiProcessEvent(self, event):
        """Is fired when the widget is visible

        :param event:  guiEventType
        """
        print("{} event on {}".format(event, self.__class__))

    def guiCreate(self):
        """Is fired when created

        add gui widgets to self.contents
        """

        # Example code
        label = QtWidgets.QLabel(self.contents)
        label.setText("Override me in derived class")
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(label)
        self.contents.setLayout(layout)
