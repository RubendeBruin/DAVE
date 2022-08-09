import logging
import vtk as vtk




"""
Create an interaction style using the Blender default key-bindings (with left-select that is).

Due to C++/Python implementation this requires re-implementing the interaction completely as the c++ methods
can not be overridden/overloaded in python.

Camera action code is largely a translation of https://github.com/Kitware/VTK/blob/master/Interaction/Style/vtkInteractorStyleTrackballCamera.cxx
Rubber band code    

Interaction:

Left buttton: select
Left buttton drag: rubber band select or line select, depends on the dragged distance 

Middle button: rotate
Middle button + shift : pan
Middle button + ctrl  : zoom
Middle button + alt   : zoom rubber band --> TODO : see https://gitlab.kitware.com/updega2/vtk/-/blob/d324b2e898b0da080edee76159c2f92e6f71abe2/Rendering/vtkInteractorStyleRubberBandZoom.cxx

Mouse wheel : zoom

Right key click: reserved for context-menu


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
            self.DrawDraggedSelection()


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
        self.end_x = self.start_x
        self.end_y = self.start_y

        self.InitializeScreenDrawing()



    def LeftButtonRelease(self, obj, event):
        self.LeftButtonDown = False

        if self.callbackSelect:
            props = self.PerformPickingOnSelection()

            for prop in props:
                prop.GetProperty().SetColor(0,254,254)
            if props:
                props[0].GetProperty().SetColor(254,254,0)

            self.callbackSelect(props)

        # remove the selection rubber band / line
        rwi = self.GetInteractor()
        rwi.Render()

    def PerformPickingOnSelection(self):
        """Preforms prop3d picking on the current dragged selection

        If the distance between the start and endpoints is less than the threshold
        then a SINGLE prop3d is picked along the line

        the selection area is drawn by the rubber band and is defined by
        self.start_x, self.start_y, self.end_x, self.end_y
        """

        # if self.selection_length() < self.selection_length_threshold:
        #
        #     logging.info('Picking along line')
        #
        #     picker = vtk.vtkPropPicker()
        #
        #     xs, ys = self.LineToPixels(self.start_x, self.end_x, self.start_y, self.end_y)
        #     current_renderer = self.GetCurrentRenderer()
        #
        #     # start picking in the middle of the line,
        #     # and work towards the endpoints
        #
        #     n = len(xs)
        #     hd = n // 2  # integer division
        #
        #     ii = []
        #     if 2*hd == n: # even
        #         ii.append(hd)
        #         for i in range(1,hd):
        #             ii.append(hd-i)
        #             ii.append(hd + i)
        #         ii.append(0)
        #
        #     else: # odd
        #         ii.append(hd)
        #         for i in range(1,hd+1):
        #             ii.append(hd-i)
        #             ii.append(hd + i)
        #
        #     for i in ii:
        #         logging.info(f'Picking index {i}')
        #         if picker.Pick(xs[i], ys[i], 0, current_renderer):
        #             return [picker.GetProp3D()]
        #
        #     logging.info('Picking along line done, did not find anything')
        #
        #     return []
        #
        # else:
        renderer = self.GetCurrentRenderer()

        # define a minimum area for picking (a bit of fuzzy picking)
        if self.start_x == self.end_x:
            self.start_x -=2
            self.end_x += 2
        if self.start_y == self.end_y:
            self.start_y -=2
            self.end_y += 2


        assemblyPath = renderer.PickProp(self.start_x, self.start_y, self.end_x, self.end_y)

        # re-pick in larger area if nothing is returned
        if not assemblyPath:
            logging.info('Did not find anything in this area, extending by 2px to all sides and picking again')
            self.start_x -= 2
            self.end_x += 2
            self.start_y -= 2
            self.end_y += 2
            assemblyPath = renderer.PickProp(self.start_x, self.start_y, self.end_x, self.end_y)

        # The nearest prop (by Z-value)
        if assemblyPath:
            logging.info(f'Renderer Pick returned {assemblyPath.GetNumberOfItems()} items in assembly-path')
            assert assemblyPath.GetNumberOfItems() == 1, "Wrong assumption on number of returned nodes when picking"
            nearest_prop = assemblyPath.GetItemAsObject(0).GetViewProp()

            # all props
            collection = renderer.GetPickResultProps()
            props = [collection.GetItemAsObject(i) for i in range(collection.GetNumberOfItems())]

            props.remove(nearest_prop)
            props.insert(0,nearest_prop)

            return props

        else:
            return []



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

            temp_out = [0,0,0]
            self.ComputeWorldToDisplay(CurrentRenderer,viewFocus[0], viewFocus[1], viewFocus[2], temp_out)
            focalDepth = temp_out[2]

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

            import numpy as np
            if np.linalg.norm(motionVector) > 10:
                logging('Unrealistic movement detected')

            logging.info(f'Moving by {motionVector}')

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

            #
            #  Automatic camera leveling
            #

            # Update

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

    def DrawDraggedSelection(self):
        rwi = self.GetInteractor()
        self.end_x, self.end_y = rwi.GetEventPosition()
        self.DrawRubberBand(self.start_x, self.end_x, self.start_y,self.end_y)


    # def selection_length(self):
    #     """Returns the distance between the two corners of the selection as dragged by the mouse while holding the left button"""
    #
    #     return ((self.start_x - self.end_x)**2 + (self.start_y-self.end_y)**2)**0.5

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


    def DrawRubberBand(self, x1,x2,y1,y2):
        rwi = self.GetInteractor()
        rwin = rwi.GetRenderWindow()

        size = rwin.GetSize()

        tempPA = vtk.vtkUnsignedCharArray()
        tempPA.DeepCopy(self.PixelArray)

        x2 = min(x2, size[0]-1)
        y2 = min(y2, size[1]-1)

        x2 = max(x2, 0)
        y2 = max(y2, 0)

        # Modify the pixel array
        width = abs(x2-x1)
        height = abs(y2-y1)
        minx = min(x2, x1)
        miny = min(y2, y1)

        # draw top and bottom
        for i in range(width):

            #c = round((10*i % 254)/254) * 254  # find some alternating color
            c = 0

            id = (miny * size[0]) + minx + i
            tempPA.SetTuple(id, (c,c,c,1))

            id = ((miny+height) * size[0]) + minx + i
            tempPA.SetTuple(id, (c, c, c, 1))

        # draw left and right
        for i in range(height):
            # c = round((10 * i % 254) / 254) * 254  # find some alternating color
            c = 0

            id = ((miny + i) * size[0]) + minx
            tempPA.SetTuple(id, (c, c, c, 1))

            id = id + width
            tempPA.SetTuple(id, (c, c, c, 1))


        # and Copy back to the window
        rwin.SetRGBACharPixelData(0, 0, size[0] - 1, size[1] - 1, tempPA, 0)
        rwin.Frame()

    def LineToPixels(self, x1,x2,y1,y2):
        """Returns the x and y values of the pixels on a line between x1,y1 and x2,y2.
        If start and end are identical then a single point is returned"""

        dx = x2 - x1
        dy = y2 - y1

        if dx==0 and dy==0:
            return [x1],[y1]

        if abs(dx) > abs(dy):
            dhdw = dy / dx
            r = range(0,dx,int(dx/abs(dx)))
            x = [x1 + i for i in r]
            y = [round(y1 + dhdw*i) for i in r]
        else:
            dwdh = dx / dy
            r = range(0,dy,int(dy/abs(dy)))
            y = [y1 + i for i in r]
            x = [round(x1 + i * dwdh) for i in r]

        return x,y

    def DrawLine(self, x1,x2,y1,y2):
        rwi = self.GetInteractor()
        rwin = rwi.GetRenderWindow()

        size = rwin.GetSize()

        tempPA = vtk.vtkUnsignedCharArray()
        tempPA.DeepCopy(self.PixelArray)

        xs,ys = self.LineToPixels(x1,x2,y1,y2)
        for x,y in zip(xs,ys):
            id = (y * size[0]) + x
            tempPA.SetTuple(id, (0,0,0, 1))

        # and Copy back to the window
        rwin.SetRGBACharPixelData(0, 0, size[0] - 1, size[1] - 1, tempPA, 0)
        rwin.Frame()

    def __init__(self):

        # Callbacks
        #
        # Callback can be assigned to functions
        #
        # callbackSelect is called whenever one or mode props are selected.
        # callback will be called with a list of props of which the first entry
        # is prop closest to the camera.
        self.callbackSelect = None

        # settings

        self.MotionFactor = 10
        self.MouseWheelMotionFactor = 0.5

        # internals

        self.start_x = 0  # start of a drag
        self.start_y = 0
        self.end_x = 0
        self.end_y = 0

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

    import vtkmodules.vtkInteractionStyle
    from vtkmodules.vtkCommonColor import vtkNamedColors
    from vtkmodules.vtkFiltersSources import vtkCubeSource, vtkLineSource
    from vtkmodules.vtkRenderingCore import (
        vtkActor,
        vtkPolyDataMapper,
        vtkRenderWindow,
        vtkRenderWindowInteractor,
        vtkRenderer
    )

    colors = vtkNamedColors()

    # Create a rendering window and renderer.
    ren = vtkRenderer()
    renWin = vtkRenderWindow()
    renWin.SetWindowName('Custom interactor style - Python')
    renWin.AddRenderer(ren)

    iren = vtkRenderWindowInteractor()
    iren.SetRenderWindow(renWin)

    # Create some cubes.
    for i in range(10):
        for j in range(10):

            cube = vtkCubeSource()
            cube.Update()

            # mapper
            cubeMapper = vtkPolyDataMapper()
            cubeMapper.SetInputData(cube.GetOutput())

            # Actor.
            cubeActor = vtkActor()
            cubeActor.SetMapper(cubeMapper)
            cubeActor.GetProperty().SetColor(colors.GetColor3d('Silver'))

            cubeActor.SetPosition(3*i, 3*j, 0)

            # Assign actor to the renderer.
            ren.AddActor(cubeActor)

    # And create some lines
    for i in range(10):
        for j in range(10):
            p0 = [0,0,30]
            p1 = [3*i,3*j,0]
            lineSource = vtkLineSource()
            lineSource.SetPoint1(p0)
            lineSource.SetPoint2(p1)
            mapper = vtkPolyDataMapper()
            mapper.SetInputConnection(lineSource.GetOutputPort())
            actor = vtkActor()
            actor.SetMapper(mapper)
            actor.GetProperty().SetLineWidth(2)
            actor.GetProperty().SetColor(colors.GetColor3d("Silver"))
            ren.AddActor(actor)




    ren.ResetCamera()
    ren.GetActiveCamera().Azimuth(30)
    ren.GetActiveCamera().Elevation(30)
    ren.ResetCameraClippingRange()
    ren.SetBackground(colors.GetColor3d('White'))

    # Enable user interface interactor.
    iren.Initialize()

    style = BlenderStyle()

    def onSelect(props): # callback when props are selected
        for prop in props:
            prop.GetProperty().SetColor(0.3,0.3,1)
        props[0].GetProperty().SetColor(1,0.5 , 0)  # color the nearest prop orange

    style.callbackSelect = onSelect

    iren.SetInteractorStyle(style)

    renWin.Render()

    logging.basicConfig(level=logging.DEBUG)
    iren.Start()




