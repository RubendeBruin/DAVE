"""
  This Source Code Form is subject to the terms of the Mozilla Public
  License, v. 2.0. If a copy of the MPL was not distributed with this
  file, You can obtain one at http://mozilla.org/MPL/2.0/.

  Ruben de Bruin - 2020

  File to open the Gui

"""
import DAVE.auto_download
from PySide2.QtWidgets import QSplashScreen, QApplication, QLabel
from PySide2.QtGui import QPixmap, QIcon

# create application
# note that the auto_download window may have already created one

if QApplication.instance() is not None:
    app = QApplication.instance()
else:
    app = QApplication()


# get the current folder
from pathlib import Path
here = Path(__file__).parent

splash = QSplashScreen(str(here / 'splash.png'))
label = QLabel(splash)
label.setText('Loading DAVE')
label.setStyleSheet("color: white")
label.move(10,10)

splash.show()
label.show()


import DAVE.gui.forms.resources_rc
app.setWindowIcon(QIcon('DAVE.ico'))

# Items that need to be available in the scripts
label.setText('Loading DAVE scenes and nodes')
label.show()

from DAVE.scene import *
from DAVE.marine import *
from DAVE.rigging import *
from DAVE.frequency_domain import *


# try:
#     # Include in try/except block if you're also targeting Mac/Linux
#     from PySide2.QtWinExtras import QtWin
#     myappid = 'mycompany.myproduct.subproduct.version'
#     QtWin.setCurrentProcessExplicitAppUserModelID(myappid)
# except ImportError:
#     pass

label.setText('Loading DAVE Gui')
label.show()

from DAVE.gui.main import Gui

label.setText('Loading numpy')
label.show()

import numpy as np

label.setText('Creating Gui')
label.show()


s = Scene()
g = Gui(s,splash=splash, app = app, client_mode=False)


