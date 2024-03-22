"""Provides outlines on actors"""
from vtkmodules.vtkCommonTransforms import vtkTransform

from DAVE.visual_helpers.constants import COLOR_OUTLINE, OUTLINE_WIDTH
from DAVE.visual_helpers.vtkHelpers import SetTransformIfDifferent, vtkMatricesAlmostEqual, SetMatrixIfDifferent


class VisualOutline:
    """

    Actor.Data -> TransformFilter -> EdgeDetection -> Actor
                   ^^^^^^^^^^^^^
                   this shall match the transform of the outlined actor

    This is setup in this way to have the correct camera angle for the silhouette.

    If not used silhoutte but outlines only, then the transform filter can be set to identity
    and the transform can be applied on the actor instead. This saves re-computation in the
    edge detection

    """

    parent_vp_actor = None
    outline_actor = None
    outline_transform = None

    I = vtkTransform()
    I.Identity()

    def update(self):
        # update transform

        do_silhouette = getattr(self.parent_vp_actor, "do_silhouette", True)

        if do_silhouette:
            SetTransformIfDifferent(
                self.outline_actor, self.I
            )  # outline actor shall have identity

            new_matrix = self.parent_vp_actor.GetMatrix()

            current_matrix = self.outline_transform.GetTransform().GetMatrix()

            if not vtkMatricesAlmostEqual(new_matrix, current_matrix):
                self.outline_transform.GetTransform().SetMatrix(new_matrix)

        else:
            if not vtkMatricesAlmostEqual(
                self.I.GetMatrix(), self.outline_transform.GetTransform().GetMatrix()
            ):
                self.outline_transform.SetTransform(self.I)

            SetMatrixIfDifferent(
                self.outline_actor, self.parent_vp_actor.GetMatrix()
            )  # outline transform shall have identity

        self.outline_actor.SetVisibility(
            getattr(self.parent_vp_actor, "xray", False)
            or self.parent_vp_actor.GetVisibility()
        )

        # get color
        color = getattr(self.parent_vp_actor, "_outline_color", COLOR_OUTLINE)
        self.outline_actor.GetProperty().SetColor(
            color[0] / 255, color[1] / 255, color[2] / 255
        )
        self.outline_actor.GetProperty().SetLineWidth(OUTLINE_WIDTH)
        self.outline_actor.GetProperty().SetRenderLinesAsTubes(False)
