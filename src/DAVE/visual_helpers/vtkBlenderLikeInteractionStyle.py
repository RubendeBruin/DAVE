import logging
import warnings

import vtk
import numpy as np
from dataclasses import dataclass

from vtkmodules.vtkRenderingCore import (
    vtkActor2D,
    vtkTextMapper,
)
from vtkmodules.vtkCommonColor import vtkNamedColors

from vtkmodules.vtkInteractionStyle import vtkInteractorStyleUser

from vtkmodules.vtkCommonCore import vtkCommand, vtkUnsignedCharArray


"""
Create an interaction style using the Blender default key-bindings (with left-select that is).

Due to C++/Python implementation this requires re-implementing the interaction completely as the c++ methods
can not be overridden/overloaded in python.

Camera action code is largely a translation of https://github.com/Kitware/VTK/blob/master/Interaction/Style/vtkInteractorStyleTrackballCamera.cxx
Rubber band code : https://gitlab.kitware.com/updega2/vtk/-/blob/d324b2e898b0da080edee76159c2f92e6f71abe2/Rendering/vtkInteractorStyleRubberBandZoom.cxx

Interaction:


Left button: Sections
----------------------
Left button: select
Left button drag: rubber band select or line select, depends on the dragged distance 

Middle button: Navigation
--------------------------

Middle button: rotate
Middle button + shift : pan
Middle button + ctrl  : zoom

Middle button + alt : center view on picked point
   OR
Middle button + alt   : zoom rubber band --> TODO : see https://gitlab.kitware.com/updega2/vtk/-/blob/d324b2e898b0da080edee76159c2f92e6f71abe2/Rendering/vtkInteractorStyleRubberBandZoom.cxx

Mouse wheel : zoom

Right button : context
-----------------------
Right key click: reserved for context-menu


Keys
------

2 or 3 : toggle perspective view
a      : zoom all
x,y,z  : view direction (toggles positive and negative)
left/right arrows: rotate 45 deg clockwise/ccw about z-axis, snaps to nearest 45 deg
b      : box zoom
m      : mouse middle lock (toggles)
space  : same as middle mouse button
g      : grab (move actors)
enter  : accept drag
esc    : cancel drag
         call callbackEscape


LAPTOP MODE:
Use space or 'm' as replacement for middle button (m is sticky, space is not)

callbacks / overriding keys:

if callbackAnyKey is assigned then this function is called on every key press. If this function returns True
then further processing of events is stopped.  


Moving actors
--------------
Actors can be moved interactively by the user.
To support custom groups of actors to be moved as a whole the following system is implemented:

When 'g' is pressed (grab) then a DragInfo dataclass object is assigned to style to style.draginfo
DragInfo includes a list of all the actors that are being dragged. By default this is the selection, but
this may be altered.
Drag is accepted using enter, click, or g. Drag is cancelled by esc

events:

self.callbackStartDrag is called when initializing the drag. This is when to assign actors and other data to draginfo. 
self.callbackEndDrag is called when the drag is accepted.

Responding to other events
---------------------------

callbackCameraDirectionChanged : executed when camera has rotated but before re-rendering





"""

@dataclass
class DragInfo:
    """Data structure containing the data required to execute dragging a node"""

    # Scene related
    dragged_node = None            # Node

    # VTK related
    actors_dragging: list
    dragged_actors_original_positions: list # original VTK positions
    start_position_3d = np.array((0,0,0))  # start position of the cursor

    delta = np.array((0,0,0))

    def __init__(self):
        self.actors_dragging = []
        self.dragged_actors_original_positions = []



