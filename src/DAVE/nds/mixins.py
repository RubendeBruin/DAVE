"""These are the mixin classes for DAVE nodes"""
from types import NoneType

from .abstracts import *
from .trimesh import TriMeshSource
from ..tools import *


class HasParent(DAVENodeBase, ABC):
    def __init__(self, scene, name):
        logging.info("HasParent.__init__")

        self._parent_for_code_export = True
        """True : use parent, 
        None : use None, 
        Node : use that Node
        Used to prevent circular references, see groups section in documentation"""

        super().__init__(scene=scene, name=name)

    @property
    def parent_for_export(self) -> Node or None:
        """Reference to node that to use as parent used during export (work-around for circular references in export of geometric-contact
        #NOGUI"""
        if self._parent_for_code_export == True:  # explicit check for True
            return self.parent
        else:
            return self._parent_for_code_export

    @property
    def parents(self) -> tuple:
        """Returns a tuple of all parents of this node"""
        r = []
        p = self.parent
        while p is not None:
            r.append(p)
            p = p.parent

        return tuple(r)

    @property
    @abstractmethod
    def parent(self) -> Node or None:
        """The node that this node is located on, if any [Node]"""
        pass

    @parent.setter
    @abstractmethod
    @node_setter_manageable
    @node_setter_observable
    def parent(self, var):
        pass

    @abstractmethod
    @node_setter_manageable
    def change_parent_to(self, new_parent):
        pass

    @node_setter_manageable
    def try_swap(self, old: "Node", new: "Node") -> bool:
        """Tries to swap the parent of this node from old to new.
        Returns True if successful, False otherwise.
        """
        succes = False
        if self.parent == old:
            try:
                self.change_parent_to(new)
                succes = True
            except:
                pass

        if succes:
            return True
        else:
            return super().try_swap(old, new)


class HasParentCore(HasParent):
    _valid_parent_types = (NoneType,)

    def __init__(self, scene, name):
        logging.info("HasParentCore.__init__")
        super().__init__(scene=scene, name=name)

    def depends_on(self):
        if self.parent_for_export is not None:
            return [self.parent_for_export]
        else:
            return []

    @property
    def parent(self) -> Node or None:
        """Determines the parent of the node if any.
        #NOGUI"""
        if self._vfNode.parent is None:
            return None
        else:
            return self._scene[self._vfNode.parent]

    @parent.setter
    @node_setter_manageable
    @node_setter_observable
    def parent(self, var):
        """Assigns a new parent. Keeps the local position and rotations the same

        See also: change_parent_to
        """
        new_parent = self._scene._node_from_node_or_str_or_None(var)

        assert isinstance(
            new_parent, self._valid_parent_types
        ), f"Invalid parent type when setting the parent of Node [{self.name}] to [{var.name if var else 'None'}], allowed types are {self._valid_parent_types}, got {type(new_parent)}"
        if new_parent is None:
            self._vfNode.parent = None
        else:
            self._vfNode.parent = new_parent._vfNode


class HasParentPure(HasParent):
    def __init__(self, scene, name):
        self._parent = None
        super().__init__(scene=scene, name=name)

    @property
    def parent(self) -> Node or None:
        """Determines the parent of the node if any.
        #NOGUI"""
        return self._parent

    @parent.setter
    @node_setter_manageable
    @node_setter_observable
    def parent(self, var):
        """Assigns a new parent. Keeps the local position and rotations the same

        See also: change_parent_to
        """
        self._parent = self._scene._node_from_node_or_str_or_None(var)


class HasFootprint(DAVENodeBase):
    def __init__(self, scene, name):
        logging.info("HasFootprint.__init__")
        assert isinstance(
            self, HasParentCore
        ), "Only Core nodes with a parent can have a footprint"
        super().__init__(scene=scene, name=name)

    @property
    def footprint(self) -> tuple:
        """Determines where on its parent the force of this node is applied.
        Tuple of tuples ((x1,y1,z1), (x2,y2,z2), .... (xn,yn,zn))"""
        r = []
        for i in range(self._vfNode.nFootprintVertices):
            r.append(self._vfNode.footprintVertexGet(i))
        return tuple(r)

    @footprint.setter
    @node_setter_manageable
    @node_setter_observable
    def footprint(self, value):
        """Sets the footprint vertices. Supply as an iterable with each element containing three floats"""
        for t in value:
            assert3f(t, "Each entry of value assigned to footprints ")

        self._vfNode.footprintVertexClearAll()
        for t in value:
            self._vfNode.footprintVertexAdd(*t)

    def add_footprint_python_code(self):
        if self.footprint:
            return f"\ns['{self.name}'].footprint = {str(self.footprint)}"
        else:
            return ""


