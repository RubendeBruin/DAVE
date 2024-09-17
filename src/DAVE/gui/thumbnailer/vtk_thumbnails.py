from vtkmodules.vtkIOGeometry import vtkOBJReader, vtkSTLReader
from vtkmodules.vtkIOImport import vtkGLTFImporter
from vtkmodules.vtkRenderingCore import vtkRenderer, vtkRenderWindow, vtkPolyDataMapper, vtkActor, vtkCamera, \
    vtkWindowToImageFilter
from vtkmodules.util.numpy_support import vtk_to_numpy
from PySide6.QtGui import QPixmap, QImage


def give_pixmap_from_3dfile(filename):
    try:
        # Create a reader based on the file extension
        if filename.endswith('.obj'):
            reader = vtkOBJReader()
        elif filename.endswith('.stl'):
            reader = vtkSTLReader()
        elif filename.endswith('.glb'):
            reader = vtkGLTFImporter()
        else:
            raise ValueError("Unsupported file format")

        reader.SetGlobalWarningDisplay(False)
        reader.SetFileName(filename)
        reader.Update()



        # Create a renderer, render window, and interactor
        renderer = vtkRenderer()
        render_window = vtkRenderWindow()
        render_window.AddRenderer(renderer)
        render_window.SetOffScreenRendering(1)  # Enable off-screen rendering

        if filename.endswith('.glb'):
            # Get the actors from the importer
            actors = reader.GetRenderer().GetActors()

            actors.InitTraversal()
            print(actors.GetNumberOfItems())

            R = []

            for i in range(actors.GetNumberOfItems()):
                renderer.AddActor(actors.GetNextActor())

        else:


            # Create a mapper and actor
            mapper = vtkPolyDataMapper()
            mapper.SetInputConnection(reader.GetOutputPort())

            actor = vtkActor()
            actor.SetMapper(mapper)

            renderer.AddActor(actor)
        renderer.SetBackground(1,1,1)  # Set the background color to white
        # Create and set up the camera
        camera = vtkCamera()
        camera.SetPosition(1, 1, 1)  # Position the camera
        camera.SetViewUp(0, 0, -1)  # Set the up direction
        camera.SetFocalPoint(0, 0, 0)  # Point the camera towards the origin
        renderer.SetActiveCamera(camera)
        renderer.ResetCamera()
        render_window.Render()

        # Capture the image
        window_to_image_filter = vtkWindowToImageFilter()
        window_to_image_filter.SetInput(render_window)
        window_to_image_filter.Update()

        vtk_image = window_to_image_filter.GetOutput()

        # Convert VTK image to QImage
        width, height, _ = vtk_image.GetDimensions()
        vtk_array = vtk_image.GetPointData().GetScalars()
        components = vtk_array.GetNumberOfComponents()
        arr = vtk_to_numpy(vtk_array).reshape(height, width, components)
        qimage = QImage(arr.data, width, height, QImage.Format_RGB888)

        # Convert QImage to QPixmap
        pixmap = QPixmap.fromImage(qimage)

        return pixmap

    except Exception as e:
        print(f"Error: {e}")
        return QPixmap()