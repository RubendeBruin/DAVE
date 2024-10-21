"""Nodes composed of basic nodes.

Sling
Shackle

"""

from os.path import dirname

from .geometry import Frame, Point, Circle
from .core import RigidBody
from .mixins import *


class Component(Frame, HasSubScene):
    """Components are frame-nodes containing a scene. The imported scene is referenced by a file-name. All impored nodes
    are placed in the components frame.
    """

    def __init__(self, scene, name):
        super().__init__(scene=scene, name=name)

        self._path = ""

        self._exposed = []
        """List of tuples containing the exposed properties (if any)"""

    def _import_scene_func(self, other_scene):
        self._scene.import_scene(
            other=other_scene,
            prefix=self.name + "/",
            container=self,
            settings=False,  # do not import environment and other settings
            do_reports=False,  # do not import reports
            do_timeline=False,
            inplace_scene_modification_ok=True,
        )

    def dissolve(self):
        """Unmanange all contained nodes, downcast self to Frame"""

        HasSubScene.dissolve(self)
        self.__class__ = Frame

    def give_python_code(self):
        code = []
        code.append("# code for {}".format(self.name))
        code.append("c = s.new_component(name='{}',".format(self.name))
        code.append("               path=r'{}',".format(self.path))
        if self.parent_for_export:
            code.append("           parent='{}',".format(self.parent_for_export.name))

        # position

        if self.fixed[0] or not self._scene._export_code_with_solved_function:
            code.append("           position=({:.6g},".format(self.position[0]))
        else:
            code.append("           position=(solved({:.6g}),".format(self.position[0]))
        if self.fixed[1] or not self._scene._export_code_with_solved_function:
            code.append("                     {:.6g},".format(self.position[1]))
        else:
            code.append("                     solved({:.6g}),".format(self.position[1]))
        if self.fixed[2] or not self._scene._export_code_with_solved_function:
            code.append("                     {:.6g}),".format(self.position[2]))
        else:
            code.append(
                "                     solved({:.6g})),".format(self.position[2])
            )

        # rotation

        if self.fixed[3] or not self._scene._export_code_with_solved_function:
            code.append("           rotation=({:.6g},".format(self.rotation[0]))
        else:
            code.append("           rotation=(solved({:.6g}),".format(self.rotation[0]))
        if self.fixed[4] or not self._scene._export_code_with_solved_function:
            code.append("                     {:.6g},".format(self.rotation[1]))
        else:
            code.append("                     solved({:.6g}),".format(self.rotation[1]))
        if self.fixed[5] or not self._scene._export_code_with_solved_function:
            code.append("                     {:.6g}),".format(self.rotation[2]))
        else:
            code.append(
                "                     solved({:.6g})),".format(self.rotation[2])
            )

        # fixeties
        code.append("           fixed =({}, {}, {}, {}, {}, {}) )".format(*self.fixed))

        code.append(self.add_footprint_python_code())

        # exposed properties (if any)
        for ep in self.exposed_properties:
            code.append(f"c.set_exposed('{ep}', {self.get_exposed(ep)})")

        return "\n".join(code)
