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

def assert1f(var, name = "Variable"):
    if not isinstance(var, numbers.Number):
        raise ValueError(name + " should be a number but {} is not a number.".format(var[i]))

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

    Ixx = rxx ** 2
    Iyy = ryy ** 2
    Izz = rzz ** 2

    rxx2 = (Ixx)
    ryy2 = (Iyy)
    rzz2 = (Izz)

    # checks
    if rxx2 > ryy2 + rzz2:
        raise Exception('Ixx should be < Iyy + Izz')
    if ryy2 > rxx2 + rzz2:
        raise Exception('Iyy should be < Ixx + Izz')
    if rzz2 > rxx2 + rzz2:
        raise Exception('Izz should be < Ixx + Iyy')

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