class BlenderStyle(vtkInteractorStyleUser):
    def RightButtonPress(self, obj, event):
        pass

    def RightButtonRelease(self, obj, event):
        pass

    def MiddleButtonPress(self, obj, event):
        self._middle_button_down = True

    def MiddleButtonRelease(self, obj, event):
        self._middle_button_down = False

        # perform middle button focus event if ALT is down
        if self.GetInteractor().GetAltKey():
            logging.info("Middle button released while ALT is down")

            # try to pick an object at the current mouse position
            rwi = self.GetInteractor()
            self.start_x, self.start_y = rwi.GetEventPosition()
            props = self.PerformPickingOnSelection()

            if props:
                self.FocusOn(props[0])

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

        MiddleButton = self._middle_button_down or self.middle_mouse_lock

        # start with the special modes
        if self._is_box_zooming:
            self.DrawDraggedSelection()
        elif MiddleButton and not Shift and not Ctrl and not Alt:
            self.Rotate()
        elif MiddleButton and Shift and not Ctrl and not Alt:
            self.Pan()
        elif MiddleButton and Ctrl and not Shift and not Alt:
            self.Zoom()  # Dolly
        elif self.draginfo is not None:
            self.ExecuteDrag()
        elif self._left_button_down and Ctrl and Shift:
            self.DrawMeasurement()
        elif self._left_button_down:
            self.DrawDraggedSelection()

        self.InvokeEvent(vtkCommand.InteractionEvent, None)

    def MoveMouseWheel(self, direction):
        interactor = self.GetInteractor()

        # Find the renderer that is active below the current mouse position
        x, y = interactor.GetEventPosition()
        self.FindPokedRenderer(
            x, y
        )  # sets the current renderer [this->SetCurrentRenderer(this->Interactor->FindPokedRenderer(x, y));]

        factor = self.mouse_motion_factor * 0.2 * self.mouse_wheel_motion_factor
        self.ZoomByStep(direction*factor)



    def ZoomByStep(self, step):
        CurrentRenderer = self.GetCurrentRenderer()

        if CurrentRenderer:
            self.StartDolly()
            self.Dolly(pow(1.1, step))
            self.EndDolly()


    def LeftButtonPress(self, obj, event):

        if self._is_box_zooming:
            return
        if self.draginfo:
            return

        self._left_button_down = True

        interactor = self.GetInteractor()
        Shift = interactor.GetShiftKey()
        Ctrl = interactor.GetControlKey()

        if Shift and Ctrl:
            if not self.GetCurrentRenderer().GetActiveCamera().GetParallelProjection():
                self.ToggleParallelProjection()

        rwi = self.GetInteractor()
        self.start_x, self.start_y = rwi.GetEventPosition()
        self.end_x = self.start_x
        self.end_y = self.start_y

        self.InitializeScreenDrawing()

    def LeftButtonRelease(self, obj, event):

        if self._is_box_zooming:
            self._is_box_zooming = False
            self.ZoomBox(self.start_x, self.start_y, self.end_x, self.end_y)
            return

        if self.draginfo:
            self.FinishDrag()
            return

        self._left_button_down = False

        interactor = self.GetInteractor()

        Shift = interactor.GetShiftKey()
        Ctrl = interactor.GetControlKey()
        Alt = interactor.GetAltKey()

        if Ctrl and Shift:
            pass # we were drawing the measurement

        else:
            if self.callbackSelect:
                props = self.PerformPickingOnSelection()

                if props:  # only call back if anything was selected
                    self.picked_props = tuple(props)
                    self.callbackSelect(props)

        # remove the selection rubber band / line
        self.DoRender()
        # rwi = self.GetInteractor()
        # rwi.Render()

    def KeyPress(self, obj, event):

        key = obj.GetKeySym()
        KEY = key.upper()

        # logging.info(f"Key Press: {key}")
        if self.callbackAnyKey:
            if self.callbackAnyKey(key):
                return


        if KEY == "M":
            self.middle_mouse_lock = not self.middle_mouse_lock
            self.UpdateMiddleMouseButtonLockActor()
        elif KEY == "G":
            if self.draginfo is not None:
                self.FinishDrag()
            else:
                if self.callbackStartDrag:
                    self.callbackStartDrag()
                else:
                    self.StartDrag() # internally calls end-drag if drag is already active
        elif KEY=="ESCAPE":
            if self.callbackEscapeKey:
                self.callbackEscapeKey()
            if self.draginfo is not None:
                self.CancelDrag()
        elif KEY=="DELETE":
            if self.callbackDeleteKey:
                self.callbackDeleteKey()
        elif KEY=="RETURN":
            if self.draginfo:
                self.FinishDrag()
        elif KEY == "SPACE":
            self.middle_mouse_lock = True
            # self.UpdateMiddleMouseButtonLockActor()
            # self.GrabFocus(vtkCommand.MouseMoveEvent, self)  # TODO: grab and release focus; possible from python?
        elif KEY == "B":
            self._is_box_zooming = True
            rwi = self.GetInteractor()
            self.start_x, self.start_y = rwi.GetEventPosition()
            self.end_x = self.start_x
            self.end_y = self.start_y
            self.InitializeScreenDrawing()
        elif KEY == "2" or KEY == "3":
            self.ToggleParallelProjection()

        elif KEY == "A":
            self.ZoomFit()
        elif KEY == "X":
            self.SetViewX()
        elif KEY == "Y":
            self.SetViewY()
        elif KEY == "Z":
            self.SetViewZ()
        elif KEY == "LEFT":
            self.RotateDiscreteStep(1)
        elif KEY == "RIGHT":
            self.RotateDiscreteStep(-1)
        elif KEY == "UP":
            self.RotateTurtableBy(0,10)
        elif KEY == "DOWN":
            self.RotateTurtableBy(0,-10)
        elif KEY == "PLUS":
            self.ZoomByStep(2)
        elif KEY == "MINUS":
            self.ZoomByStep(-2)
        elif KEY == "F":
            if self.callbackFocusKey:
                self.callbackFocusKey()

        self.InvokeEvent(vtkCommand.InteractionEvent, None)

    def KeyRelease(self, obj, event):

        key = obj.GetKeySym()
        KEY = key.upper()

        logging.info(f"Key release: {key}")

        if KEY == "SPACE":
            if self.middle_mouse_lock:
                self.middle_mouse_lock = False
                self.UpdateMiddleMouseButtonLockActor()

    def WindowResized(self):
        logging.info("window resized")
        self.InitializeScreenDrawing()

    def RotateDiscreteStep(self, movement_direction, step=22.5):
        """Rotates CW or CCW to the nearest 45 deg angle - includes some fuzzyness to determine about which axis"""

        CurrentRenderer = self.GetCurrentRenderer()
        camera = CurrentRenderer.GetActiveCamera()

        step = np.deg2rad(step)

        direction = -np.array(camera.GetViewPlaneNormal())  # current camera direction

        if (
            abs(direction[2]) < 0.7
        ):  # horizontal view, rotate camera position about Z-axis
            angle = np.arctan2(direction[1], direction[0])

            # find the nearest angle that is an integer number of steps
            if movement_direction > 0:
                angle = step * np.floor((angle + 0.1 * step) / step) + step
            else:
                angle = -step * np.floor(-(angle - 0.1 * step) / step) - step

            dist = np.linalg.norm(direction[:2])

            direction[0] = np.cos(angle) * dist
            direction[1] = np.sin(angle) * dist

            self.SetCameraDirection(direction)

        else:  # Top or bottom like view - rotate camera "up" direction

            up = np.array(camera.GetViewUp())

            angle = np.arctan2(up[1], up[0])

            # find the nearest angle that is an integer number of steps
            if movement_direction > 0:
                angle = step * np.floor((angle + 0.1 * step) / step) + step
            else:
                angle = -step * np.floor(-(angle - 0.1 * step) / step) - step

            dist = np.linalg.norm(up[:2])

            up[0] = np.cos(angle) * dist
            up[1] = np.sin(angle) * dist


            camera.SetViewUp(up)
            camera.OrthogonalizeViewUp()

            self.DoRender()


    def ToggleParallelProjection(self):
        renderer = self.GetCurrentRenderer()
        camera = renderer.GetActiveCamera()
        camera.SetParallelProjection(not bool(camera.GetParallelProjection()))
        # self.GetInteractor().Render()
        self.DoRender()

    def SetViewX(self):
        self.SetCameraPlaneDirection((1, 0, 0))

    def SetViewY(self):
        self.SetCameraPlaneDirection((0, 1, 0))

    def SetViewZ(self):
        self.SetCameraPlaneDirection((0, 0, 1))

    def ZoomFit(self):
        self.GetCurrentRenderer().ResetCamera()
        self.DoRender()

    def SetCameraPlaneDirection(self, direction):
        """Sets the camera to display a plane of which direction is the normal - includes logic to reverse the direction if benificial"""

        CurrentRenderer = self.GetCurrentRenderer()
        camera = CurrentRenderer.GetActiveCamera()

        direction = np.array(direction)

        normal = camera.GetViewPlaneNormal()
        # can not set the normal, need to change the position to do that

        current_alignment = np.dot(normal, -direction)
        logging.info(f"Current alignment = {current_alignment}")

        if abs(current_alignment) > 0.9999:
            logging.info("toggling")
            direction = -np.array(normal)
        elif current_alignment > 0:  # find the nearest plane
            logging.info("reversing to find nearest")
            direction = -direction

        self.SetCameraDirection(-direction)

    def SetCameraDirection(self, direction):
        """Sets the camera to this direction, sets view up if horizontal enough"""
        direction = np.array(direction)

        CurrentRenderer = self.GetCurrentRenderer()
        camera = CurrentRenderer.GetActiveCamera()
        rwi = self.GetInteractor()

        pos = np.array(camera.GetPosition())
        focal = np.array(camera.GetFocalPoint())
        dist = np.linalg.norm(pos - focal)

        pos = focal - dist * direction
        camera.SetPosition(pos)

        if abs(direction[2]) < 0.9:
            camera.SetViewUp(0, 0, 1)
        elif direction[2] > 0.9:
            camera.SetViewUp(0,-1,0)
        else:
            camera.SetViewUp(0, 1, 0)

        camera.OrthogonalizeViewUp()

        if self.GetAutoAdjustCameraClippingRange():
            CurrentRenderer.ResetCameraClippingRange()

        if rwi.GetLightFollowCamera():
            CurrentRenderer.UpdateLightsGeometryToFollowCamera()

        if self.callbackCameraDirectionChanged:
            self.callbackCameraDirectionChanged()

        self.DoRender()

    def PerformPickingOnSelection(self):
        """Preforms prop3d picking on the current dragged selection

        If the distance between the start and endpoints is less than the threshold
        then a SINGLE prop3d is picked along the line

        the selection area is drawn by the rubber band and is defined by
        self.start_x, self.start_y, self.end_x, self.end_y
        """

        renderer = self.GetCurrentRenderer()

        assemblyPath = renderer.PickProp(
            self.start_x, self.start_y, self.end_x, self.end_y
        )

        # re-pick in larger area if nothing is returned
        if not assemblyPath:
            logging.info(
                "Did not find anything in this area, extending by 2px to all sides and picking again"
            )
            self.start_x -= 2
            self.end_x += 2
            self.start_y -= 2
            self.end_y += 2
            assemblyPath = renderer.PickProp(
                self.start_x, self.start_y, self.end_x, self.end_y
            )

        # The nearest prop (by Z-value)
        if assemblyPath:
            logging.info(
                f"Renderer Pick returned {assemblyPath.GetNumberOfItems()} items in assembly-path"
            )
            assert (
                assemblyPath.GetNumberOfItems() == 1
            ), "Wrong assumption on number of returned nodes when picking"
            nearest_prop = assemblyPath.GetItemAsObject(0).GetViewProp()

            # all props
            collection = renderer.GetPickResultProps()
            props = [
                collection.GetItemAsObject(i)
                for i in range(collection.GetNumberOfItems())
            ]

            props.remove(nearest_prop)
            props.insert(0, nearest_prop)

            return props

        else:
            return []


    # ----------- actor dragging ------------

    def StartDrag(self):
        if self.callbackStartDrag:
            logging.info("Calling callbackStartDrag")
            self.callbackStartDrag()
            return
        else:  # grab the current selection
            if self.picked_props:
                self.StartDragOnProps(self.picked_props)
            else:
                logging.info('Can not start drag, nothing selected and callbackStartDrag not assigned')

    def FinishDrag(self):
        logging.info('Finished drag')
        if self.callbackEndDrag:
            # reset actor positions as actors positions will be controlled by called functions
            for pos0, actor in zip(self.draginfo.dragged_actors_original_positions, self.draginfo.actors_dragging):
                actor.SetPosition(pos0)
            self.callbackEndDrag(self.draginfo)

        self.draginfo = None

    def StartDragOnProps(self, props):
        """Starts drag on the provided props (actors) by filling self.draginfo"""
        if self.draginfo is not None:
            self.FinishDrag()
            return

        logging.info('Starting drag')

        # create and fill drag-info
        draginfo = DragInfo()

        #
        # draginfo.dragged_node = node
        #
        # # find all actors and outlines corresponding to this node
        # actors = [*self.actor_from_node(node).actors.values()]
        # outlines = [ol.outline_actor for ol in self.node_outlines if ol.parent_vp_actor in actors]

        draginfo.actors_dragging = props # [*actors, *outlines]

        for a in draginfo.actors_dragging:
            draginfo.dragged_actors_original_positions.append(a.GetPosition())  # numpy ndarray

        # Get the start position of the drag in 3d

        rwi = self.GetInteractor()
        CurrentRenderer = self.GetCurrentRenderer()
        camera = CurrentRenderer.GetActiveCamera()
        viewFocus = camera.GetFocalPoint()

        temp_out = [0, 0, 0]
        self.ComputeWorldToDisplay(
            CurrentRenderer, viewFocus[0], viewFocus[1], viewFocus[2], temp_out
        )
        focalDepth = temp_out[2]

        newPickPoint = [0, 0, 0, 0]
        x, y = rwi.GetEventPosition()
        self.ComputeDisplayToWorld(CurrentRenderer, x, y, focalDepth, newPickPoint)

        mouse_pos_3d = np.array(newPickPoint[:3])

        draginfo.start_position_3d = mouse_pos_3d


        self.draginfo = draginfo

    def ExecuteDrag(self):

        rwi =  self.GetInteractor()
        CurrentRenderer = self.GetCurrentRenderer()


        camera = CurrentRenderer.GetActiveCamera()
        viewFocus = camera.GetFocalPoint()

        # Get the picked point in 3d

        temp_out = [0, 0, 0]
        self.ComputeWorldToDisplay(
            CurrentRenderer, viewFocus[0], viewFocus[1], viewFocus[2], temp_out
        )
        focalDepth = temp_out[2]

        newPickPoint = [0, 0, 0, 0]
        x, y = rwi.GetEventPosition()
        self.ComputeDisplayToWorld(CurrentRenderer, x, y, focalDepth, newPickPoint)

        mouse_pos_3d = np.array(newPickPoint[:3])

        # compute the delta and execute

        delta = np.array(mouse_pos_3d) - self.draginfo.start_position_3d
        logging.info(f'Delta = {delta}')
        view_normal = np.array(self.GetCurrentRenderer().GetActiveCamera().GetViewPlaneNormal())

        delta_inplane = delta - view_normal * np.dot(delta, view_normal)
        logging.info(f'delta_inplane = {delta_inplane}')

        for pos0, actor in zip(self.draginfo.dragged_actors_original_positions, self.draginfo.actors_dragging):
            m = actor.GetUserMatrix()
            if m:
                warnings.warn('UserMatrices/transforms not supported')
                # m.Invert() #inplace
                # rotated = m.MultiplyFloatPoint([*delta_inplane, 1])
                # actor.SetPosition(pos0 + np.array(rotated[:3]))
            actor.SetPosition(pos0 + delta_inplane)

        logging.info(f'Set position to {pos0 + delta_inplane}')

        self.draginfo.delta = delta_inplane  # store the current delta

        # self.GetInteractor().Render()
        self.DoRender()

    def CancelDrag(self):
        """Cancels the drag and restored the original positions of all dragged actors"""
        for pos0, actor in zip(self.draginfo.dragged_actors_original_positions, self.draginfo.actors_dragging):
            actor.SetPosition(pos0)
        self.draginfo = None
        self.DoRender()

    # ----------- end dragging --------------

    def Zoom(self):
        rwi = self.GetInteractor()
        x, y = rwi.GetEventPosition()
        xp, yp = rwi.GetLastEventPosition()

        direction = y - yp
        self.MoveMouseWheel(direction / 10)

    def Pan(self):

        CurrentRenderer = self.GetCurrentRenderer()

        if CurrentRenderer:

            rwi = self.GetInteractor()

            #   // Calculate the focal depth since we'll be using it a lot
            camera = CurrentRenderer.GetActiveCamera()
            viewFocus = camera.GetFocalPoint()

            temp_out = [0, 0, 0]
            self.ComputeWorldToDisplay(
                CurrentRenderer, viewFocus[0], viewFocus[1], viewFocus[2], temp_out
            )
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

            viewFocus = (
                camera.GetFocalPoint()
            )  # do we need to do this again? Already did this
            viewPoint = camera.GetPosition()

            camera.SetFocalPoint(
                motionVector[0] + viewFocus[0],
                motionVector[1] + viewFocus[1],
                motionVector[2] + viewFocus[2],
            )
            camera.SetPosition(
                motionVector[0] + viewPoint[0],
                motionVector[1] + viewPoint[1],
                motionVector[2] + viewPoint[2],
            )

            if rwi.GetLightFollowCamera():
                CurrentRenderer.UpdateLightsGeometryToFollowCamera()

            # rwi.Render()
            self.DoRender()

    def Rotate(self):

        CurrentRenderer = self.GetCurrentRenderer()

        if CurrentRenderer:

            rwi = self.GetInteractor()
            dx = rwi.GetEventPosition()[0] - rwi.GetLastEventPosition()[0]
            dy = rwi.GetEventPosition()[1] - rwi.GetLastEventPosition()[1]

            size = CurrentRenderer.GetRenderWindow().GetSize()
            delta_elevation = -20.0 / size[1]
            delta_azimuth = -20.0 / size[0]

            rxf = dx * delta_azimuth * self.mouse_motion_factor
            ryf = dy * delta_elevation * self.mouse_motion_factor

            self.RotateTurtableBy(rxf, ryf)

    def RotateTurtableBy(self, rxf, ryf):

        CurrentRenderer = self.GetCurrentRenderer()
        rwi = self.GetInteractor()

        # rfx is rotation about the global Z vector (turn-table mode)
        # rfy is rotation about the side vector

        camera = CurrentRenderer.GetActiveCamera()
        campos = np.array(camera.GetPosition())
        focal = np.array(camera.GetFocalPoint())
        up = camera.GetViewUp()
        upside_down_factor = -1 if up[2]<0 else 1

        # rotate about focal point

        P = campos - focal  # camera position

        # Rotate left/right about the global Z axis
        H = np.linalg.norm(P[:2])     # horizontal distance of camera to focal point
        elev = np.arctan2(P[2], H)    # elevation

        # if the camera is near the poles, then derive the azimuth from the up-vector
        sin_elev = np.sin(elev)
        if abs(sin_elev) < 0.8:
            azi = np.arctan2(P[1], P[0])  # azimuth from camera position
        else:
            if sin_elev < -0.8:
                azi = np.arctan2(upside_down_factor*up[1], upside_down_factor*up[0])
            else:
                azi = np.arctan2(-upside_down_factor*up[1], -upside_down_factor*up[0])

        D = np.linalg.norm(P)         # distance from focal point to camera

        # apply the change in azimuth and elevation
        azi_new = azi + rxf / 60

        elev_new = elev + upside_down_factor * ryf / 60

        # the changed elevation changes H (D stays the same)
        Hnew = D*np.cos(elev_new)


        # calculate new camera position relative to focal point
        Pnew = np.array((Hnew*np.cos(azi_new),
                         Hnew*np.sin(azi_new),
                         D*np.sin(elev_new)))



        # calculate the up-direction of the camera
        up_z = upside_down_factor * np.cos(elev_new)  # z follows directly from elevation
        up_h = upside_down_factor * np.sin(elev_new)  # horizontal component
        #
        # if upside_down:
        #     up_z = -up_z
        #     up_h = -up_h


        up = (-up_h * np.cos(azi_new),
              -up_h * np.sin(azi_new),
              up_z)

        new_pos = focal + Pnew

        camera.SetViewUp(up)
        camera.SetPosition(new_pos)

        camera.OrthogonalizeViewUp()

        # Update

        if self.GetAutoAdjustCameraClippingRange():
            CurrentRenderer.ResetCameraClippingRange()

        if rwi.GetLightFollowCamera():
            CurrentRenderer.UpdateLightsGeometryToFollowCamera()

        if self.callbackCameraDirectionChanged:
            self.callbackCameraDirectionChanged()

        self.DoRender()


    def ZoomBox(self, x1, y1, x2, y2):
        """Zooms to a box"""
        # int width, height;
        #   width = abs(this->EndPosition[0] - this->StartPosition[0]);
        #   height = abs(this->EndPosition[1] - this->StartPosition[1]);

        if x1 > x2:
            _ = x1
            x1 = x2
            x2 = _
        if y1 > y2:
            _ = y1
            y1 = y2
            y2 = _

        width = x2 - x1
        height = y2 - y1

        #   int *size = this->CurrentRenderer->GetSize();
        CurrentRenderer = self.GetCurrentRenderer()
        size = CurrentRenderer.GetSize()
        origin = CurrentRenderer.GetOrigin()
        camera = CurrentRenderer.GetActiveCamera()

        rbcenter = (x1 + width / 2, y1 + height / 2, 0)

        CurrentRenderer.SetDisplayPoint(rbcenter)
        CurrentRenderer.DisplayToView()
        CurrentRenderer.ViewToWorld()

        worldRBCenter = CurrentRenderer.GetWorldPoint()

        invw = 1.0 / worldRBCenter[3]
        worldRBCenter = [c * invw for c in worldRBCenter]
        #
        #   double winCenter[3];
        winCenter = [origin[0] + 0.5 * size[0], origin[1] + 0.5 * size[1], 0]

        CurrentRenderer.SetDisplayPoint(winCenter)
        CurrentRenderer.DisplayToView()
        CurrentRenderer.ViewToWorld()

        worldWinCenter = CurrentRenderer.GetWorldPoint()
        invw = 1.0 / worldWinCenter[3]
        worldWinCenter = [c * invw for c in worldWinCenter]

        translation = [
            worldRBCenter[0] - worldWinCenter[0],
            worldRBCenter[1] - worldWinCenter[1],
            worldRBCenter[2] - worldWinCenter[2],
        ]

        pos = camera.GetPosition()
        fp = camera.GetFocalPoint()
        #
        pos = [pos[i] + translation[i] for i in range(3)]
        fp = [fp[i] + translation[i] for i in range(3)]

        #
        camera.SetPosition(pos)
        camera.SetFocalPoint(fp)

        if width > height:
            camera.Zoom(size[0] / width)
        else:
            camera.Zoom(size[1] / height)

        # self.GetInteractor().Render()
        self.DoRender()

    def FocusOn(self, prop3D):
        """Move the camera to focus on this particular prop3D"""

        position = prop3D.GetPosition()

        logging.info(f"Focus on {position}")

        CurrentRenderer = self.GetCurrentRenderer()
        camera = CurrentRenderer.GetActiveCamera()

        fp = camera.GetFocalPoint()
        pos = camera.GetPosition()

        camera.SetFocalPoint(position)
        camera.SetPosition(
            position[0] - fp[0] + pos[0],
            position[1] - fp[1] + pos[1],
            position[2] - fp[2] + pos[2],
        )

        if self.GetAutoAdjustCameraClippingRange():
            CurrentRenderer.ResetCameraClippingRange()

        rwi = self.GetInteractor()
        if rwi.GetLightFollowCamera():
            CurrentRenderer.UpdateLightsGeometryToFollowCamera()

        # rwi.Render()
        self.DoRender()

    def Dolly(self, factor):
        CurrentRenderer = self.GetCurrentRenderer()

        if CurrentRenderer:
            camera = CurrentRenderer.GetActiveCamera()

            if camera.GetParallelProjection():
                camera.SetParallelScale(camera.GetParallelScale() / factor)
            else:
                camera.Dolly(factor)
                if self.GetAutoAdjustCameraClippingRange():
                    CurrentRenderer.ResetCameraClippingRange()

            rwi = self.GetInteractor()
            if rwi.GetLightFollowCamera():
                CurrentRenderer.UpdateLightsGeometryToFollowCamera()

            # rwi.Render()
            self.DoRender()

    def DrawMeasurement(self):
        rwi = self.GetInteractor()
        self.end_x, self.end_y = rwi.GetEventPosition()
        self.DrawLine(self.start_x, self.end_x, self.start_y, self.end_y)

    def DrawDraggedSelection(self):
        rwi = self.GetInteractor()
        self.end_x, self.end_y = rwi.GetEventPosition()
        self.DrawRubberBand(self.start_x, self.end_x, self.start_y, self.end_y)

    def InitializeScreenDrawing(self):
        # make an image of the currently rendered image

        rwi = self.GetInteractor()
        rwin = rwi.GetRenderWindow()

        size = rwin.GetSize()

        self._pixel_array.Initialize()
        self._pixel_array.SetNumberOfComponents(4)
        self._pixel_array.SetNumberOfTuples(size[0] * size[1])

        front = 1  # what does this do?
        rwin.GetRGBACharPixelData(
            0, 0, size[0] - 1, size[1] - 1, front, self._pixel_array
        )

    def DrawRubberBand(self, x1, x2, y1, y2):
        rwi = self.GetInteractor()
        rwin = rwi.GetRenderWindow()

        size = rwin.GetSize()

        tempPA = vtkUnsignedCharArray()
        tempPA.DeepCopy(self._pixel_array)

        # check size, viewport may have been resized in the mean-time
        if tempPA.GetNumberOfTuples() != size[0] * size[1]:
            logging.info(
                "Starting new screen-image - viewport has resized without us knowing"
            )
            self.InitializeScreenDrawing()
            self.DrawRubberBand(x1, x2, y1, y2)
            return

        x2 = min(x2, size[0] - 1)
        y2 = min(y2, size[1] - 1)

        x2 = max(x2, 0)
        y2 = max(y2, 0)

        # Modify the pixel array
        width = abs(x2 - x1)
        height = abs(y2 - y1)
        minx = min(x2, x1)
        miny = min(y2, y1)

        # draw top and bottom
        for i in range(width):

            # c = round((10*i % 254)/254) * 254  # find some alternating color
            c = 0

            id = (miny * size[0]) + minx + i
            tempPA.SetTuple(id, (c, c, c, 1))

            id = ((miny + height) * size[0]) + minx + i
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

    def LineToPixels(self, x1, x2, y1, y2):
        """Returns the x and y values of the pixels on a line between x1,y1 and x2,y2.
        If start and end are identical then a single point is returned"""

        dx = x2 - x1
        dy = y2 - y1

        if dx == 0 and dy == 0:
            return [x1], [y1]

        if abs(dx) > abs(dy):
            dhdw = dy / dx
            r = range(0, dx, int(dx / abs(dx)))
            x = [x1 + i for i in r]
            y = [round(y1 + dhdw * i) for i in r]
        else:
            dwdh = dx / dy
            r = range(0, dy, int(dy / abs(dy)))
            y = [y1 + i for i in r]
            x = [round(x1 + i * dwdh) for i in r]

        return x, y


    def DrawLine(self, x1, x2, y1, y2):
        rwi = self.GetInteractor()
        rwin = rwi.GetRenderWindow()

        size = rwin.GetSize()

        x1 = min(max(x1,0), size[0])
        x2 = min(max(x2,0), size[0])
        y1 = min(max(y1,0), size[1])
        y2 = min(max(y2,0), size[1])


        tempPA = vtkUnsignedCharArray()
        tempPA.DeepCopy(self._pixel_array)

        xs, ys = self.LineToPixels(x1, x2, y1, y2)
        for x, y in zip(xs, ys):
            id = (y * size[0]) + x
            tempPA.SetTuple(id, (0, 0, 0, 1))

        # and Copy back to the window
        rwin.SetRGBACharPixelData(0, 0, size[0] - 1, size[1] - 1, tempPA, 0)

        camera = self.GetCurrentRenderer().GetActiveCamera()
        scale = camera.GetParallelScale()

        # Set/Get the scaling used for a parallel projection, i.e.
        #
        # the half of the height of the viewport in world-coordinate distances.
        # The default is 1. Note that the "scale" parameter works as an "inverse scale" — larger numbers produce smaller images. This method has no effect in perspective projection mode

        half_height = size[1] / 2
        # half_height [px] = scale [world-coordinates]

        length = ((x2-x1)**2 + (y2-y1)**2)**0.5
        meters_per_pixel = scale / half_height
        meters = length * meters_per_pixel

        if camera.GetParallelProjection():
            print(f'Line length = {length} px = {meters} m')
        else:
            print('Need to be in non-perspective mode to measure. Press 2 or 3 to get there')

        if self.callbackMeasure:
            self.callbackMeasure(meters)

        #
        # # can we add something to the window here?
        # freeType = vtk.vtkFreeTypeTools.GetInstance()
        # textProperty = vtk.vtkTextProperty()
        # textProperty.SetJustificationToLeft()
        # textProperty.SetFontSize(24)
        # textProperty.SetOrientation(25)
        #
        # textImage = vtk.vtkImageData()
        # freeType.RenderString(textProperty, "a somewhat longer text", 72, textImage) # this does not give an error, assume it works
        # #
        # textImage.GetDimensions()
        # textImage.GetExtent()
        #
        # # # Now put the textImage in the RenderWindow
        # rwin.SetRGBACharPixelData(0, 0, size[0] - 1, size[1] - 1, textImage, 0)

        rwin.Frame()

    def UpdateMiddleMouseButtonLockActor(self):

        if self.middle_mouse_lock_actor is None:
            # create the actor
            # Create a text on the top-rightcenter
            textMapper = vtkTextMapper()
            textMapper.SetInput("Middle mouse lock [m or space] active")
            textProp = textMapper.GetTextProperty()
            textProp.SetFontSize(12)
            textProp.SetFontFamilyToTimes()
            textProp.BoldOff()
            textProp.ItalicOff()
            textProp.ShadowOff()
            textProp.SetVerticalJustificationToTop()
            textProp.SetJustificationToCentered()
            textProp.SetColor((0,0,0))

            self.middle_mouse_lock_actor = vtkActor2D()
            self.middle_mouse_lock_actor.SetMapper(textMapper)
            self.middle_mouse_lock_actor.GetPositionCoordinate().SetCoordinateSystemToNormalizedDisplay()
            self.middle_mouse_lock_actor.GetPositionCoordinate().SetValue(0.5, 0.98)

            self.GetCurrentRenderer().AddActor(self.middle_mouse_lock_actor)

        self.middle_mouse_lock_actor.SetVisibility(self.middle_mouse_lock)
        self.DoRender()

    def DoRender(self):
        self.GetInteractor().Render()


    def __init__(self):

        # Callbacks
        #
        # Callback can be assigned to functions
        #
        # callbackSelect is called whenever one or mode props are selected.
        # callback will be called with a list of props of which the first entry
        # is prop closest to the camera.
        self.callbackSelect = None
        self.callbackStartDrag = None
        self.callbackEndDrag = None
        self.callbackEscapeKey = None
        self.callbackDeleteKey = None
        self.callbackFocusKey = None
        self.callbackAnyKey = None
        self.callbackMeasure = None  # callback with argument float (meters)

        self.callbackCameraDirectionChanged = None

        # active drag
        self.draginfo: DragInfo or None = None  # assigned to a DragInfo object when dragging is active

        # picking
        self.picked_props = [] # will be filled by latest pick

        # settings

        self.mouse_motion_factor = 20
        self.mouse_wheel_motion_factor = 0.5

        # internals

        self.start_x = 0  # start of a drag
        self.start_y = 0
        self.end_x = 0
        self.end_y = 0

        self.middle_mouse_lock = False
        self.middle_mouse_lock_actor = None  # will be created when required

        # Special Modes
        self._is_box_zooming = False

        self._pixel_array = (
            vtkUnsignedCharArray()
        )  # holds an image of the renderer output at the start of a drawing event

        self._upside_down = False

        self._left_button_down = False
        self._middle_button_down = False

        self.AddObserver(vtkCommand.RightButtonPressEvent, self.RightButtonPress)
        self.AddObserver(vtkCommand.RightButtonReleaseEvent, self.RightButtonRelease)
        self.AddObserver(vtkCommand.MiddleButtonPressEvent, self.MiddleButtonPress)
        self.AddObserver(vtkCommand.MiddleButtonReleaseEvent, self.MiddleButtonRelease)
        self.AddObserver(vtkCommand.MouseWheelForwardEvent, self.MouseWheelForward)
        self.AddObserver(vtkCommand.MouseWheelBackwardEvent, self.MouseWheelBackward)
        self.AddObserver(vtkCommand.LeftButtonPressEvent, self.LeftButtonPress)
        self.AddObserver(vtkCommand.LeftButtonReleaseEvent, self.LeftButtonRelease)
        self.AddObserver(vtkCommand.MouseMoveEvent, self.MouseMove)
        self.AddObserver(
            vtkCommand.WindowResizeEvent, self.WindowResized
        )  # does not seem to fire!

        self.AddObserver(vtkCommand.KeyPressEvent, self.KeyPress)
        self.AddObserver(vtkCommand.KeyReleaseEvent, self.KeyRelease)


