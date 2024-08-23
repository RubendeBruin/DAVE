from enum import Enum

import numpy as np

from .pure import NodePurePython
from .geometry import Point, Frame
from ..tools import something_orthogonal_to

"""
Measurement
------------

The Measurement node is used to measure distances and angles between points in the scene.

A user-reference is used to define the direction of the measurement.
This can be either a vector or a plane.

If it is a plane, then the reference vector is derived from that plane as the projection of the
measurement vector onto that plane. 
If a positive direction guide is defined, then the projection is made such that the reference vector
has a positive dot product with the positive direction guide.


"""

class MeasurementDirection(Enum):
    X = 1
    Y = 2
    Z = 3
    negative_X = 4
    negative_Y = 5
    negative_Z = 6
    XY = 7
    YZ = 8
    XZ = 9
    XY_negative = 11
    YZ_negative = 12
    XZ_negative = 13

    Total = 99

    def as_vector(self):
        if self == MeasurementDirection.X or self == MeasurementDirection.YZ:
            return np.array([1, 0, 0])
        elif self == MeasurementDirection.Y or self == MeasurementDirection.XZ:
            return np.array([0, 1, 0])
        elif self == MeasurementDirection.Z or self == MeasurementDirection.XY:
            return np.array([0, 0, 1])
        elif self == MeasurementDirection.negative_X or self == MeasurementDirection.YZ_negative:
            return np.array([-1, 0, 0])
        elif self == MeasurementDirection.negative_Y or self == MeasurementDirection.XZ_negative:
            return np.array([0, -1, 0])
        elif self == MeasurementDirection.negative_Z or self == MeasurementDirection.XY_negative:
            return np.array([0, 0, -1])
        else:
            return None

    def is_plane(self):
        return self in [MeasurementDirection.XY, MeasurementDirection.YZ, MeasurementDirection.XZ, MeasurementDirection.XY_negative, MeasurementDirection.YZ_negative, MeasurementDirection.XZ_negative]


class MeasurementType(Enum):
    Distance = 1
    Angle = 2


