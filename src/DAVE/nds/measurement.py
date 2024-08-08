from enum import Enum

import numpy as np

from .pure import NodePurePython
from .geometry import Point, Frame


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
    Total = 10

    def as_vector(self):
        if self == MeasurementDirection.X or self == MeasurementDirection.YZ:
            return np.array([1, 0, 0])
        elif self == MeasurementDirection.Y or self == MeasurementDirection.XZ:
            return np.array([0, 1, 0])
        elif self == MeasurementDirection.Z or self == MeasurementDirection.XY:
            return np.array([0, 0, 1])
        elif self == MeasurementDirection.negative_X or self == MeasurementDirection.YZ:
            return np.array([-1, 0, 0])
        elif self == MeasurementDirection.negative_Y or self == MeasurementDirection.XZ:
            return np.array([0, -1, 0])
        elif self == MeasurementDirection.negative_Z or self == MeasurementDirection.XY:
            return np.array([0, 0, -1])
        else:
            return None

    def is_perpendicular(self):
        return self in [MeasurementDirection.XY, MeasurementDirection.YZ, MeasurementDirection.XZ]


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

        self.direction: MeasurementDirection = MeasurementDirection.Total
        self.reference: Frame or None = None

    def depends_on(self) -> list:
        if self.reference:
            return [self.point1, self.point2, self.reference]
        else:
            return [self.point1, self.point2]

    @property
    def p1(self):
        """Global position of first point [m,m,m]"""
        return self.point1.global_position

    @property
    def p2(self):
        """Global position of second point [m,m,m]"""
        return self.point2.global_position

    def points(self):

        # global position of the two points
        p1 = np.array(self.p1)
        p2 = np.array(self.p2)

        # total distance
        if self.direction == MeasurementDirection.Total:
            return (p1,p2,p2,p1),1

        # projected distance
        #
        # get the projection direction

        direction = self.direction.as_vector()

        if direction is None:
            raise ValueError(f"Invalid direction for measurement {self.name}")

        # in reference system?
        if self.reference:
            assert isinstance(self.reference, Frame)
            direction = np.array(self.reference.to_glob_direction(direction))

        # is the direction defined as perpendicular-to?
        if self.direction.is_perpendicular():
            # calculate the perpendicular direction
            perp = np.cross(direction, p2 - p1)

            if np.linalg.norm(perp) <= 1e-20:
                return (p1,p2,p1,p1),1

            direction = np.cross(perp, direction)
            # normalize
            direction /= np.linalg.norm(direction)

        # calculate p3
        projected_distance = np.dot(p2 - p1, direction)
        p3 = p1 + projected_distance * direction

        sign = np.sign(projected_distance)

        p4 = p1 + abs(projected_distance) * direction

        return (p1,p2,p3,p4), sign


    @property
    def value(self):
        """Value of the measurement"""

        if self.kind == MeasurementType.Distance:
            return self._distance()
        else:
            return self._angle()

    @property
    def value_str(self):
        """Value of the measurement as string"""

        if self.kind == MeasurementType.Distance:
            return f"{self._distance():.3f}m"
        else:
            return f"{self._angle():.2f}°"

    def _distance(self):
        """Calculate distance"""

        (p1, p2, p3, p4), sign = self.points()

        return sign * np.linalg.norm(p3 - p1)


    def _angle(self):
        """Calculate angle"""

        (p1, p2, p3, p4), sign = self.points()

        line1 = p2-p1

        if sign>0:
            line2 = p3-p1
        else:
            line2 = p4-p1

        L1 = np.linalg.norm(line1)
        L2 = np.linalg.norm(line2)

        if L2 == 0:
            return 0
        if L1 == 0:
            return 90

        angle = np.arccos(np.dot(line1, line2) / (np.linalg.norm(line1) * np.linalg.norm(line2)))

        return np.degrees(angle)
