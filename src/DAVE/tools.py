"""
  This Source Code Form is subject to the terms of the Mozilla Public
  License, v. 2.0. If a copy of the MPL was not distributed with this
  file, You can obtain one at http://mozilla.org/MPL/2.0/.

  Ruben de Bruin - 2019


  Some tools

"""
import math
import numbers
import os

from DAVE.scene import *
import DAVE.settings as ds
from DAVE.helpers.string_functions import increment_string_end
import numpy as np
from scipy.spatial.transform import Rotation
from glob import glob


def running_in_gui():
    """Returns True if running in a GUI environment, False otherwise"""
    try:
        from PySide6.QtWidgets import QApplication

        if QApplication.instance() is not None:
            return True

    except ImportError:
        pass

    return False


def MostLikelyMatch(search_for, choices) -> str:
    """Uses rapidfuzz to get a best match"""

    try:
        from rapidfuzz import process, fuzz

        best = process.extractOne(search_for, choices, scorer=fuzz.WRatio)
        return best[0]
    except:
        return "[install rapidfuzz to get a suggestion]"



def assertBool(var, name="Variable"):
    if not isinstance(var, bool):
        raise ValueError(
            name + " should be a boolean (True/False) but is {}".format(var)
        )


def is_number(var):
    if isinstance(var, bool):
        return False
    if isinstance(var, numbers.Number):
        return True
    return False


def assert1f(var, name="Variable"):
    if not is_number(var):
        raise ValueError(
            name + " should be a number but {} is not a number.".format(var)
        )


def assert1i_positive_or_zero(var, name="Variable"):
    assert round(var) == var, f"{name} should be an integer (round number), not {var}"

    if not is_number(var):
        raise ValueError(
            name + " should be a number but {} is not a number.".format(var)
        )
    if var < 0:
        raise ValueError(name + " can not be negative.".format(var))


def assert1f_positive_or_zero(var, name="Variable"):
    if not is_number(var):
        raise ValueError(
            name + " should be a number but {} is not a number.".format(var)
        )
    if var < 0:
        raise ValueError(name + " can not be negative.".format(var))


def assert1f_positive(var, name="Variable"):
    if not is_number(var):
        raise ValueError(
            name + " should be a number but {} is not a number.".format(var)
        )
    if var < 1e-6:
        raise ValueError(name + " should be >= 1e-6.".format(var))


def assert3f(var, name="Variable"):
    """Asserts that variable has length three and contains only numbers"""
    assert len(var) == 3, name + " should have length 3 but has length {}".format(
        len(var)
    )
    for i in range(3):
        if not is_number(var[i]):
            raise ValueError(
                name
                + " should contain three numbers but {} is not a number.".format(var[i])
            )


def assert3f_positive(var, name="Variable"):
    """Asserts that variable has length three and contains only numbers"""
    assert len(var) == 3, name + " should have length 3 but has length {}".format(
        len(var)
    )
    for i in range(3):
        if not is_number(var[i]):
            raise ValueError(
                name
                + " should contain three positive numbers but {} is not a number.".format(
                    var[i]
                )
            )
        if var[i] < 0:
            raise ValueError(
                name
                + " should contain three positive numbers but {} is not > 0.".format(
                    var[i]
                )
            )


def assert6f(var, name="Variable"):
    """Asserts that variable has length six and contains only numbers"""
    assert len(var) == 6, name + " should have length 6 but has length {}".format(
        len(var)
    )
    for i in range(6):
        if not is_number(var[i]):
            raise ValueError(
                name
                + " should contain six numbers but {} is not a number.".format(var[i])
            )


def assertValidName(var):
    assert isinstance(var, str), "Name should be a string"
    if ds.VF_NAME_SPLIT in var:
        raise ValueError(
            'Name should not contain "{}", but "{}" does'.format(ds.VF_NAME_SPLIT, var)
        )


def assertIterableNumbers(var):
    try:
        _ = iter(var)
        for e in var:
            assert1f(e)
        return True
    except:
        return False


def assertPoi(var, name="Node"):
    if isinstance(var, Point):
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


def fancy_format(text, number="{:.3f}"):
    # do some formatting

    # if isinstance(text, bool):
    #     return str(text)

    if isinstance(text, float):
        a = float(text)
        result = number.format(a)
        return result

    try:
        len(text)
    except:
        return str(text)

    if len(text) > 0:
        try:
            float(text[0])
        except:
            return text

        a = []
        for e in text:
            try:
                r = float(e)
                a.append(number.format(r))
            except:
                a.append(e)

        result = "("
        for e in a:
            result += e
            result += ", "
        result = result[:-2]
        result += " )"
        return result

    return text


def radii_from_box_shape(dx, dy, dz, mass_distribution_factor=1.0):
    """Returns the radii of gyration of a box with size dx,dy,dz.

    For hollow boxes set mass_distribution_factor to 1.5, for solid set it to 1.0
    """

    f = mass_distribution_factor / 12

    rxx = math.sqrt(f * (dy * dy + dz * dz))
    ryy = math.sqrt(f * (dx * dx + dz * dz))
    rzz = math.sqrt(f * (dx * dx + dy * dy))

    return (rxx, ryy, rzz)


