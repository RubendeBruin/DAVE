import numpy as np

from vtkmodules.vtkCommonCore import vtkFloatArray, vtkPoints
from vtkmodules.vtkCommonDataModel import vtkStructuredGrid, vtkPolyData, vtkCellArray
from vtkmodules.vtkFiltersGeometry import vtkStructuredGridGeometryFilter
from vtkmodules.vtkIOImage import vtkJPEGReader
from vtkmodules.vtkRenderingCore import vtkActor, vtkPolyDataMapper, vtkTexture

from DAVE.visual_helpers.constants import TEXTURE_WAVEPLANE


class WaveField:
    def __init__(self, texture=None):
        self.actor = None
        self.pts = None
        self.elevation = None

        self.texture = vtkTexture()
        input = vtkJPEGReader()

        if texture is None:
            input.SetFileName(TEXTURE_WAVEPLANE)
        else:
            input.SetFileName(texture)
        self.texture.SetInputConnection(input.GetOutputPort())

        self.texture.SetRepeat(True)
        self.texture.SetEdgeClamp(True)
        self.texture.Modified()

    @property
    def nt(self):
        if self.elevation is None:
            return 0
        else:
            _, _, nt = self.elevation.shape
            return nt

    def update(self, t):
        nx, ny, nt = self.elevation.shape
        i = int(t / self.dt) % nt

        for ix in range(nx):
            for iy in range(ny):
                count = ix + iy * nx

                x, y, _ = self.pts.GetPoint(count)
                self.pts.SetPoint(count, x, y, self.elevation[ix, iy, i])

        self.pts.Modified()

        pts = getattr(self, "line_pts", None)
        if pts is not None:
            for ix in range(nx):
                x, y, _ = pts.GetPoint(ix)
                pts.SetPoint(ix, x, y, self.elevation[ix, 0, i])
            pts.Modified()

    def make_grid(self, xmin, xmax, ymin, ymax, nx, ny, wave_direction):
        """Constructs the wave-grid and stores the result in
        self.xv and self.yv.

        wave-direction is the direction in which the waves progress. Mathematical angle in [deg]
        """

        # xfactor = np.linspace(-1,1, nx)
        # xg = dx * xfactor * np.sqrt(np.abs(xfactor))
        xg = np.linspace(xmin, xmax, nx)
        yg = np.linspace(ymin, ymax, ny)

        # create a grid in direction of wave-direction
        # xv, yv = np.meshgrid(xg, yg) # pre-allocate the grid
        yv, xv = np.meshgrid(yg, xg)  # pre-allocate the grid

        for iy in range(ny):
            for ix in range(nx):
                x = xg[ix]
                y = yg[iy]

                xr = (
                    np.cos(np.deg2rad(wave_direction)) * x
                    - np.sin(np.deg2rad(wave_direction)) * y
                )
                yr = (
                    np.sin(np.deg2rad(wave_direction)) * x
                    + np.cos(np.deg2rad(wave_direction)) * y
                )

                xv[ix, iy] = xr
                yv[ix, iy] = yr

        self.yv = yv
        self.xv = xv

    def create_waveplane(
        self,
        wave_direction,
        wave_amplitude,
        wave_length,
        wave_period,
        nt,
        nx,
        ny,
        dx,
        dy,
    ):
        # create the grid
        self.make_grid(-dx / 2, 1.5 * dx, -dy, dy, nx, 2, wave_direction)

        xv = self.xv  # alias
        yv = self.yv

        u = np.array(
            (np.cos(np.deg2rad(wave_direction)), np.sin(np.deg2rad(wave_direction)))
        )

        dist_phasor = np.exp(1j * (xv * u[0] + yv * u[1]) * (2 * np.pi / wave_length))

        t = np.linspace(0, wave_period, nt)
        time_phasor = np.exp(-1j * (2 * np.pi * t / wave_period))

        elevation = np.zeros((*xv.shape, nt))

        for i in range(nt):
            elevation[:, :, i] = wave_amplitude * np.real(time_phasor[i] * dist_phasor)

        # the vtk stuff
        self.elevation = elevation

        self.dt = wave_period / nt

        self.create_actor()
        self.create_line_actor()

    def create_line_actor(self):
        nx, ny, nt = self.elevation.shape

        # make grid
        pts = vtkPoints()
        for ix in range(nx):
            x = self.xv[ix, 0]
            y = self.yv[ix, 0]

            pts.InsertNextPoint(x, y, self.elevation[ix, 0, 0])  # use t=0 and y=y[0]

        segments = vtkCellArray()
        segments.InsertNextCell(nx)
        for i in range(nx):
            segments.InsertCellPoint(i)

        poly = vtkPolyData()
        poly.SetPoints(pts)
        poly.SetLines(segments)

        # make mapper
        mapper = vtkPolyDataMapper()
        mapper.SetInputData(poly)

        actor = vtkActor()
        actor.SetMapper(mapper)
        actor.GetProperty().SetColor(0.0, 0.0, 0.0)
        actor.GetProperty().SetLineWidth(2)

        self.line_actor = actor
        self.line_pts = pts

    def create_actor(self):
        ny, nx, nt = self.elevation.shape

        # make grid
        pts = vtkPoints()
        for ix in range(nx):
            for iy in range(ny):
                pts.InsertNextPoint(
                    self.xv[iy, ix], self.yv[iy, ix], self.elevation[iy, ix, 1]
                )

        grid = vtkStructuredGrid()
        grid.SetDimensions(ny, nx, 1)
        grid.SetPoints(pts)

        # make mapper
        filter = vtkStructuredGridGeometryFilter()
        filter.SetInputData(grid)

        # texture stuff
        TextureCooridinates = vtkFloatArray()
        TextureCooridinates.SetNumberOfComponents(2)
        TextureCooridinates.SetName("TextureCoordinates")

        tex_repeat = 4

        for i in range(0, nx):
            for j in range(0, ny):
                TextureCooridinates.InsertNextTuple2(
                    tex_repeat * i / (nx - 1), tex_repeat * j / (ny - 1)
                )

        grid.GetPointData().SetTCoords(TextureCooridinates)

        mapper = vtkPolyDataMapper()
        mapper.SetInputConnection(filter.GetOutputPort())

        actor = vtkActor()
        actor.SetMapper(mapper)
        #
        #
        # actor.GetProperty().SetColor(0.0, 0.5, 0.5)
        actor.GetProperty().SetOpacity(0.8)
        actor.GetProperty().SetAmbient(1.0)
        actor.GetProperty().SetDiffuse(0.0)
        actor.GetProperty().SetSpecular(0.0)
        actor.SetTexture(self.texture)

        self.actor = actor
        self.pts = pts
