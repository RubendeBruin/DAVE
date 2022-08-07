from PySide2.QtWidgets import QWidget, QApplication
from vedo import *
import vtk as vtk
from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor


app = QApplication()
widget = QWidget()
widget.setFixedWidth(400)
widget.setFixedHeight(400)

vtkWidget = QVTKRenderWindowInteractor(widget)


C = Cube()
P = Plotter(qtWidget=vtkWidget)
P += C

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


style = BlenderStyle()

invoked_style = vtk.vtkInteractorStyleTrackballCamera()


P.show(mode=-1)

P.interactor.SetInteractorStyle(style)

widget.show()
app.exec_()

"""

/*=========================================================================
  Program:   Visualization Toolkit
  Module:    vtkInteractorStyleTrackballCamera.cxx
  Copyright (c) Ken Martin, Will Schroeder, Bill Lorensen
  All rights reserved.
  See Copyright.txt or http://www.kitware.com/Copyright.htm for details.
     This software is distributed WITHOUT ANY WARRANTY; without even
     the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR
     PURPOSE.  See the above copyright notice for more information.
=========================================================================*/
#include "vtkInteractorStyleTrackballCamera.h"

#include "vtkCallbackCommand.h"
#include "vtkCamera.h"
#include "vtkMath.h"
#include "vtkMatrix3x3.h"
#include "vtkObjectFactory.h"
#include "vtkRenderWindow.h"
#include "vtkRenderWindowInteractor.h"
#include "vtkRenderer.h"

vtkStandardNewMacro(vtkInteractorStyleTrackballCamera);

//------------------------------------------------------------------------------
vtkInteractorStyleTrackballCamera::vtkInteractorStyleTrackballCamera()
{
  this->MotionFactor = 10.0;
}

//------------------------------------------------------------------------------
vtkInteractorStyleTrackballCamera::~vtkInteractorStyleTrackballCamera() = default;

//------------------------------------------------------------------------------
void vtkInteractorStyleTrackballCamera::OnMouseMove()
{
  int x = this->Interactor->GetEventPosition()[0];
  int y = this->Interactor->GetEventPosition()[1];

  switch (this->State)
  {
    case VTKIS_ENV_ROTATE:
      this->FindPokedRenderer(x, y);
      this->EnvironmentRotate();
      this->InvokeEvent(vtkCommand::InteractionEvent, nullptr);
      break;

    case VTKIS_ROTATE:
      this->FindPokedRenderer(x, y);
      this->Rotate();
      this->InvokeEvent(vtkCommand::InteractionEvent, nullptr);
      break;

    case VTKIS_PAN:
      this->FindPokedRenderer(x, y);
      this->Pan();
      this->InvokeEvent(vtkCommand::InteractionEvent, nullptr);
      break;

    case VTKIS_DOLLY:
      this->FindPokedRenderer(x, y);
      this->Dolly();
      this->InvokeEvent(vtkCommand::InteractionEvent, nullptr);
      break;

    case VTKIS_SPIN:
      this->FindPokedRenderer(x, y);
      this->Spin();
      this->InvokeEvent(vtkCommand::InteractionEvent, nullptr);
      break;
  }
}

//------------------------------------------------------------------------------
void vtkInteractorStyleTrackballCamera::OnLeftButtonDown()
{
  this->FindPokedRenderer(
    this->Interactor->GetEventPosition()[0], this->Interactor->GetEventPosition()[1]);
  if (this->CurrentRenderer == nullptr)
  {
    return;
  }

  this->GrabFocus(this->EventCallbackCommand);
  if (this->Interactor->GetShiftKey())
  {
    if (this->Interactor->GetControlKey())
    {
      this->StartDolly();
    }
    else
    {
      this->StartPan();
    }
  }
  else
  {
    if (this->Interactor->GetControlKey())
    {
      this->StartSpin();
    }
    else
    {
      this->StartRotate();
    }
  }
}

//------------------------------------------------------------------------------
void vtkInteractorStyleTrackballCamera::OnLeftButtonUp()
{
  switch (this->State)
  {
    case VTKIS_DOLLY:
      this->EndDolly();
      break;

    case VTKIS_PAN:
      this->EndPan();
      break;

    case VTKIS_SPIN:
      this->EndSpin();
      break;

    case VTKIS_ROTATE:
      this->EndRotate();
      break;
  }

  if (this->Interactor)
  {
    this->ReleaseFocus();
  }
}

//------------------------------------------------------------------------------
void vtkInteractorStyleTrackballCamera::OnMiddleButtonDown()
{
  this->FindPokedRenderer(
    this->Interactor->GetEventPosition()[0], this->Interactor->GetEventPosition()[1]);
  if (this->CurrentRenderer == nullptr)
  {
    return;
  }

  this->GrabFocus(this->EventCallbackCommand);
  this->StartPan();
}

//------------------------------------------------------------------------------
void vtkInteractorStyleTrackballCamera::OnMiddleButtonUp()
{
  switch (this->State)
  {
    case VTKIS_PAN:
      this->EndPan();
      if (this->Interactor)
      {
        this->ReleaseFocus();
      }
      break;
  }
}

//------------------------------------------------------------------------------
void vtkInteractorStyleTrackballCamera::OnRightButtonDown()
{
  this->FindPokedRenderer(
    this->Interactor->GetEventPosition()[0], this->Interactor->GetEventPosition()[1]);
  if (this->CurrentRenderer == nullptr)
  {
    return;
  }

  this->GrabFocus(this->EventCallbackCommand);

  if (this->Interactor->GetShiftKey())
  {
    this->StartEnvRotate();
  }
  else
  {
    this->StartDolly();
  }
}

//------------------------------------------------------------------------------
void vtkInteractorStyleTrackballCamera::OnRightButtonUp()
{
  switch (this->State)
  {
    case VTKIS_ENV_ROTATE:
      this->EndEnvRotate();
      break;

    case VTKIS_DOLLY:
      this->EndDolly();
      break;
  }

  if (this->Interactor)
  {
    this->ReleaseFocus();
  }
}

//------------------------------------------------------------------------------
void vtkInteractorStyleTrackballCamera::OnMouseWheelForward()
{
  this->FindPokedRenderer(
    this->Interactor->GetEventPosition()[0], this->Interactor->GetEventPosition()[1]);
  if (this->CurrentRenderer == nullptr)
  {
    return;
  }

  this->GrabFocus(this->EventCallbackCommand);
  this->StartDolly();
  double factor = this->MotionFactor * 0.2 * this->MouseWheelMotionFactor;
  this->Dolly(pow(1.1, factor));
  this->EndDolly();
  this->ReleaseFocus();
}

//------------------------------------------------------------------------------
void vtkInteractorStyleTrackballCamera::OnMouseWheelBackward()
{
  this->FindPokedRenderer(
    this->Interactor->GetEventPosition()[0], this->Interactor->GetEventPosition()[1]);
  if (this->CurrentRenderer == nullptr)
  {
    return;
  }

  this->GrabFocus(this->EventCallbackCommand);
  this->StartDolly();
  double factor = this->MotionFactor * -0.2 * this->MouseWheelMotionFactor;
  this->Dolly(pow(1.1, factor));
  this->EndDolly();
  this->ReleaseFocus();
}

//------------------------------------------------------------------------------


//------------------------------------------------------------------------------
void vtkInteractorStyleTrackballCamera::Spin()
{
  if (this->CurrentRenderer == nullptr)
  {
    return;
  }

  vtkRenderWindowInteractor* rwi = this->Interactor;

  double* center = this->CurrentRenderer->GetCenter();

  double newAngle = vtkMath::DegreesFromRadians(
    atan2(rwi->GetEventPosition()[1] - center[1], rwi->GetEventPosition()[0] - center[0]));

  double oldAngle = vtkMath::DegreesFromRadians(
    atan2(rwi->GetLastEventPosition()[1] - center[1], rwi->GetLastEventPosition()[0] - center[0]));

  vtkCamera* camera = this->CurrentRenderer->GetActiveCamera();
  camera->Roll(newAngle - oldAngle);
  camera->OrthogonalizeViewUp();

  rwi->Render();
}

//------------------------------------------------------------------------------


//------------------------------------------------------------------------------
void vtkInteractorStyleTrackballCamera::Dolly()
{
  if (this->CurrentRenderer == nullptr)
  {
    return;
  }

  vtkRenderWindowInteractor* rwi = this->Interactor;
  double* center = this->CurrentRenderer->GetCenter();
  int dy = rwi->GetEventPosition()[1] - rwi->GetLastEventPosition()[1];
  double dyf = this->MotionFactor * dy / center[1];
  this->Dolly(pow(1.1, dyf));
}

//------------------------------------------------------------------------------
void vtkInteractorStyleTrackballCamera::Dolly(double factor)
{
  if (this->CurrentRenderer == nullptr)
  {
    return;
  }

  vtkCamera* camera = this->CurrentRenderer->GetActiveCamera();
  if (camera->GetParallelProjection())
  {
    camera->SetParallelScale(camera->GetParallelScale() / factor);
  }
  else
  {
    camera->Dolly(factor);
    if (this->AutoAdjustCameraClippingRange)
    {
      this->CurrentRenderer->ResetCameraClippingRange();
    }
  }

  if (this->Interactor->GetLightFollowCamera())
  {
    this->CurrentRenderer->UpdateLightsGeometryToFollowCamera();
  }

  this->Interactor->Render();
}

//------------------------------------------------------------------------------
void vtkInteractorStyleTrackballCamera::EnvironmentRotate()
{
  if (this->CurrentRenderer == nullptr)
  {
    return;
  }

  vtkRenderWindowInteractor* rwi = this->Interactor;

  int dx = rwi->GetEventPosition()[0] - rwi->GetLastEventPosition()[0];
  int sizeX = this->CurrentRenderer->GetRenderWindow()->GetSize()[0];

  vtkNew<vtkMatrix3x3> mat;

  double* up = this->CurrentRenderer->GetEnvironmentUp();
  double* right = this->CurrentRenderer->GetEnvironmentRight();

  double front[3];
  vtkMath::Cross(right, up, front);
  for (int i = 0; i < 3; i++)
  {
    mat->SetElement(i, 0, right[i]);
    mat->SetElement(i, 1, up[i]);
    mat->SetElement(i, 2, front[i]);
  }

  double angle = (dx / static_cast<double>(sizeX)) * this->MotionFactor;

  double c = std::cos(angle);
  double s = std::sin(angle);
  double t = 1.0 - c;

  vtkNew<vtkMatrix3x3> rot;

  rot->SetElement(0, 0, t * up[0] * up[0] + c);
  rot->SetElement(0, 1, t * up[0] * up[1] - up[2] * s);
  rot->SetElement(0, 2, t * up[0] * up[2] + up[1] * s);

  rot->SetElement(1, 0, t * up[0] * up[1] + up[2] * s);
  rot->SetElement(1, 1, t * up[1] * up[1] + c);
  rot->SetElement(1, 2, t * up[1] * up[2] - up[0] * s);

  rot->SetElement(2, 0, t * up[0] * up[2] - up[1] * s);
  rot->SetElement(2, 1, t * up[1] * up[2] + up[0] * s);
  rot->SetElement(2, 2, t * up[2] * up[2] + c);

  vtkMatrix3x3::Multiply3x3(rot, mat, mat);

  // update environment orientation
  this->CurrentRenderer->SetEnvironmentUp(
    mat->GetElement(0, 1), mat->GetElement(1, 1), mat->GetElement(2, 1));
  this->CurrentRenderer->SetEnvironmentRight(
    mat->GetElement(0, 0), mat->GetElement(1, 0), mat->GetElement(2, 0));

  rwi->Render();
}

//------------------------------------------------------------------------------
void vtkInteractorStyleTrackballCamera::PrintSelf(ostream& os, vtkIndent indent)
{
  this->Superclass::PrintSelf(os, indent);
  os << indent << "MotionFactor: " << this->MotionFactor << "\n";
}

"""