def radii_to_positions(rxx, ryy, rzz):
    """decouple radii of gyration into six point discrete positions"""

    rxx2 = rxx**2
    ryy2 = ryy**2
    rzz2 = rzz**2

    assert rxx2 <= (ryy2 + rzz2), ValueError(
        "rxx^2 should be <= ryy^2 + rzz^2, but rxx={}, ryy={}, rzz={}; maximum value for rxx = {}".format(
            rxx, ryy, rzz, math.sqrt(ryy2 + rzz2)
        )
    )
    assert ryy2 <= (rxx2 + rzz2), ValueError(
        "ryy^2 should be <= rxx^2 + rzz^2, but rxx={}, ryy={}, rzz={}; maximum value for ryy = {}".format(
            rxx, ryy, rzz, math.sqrt(rxx2 + rzz2)
        )
    )
    assert rzz2 <= (rxx2 + ryy2), ValueError(
        "rzz^2 should be <= rxx^2 + ryy^2, but rxx={}, ryy={}, rzz={}; maximum value for rzz = {}".format(
            rxx, ryy, rzz, math.sqrt(rxx2 + ryy2)
        )
    )

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


def rotvec_inverse(rotvec):
    """Returns the inverse of the rotation vector"""
    r = Rotation.from_rotvec(np.deg2rad(rotvec))
    return np.rad2deg(r.inv().as_rotvec())


def rotvec_from_y_and_z_axis_direction(y, z):
    """Returns an orientation with the z-axis upwards as much as possible and the y-axis in the requested direction"""

    y = np.array(y) / np.linalg.norm(y)
    x = np.cross(y, z)
    x = x / np.linalg.norm(x)
    z = np.cross(x, y)

    # np.linalg.det([x, y, z]) check

    # now construct a rotation vector from the three vector basis

    r = Rotation.from_matrix(np.transpose([x, y, z]))

    return np.rad2deg(r.as_rotvec())


def rotvec_from_y_axis_direction(direction):
    """Returns an orientation with the z-axis upwards as much as possible and the y-axis in the requested direction"""

    y = np.array(direction) / np.linalg.norm(direction)
    z = (0, 0, 1)
    x = np.cross(y, z)

    if np.linalg.norm(x) < 1e-9:  # y==z or y==-z
        z = (0, -1, 0)
        x = np.cross(y, z)

    return rotvec_from_y_and_z_axis_direction(y, z)


def rotation_from_y_axis_direction(direction):
    """Returns a rotation vector that rotates the Y-axis (0,1,0) to the given direction"""
    return rotation_from_axis_direction(direction, (0, 1, 0))


def rotation_from_x_axis_direction(direction):
    """Returns a rotation vector that rotates the X-axis (1,0,0) to the given direction"""
    return rotation_from_axis_direction(direction, (1, 0, 0))


def rotation_from_axis_direction(direction, source_axis):
    """Returns a rotation vector that rotates the source_axis to the given direction"""

    # the direction of the rotation is the cross product between y and target
    axis = np.cross(direction, source_axis)

    if np.linalg.norm(axis) < 1e-9:
        # axis are perpendicular
        # but may still be in exactly opposite direction
        if np.dot(direction, source_axis) > 0:
            return (0, 0, 0)
        else:
            return (0, 0, 180)

    axis = axis / np.linalg.norm(axis)  # normalize

    # the required angle of rotation is best calculated using the atan2

    # construct the y / target plane
    perp = np.cross(axis, source_axis)  # no need to normalize

    compx = np.dot(direction, source_axis)
    compy = np.dot(direction, perp)

    angle = np.arctan2(compy, compx)

    return np.rad2deg(angle * axis)


def angle_between_rotvects(v1, v2):
    """Returns the angle of rotation required to rotate from v1 to v2 via the shortest path"""

    R1 = Rotation.from_rotvec(rotvec=v1, degrees=True)
    R2 = Rotation.from_rotvec(rotvec=v2, degrees=True)

    relative = R1.inv() * R2
    return np.rad2deg(relative.magnitude())


def round3d(value):
    """Rounds to three decimal places, the expected way; not the numpy way (ie: 0.0005 --> 0.001)"""
    value = np.array(value, dtype=float)
    offset = 0.0005 * np.ones_like(value)

    return np.floor(1000 * np.array(value + offset, dtype=float)) / 1000


def remove_duplicates_from_list_keep_order(seq):
    """Returns a copy of the list (or tuple) with duplicated removed
    See: https://stackoverflow.com/questions/480214/how-do-you-remove-duplicates-from-a-list-whilst-preserving-order
    """
    seen = set()
    seen_add = seen.add
    return [x for x in seq if not (x in seen or seen_add(x))]


