"""Tests the slicing function"""
from matplotlib import pyplot as plt
from vtkmodules.vtkCommonCore import vtkLogger

from DAVE import *
from DAVE.visual_helpers.vtkHelpers import *

def test_slice():
    s = Scene()

    # print(s.get_resource_list('.obj'))

    v = s.new_visual('Visual', path = "res: cube_with_bevel.obj")

    fig,ax = plt.subplots()

    x,y  = VisualToSlice(v, ax=ax)
    v.scale = (2,2,2)
    v.rotation = (0,0,45)

    VisualToSlice(v, ax=ax)


    plt.plot(x,y)

    # plt.show()