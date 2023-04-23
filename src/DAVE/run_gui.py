"""
  This Source Code Form is subject to the terms of the Mozilla Public
  License, v. 2.0. If a copy of the MPL was not distributed with this
  file, You can obtain one at http://mozilla.org/MPL/2.0/.

  Ruben de Bruin - 2020

  File to open the Gui

"""
from PySide6.QtWidgets import QSplashScreen, QApplication, QLabel
from PySide6.QtGui import QPixmap, QIcon


if __name__ == '__main__':
    import logging
    from multiprocessing import freeze_support

    freeze_support()

    # create application
    # note that the auto_download window may have already created one


    if QApplication.instance() is not None:
        app = QApplication.instance()
    else:
        app = QApplication()


    # get the current folder
    from pathlib import Path
    here = Path(__file__).parent

    picture = QPixmap(str(here / 'splash.png'))
    splash = QSplashScreen(picture)
    label = QLabel(splash)
    label.setText('Starting DAVE')
    label.setStyleSheet("color: white")
    label.move(10,10)


    log = ['Starting DAVE']

    def update_log():
        label.setText('\n'.join(log))
        label.adjustSize()
        app.processEvents()

    splash.show()
    label.show()
    app.processEvents()

    log.append('Checking for DAVE-core')
    update_log()
    import DAVE.auto_download


    log[-1] = "DAVE-core: OK"
    update_log()


    import DAVE.gui.forms.resources_rc
    app.setWindowIcon(QIcon('DAVE.ico'))

    # Items that need to be available in the scripts
    log.append('Loading DAVE scenes and nodes')
    update_log()

    import DAVE.scene
    import DAVE.marine
    import DAVE.rigging
    import DAVE.frequency_domain

    log[-1] = 'Loading DAVE scenes and nodes: OK'
    log.append('Checking for modules')

    try:
        import DAVE_timeline.gui
        log.append('Timeline: OK')
    except:
        log.append('Timeline: not available')

    update_log()

    try:
        import DAVE_reporting.gui
        log.append('DAVE_reporting: OK')
    except:
        log.append('DAVE_reporting: not available')

    update_log()

    try:
        import DAVE_BaseExtensions.gui
        log.append('BaseExtensions: OK')
    except:
        log.append('BaseExtensions: not available')

    update_log()

    try:
        import DAVE_rigging.gui
        log.append('Rigging: OK')
    except:
        log.append('Rigging: not available')

    update_log()

    try:
        import DAVE_vessels.gui
        log.append('Vessels: OK')
    except:
        log.append('Vessels: not available')

    log.append('Dynamics: <beta>')
    log.append('Creating GUI')

    update_log()

    import netCDF4

    from DAVE.gui.main import Gui

    import numpy as np

    import sys
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    else:
        filename = None

    s = DAVE.Scene()
    g = Gui(s,splash=splash, app = app, client_mode=False, filename=filename)