def sort_by_name(nodes):
    """Returns a sorted list of nodes by name in alphabetical order"""
    nodes = list(nodes)
    nodes.sort(key=lambda x: x.name, reverse=False)
    return nodes


def get_all_files_with_extension(root_dir, extension, include_subdirs=True):
    """Returns a list of str with files matching the given parameters.
    extension can be a string or a list of strings"""

    # if extension.startswith("."):
    #     extension = extension[1:]
    #
    # if include_subdirs:
    #     a = glob(pathname=f"**/*.{extension}", root_dir=root_dir, recursive=True)
    # else:
    #     a = glob(pathname=f"*.{extension}", root_dir=root_dir, recursive=False)
    #
    # return a

    if isinstance(extension, str):
        extension = [extension]

    extensions = [ext.lstrip(".") for ext in extension]

    files = []
    for root, _, filenames in os.walk(root_dir):
        for filename in filenames:
            if any(filename.endswith(ext) for ext in extensions):
                files.append(os.path.join(root, filename))
        if not include_subdirs:
            break

    # remove root_dir from the path
    files = [f[len(str(root_dir)) + 1 :] for f in files]

    return files


def align_y0_axis_and_below_half_height(ax1, ax2):
    """Aligns the y0 axis of the two given axes



    Source: the internet
    """

    ax1_ylims = ax1.axes.get_ylim()  # Find y-axis limits set by the plotter
    ax2_ylims = ax2.axes.get_ylim()  # Find y-axis limits set by the plotter

    if (
        -ax1_ylims[0] > ax1_ylims[1] or -ax2_ylims[0] > ax2_ylims[1]
    ):  #  More data below 0 than above
        # move 0 line to center
        max1 = max(abs(ax1_ylims[0]), abs(ax1_ylims[1]))
        max2 = max(abs(ax2_ylims[0]), abs(ax2_ylims[1]))

        ax1.set_ylim((-max1, max1))
        ax2.set_ylim((-max2, max2))
        return

    ax1_yratio = (
        ax1_ylims[0] / ax1_ylims[1]
    )  # Calculate ratio of lowest limit to highest limit
    ax2_yratio = (
        ax2_ylims[0] / ax2_ylims[1]
    )  # Calculate ratio of lowest limit to highest limit

    # If the plot limits ratio of plot 1 is smaller than plot 2, the first data set has
    # a wider range than the second data set. Calculate a new low limit for the
    # second data set to obtain a similar ratio to the first data set.
    # Else, do it the other way around

    if ax1_yratio < ax2_yratio:
        ax2.set_ylim(bottom=ax2_ylims[1] * ax1_yratio)
    else:
        ax1.set_ylim(bottom=ax1_ylims[1] * ax2_yratio)

    #


def debug_yml_dump(d):
    """Checks if the dict can be dumped to yml, if not then
    raises a sensible error message"""
    from yaml import safe_dump

    for key, value in d.items():
        if isinstance(value, dict):
            debug_yml_dump(value)
            continue

        if isinstance(value, list):
            for v in value:
                if isinstance(v, dict):
                    debug_yml_dump(v)
                else:
                    try:
                        safe_dump(v)
                    except:
                        raise ValueError(
                            f"Failed to dump {key, v} to YML. Type of value is {type(v)}"
                        )

            continue

        try:
            safe_dump(value)
        except:
            raise ValueError(
                f"Failed to dump key '{key}' with value {value} to YML. Type of value is {type(value)}"
            )


"""
 # We need to make sure that there are no clashes with the names
            # In the target scene the name
            # prefix + name needs to be available
            # in the private scene the suggested_name needs to be available if it is not the same as the name

            new_name = get_two_scene_available_name_like(
                current_name=node.name,
                target_scene_names=target.node_names,
                prefix=prefix,
                private_scene_names=self.private_scene.node_names,
            )"""


def get_two_scene_available_name_like(
    current_name: str,
    target_scene_names: tuple[str],
    prefix: str,
    private_scene_names: tuple[str],
):
    """Returns a name that is available in both scenes"""

    assert (
        current_name in private_scene_names
    ), f"The current name {current_name} should be in the private scene"

    # First check if the current name is available in the target scene
    if prefix + current_name not in target_scene_names:
        return current_name

    # we need to come-up with a good suggestion
    suggested_name = current_name

    while True:
        suggested_name = increment_string_end(suggested_name)
        if prefix + suggested_name not in target_scene_names:
            if suggested_name not in private_scene_names:
                return suggested_name

def something_orthogonal_to(x):
    """Returns a vector that is orthogonal to the given vector x
    such that the dot product between x and the result is zero"""

    if abs(x[0]) > 1e-20:
        return np.array([x[1], -x[0], 0])
    elif abs(x[1]) > 1e-20:
        return np.array([x[1], -x[0], 0])
    elif abs(x[2]) > 1e-20:
        return np.array([0, x[2], -x[1]])
    else:
        return np.array([1, 0, 0])