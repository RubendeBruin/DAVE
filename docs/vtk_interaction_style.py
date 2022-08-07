
import vtk as vtk




"""
Create an interaction style using the Blender default key-bindings (with left-select that is).

Due to C++/Python implementation this requires re-implementing the interaction completely as the c++ methods
can not be overridden/overloaded in python.

Camera action code is largely a translation of https://github.com/Kitware/VTK/blob/master/Interaction/Style/vtkInteractorStyleTrackballCamera.cxx
Rubber band code    

Interaction:

Left buttton: select
Left buttton drag: rubber band select

Middle buttton: rotate
Middle buttton + shift : pan
Middle buttton + ctrl  : zoom

Mouse wheel : zoom

Right key: reserved for context-menu

LAPTOP MODE:






"""


class BlenderStyle(vtk.vtkInteractorStyleUser):
    def RightButtonPress(self, obj, event):
        self.mode = "R"

    def RightButtonRelease(self, obj, event):
        self.mode = None

    def MiddleButtonPress(self, obj, event):
        self.MiddleButtonDown = True

    def MiddleButtonRelease(self, obj, event):
        self.MiddleButtonDown = False

    def MouseWheelBackward(self, obj, event):
        self.MoveMouseWheel(-1)

    def MouseWheelForward(self, obj, event):
        self.MoveMouseWheel(1)

    def MouseMove(self, obj, event):

        interactor = self.GetInteractor()

        # Find the renderer that is active below the current mouse position
        x, y = interactor.GetEventPosition()
        self.FindPokedRenderer(
            x, y
        )  # sets the current renderer [this->SetCurrentRenderer(this->Interactor->FindPokedRenderer(x, y));]

        Shift = interactor.GetShiftKey()
        Ctrl = interactor.GetControlKey()
        Alt = interactor.GetAltKey()

        if self.MiddleButtonDown and not Shift and not Ctrl:
            self.Rotate()
        elif self.MiddleButtonDown and Shift and not Ctrl:
            self.Pan()
        elif self.MiddleButtonDown and Ctrl and not Shift:
            self.Zoom()  # Dolly
        elif self.LeftButtonDown:
            self.DrawRubberBand()

        self.InvokeEvent(vtk.vtkCommand.InteractionEvent, None)

    def MoveMouseWheel(self, direction):
        interactor = self.GetInteractor()

        # Find the renderer that is active below the current mouse position
        x, y = interactor.GetEventPosition()
        self.FindPokedRenderer(
            x, y
        )  # sets the current renderer [this->SetCurrentRenderer(this->Interactor->FindPokedRenderer(x, y));]

        CurrentRenderer = self.GetCurrentRenderer()

        if CurrentRenderer:
            # self.GrabFocus(self.EventCallbackCommand)  # TODO: grab and release focus; possible?
            self.StartDolly()
            factor = self.MotionFactor * 0.2 * self.MouseWheelMotionFactor
            self.Dolly(pow(1.1, direction*factor))
            self.EndDolly()
            # self.ReleaseFocus()

    def LeftButtonPress(self, obj, event):
        self.LeftButtonDown = True

        rwi = self.GetInteractor()
        self.start_x, self.start_y = rwi.GetEventPosition()

        self.InitializeScreenDrawing()


    def LeftButtonRelease(self, obj, event):
        self.LeftButtonDown = False
        rwi = self.GetInteractor()
        rwi.Render()

    def Zoom(self):
        rwi = self.GetInteractor()
        x, y = rwi.GetEventPosition()
        xp, yp = rwi.GetLastEventPosition()

        direction = y - yp
        self.MoveMouseWheel(direction/10)


    def Pan(self):

        CurrentRenderer = self.GetCurrentRenderer()

        if CurrentRenderer:

            rwi = self.GetInteractor()

            #   // Calculate the focal depth since we'll be using it a lot

            camera = CurrentRenderer.GetActiveCamera()
            viewFocus = camera.GetFocalPoint()

            focalDepth = viewFocus[2]

            newPickPoint = [0, 0, 0, 0]
            x, y = rwi.GetEventPosition()
            self.ComputeDisplayToWorld(CurrentRenderer, x, y, focalDepth, newPickPoint)

            #   // Has to recalc old mouse point since the viewport has moved,
            #   // so can't move it outside the loop

            oldPickPoint = [0, 0, 0, 0]
            xp, yp = rwi.GetLastEventPosition()
            self.ComputeDisplayToWorld(
                CurrentRenderer, xp, yp, focalDepth, oldPickPoint
            )
            #
            #   // Camera motion is reversed
            #
            motionVector = (
                oldPickPoint[0] - newPickPoint[0],
                oldPickPoint[1] - newPickPoint[1],
                oldPickPoint[2] - newPickPoint[2],
            )

            viewFocus = camera.GetFocalPoint()  # do we need to do this again? Already did this
            viewPoint = camera.GetPosition()

            camera.SetFocalPoint(motionVector[0] + viewFocus[0], motionVector[1] + viewFocus[1], motionVector[2] + viewFocus[2])
            camera.SetPosition(motionVector[0] + viewPoint[0], motionVector[1] + viewPoint[1], motionVector[2] + viewPoint[2])

            if rwi.GetLightFollowCamera():
                CurrentRenderer.UpdateLightsGeometryToFollowCamera()

            rwi.Render()

    def Rotate(self):

        CurrentRenderer = self.GetCurrentRenderer()

        if CurrentRenderer:

            rwi = self.GetInteractor()
            dx = rwi.GetEventPosition()[0] - rwi.GetLastEventPosition()[0]
            dy = rwi.GetEventPosition()[1] - rwi.GetLastEventPosition()[1]

            size = CurrentRenderer.GetRenderWindow().GetSize()
            delta_elevation = -20.0 / size[1]
            delta_azimuth = -20.0 / size[0]

            rxf = dx * delta_azimuth * self.MotionFactor
            ryf = dy * delta_elevation * self.MotionFactor

            camera = CurrentRenderer.GetActiveCamera()

            camera.Azimuth(rxf)
            camera.Elevation(ryf)
            camera.OrthogonalizeViewUp()

            if self.GetAutoAdjustCameraClippingRange():
                CurrentRenderer.ResetCameraClippingRange()

            if rwi.GetLightFollowCamera():
                CurrentRenderer.UpdateLightsGeometryToFollowCamera()

            rwi.Render()

    def Dolly(self, factor):
        CurrentRenderer = self.GetCurrentRenderer()

        if CurrentRenderer:
            camera = CurrentRenderer.GetActiveCamera()

            if camera.GetParallelProjection():
                camera.SetParallelScale(camera.GetParallelScale / factor)
            else:
                camera.Dolly(factor)
                if self.GetAutoAdjustCameraClippingRange():
                    CurrentRenderer.ResetCameraClippingRange()

            rwi = self.GetInteractor()
            if rwi.GetLightFollowCamera():
                CurrentRenderer.UpdateLightsGeometryToFollowCamera()

            rwi.Render()

    def InitializeScreenDrawing(self):
        # make an image of the currently rendered image

        rwi = self.GetInteractor()
        rwin = rwi.GetRenderWindow()

        size = rwin.GetSize()

        self.PixelArray.Initialize()
        self.PixelArray.SetNumberOfComponents(4)
        self.PixelArray.SetNumberOfTuples(size[0] * size[1])

        front = 1  # what does this do?
        rwin.GetRGBACharPixelData(0, 0, size[0] - 1, size[1] - 1, front, self.PixelArray)


    def DrawRubberBand(self):
        rwi = self.GetInteractor()
        rwin = rwi.GetRenderWindow()

        x, y = rwi.GetEventPosition()

        size = rwin.GetSize()

        tempPA = vtk.vtkUnsignedCharArray()
        tempPA.DeepCopy(self.PixelArray)

        x = min(x, size[0]-1)
        y = min(y, size[1]-1)

        x = max(x, 0)
        y = max(y, 0)

        # Modify the pixel array
        width = abs(x-self.start_x)
        height = abs(y-self.start_y)
        minx = min(x, self.start_x)
        miny = min(y, self.start_y)

        # draw top and bottom
        for i in range(width):

            c = round((10*i % 254)/254) * 254  # find some alternating color

            id = (miny * size[0]) + minx + i
            tempPA.SetTuple(id, (c,c,c,1))

            id = ((miny+height) * size[0]) + minx + i
            tempPA.SetTuple(id, (c, c, c, 1))

        # draw left and right
        for i in range(height):
            c = round((10 * i % 254) / 254) * 254  # find some alternating color

            id = ((miny + i) * size[0]) + minx
            tempPA.SetTuple(id, (c, c, c, 1))

            id = id + width
            tempPA.SetTuple(id, (c, c, c, 1))


        # and Copy back to the window
        rwin.SetRGBACharPixelData(0, 0, size[0] - 1, size[1] - 1, tempPA, 0)
        rwin.Frame()



        #   this->Interactor->GetRenderWindow()->SetRGBACharPixelData(
        #     0, 0, size[0] - 1, size[1] - 1, pixels, 0);
        #   this->Interactor->GetRenderWindow()->Frame();


        #
        #   vtkUnsignedCharArray* tmpPixelArray = vtkUnsignedCharArray::New();
        #   tmpPixelArray->DeepCopy(this->PixelArray);
        #   unsigned char* pixels = tmpPixelArray->GetPointer(0);
        #
        #   int min[2], max[2];
        #
        #   min[0] =
        #     this->StartPosition[0] <= this->EndPosition[0] ? this->StartPosition[0] : this->EndPosition[0];
        #   if (min[0] < 0)
        #   {
        #     min[0] = 0;
        #   }
        #   if (min[0] >= size[0])
        #   {
        #     min[0] = size[0] - 1;
        #   }
        #
        #   min[1] =
        #     this->StartPosition[1] <= this->EndPosition[1] ? this->StartPosition[1] : this->EndPosition[1];
        #   if (min[1] < 0)
        #   {
        #     min[1] = 0;
        #   }
        #   if (min[1] >= size[1])
        #   {
        #     min[1] = size[1] - 1;
        #   }
        #
        #   max[0] =
        #     this->EndPosition[0] > this->StartPosition[0] ? this->EndPosition[0] : this->StartPosition[0];
        #   if (max[0] < 0)
        #   {
        #     max[0] = 0;
        #   }
        #   if (max[0] >= size[0])
        #   {
        #     max[0] = size[0] - 1;
        #   }
        #
        #   max[1] =
        #     this->EndPosition[1] > this->StartPosition[1] ? this->EndPosition[1] : this->StartPosition[1];
        #   if (max[1] < 0)
        #   {
        #     max[1] = 0;
        #   }
        #   if (max[1] >= size[1])
        #   {
        #     max[1] = size[1] - 1;
        #   }
        #
        #   int i;
        #   for (i = min[0]; i <= max[0]; i++)
        #   {
        #     pixels[4 * (min[1] * size[0] + i)] = 255 ^ pixels[4 * (min[1] * size[0] + i)];
        #     pixels[4 * (min[1] * size[0] + i) + 1] = 255 ^ pixels[4 * (min[1] * size[0] + i) + 1];
        #     pixels[4 * (min[1] * size[0] + i) + 2] = 255 ^ pixels[4 * (min[1] * size[0] + i) + 2];
        #     pixels[4 * (max[1] * size[0] + i)] = 255 ^ pixels[4 * (max[1] * size[0] + i)];
        #     pixels[4 * (max[1] * size[0] + i) + 1] = 255 ^ pixels[4 * (max[1] * size[0] + i) + 1];
        #     pixels[4 * (max[1] * size[0] + i) + 2] = 255 ^ pixels[4 * (max[1] * size[0] + i) + 2];
        #   }
        #   for (i = min[1] + 1; i < max[1]; i++)
        #   {
        #     pixels[4 * (i * size[0] + min[0])] = 255 ^ pixels[4 * (i * size[0] + min[0])];
        #     pixels[4 * (i * size[0] + min[0]) + 1] = 255 ^ pixels[4 * (i * size[0] + min[0]) + 1];
        #     pixels[4 * (i * size[0] + min[0]) + 2] = 255 ^ pixels[4 * (i * size[0] + min[0]) + 2];
        #     pixels[4 * (i * size[0] + max[0])] = 255 ^ pixels[4 * (i * size[0] + max[0])];
        #     pixels[4 * (i * size[0] + max[0]) + 1] = 255 ^ pixels[4 * (i * size[0] + max[0]) + 1];
        #     pixels[4 * (i * size[0] + max[0]) + 2] = 255 ^ pixels[4 * (i * size[0] + max[0]) + 2];
        #   }
        #
        #   this->Interactor->GetRenderWindow()->SetRGBACharPixelData(
        #     0, 0, size[0] - 1, size[1] - 1, pixels, 0);
        #   this->Interactor->GetRenderWindow()->Frame();
        #
        #   tmpPixelArray->Delete();




    def __init__(self):

        self.mode = None
        self.MotionFactor = 10
        self.MouseWheelMotionFactor = 0.5

        self.start_x = 0  # start of a drag
        self.start_y = 0

        self.PixelArray = vtk.vtkUnsignedCharArray() # holds an image of the renderer output at the start of a drawing event

        self.LeftButtonDown = False
        self.MiddleButtonDown = False

        self.AddObserver(vtk.vtkCommand.RightButtonPressEvent, self.RightButtonPress)
        self.AddObserver(vtk.vtkCommand.RightButtonReleaseEvent, self.RightButtonRelease)
        self.AddObserver(vtk.vtkCommand.MiddleButtonPressEvent, self.MiddleButtonPress)
        self.AddObserver(vtk.vtkCommand.MiddleButtonReleaseEvent, self.MiddleButtonRelease )
        self.AddObserver(vtk.vtkCommand.MouseWheelForwardEvent, self.MouseWheelForward )
        self.AddObserver(vtk.vtkCommand.MouseWheelBackwardEvent, self.MouseWheelBackward )
        self.AddObserver(vtk.vtkCommand.LeftButtonPressEvent, self.LeftButtonPress)
        self.AddObserver(vtk.vtkCommand.LeftButtonReleaseEvent, self.LeftButtonRelease)
        self.AddObserver(vtk.vtkCommand.MouseMoveEvent, self.MouseMove)


if __name__ == '__main__':
    from PySide2.QtWidgets import QWidget, QApplication
    from vedo import Cube, Plotter
    from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor

    app = QApplication()
    widget = QWidget()
    widget.setFixedWidth(400)
    widget.setFixedHeight(400)

    vtkWidget = QVTKRenderWindowInteractor(widget)


    P = Plotter(qtWidget=vtkWidget)

    for i in range(10):
        for j in range(10):
            C = Cube(pos=(2*i-4.5, 2*j-4.5, 1), side=1, c="b4")
            P += C

    style = BlenderStyle()

    invoked_style = vtk.vtkInteractorStyleTrackballCamera()

    P.show(mode=-1)


    P.interactor.SetInteractorStyle(style)

    widget.show()
    app.exec_()

