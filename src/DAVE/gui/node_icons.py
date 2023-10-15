from DAVE.settings_visuals import ICONS
import DAVE.nodes as dn
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication

import DAVE.gui.forms.resources_rc

if QApplication.instance() is None:
    app = QApplication()

ICONS[dn.Component] = QIcon(":/icons/component.png")
ICONS[dn.RigidBody] = QIcon(":/icons/cube.png")
ICONS[dn.Frame] = QIcon(":/icons/axis_blue.png")
ICONS[dn.Point] = QIcon(":/icons/point_blue.png")
ICONS[dn.Cable] = QIcon(":/icons/cable.png")
ICONS[dn.Visual] = QIcon(":/icons/visual.png")
ICONS[dn.LC6d] = QIcon(":/icons/lincon6.png")
ICONS[dn.Connector2d] = QIcon(":/icons/con2d.png")
ICONS[dn.Beam] = QIcon(":/icons/beam.png")
ICONS[dn.HydSpring] = QIcon(":/icons/linhyd.png")
ICONS[dn.Force] = QIcon(":/icons/force.png")
ICONS[dn.Circle] = QIcon(":/icons/circle_blue.png")
ICONS[dn.Buoyancy] = QIcon(":/icons/trimesh.png")
ICONS[dn.WaveInteraction1] = QIcon(":/icons/waveinteraction.png")
ICONS[dn.ContactBall] = QIcon(":/icons/contactball.png")
ICONS[dn.ContactMesh] = QIcon(":/icons/contactmesh.png")
ICONS[dn.GeometricContact] = QIcon(":/icons/pin_hole.png")
ICONS[dn.Sling] = QIcon(":/icons/sling.png")
ICONS[dn.Tank] = QIcon(":/icons/tank.png")
ICONS[dn.WindArea] = QIcon(":/icons/wind.png")
ICONS[dn.CurrentArea] = QIcon(":/icons/current.png")
ICONS[dn.SPMT] = QIcon(":/icons/spmt.png")
ICONS[dn.Shackle] = QIcon(":/icons/shackle.png")