if __name__ == "__main__":

    from vtkmodules.vtkCommonColor import vtkNamedColors
    from vtkmodules.vtkFiltersSources import vtkCubeSource, vtkLineSource, vtkConeSource
    from vtkmodules.vtkRenderingCore import (
        vtkActor,
        vtkPolyDataMapper,
        vtkRenderWindow,
        vtkRenderWindowInteractor,
        vtkRenderer,
    )

    colors = vtkNamedColors()

    # Create a rendering window and renderer.
    ren = vtkRenderer()
    renWin = vtkRenderWindow()
    renWin.SetWindowName("Custom interactor style - Python")
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
            cubeActor.GetProperty().SetColor(colors.GetColor3d("Silver"))

            cubeActor.SetPosition(3 * i, 3 * j, 0)

            # Assign actor to the renderer.
            ren.AddActor(cubeActor)


    # And create some lines
    for i in range(10):
        for j in range(10):
            p0 = [0, 0, 30]
            p1 = [3 * i, 3 * j, 0]
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



    coneSource = vtkConeSource()
    coneSource.SetHeight(5)
    mapper = vtkPolyDataMapper()
    mapper.SetInputConnection(coneSource.GetOutputPort())
    actor = vtkActor()
    actor.SetPosition((0, 0, -2))
    actor.SetMapper(mapper)
    actor.GetProperty().SetColor(colors.GetColor3d("Green"))
    ren.AddActor(actor)

    ren.ResetCamera()
    ren.GetActiveCamera().Azimuth(30)
    ren.GetActiveCamera().Elevation(30)
    ren.ResetCameraClippingRange()
    ren.SetBackground(colors.GetColor3d("White"))

    # Enable user interface interactor.
    iren.Initialize()

    style = BlenderStyle()

    # Callbacks

    # - selections

    def onSelect(props):  # callback when props are selected
        for prop in props:
            prop.GetProperty().SetColor(0.3, 0.3, 1)
        props[0].GetProperty().SetColor(1, 0.5, 0)  # color the nearest prop orange

    style.callbackSelect = onSelect

    # - actor dragging
    def onStartDrag():
        print('Starting drag')
        # here style.StartDragOnProps can be called to assing other props to drag
        style.StartDragOnProps(style.picked_props)

    def onDragEnd(info : DragInfo):
        print('Accepted drag')
        print(info)

    style.callbackStartDrag = onStartDrag
    style.callbackEndDrag = onDragEnd

    # - other keys
    style.callbackEscapeKey = lambda : print('ESCAPE KEY PRESSED')
    style.callbackFocusKey = lambda : print('FOCUS KEY PRESSED')

    # any key callback (fires on modifier keys as well)
    # style.callbackAnyKey = lambda x : print(f'Key {x} pressed - return True to prevent further processing')

    style.callbackMeasure = lambda x : print(f"Measure distance = {x} m")


    iren.SetInteractorStyle(style)



    renWin.Render()

    logging.basicConfig(level=logging.DEBUG)



    iren.Start()