class HasTrimesh(DAVENodeBase):
    def __init__(self, scene, name):
        logging.info("HasTrimesh.__init__")
        assert isinstance(
            self, HasParentCore
        ), "Only Core nodes with a parent can have a trimesh"

        self._trimesh = TriMeshSource(
            self._scene, source=self._vfNode.trimesh
        )  # the tri-mesh is wrapped in a custom object

        super().__init__(scene=scene, name=name)

    @property
    def trimesh(self) -> "TriMeshSource":
        """Reference to TriMeshSource object
        #NOGUI"""
        return self._trimesh

    @property
    def trimesh_is_empty(self) -> bool:
        """True if the trimesh is empty
        #NOGUI"""
        return self.trimesh.is_empty

    @node_setter_manageable
    def change_parent_to(self, new_parent):
        """See also Visual.change_parent_to"""

        from DAVE.nodes import Frame

        if not (isinstance(new_parent, Frame) or new_parent is None):
            raise ValueError(
                "Trimeshes can only be attached to a Frame (or derived) or None"
            )

        if self.trimesh_is_empty:
            self.parent = new_parent
            return

        # get current position and orientation
        if self.parent is not None:
            cur_position = self.parent.to_glob_position(self.trimesh._offset)
            cur_rotation = self.parent.to_glob_rotation(self.trimesh._rotation)
        else:
            cur_position = self.trimesh._offset
            cur_rotation = self.trimesh._rotation

        self.parent = new_parent

        if new_parent is None:
            new_offset = cur_position
            new_rotation = cur_rotation
        else:
            new_offset = new_parent.to_loc_position(cur_position)
            new_rotation = new_parent.to_loc_rotation(cur_rotation)

        self.trimesh.load_file(
            url=self.trimesh._path,
            offset=new_offset,
            rotation=new_rotation,
            scale=self.trimesh._scale,
            invert_normals=self.trimesh._invert_normals,
        )


class Manager(DAVENodeBase, ABC):
    """
    Notes:
        1. A manager shall manage the names of all nodes it creates - do this by implementing _on_name_changed()
    """

    def __init__(self, scene, name):
        logging.info("Manager.__init__")

        assert isinstance(
            self, (NodePurePython, NodeCoreConnected)
        ), "Manager is a mixin class and must be used togeher with NodePurePython or NodeCoreConnected"

        super().__init__(scene=scene, name=name)

    def helper_update_node_prefix(self, nodes, old_prefix, new_prefix):
        """Helper function to update the node names of the given nodes, management is claimed"""

        with ClaimManagement(self._scene, self):
            for node in nodes:
                if (
                    node.manager is None or node.manager == self
                ):  # only rename un-managed nodes or nodes managed by me - managed nodes will be renamed by their manager
                    if node.name.startswith(old_prefix):
                        node.name = node.name.replace(old_prefix, new_prefix)
                    else:
                        raise Exception(
                            f"Unexpected name when re-naming managed node '{node.name}' of node '{self.name}'. Expected name to start with {old_prefix}."
                        )

    @abstractmethod
    def delete(self):
        """Carefully remove the manager, reinstate situation as before.
        - Delete all the nodes it created.
        - Release management on all other nodes
        - Do not delete the manager itself
        """
        super().delete()

    @abstractmethod
    def creates(self, node: Node):
        """Returns True if node is created by this manager"""
        pass

    @abstractmethod
    def name(self):
        "Enforce that the name property is implemented in any derived class"
        pass

    def store_copy_of_limits(self):
        """Creates/updates a copy of the limits of all managed nodes and stores that in
        each node in a dict ._limits_by_manager.

        This is used to determine which limits need to be saved by the scene
        """

        for node in self.managed_nodes():
            node._limits_by_manager = node.limits.copy()

    def dissolve_some(self) -> tuple:
        """Managers can always be dissolved. Simply release management of all managed nodes"""

        work_done = False
        with ClaimManagement(self._scene, self):
            for d in self._scene.nodes_managed_by(self):
                work_done = True
                if self in d.observers:
                    d.observers.remove(self)
                d.manager = None

        if work_done:
            return True, "Unmanaged all managed nodes of {}".format(self.name)
        else:
            return False, "Nothing to unmanage"


class HasContainer(Manager):
    """Containers are nodes containing nodes. Nodes are stored in self._nodes"""

    def __init__(self, scene, name):
        logging.info("Container.__init__")
        super().__init__(scene=scene, name=name)
        self._nodes = []
        """Nodes contained in and managed by this node"""

        self._name_prefix = (
            name + "/"
        )  # prefix used for all nodes created by this container

    def _on_name_changed(self):
        super()._on_name_changed()

        old_prefix = self._name_prefix
        new_prefix = self.name + "/"
        self.helper_update_node_prefix(self._nodes, old_prefix, new_prefix)
        self._name_prefix = new_prefix

    def dissolve_some(self) -> tuple[bool, str]:
        # Un-manage all managed nodes

        """Note that not all created nodes are necessarily managed by this container.
        This container may have created a geometric contact between one or two of the created nodes.
        In that case the geometric contract will manage the nodes.
        """

        unmanaged = []

        if self._nodes:
            with ClaimManagement(self._scene, self):
                for node in self._scene.nodes_managed_by(self):
                    if node.manager == self:
                        node.manager = self.manager
                        if self in node.observers:
                            node.observers.remove(self)
                        unmanaged.append(node)

            for node in unmanaged:
                try:
                    self._nodes.remove(node)
                except Exception as M:
                    print(
                        f"Failed to remove node list of managed nodes of {self.name} because {str(M)}"
                    )

            if unmanaged:
                return (
                    True,
                    f"Managed nodes of {self.name} unmanaged",
                )  # No need to call other supers, work was done so good enough

        return super().dissolve_some()

    def dissolve(self):
        """Un-manage all managed nodes and then delete the container"""
        Manager.dissolve_some(self)
        self._nodes = tuple()  # clear the list, we're not managing anything anymore

    def delete(self):
        # remove all imported nodes
        self._scene._unmanage_and_delete(self._nodes)

    def creates(self, node: Node):
        return node in self._nodes


