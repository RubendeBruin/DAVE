

try:
    import pyo3dt
except ModuleNotFoundError:

    print("module pyo3d is not found on your system. No problem, we can download and install it automatically for you, proceed?")

    import os
    import sys
    path = os.path.dirname(os.path.dirname(__file__))

    import urllib.request

    # check python version

    minor = sys.version_info.minor

    if (minor == 7):
        url = 'https://open-ocean.org/files/pyo3d.pyd'
    if (minor == 8):
        url = 'https://open-ocean.org/files/pyo3d.cp38-win_amd64.pyd'


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



