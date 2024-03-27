"""Provides outlines on actors"""
from vtkmodules.vtkCommonTransforms import vtkTransform
from vtkmodules.vtkFiltersCore import vtkCleanPolyData, vtkFeatureEdges
from vtkmodules.vtkFiltersGeneral import vtkTransformPolyDataFilter
from vtkmodules.vtkFiltersHybrid import vtkPolyDataSilhouette
from vtkmodules.vtkRenderingCore import vtkActor, vtkProperty2D, vtkPolyDataMapper, vtkCamera

from DAVE.visual_helpers.constants import COLOR_OUTLINE, OUTLINE_WIDTH
from DAVE.visual_helpers.vtkHelpers import SetTransformIfDifferent, vtkMatricesAlmostEqual, SetMatrixIfDifferent, \
    SetIdentityTransform


class VisualOutline:
    """
    The visual outline is a helper class to create outlines on actors.
    It is used to create
    - a silhouette of the actor
    - the feature edges of the actor

    The feature-edges do not depend on the camera angle, while the silhouette does.



    Actor.Data -> TransformFilter -> EdgeDetection -> Actor
                   ^^^^^^^^^^^^^
                   this shall match the transform of the outlined actor

    This is setup in this way to have the correct camera angle for the silhouette.

    If only the feature edges are used, then the transform filter can be set to identity
    and the transform can be applied on the actor instead. This saves re-computation in the
    edge detection

    """

    # Class variables (constant)
    I = vtkTransform()
    I.Identity()

    @staticmethod
    def actor_needs_outline(actor : vtkActor):
        """Returns True of an actor needs an outline, that is:
        - it is not an annotation
        - it is not a wireframe
        - it does not have the no_outline attribute set to True
        - it is a polydata actor
        """
        if isinstance(
                actor.GetProperty(), vtkProperty2D
        ):  # annotations
            return False

        try:
            if actor.GetProperty().GetRepresentation() == 1:  # wireframe
                return False
        except:
            return False

        if getattr(actor, "no_outline", False):
            return False

        if not isinstance(actor.GetMapper(), vtkPolyDataMapper):
            return False

        return True

    def __init__(self, actor : vtkActor, camera : vtkCamera, linewidth):
        """Creates an outline for an actor"""

        # create a clean copy of the polydata of the actor
        cleaner = vtkCleanPolyData()
        cleaner.SetInputData(actor.GetMapper().GetInputAsDataSet())
        cleaner.Update()
        self.cleaned_poly_data  = cleaner.GetOutput()

        # create the outline actor based on the cleaned poly data and a transform
        tr = vtkTransformPolyDataFilter()

        tr.SetInputData(self.cleaned_poly_data)

        # initially set the transform to identity
        temp = vtkTransform()
        temp.Identity()
        tr.SetTransform(temp)
        tr.Update()

        do_silhouette = getattr(actor, "do_silhouette", True)

        self.is_silhouette = do_silhouette

        if do_silhouette:
            ol = vtkPolyDataSilhouette()
            ol.SetInputConnection(tr.GetOutputPort())
            ol.SetEnableFeatureAngle(True)
            ol.SetCamera(camera)
            ol.SetBorderEdges(True)

        else:
            ol = vtkFeatureEdges()
            ol.SetColoring(False)  # does not seem to do anything
            ol.SetInputConnection(tr.GetOutputPort())
            ol.ExtractAllEdgeTypesOff()
            ol.BoundaryEdgesOn()
            ol.SetFeatureAngle(25)
            ol.FeatureEdgesOn()

        mapper = vtkPolyDataMapper()
        mapper.SetInputConnection(ol.GetOutputPort())
        mapper.ScalarVisibilityOff()  # No colors!

        outline_actor = vtkActor()
        outline_actor.SetMapper(mapper)
        outline_actor.GetProperty().SetColor(0, 0, 0)
        outline_actor.GetProperty().SetLineWidth(linewidth)

        # store the things that we need
        self.outlined_actor = actor
        self.outline_actor = outline_actor
        self.outline_transform = tr



    def update(self):
        # update transform

        if self.is_silhouette:

            SetTransformIfDifferent(
                self.outline_actor, self.I
            )  # outline actor shall have identity

            new_matrix = self.outlined_actor.GetMatrix()
            current_matrix = self.outline_transform.GetTransform().GetMatrix()

            if not vtkMatricesAlmostEqual(new_matrix, current_matrix):
                self.outline_transform.GetTransform().SetMatrix(new_matrix)

        else:

            if not vtkMatricesAlmostEqual(
                self.I.GetMatrix(), self.outline_transform.GetTransform().GetMatrix()  # setting is quicker than checking
            ):
                self.outline_transform.SetTransform(self.I)

            SetMatrixIfDifferent(
                self.outline_actor, self.outlined_actor.GetMatrix()
            )  # outline transform shall have identity

        self.outline_actor.SetVisibility(
            getattr(self.outlined_actor, "xray", False)
            or self.outlined_actor.GetVisibility()
        )

        # get color
        color = getattr(self.outlined_actor, "_outline_color", COLOR_OUTLINE)
        self.outline_actor.GetProperty().SetColor(
            color[0] / 255, color[1] / 255, color[2] / 255
        )
        self.outline_actor.GetProperty().SetLineWidth(OUTLINE_WIDTH)
        self.outline_actor.GetProperty().SetRenderLinesAsTubes(False)
