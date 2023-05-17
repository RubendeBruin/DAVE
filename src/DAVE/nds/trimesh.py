"""Trimesh is not a node but a data-source for a node.

It receives a reference to the scene,
TODO: would be more logical to have a reference to the node that is belongs to instead.
"""
import numpy as np

class TriMeshSource():  # not an instance of Node
    """
    TriMesh

    A TriMesh node contains triangular mesh which can be used for buoyancy or contact.

    The mesh is first scaled, then rotated and then offset

    """

    def __init__(self, scene, source):

        # name = scene.available_name_like("Names of trimesh-sources are not used")
        # super().__init__(scene, name=name, _do_not_add_to_scene=True)

        self._scene = scene

        # Note: TriMeshSource does not have a corresponding vfCore Node in the scene but does have a vfCore
        self._TriMesh = source
        self._new_mesh = True  # cheat for visuals

        self._path = ""  # stores the data that was used to load the obj
        self._offset = (0, 0, 0)
        self._scale = (1, 1, 1)
        self._rotation = (0, 0, 0)

        self._invert_normals = False

        self.boundary_edges = []
        self.non_manifold_edges = []

    def depends_on(self) -> list:
        return []

    @property
    def is_empty(self):
        return self._TriMesh.nVertices == 0

    def AddVertex(self, x, y, z):
        """Adds a vertex (point)"""
        self._TriMesh.AddVertex(x, y, z)

    def AddFace(self, i, j, k):
        """Adds a triangular face between vertex numbers i,j and k"""
        self._TriMesh.AddFace(i, j, k)

    def get_extends(self):
        """Returns the extends of the mesh in global coordinates

        Returns: (minimum_x, maximum_x, minimum_y, maximum_y, minimum_z, maximum_z)

        """

        t = self._TriMesh

        if t.nFaces == 0:
            return (0, 0, 0, 0, 0, 0)

        v = t.GetVertex(0)
        xn = v[0]
        xp = v[0]
        yn = v[1]
        yp = v[1]
        zn = v[2]
        zp = v[2]

        for i in range(t.nVertices):
            v = t.GetVertex(i)
            x = v[0]
            y = v[1]
            z = v[2]

            if x < xn:
                xn = x
            if x > xp:
                xp = x
            if y < yn:
                yn = y
            if y > yp:
                yp = y
            if z < zn:
                zn = z
            if z > zp:
                zp = z

        return (xn, xp, yn, yp, zn, zp)

    def _fromVTKpolydata(
        self, polydata, offset=None, rotation=None, scale=None, invert_normals=False
    ):

        import vtk

        tri = vtk.vtkTriangleFilter()

        tri.SetInputConnection(polydata)

        scaleFilter = vtk.vtkTransformPolyDataFilter()
        rotationFilter = vtk.vtkTransformPolyDataFilter()

        s = vtk.vtkTransform()
        s.Identity()
        r = vtk.vtkTransform()
        r.Identity()

        scaleFilter.SetInputConnection(tri.GetOutputPort())
        rotationFilter.SetInputConnection(scaleFilter.GetOutputPort())

        if scale is not None:
            s.Scale(*scale)

        if rotation is not None:
            q = rotation
            angle = (q[0] ** 2 + q[1] ** 2 + q[2] ** 2) ** (0.5)
            if angle > 0:
                r.RotateWXYZ(angle, q[0] / angle, q[1] / angle, q[2] / angle)

        if offset is None:
            offset = [0, 0, 0]

        scaleFilter.SetTransform(s)
        rotationFilter.SetTransform(r)

        clean = vtk.vtkCleanPolyData()
        clean.SetInputConnection(rotationFilter.GetOutputPort())

        clean.ConvertLinesToPointsOff()
        clean.ConvertPolysToLinesOff()
        clean.ConvertStripsToPolysOff()
        clean.PointMergingOn()
        clean.ToleranceIsAbsoluteOn()
        clean.SetAbsoluteTolerance(0.001)

        clean.Update()
        data = clean.GetOutput()

        self._TriMesh.Clear()

        for i in range(data.GetNumberOfPoints()):
            point = data.GetPoint(i)
            self._TriMesh.AddVertex(
                point[0] + offset[0], point[1] + offset[1], point[2] + offset[2]
            )

        for i in range(data.GetNumberOfCells()):
            cell = data.GetCell(i)

            if isinstance(cell, vtk.vtkLine):
                print("Cell nr {} is a line, not adding to mesh".format(i))
                continue

            if isinstance(cell, vtk.vtkVertex):
                print("Cell nr {} is a vertex, not adding to mesh".format(i))
                continue

            id0 = cell.GetPointId(0)
            id1 = cell.GetPointId(1)
            id2 = cell.GetPointId(2)

            if invert_normals:
                self._TriMesh.AddFace(id2, id1, id0)
            else:
                self._TriMesh.AddFace(id0, id1, id2)

        # check if anything was loaded
        if self._TriMesh.nFaces == 0:
            raise Exception(
                "No faces in poly-data - no geometry added (hint: empty obj file?)"
            )
        self._new_mesh = True
        self._scene.update()

    def check_shape(self):
        """Performs some checks on the shape in the trimesh
        - Boundary edges (edge with only one face attached)
        - Non-manifold edges (edit with more than two faces attached)
        - Volume should be positive
        """

        tm = self._TriMesh

        if tm.nFaces == 0:
            return ["No mesh"]

        # # make sure the mesh is clean: vertices should be unique
        # vertices = []
        # for i in range(tm.nVertices):
        #     vertex = np.array(tm.GetVertex(i))
        #     for v in vertices:
        #         if np.linalg.norm(vertex-v) < 0.001:
        #             print("Duplicate vertex" + str(vertex-v))
        #     else:
        #         vertices.append(vertex)

        # Make a list of all boundaries using their vertex IDs
        boundaries = np.zeros((3 * tm.nFaces, 2), dtype=int)
        for i in range(tm.nFaces):
            face = tm.GetFace(i)
            boundaries[3 * i] = [face[0], face[1]]
            boundaries[3 * i + 1] = [face[1], face[2]]
            boundaries[3 * i + 2] = [face[2], face[0]]

        # For an edge is doesn't matter in which direction it runs
        boundaries.sort(axis=1)

        # every boundary should be present twice

        values, rows_occurance_count = np.unique(
            boundaries, axis=0, return_counts=True
        )  # count of rows

        n_boundary = np.count_nonzero(rows_occurance_count == 1)
        n_nonmanifold = np.count_nonzero(rows_occurance_count > 2)

        messages = []

        boundary_edges = []
        non_manifold_edges = []

        if n_boundary > 0:
            messages.append(f"Mesh contains {n_boundary} boundary edges")

            i_boundary = np.argwhere(rows_occurance_count == 1)
            for i in i_boundary:
                edge = values[i][0]
                v1 = tm.GetVertex(edge[0])
                v2 = tm.GetVertex(edge[1])
                boundary_edges.append((v1, v2))

        if n_nonmanifold > 0:
            messages.append(f"Mesh contains {n_nonmanifold} non-manifold edges")
            i_boundary = np.argwhere(rows_occurance_count > 2)
            for i in i_boundary:
                edge = values[i][0]
                v1 = tm.GetVertex(edge[0])
                v2 = tm.GetVertex(edge[1])
                non_manifold_edges.append((v1, v2))

        if len(messages) == 2:
            messages.append("Boundary edges are shown in Red")
            messages.append("Non-manifold edges are shown in Pink")

        try:
            volume = tm.Volume()
        except:
            volume = 1  # no available in every DAVEcore yet

        if volume < 0:
            messages.append(
                f"Total mesh volume is negative ({volume:.2f} m3 of enclosed volume)."
            )
            messages.append("Hint: Use invert-normals")

        self.boundary_edges = boundary_edges
        self.non_manifold_edges = non_manifold_edges

        return messages

    def load_vtk_polydataSource(self, polydata):
        """Fills the triangle data from a vtk polydata such as a cubeSource.

        The vtk TriangleFilter is used to triangulate the source

        Examples:
            cube = vtk.vtkCubeSource()
            cube.SetXLength(122)
            cube.SetYLength(38)
            cube.SetZLength(10)
            trimesh.load_vtk_polydataSource(cube)
        """

        self._fromVTKpolydata(polydata.GetOutputPort())

    def load_obj(
        self, filename, offset=None, rotation=None, scale=None, invert_normals=False
    ):
        self.load_file(filename, offset, rotation, scale, invert_normals)

    def load_file(
        self, url, offset=None, rotation=None, scale=None, invert_normals=False
    ):
        """Loads an .obj or .stl file and and triangulates it.

        Order of modifications:

        1. rotate
        2. scale
        3. offset

        Args:
            url: (str or path or resource): file to load
            offset: : offset
            rotation:  : rotation
            scale:  scale

        """

        self._path = str(url)

        filename = str(self._scene.get_resource_path(url))

        import vtk

        ext = filename.lower()[-3:]
        if ext == "obj":
            obj = vtk.vtkOBJReader()
            obj.SetFileName(filename)
        elif ext == "stl":
            obj = vtk.vtkSTLReader()
            obj.SetFileName(filename)
        else:
            raise ValueError(
                f"File should be an .obj or .stl file but has extension {ext}"
            )

        # Add cleaning
        cln = vtk.vtkCleanPolyData()
        cln.SetInputConnection(obj.GetOutputPort())

        self._fromVTKpolydata(
            cln.GetOutputPort(),
            offset=offset,
            rotation=rotation,
            scale=scale,
            invert_normals=invert_normals,
        )

        self._scale = scale
        self._offset = offset
        self._rotation = rotation

        if self._scale is None:
            self._scale = (1.0, 1.0, 1.0)
        if self._offset is None:
            self._offset = (0.0, 0.0, 0.0)
        if self._rotation is None:
            self._rotation = (0.0, 0.0, 0.0)
        self._invert_normals = invert_normals

    def _load_from_privates(self):
        """(Re)Loads the mesh using the values currently stored in _scale, _offset, _rotation and _invert_normals"""
        self.load_file(
            url=self._path,
            scale=self._scale,
            offset=self._offset,
            rotation=self._rotation,
            invert_normals=self._invert_normals,
        )

    def give_python_code(self):
        code = "# No code generated for TriMeshSource"
        return code

