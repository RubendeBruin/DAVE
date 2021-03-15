"""
This module tries to import pyo3d. If it can not be imported, then it attempts to download is after the user
accepts it.

This module is imported by the Gui, so it only works when using the gui. It needs to because it uses a popup for
user notifications.

Only supported on windows
"""

"""
  This Source Code Form is subject to the terms of the Mozilla Public
  License, v. 2.0. If a copy of the MPL was not distributed with this
  file, You can obtain one at http://mozilla.org/MPL/2.0/.

  Ruben de Bruin - 2020
"""

try:
    import pyo3d

    try:
        version = pyo3d.version()
        print(f'Equilibrium-core version = {version}')
    except:
        raise ModuleNotFoundError

except ImportError as err:

    # we did find a file, but were unable to import it. Why?
    if hasattr(err, 'path'):
        print(f'Attempting to load:\n {err.path}\nfailed because:')
        print(err)
        print('If problems persist then removing this file from your system may help')


    print("The required version of pyo3d is not found on your system. No problem, we can download and install it automatically for you, proceed?")

    import os
    import sys
    path = os.path.dirname(os.path.dirname(__file__))

    import urllib.request

    # check python version

    minor = sys.version_info.minor

    if (minor == 7):
        url = 'https://open-ocean.org/files/pyo3d.pyd'
    else:
        url = f'https://open-ocean.org/files/pyo3d.cp3{minor}-win_amd64.pyd'

    target = path + '\\' + os.path.basename(url)

    from PySide2.QtWidgets import QApplication
    from PySide2.QtWidgets import QDialog
    from PySide2.QtWidgets import QDialogButtonBox, QVBoxLayout, QLabel

    app = QApplication()
    dlg = QDialog()
    QBtn = QDialogButtonBox.Ok | QDialogButtonBox.Cancel

    def accept():
        print('downloading')
        urllib.request.urlretrieve(url, target)
        print('done')
        dlg.close()

    def reject():
        exit(0)

    buttonBox = QDialogButtonBox(QBtn)
    buttonBox.accepted.connect(accept)
    buttonBox.rejected.connect(reject)

    layout = QVBoxLayout()
    label = QLabel(dlg)
    label.setText(f'Equilibrium core (pyo3d) was not found on your system.\nNo problem, we can download it automatically\n\nFile will be downloaded from:\n{url} \n\nand will be saved as:\n{target}')
    layout.addWidget(label)

    link = QLabel(dlg)
    link.setText('<a href="https://www.open-ocean.org/equilibrium-core/">More info: https://www.open-ocean.org/equilibrium-core/ </a>')
    link.setOpenExternalLinks(True)
    layout.addWidget(link)

    layout.addWidget(buttonBox)
    dlg.setLayout(layout)
    dlg.exec_()

    import pyo3d