class Measurement(NodePurePython):
    """Measurement node

    Measures the distance or angle between two points.
    """

    def __init__(self, scene, name: str):
        super().__init__(scene=scene, name=name)

        self.point1: Frame or Point or None = None
        self.point2: Frame or Point or None = None

        self.kind: MeasurementType = MeasurementType.Distance

        self._reference: MeasurementDirection = MeasurementDirection.Total
        """controlled by reference property"""
        self._reference_frame: Frame or None = None

        self._positive_direction_guide : tuple[float, float, float] or None = None #
        """The direction with which which the direction vector should have a positive dot product.
        """

        self.flip_angle_direction : bool = False
        """True means invert, False means do not invert"""


    @property
    def reference_frame(self):
        return self._reference_frame

    @reference_frame.setter
    def reference_frame(self, value):
        assert value is None or isinstance(value, Frame), f'Error when setting refernce_frame on {self.name}: Reference frame should be a Frame or None'
        self._reference_frame = value
        self.update_positive_direction_guide()

    def depends_on(self) -> list:
        if self._reference_frame:
            return [self.point1, self.point2, self._reference_frame]
        else:
            return [self.point1, self.point2]

    @property
    def p1(self) -> tuple[float,float,float]:
        """Global position of first point [m,m,m]"""
        return self.point1.global_position

    @property
    def p2(self) -> tuple[float,float,float]:
        """Global position of second point [m,m,m]"""
        return self.point2.global_position

    @property
    def measurement_vector(self) -> np.ndarray:
        """The measurement vector in global coordinates [m,m,m]"""

        return np.array(self.p2) - np.array(self.p1)

    @property
    def reference_vector(self) -> np.ndarray or None:
        """Reference vector for the measurement, in global coordinates [m,m,m] or None in case of total distance

        If it is a plane, then the reference vector is derived from that plane as the projection of the
        measurement vector onto that plane.

        If a positive direction guide is defined, then the projection is made such that the reference vector
        has a positive dot product with the positive direction guide.

        """

        if self.reference == MeasurementDirection.Total:
            return None

        if not self.reference.is_plane(): # not a plane, so a vector

            direction = self._in_global(self.reference.as_vector())

            direction = np.dot(self.measurement_vector, direction) * direction
            return self._apply_direction_guide(direction)

        # we have a plane, calculate the projection

        normal = self._in_global(self.reference.as_vector())

        # calculate the projection of the measurement vector onto the plane (normal is a unit vector)

        projection = self.measurement_vector - np.dot(self.measurement_vector, normal) * normal

        return self._apply_direction_guide(projection)


    def _in_global(self, vector) -> np.ndarray:
        """Vector in global coordinates using reference_frame (if any)"""
        if self._reference_frame is not None:
            return np.array(self._reference_frame.to_glob_direction(vector))
        else:
            return np.array(vector)

    def _apply_direction_guide(self, vector):
        if self._positive_direction_guide is not None:

            positive_direction = self._in_global(self._positive_direction_guide)

            # make sure the direction is in the same direction as the positive direction guide
            if np.dot(vector, positive_direction) < 0:
                vector = -vector
        return vector

    def points_for_drawing(self):
        """Returns points 1,2 3 and 4

        P1 is the first point
        P2 is the second point

        P3 is the point on the reference plane that is closest to P2
        P4 is the point at the end of the reference vector
        P3 and P4 may be equal

        drawing order:
        1,2,3,1,4

        """

        p1 = np.array(self.p1)
        p2 = np.array(self.p2)

        if self.reference_vector is None:
            return p1, p2, p2, p1

        p4 = p1 + self.reference_vector
        p3 = p1 - self.reference_vector

        # if p4 is closer to p2 than p3, then p3 should be p4
        if np.linalg.norm(p2 - p4) <= np.linalg.norm(p2 - p3):
            p3 = p4

        return p1, p2, p3, p4




    @property
    def reference(self):
        return self._reference

    @reference.setter
    def reference(self, value):
        if value != self._reference:
            self._reference = value
            self.update_positive_direction_guide()

    def update_positive_direction_guide(self, invert=False):
        """Updates the angle reference vector, automatically called when direction is changed"""

        m = self.measurement_vector
        if self._reference_frame is not None:
            m = self._reference_frame.to_loc_direction(m)

        if invert:
            self._positive_direction_guide = -m
        else:
            self._positive_direction_guide = m


    @property
    def value(self) -> float:
        """Value of the measurement [m or deg]"""

        if self.kind == MeasurementType.Distance:
            return self._distance()
        else:
            return self._angle()

    @property
    def value_str(self) -> str:
        """Value of the measurement as string []"""

        if self.kind == MeasurementType.Distance:
            return f"{self._distance():.3f}m"
        else:
            return f"{self._angle():.2f}°"

    def _distance(self):
        """Calculate distance"""
        refvec = self.reference_vector

        if refvec is None:
            return np.linalg.norm(self.measurement_vector)
        else:

            if np.dot(self.measurement_vector, refvec) < 0:
                return -np.linalg.norm(refvec)
            else:
                return np.linalg.norm(refvec)

    def _angle_measurement_plane(self) -> tuple[np.ndarray, np.ndarray]:
        """Returns the oriented plane in which the angle is measured. Returns x and y vectors of the plane"""
        refvec = self.reference_vector

        if refvec is None:
            raise ValueError(f'Angle measurement without reference vector is not possible for {self.name}')


        m = self.measurement_vector

        if np.linalg.norm(refvec) < 1e-6:  # measurement is orthogonal to the reference vector
            refvec = something_orthogonal_to(m)

        # calculate the angle between the measurement vector and the reference vector in degrees
        # consider the direction and use atan2 to get the correct angle

        perp = np.cross(refvec,m)

        # are the vectors parallel?
        if np.linalg.norm(perp) < 1e-6:
            # if the vectors are parallel, then the angle is zero
            # construct an other vector that is perpendicular to the measurement vector

            perp = something_orthogonal_to(m)

        perp = perp / np.linalg.norm(perp)

        x = refvec / np.linalg.norm(refvec)
        y = np.cross(perp, x)

        return x, y


    def _angle(self):
        """Calculate angle"""
        x,y = self._angle_measurement_plane()
        m = self.measurement_vector
        angle = np.arctan2(np.dot(m, y), np.dot(m, x))

        # is the measurement vector in the direction of the normal of the plane?
        # (if we have one)
        # if so then the angle is positive, otherwise it is negative

        if self.reference.is_plane():
            normal = self._in_global(self.reference.as_vector())
            if np.dot(m, normal) < 0:
                angle = -angle

        if self.flip_angle_direction:
            angle = -angle

        return np.degrees(angle)


    def give_python_code(self):
        code = []
        code.append(f"m = Measurement(s, '{self.name}')")
        code.append(f"m.point1 = s['{self.point1.name}']")
        code.append(f"m.point2 = s['{self.point2.name}']")
        code.append(f"m.kind = MeasurementType.{self.kind.name}")
        code.append(f"m.direction = MeasurementDirection.{self.reference.name}")
        if self._reference_frame:
            code.append(f"m.reference = s['{self._reference_frame.name}']")
        if self._positive_direction_guide is not None:
            code.append(f"m._angle_reference = {str(tuple(self._positive_direction_guide))}")

        return "\n".join(code)

