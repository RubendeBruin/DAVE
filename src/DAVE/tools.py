"""
  This Source Code Form is subject to the terms of the Mozilla Public
  License, v. 2.0. If a copy of the MPL was not distributed with this
  file, You can obtain one at http://mozilla.org/MPL/2.0/.

  Ruben de Bruin - 2019


  Some tools

"""

import numbers
from DAVE.scene import *
import DAVE.settings as ds
import numpy as np

def assert1f(var, name = "Variable"):
    if not isinstance(var, numbers.Number):
        raise ValueError(name + " should be a number but {} is not a number.".format(var))

def assert1f_positive(var, name = "Variable"):
    if not isinstance(var, numbers.Number):
        raise ValueError(name + " should be a number but {} is not a number.".format(var))
    if var < 0:
        raise ValueError(name + " can not be negative.".format(var))

def assert3f(var, name = "Variable"):
    """Asserts that variable has length three and contains only numbers"""
    assert len(var) == 3, name + " should have length 3 but has length {}".format(len(var))
    for i in range(3):
        if not isinstance(var[i], numbers.Number):
            raise ValueError(name + " should contain three numbers but {} is not a number.".format(var[i]))

def assert3f_positive(var, name = "Variable"):
    """Asserts that variable has length three and contains only numbers"""
    assert len(var) == 3, name + " should have length 3 but has length {}".format(len(var))
    for i in range(3):
        if not isinstance(var[i], numbers.Number):
            raise ValueError(name + " should contain three positive numbers but {} is not a number.".format(var[i]))
        if var[i]<0:
            raise ValueError(name + " should contain three positive numbers but {} is not > 0.".format(var[i]))

def assert6f(var, name = "Variable"):
    """Asserts that variable has length six and contains only numbers"""
    assert len(var) == 6, name + " should have length 6 but has length {}".format(len(var))
    for i in range(6):
        if not isinstance(var[i], numbers.Number):
            raise ValueError(name + " should contain six numbers but {} is not a number.".format(var[i]))


def assertValidName(var):
    assert isinstance(var, str), "Name should be a string"
    if ds.VF_NAME_SPLIT in var:
        raise ValueError('Name should not contain "{}", but "{}" does'.format(ds.VF_NAME_SPLIT, var))

def assertPoi(var, name = "Node"):
    if isinstance(var, Poi):
        return
    else:
        raise ValueError(name + " be of type Poi but is a ".format(type(var)))

def make_iterable(v):
    """Makes an variable iterable by putting it in a list if needed"""

    try:
        _ = iter(v)
        return v
    except:
        return [v]


def radii_to_positions(rxx,ryy,rzz):
    """decouple radii of gyration into six point discrete positions"""

    rxx2 = rxx ** 2
    ryy2 = ryy ** 2
    rzz2 = rzz ** 2

    assert (rxx2 <= (ryy2 + rzz2)) , ValueError('rxx^2 should be <= ryy^2 + rzz^2, but rxx={}, ryy={}, rzz={}'.format(rxx,ryy,rzz))
    assert (ryy2 <= (rxx2 + rzz2)),  ValueError('ryy^2 should be <= rxx^2 + rzz^2, but rxx={}, ryy={}, rzz={}'.format(rxx,ryy,rzz))
    assert (rzz2 <= (rxx2 + ryy2)),  ValueError('rzz^2 should be <= rxx^2 + ryy^2, but rxx={}, ryy={}, rzz={}'.format(rxx,ryy,rzz))

    x = np.sqrt(0.5 * (-rxx2 + ryy2 + rzz2)) * np.sqrt(3)
    y = np.sqrt(0.5 * (rxx2 - ryy2 + rzz2)) * np.sqrt(3)
    z = np.sqrt(0.5 * (rxx2 + ryy2 - rzz2)) * np.sqrt(3)

    # Add the point masses
    ps = list()
    ps.append([x, 0, 0])
    ps.append([-x, 0, 0])
    ps.append([0, y, 0])
    ps.append([0, -y, 0])
    ps.append([0, 0, z])
    ps.append([0, 0, -z])

    return ps

def rotation_from_y_axis_direction(direction):
    """Returns a rotation vector that rotates the Y-axis (0,1,0) into the given direction"""

    # the direction of the rotation is the cross product between y and target
    axis = np.cross(direction, (0,1,0))

    if np.linalg.norm(axis) < 1e-9:
        # axis are perpendicular
        # but may still be in exactly opposite direction
        if np.dot(direction, (0,1,0)) > 0:
            return (0,0,0)
        else:
            return (0,0,180)

    axis = axis / np.linalg.norm(axis)  # normalize

    # the required angle of rotation is best calcualted using the atan2

    # construct the y / target plane
    perp = np.cross(axis, (0,1,0))  # no need to normalize

    compx = np.dot(direction, (0,1,0))
    compy = np.dot(direction, perp)

    angle = np.arctan2(compy, compx)

    return np.rad2deg(angle * axis)



