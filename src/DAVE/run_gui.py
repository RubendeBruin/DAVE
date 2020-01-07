"""
  This Source Code Form is subject to the terms of the Mozilla Public
  License, v. 2.0. If a copy of the MPL was not distributed with this
  file, You can obtain one at http://mozilla.org/MPL/2.0/.

  Ruben de Bruin - 2020

  File to open the Gui

"""

import DAVE.gui.forms.resources_rc
from PySide2.QtWidgets import QSplashScreen, QApplication
from PySide2.QtGui import QPixmap

# Items that need to be available in the scripts
from DAVE.scene import *
from DAVE.marine import *
from DAVE.rigging import *

def run():
    app = QApplication()

    splash = QSplashScreen(QPixmap(":/icons/splashscreen.png"))
    splash.show()
    from DAVE.gui.main import Gui

    import numpy as np

    s = Scene()
    g = Gui(s,splash=splash, app = app)


if __name__ == '__main__':

    run()