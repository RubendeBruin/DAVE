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

MINIMUM_REQUIRED_VERSION_PYO3D = 2.1

import os
import sys
from pathlib import Path

path = os.path.dirname(os.path.dirname(__file__))

version_file = Path(path) / "pyo3d.version"

try:
    with open(version_file, "r") as f:
        version = float(f.read())
except:
    version = 0


minor = sys.version_info.minor
filename = f"pyo3d.cp3{minor}-win_amd64.pyd"

target = path + "\\" + filename

if version < MINIMUM_REQUIRED_VERSION_PYO3D:
    if Path(target).exists():
        print(f"Outdated version of pyo3d found on system - removing : {target}")
        os.remove(target)

try:
    import pyo3d

    try:
        version = pyo3d.version()
        print(f"Equilibrium-core version = {version}")
        if version < MINIMUM_REQUIRED_VERSION_PYO3D:
            raise ValueError(
                f"The version of pyo3d found here: {pyo3d.__file__} does not meet the minimum version requirement {MINIMUM_REQUIRED_VERSION_PYO3D}.\n"
                "Advise to remove the beforementioned file and then restart DAVE to let it automatically download a more recent version"
            )

    except ValueError as e:
        raise e
    except:
        raise ModuleNotFoundError

except ValueError as v:
    raise v


except ImportError as err:

    # we did find a file, but were unable to import it. Why?
    if hasattr(err, "path"):
        print(f"Attempting to load:\n {err.path}\nfailed because:")
        print(err)
        print("If problems persist then removing this file from your system may help")

    print(
        "The required version of pyo3d is not found on your system. No problem, we can download and install it automatically for you, proceed?"
    )

    import urllib.request

    url = f"https://open-ocean.org/files/{filename}"

    from PySide2.QtWidgets import QApplication
    from PySide2.QtWidgets import QDialog
    from PySide2.QtWidgets import QDialogButtonBox, QVBoxLayout, QLabel

    app = QApplication()
    dlg = QDialog()
    QBtn = QDialogButtonBox.Ok | QDialogButtonBox.Cancel

    def accept():
        print(f"downloading {url} to {target}")
        urllib.request.urlretrieve(url, target)

        if not Path(target).exists():
            raise ValueError("Could not download")

        print(f"downloaded to {target}")

        # for local debugging

        dlg.close()

    def reject():
        exit(0)

    buttonBox = QDialogButtonBox(QBtn)
    buttonBox.accepted.connect(accept)
    buttonBox.rejected.connect(reject)

    layout = QVBoxLayout()
    label = QLabel(dlg)
    label.setText(
        f"Equilibrium core (pyo3d) was not found on your system.\nNo problem, we can download it automatically\n\nFile will be downloaded from:\n{url} \n\nand will be saved as:\n{target}"
    )
    layout.addWidget(label)

    link = QLabel(dlg)
    link.setText(
        '<a href="https://www.open-ocean.org/equilibrium-core/">More info: https://www.open-ocean.org/equilibrium-core/ </a>'
    )
    link.setOpenExternalLinks(True)
    layout.addWidget(link)

    layout.addWidget(buttonBox)
    dlg.setLayout(layout)
    dlg.exec_()

    import pyo3d

    version = pyo3d.version()

    with open(version_file, "w") as f:
        f.write(str(version))