class HasSubScene(HasContainer):
    """A group of nodes (container) that can be loaded from a .DAVE file. Basically a component without a frame.
    The nodes can have "exposed" properties"""

    def __init__(self, scene, name):
        super().__init__(scene=scene, name=name)

        self._path = ""
        self._exposed = []
        """List of tuples containing the exposed properties (if any)"""

    def dissolve(self):
        return HasContainer.dissolve(self)

    @property
    def path(self) -> str:
        """Path of the model-file. For example res: padeye.dave"""
        return self._path

    @path.setter
    @node_setter_manageable
    def path(self, value):
        self.load_subscene(value)
        self._path = value

    @property
    def imported_nodes(self) -> tuple:
        """Returns a tuple of all nodes that were imported from the subscene, including recursively imported nodes from subscenes of subscenes"""
        nodes = []
        for node in self._nodes:
            nodes.append(node)
            if isinstance(node, HasSubScene):
                nodes.extend(node.imported_nodes)
        return tuple(nodes)

    def load_subscene(self, value):
        """Load the subscene into self._nodes"""
        from ..scene import Scene

        # first see if we can load
        filename = self._scene.get_resource_path(value)
        t = Scene(
            filename=filename,
            resource_provider=self._scene.resource_provider,
        )

        # then remove all existing nodes
        self.delete()

        # and re-import them
        old_scene_exposed = getattr(self._scene, "exposed", None)

        self._import_scene_func(other_scene=t)

        all_imported_nodes = t._nodes.copy()
        auto_created_nodes = t.get_implicitly_created_nodes()

        # Use the name of the nodes to created references to the imported nodes

        directly_created_nodes = [
            node for node in all_imported_nodes if node not in auto_created_nodes
        ]

        self._nodes.clear()
        self._nodes.extend([self._scene[node.name] for node in directly_created_nodes])

        # claim ownership of unmanaged nodes
        for node in self._nodes:
            # if node.manager is None:
            node._manager = self
            node._limits_by_manager = node.limits.copy()
            node._watches_by_manager = node.watches.copy()

        # Get exposed properties (if any)
        self._exposed = getattr(t, "exposed", [])

        # and restore the _scenes old exposed
        if old_scene_exposed is not None:
            self._scene.exposed = old_scene_exposed
        else:  # there was none, remove it if it is there now
            if hasattr(self._scene, "exposed"):
                del self._scene.exposed

        self._path = value

    def _import_scene_func(self, other_scene):
        self._scene.import_scene(
            other=other_scene,
            prefix=self.name + "/",
            containerize=False,
            settings=False,  # do not import environment and other settings
        )

    @property
    def exposed_properties(self) -> tuple:
        """Names of exposed properties"""
        return tuple([e[0] for e in self._exposed])

    def _get_exposed_node(self, name):
        """Returns the managed node with original name name"""
        full_name = self.name + "/" + name
        for node in self._nodes:
            if node.name == full_name:
                return node

        raise ValueError(f"No exposed node with name {name} in component {self.name}")

    def _get_exposed_property_data(self, name):
        for e in self._exposed:
            if e[0] == name:
                return e
        raise ValueError(f"No exposed property with name {name}")

    def get_exposed(self, name):
        """Returns the value of the exposed property"""
        e = self._get_exposed_property_data(name)
        node_name = e[1]
        prop_name = e[2]
        node = self._get_exposed_node(node_name)
        return getattr(node, prop_name)

    def get_exposed_type(self, name):
        """Returns the value of the exposed property"""
        e = self._get_exposed_property_data(name)
        node_name = e[1]
        prop_name = e[2]
        node = self._get_exposed_node(node_name)
        doc = self._scene.give_documentation(node, prop_name)
        return doc.property_type

    def set_exposed(self, name, value):
        e = self._get_exposed_property_data(name)
        node_name = e[1]
        prop_name = e[2]
        node = self._get_exposed_node(node_name)

        with ClaimManagement(self._scene, self):
            setattr(node, prop_name, value)
