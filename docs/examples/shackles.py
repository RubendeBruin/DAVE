from DAVE.scene import *
from DAVE.rigging import create_shackle_gphd
# from DAVE.tools import rotation_from_y_axis_direction

s = Scene()

sizes = (120,150,200,250,300,400,500,600,700,800,900,1000,1250,1500)
# sizes = (1250,1500)

for gp in sizes:
    b = create_shackle_gphd(s, f'sh{gp}', gp)
    b.x = gp / 100
s.new_geometriccontact("quick_action", "sh1500pin", "sh1250inside")
s.delete("sh1500") # <-- this actually decouples the connection !!!

s.print_node_tree()


#
# s.new_geometriccontact("quick_action_1", "sh1000inside", "sh1500bow")
#
# s['sh1250'].fixed = (True, True, True, False, True, True)
# s['sh1250'].mass = 1.99
#
# s['sh1250'].rotation = (5.0, 0.0, 0.0)
# s['sh1250'].mass = 1.99
#
# s['sh1250'].rotation = (10.0, 0.0, 0.0)
# s['sh1250'].mass = 1.99
#
# s['sh1250'].rotation = (180.0, -5.0, 0.0)
# s['sh1250'].mass = 1.99
#
# s['sh1250'].rotation = (180.0, -10.0, 0.0)
# s['sh1250'].mass = 1.99
#
# s['sh1250'].rotation = (180.0, -15.0, 0.0)
# s['sh1250'].mass = 1.99
#
# s['sh1250'].rotation = (180.0, -20.0, 0.0)
# s['sh1250'].mass = 1.99
#
# s['sh1250'].rotation = (180.0, -10.0, 0.0)
# s['sh1250'].mass = 1.99
#
# s['sh1250'].rotation = (175.0, -10.0, 0.0)
# s['sh1250'].mass = 1.99
#
# s['sh1250'].rotation = (170.0, -10.0, 0.0)
# s['sh1250'].mass = 1.99
#
# s['sh1250'].rotation = (165.0, -10.0, 0.0)
# s['sh1250'].mass = 1.99
#
# s['sh1250'].rotation = (160.0, -10.0, 0.0)
# s['sh1250'].mass = 1.99
#
# s['sh1250'].rotation = (150.0, -10.0, 0.0)
# s['sh1250'].mass = 1.99
#
# s['sh1250'].rotation = (140.0, -10.0, 0.0)
# s['sh1250'].mass = 1.99
#
# s['quick_action_1'].flipped = True
#
# s['quick_action_1'].flipped = False
#
# s['quick_action_1'].flipped = True
#
# s['quick_action_1'].flipped = False
#
# s['quick_action_1'].flipped = True
#
# s['quick_action_1'].flipped = False
#
# s['quick_action_1'].flipped = True
#
# s['quick_action_1'].flipped = False
#
# s['quick_action_1'].flipped = True
# s.delete("quick_action_1")
#
#
# s['sh1000'].position = (12.5, -0.0, -3.021)
# s['sh1000'].rotation = (127.279, 127.279, -0.0)
# s['sh1000'].cog = (0.0, 0.0, 0.359)
#
# s['sh1000'].position = (12.5, -0.0, -5.021)
# s['sh1000'].rotation = (127.279, 127.279, -0.0)
#
# s['sh1000'].position = (12.5, -0.0, -6.021)
# s['sh1000'].rotation = (127.279, 127.279, -0.0)
#
# s['sh1000'].position = (12.5, -0.0, -7.021)
# s['sh1000'].rotation = (127.279, 127.279, -0.0)
# s.new_geometriccontact("quick_action_1", "sh1000inside", "sh900pin")
# s.new_geometriccontact("quick_action_4", "sh800inside", "sh1000pin")
# s.new_geometriccontact("quick_action_5", "sh700inside", "sh800pin")
# s.new_geometriccontact("quick_action_6", "sh600inside", "sh700pin")
# s.new_cable("quick_action_7", poiA="sh600pin", poiB = "sh500inside")
#
# s['quick_action_7'].length = 6.0
# s['quick_action_7'].connections = ('sh600pin','sh500inside')
#
# s['quick_action_7'].EA = 1.0
# s['quick_action_7'].connections = ('sh600pin','sh500inside')
#
# s['quick_action_7'].EA = 10.0
# s['quick_action_7'].connections = ('sh600pin','sh500inside')
#
# s['quick_action_7'].EA = 100.0
# s['quick_action_7'].connections = ('sh600pin','sh500inside')
#
# s['quick_action_7'].EA = 1000.0
# s['quick_action_7'].connections = ('sh600pin','sh500inside')
#
# # auto generated pyhton code
# # By beneden
# # Time: 2020-05-21 09:49:31 UTC
#
# # To be able to distinguish the important number (eg: fixed positions) from
# # non-important numbers (eg: a position that is solved by the static solver) we use a dummy-function called 'solved'.
# # For anything written as solved(number) that actual number does not influence the static solution
# def solved(number):
#     return number
#
# # code for sh120
# s.new_rigidbody(name='sh120',
#                 mass=0.11000000000000001,
#                 cog=(0.0,
#                      0.0,
#                      0.18083333333333335),
#                 position=(1.2,
#                           0.0,
#                           0.0),
#                 rotation=(0.0,
#                           0.0,
#                           0.0),
#                 fixed =(True, True, True, True, True, True) )
# # code for sh150
# s.new_rigidbody(name='sh150',
#                 mass=0.16,
#                 cog=(0.0,
#                      0.0,
#                      0.19066666666666665),
#                 position=(1.5,
#                           0.0,
#                           0.0),
#                 rotation=(0.0,
#                           0.0,
#                           0.0),
#                 fixed =(True, True, True, True, True, True) )
# # code for sh200
# s.new_rigidbody(name='sh200',
#                 mass=0.23499999999999996,
#                 cog=(0.0,
#                      0.0,
#                      0.23600000000000002),
#                 position=(2.0,
#                           0.0,
#                           0.0),
#                 rotation=(0.0,
#                           0.0,
#                           0.0),
#                 fixed =(True, True, True, True, True, True) )
# # code for sh250
# s.new_rigidbody(name='sh250',
#                 mass=0.295,
#                 cog=(0.0,
#                      0.0,
#                      0.2546666666666667),
#                 position=(2.5,
#                           0.0,
#                           0.0),
#                 rotation=(0.0,
#                           0.0,
#                           0.0),
#                 fixed =(True, True, True, True, True, True) )
# # code for sh300
# s.new_rigidbody(name='sh300',
#                 mass=0.368,
#                 cog=(0.0,
#                      0.0,
#                      0.28099999999999997),
#                 position=(3.0,
#                           0.0,
#                           0.0),
#                 rotation=(0.0,
#                           0.0,
#                           0.0),
#                 fixed =(True, True, True, True, True, True) )
# # code for sh400
# s.new_rigidbody(name='sh400',
#                 mass=0.56,
#                 cog=(0.0,
#                      0.0,
#                      0.3101666666666667),
#                 position=(4.0,
#                           0.0,
#                           0.0),
#                 rotation=(0.0,
#                           0.0,
#                           0.0),
#                 fixed =(True, True, True, True, True, True) )
# # code for sh500
# s.new_rigidbody(name='sh500',
#                 mass=0.685,
#                 cog=(0.0,
#                      0.0,
#                      0.3318333333333333),
#                 position=(5.0,
#                           0.0,
#                           0.0),
#                 rotation=(0.0,
#                           0.0,
#                           0.0),
#                 fixed =(True, True, True, True, True, True) )
# # code for sh900
# s.new_rigidbody(name='sh900',
#                 mass=1.28,
#                 cog=(0.0,
#                      0.0,
#                      0.35433333333333333),
#                 position=(9.0,
#                           0.0,
#                           0.0),
#                 rotation=(0.0,
#                           0.0,
#                           0.0),
#                 fixed =(True, True, True, True, True, True) )
# # code for sh1250
# s.new_rigidbody(name='sh1250',
#                 mass=1.9900000000000002,
#                 cog=(0.0,
#                      0.0,
#                      0.391),
#                 position=(12.5,
#                           0.0,
#                           0.0),
#                 rotation=(solved(-179.99999999936628),
#                           0.0,
#                           0.0),
#                 fixed =(True, True, True, False, True, True) )
# # code for sh120pin_poi
# s.new_point(name='sh120pin_poi',
#           parent='sh120',
#           position=(0.0,
#                     0.0,
#                     0.0))
# # code for sh120bow_poi
# s.new_point(name='sh120bow_poi',
#           parent='sh120',
#           position=(0.0,
#                     0.0,
#                     0.495))
# # code for sh120inside_circle_center
# s.new_point(name='sh120inside_circle_center',
#           parent='sh120',
#           position=(0.0,
#                     0.0,
#                     0.3285))
# # code for sh120_visual
# s.new_visual(name='sh120_visual',
#             parent='sh120',
#             path=r'shackle_gp800.obj',
#             offset=(0, 0, 0),
#             rotation=(0, 0, 0),
#             scale=(0.5305466237942122, 0.5305466237942122, 0.5305466237942122) )
# # code for sh150pin_poi
# s.new_point(name='sh150pin_poi',
#           parent='sh150',
#           position=(0.0,
#                     0.0,
#                     0.0))
# # code for sh150bow_poi
# s.new_point(name='sh150bow_poi',
#           parent='sh150',
#           position=(0.0,
#                     0.0,
#                     0.5165))
# # code for sh150inside_circle_center
# s.new_point(name='sh150inside_circle_center',
#           parent='sh150',
#           position=(0.0,
#                     0.0,
#                     0.32649999999999996))
# # code for sh150_visual
# s.new_visual(name='sh150_visual',
#             parent='sh150',
#             path=r'shackle_gp800.obj',
#             offset=(0, 0, 0),
#             rotation=(0, 0, 0),
#             scale=(0.5535905680600214, 0.5535905680600214, 0.5535905680600214) )
# # code for sh200pin_poi
# s.new_point(name='sh200pin_poi',
#           parent='sh200',
#           position=(0.0,
#                     0.0,
#                     0.0))
# # code for sh200bow_poi
# s.new_point(name='sh200bow_poi',
#           parent='sh200',
#           position=(0.0,
#                     0.0,
#                     0.6380000000000001))
# # code for sh200inside_circle_center
# s.new_point(name='sh200inside_circle_center',
#           parent='sh200',
#           position=(0.0,
#                     0.0,
#                     0.43300000000000005))
# # code for sh200_visual
# s.new_visual(name='sh200_visual',
#             parent='sh200',
#             path=r'shackle_gp800.obj',
#             offset=(0, 0, 0),
#             rotation=(0, 0, 0),
#             scale=(0.6838156484458736, 0.6838156484458736, 0.6838156484458736) )
# # code for sh250pin_poi
# s.new_point(name='sh250pin_poi',
#           parent='sh250',
#           position=(0.0,
#                     0.0,
#                     0.0))
# # code for sh250bow_poi
# s.new_point(name='sh250bow_poi',
#           parent='sh250',
#           position=(0.0,
#                     0.0,
#                     0.6890000000000001))
# # code for sh250inside_circle_center
# s.new_point(name='sh250inside_circle_center',
#           parent='sh250',
#           position=(0.0,
#                     0.0,
#                     0.47150000000000014))
# # code for sh250_visual
# s.new_visual(name='sh250_visual',
#             parent='sh250',
#             path=r'shackle_gp800.obj',
#             offset=(0, 0, 0),
#             rotation=(0, 0, 0),
#             scale=(0.7384780278670955, 0.7384780278670955, 0.7384780278670955) )
# # code for sh300pin_poi
# s.new_point(name='sh300pin_poi',
#           parent='sh300',
#           position=(0.0,
#                     0.0,
#                     0.0))
# # code for sh300bow_poi
# s.new_point(name='sh300bow_poi',
#           parent='sh300',
#           position=(0.0,
#                     0.0,
#                     0.7629999999999999))
# # code for sh300inside_circle_center
# s.new_point(name='sh300inside_circle_center',
#           parent='sh300',
#           position=(0.0,
#                     0.0,
#                     0.5405))
# # code for sh300_visual
# s.new_visual(name='sh300_visual',
#             parent='sh300',
#             path=r'shackle_gp800.obj',
#             offset=(0, 0, 0),
#             rotation=(0, 0, 0),
#             scale=(0.8177920685959272, 0.8177920685959272, 0.8177920685959272) )
# # code for sh400pin_poi
# s.new_point(name='sh400pin_poi',
#           parent='sh400',
#           position=(0.0,
#                     0.0,
#                     0.0))
# # code for sh400bow_poi
# s.new_point(name='sh400bow_poi',
#           parent='sh400',
#           position=(0.0,
#                     0.0,
#                     0.8405))
# # code for sh400inside_circle_center
# s.new_point(name='sh400inside_circle_center',
#           parent='sh400',
#           position=(0.0,
#                     0.0,
#                     0.5930000000000001))
# # code for sh400_visual
# s.new_visual(name='sh400_visual',
#             parent='sh400',
#             path=r'shackle_gp800.obj',
#             offset=(0, 0, 0),
#             rotation=(0, 0, 0),
#             scale=(0.9008574490889605, 0.9008574490889605, 0.9008574490889605) )
# # code for sh500pin_poi
# s.new_point(name='sh500pin_poi',
#           parent='sh500',
#           position=(0.0,
#                     0.0,
#                     0.0))
# # code for sh500bow_poi
# s.new_point(name='sh500bow_poi',
#           parent='sh500',
#           position=(0.0,
#                     0.0,
#                     0.9005))
# # code for sh500inside_circle_center
# s.new_point(name='sh500inside_circle_center',
#           parent='sh500',
#           position=(0.0,
#                     0.0,
#                     0.6355))
# # code for sh500_visual
# s.new_visual(name='sh500_visual',
#             parent='sh500',
#             path=r'shackle_gp800.obj',
#             offset=(0, 0, 0),
#             rotation=(0, 0, 0),
#             scale=(0.9651661307609861, 0.9651661307609861, 0.9651661307609861) )
# # code for sh900bow_poi
# s.new_point(name='sh900bow_poi',
#           parent='sh900',
#           position=(0.0,
#                     0.0,
#                     0.943))
# # code for sh900inside_circle_center
# s.new_point(name='sh900inside_circle_center',
#           parent='sh900',
#           position=(0.0,
#                     0.0,
#                     0.623))
# # code for sh900_visual
# s.new_visual(name='sh900_visual',
#             parent='sh900',
#             path=r'shackle_gp800.obj',
#             offset=(0, 0, 0),
#             rotation=(0, 0, 0),
#             scale=(1.0107181136120043, 1.0107181136120043, 1.0107181136120043) )
# # code for sh1250pin_poi
# s.new_point(name='sh1250pin_poi',
#           parent='sh1250',
#           position=(0.0,
#                     0.0,
#                     0.0))
# # code for sh1250bow_poi
# s.new_point(name='sh1250bow_poi',
#           parent='sh1250',
#           position=(0.0,
#                     0.0,
#                     1.033))
# # code for sh1250_visual
# s.new_visual(name='sh1250_visual',
#             parent='sh1250',
#             path=r'shackle_gp800.obj',
#             offset=(0, 0, 0),
#             rotation=(0, 0, 0),
#             scale=(1.1071811361200428, 1.1071811361200428, 1.1071811361200428) )
# # This is the code for the elements managed by quick_action
# # First create the elements that need to exist before the connection can be made
# # The slaved system is here created with None as parent. This will be changed when the connection is created
# # code for sh1500
# s.new_rigidbody(name='sh1500',
#                 mass=2.4,
#                 cog=(0.0,
#                      0.0,
#                      0.41766666666666663),
#                 position=(0.0,
#                           0.0,
#                           0.0),
#                 rotation=(0.0,
#                           0.0,
#                           0.0),
#                 fixed =(True, True, True, True, True, True) )
# # code for sh1500pin_poi
# s.new_point(name='sh1500pin_poi',
#           parent='sh1500',
#           position=(0.0,
#                     0.0,
#                     0.0))
# # code for sh1500pin
# s.new_circle(name='sh1500pin',
#             parent='sh1500pin_poi',
#             axis=(0.0, 1.0, 0.0),
#             radius=0.145 )
# # code for sh1250inside_circle_center
# s.new_point(name='sh1250inside_circle_center',
#           parent='sh1250',
#           position=(0.0,
#                     0.0,
#                     0.678))
# # code for sh1250inside
# s.new_circle(name='sh1250inside',
#             parent='sh1250inside_circle_center',
#             axis=(1.0, 0.0, 0.0),
#             radius=0.225 )
# # now create the connection
# s.new_geometriccontact(name = 'quick_action',
#                        item1 = 'sh1500pin',
#                        item2 = 'sh1250inside')
# # This is the code for the elements managed by quick_action_1
# # First create the elements that need to exist before the connection can be made
# # The slaved system is here created with None as parent. This will be changed when the connection is created
# # code for sh1000
# s.new_rigidbody(name='sh1000',
#                 mass=1.46,
#                 cog=(0.0,
#                      0.0,
#                      0.359),
#                 position=(-6.668601455273645e-16,
#                           4.235164736271502e-22,
#                           -0.6279999999999999),
#                 rotation=(6.677624597059091e-15,
#                           3.493934275821372e-14,
#                           90.0),
#                 fixed =(True, True, True, True, True, True) )
# # code for sh1000inside_circle_center
# s.new_point(name='sh1000inside_circle_center',
#           parent='sh1000',
#           position=(0.0,
#                     0.0,
#                     0.628))
# # code for sh1000inside
# s.new_circle(name='sh1000inside',
#             parent='sh1000inside_circle_center',
#             axis=(1.0, 0.0, 0.0),
#             radius=0.21 )
# # code for sh900pin_poi
# s.new_point(name='sh900pin_poi',
#           parent='sh900',
#           position=(0.0,
#                     0.0,
#                     0.0))
# # code for sh900pin
# s.new_circle(name='sh900pin',
#             parent='sh900pin_poi',
#             axis=(0.0, 1.0, 0.0),
#             radius=0.115 )
# # now create the connection
# s.new_geometriccontact(name = 'quick_action_1',
#                        item1 = 'sh1000inside',
#                        item2 = 'sh900pin')
# # code for sh120pin
# s.new_circle(name='sh120pin',
#             parent='sh120pin_poi',
#             axis=(0.0, 1.0, 0.0),
#             radius=0.0475 )
# # code for sh120bow
# s.new_circle(name='sh120bow',
#             parent='sh120bow_poi',
#             axis=(0.0, 1.0, 0.0),
#             radius=0.0475 )
# # code for sh120inside
# s.new_circle(name='sh120inside',
#             parent='sh120inside_circle_center',
#             axis=(1.0, 0.0, 0.0),
#             radius=0.119 )
# # code for sh150pin
# s.new_circle(name='sh150pin',
#             parent='sh150pin_poi',
#             axis=(0.0, 1.0, 0.0),
#             radius=0.054 )
# # code for sh150bow
# s.new_circle(name='sh150bow',
#             parent='sh150bow_poi',
#             axis=(0.0, 1.0, 0.0),
#             radius=0.0525 )
# # code for sh150inside
# s.new_circle(name='sh150inside',
#             parent='sh150inside_circle_center',
#             axis=(1.0, 0.0, 0.0),
#             radius=0.1375 )
# # code for sh200pin
# s.new_circle(name='sh200pin',
#             parent='sh200pin_poi',
#             axis=(0.0, 1.0, 0.0),
#             radius=0.065 )
# # code for sh200bow
# s.new_circle(name='sh200bow',
#             parent='sh200bow_poi',
#             axis=(0.0, 1.0, 0.0),
#             radius=0.06 )
# # code for sh200inside
# s.new_circle(name='sh200inside',
#             parent='sh200inside_circle_center',
#             axis=(1.0, 0.0, 0.0),
#             radius=0.145 )
# # code for sh250pin
# s.new_circle(name='sh250pin',
#             parent='sh250pin_poi',
#             axis=(0.0, 1.0, 0.0),
#             radius=0.07 )
# # code for sh250bow
# s.new_circle(name='sh250bow',
#             parent='sh250bow_poi',
#             axis=(0.0, 1.0, 0.0),
#             radius=0.065 )
# # code for sh250inside
# s.new_circle(name='sh250inside',
#             parent='sh250inside_circle_center',
#             axis=(1.0, 0.0, 0.0),
#             radius=0.1525 )
# # code for sh300pin
# s.new_circle(name='sh300pin',
#             parent='sh300pin_poi',
#             axis=(0.0, 1.0, 0.0),
#             radius=0.075 )
# # code for sh300bow
# s.new_circle(name='sh300bow',
#             parent='sh300bow_poi',
#             axis=(0.0, 1.0, 0.0),
#             radius=0.07 )
# # code for sh300inside
# s.new_circle(name='sh300inside',
#             parent='sh300inside_circle_center',
#             axis=(1.0, 0.0, 0.0),
#             radius=0.1525 )
# # code for sh400pin
# s.new_circle(name='sh400pin',
#             parent='sh400pin_poi',
#             axis=(0.0, 1.0, 0.0),
#             radius=0.0875 )
# # code for sh400bow
# s.new_circle(name='sh400bow',
#             parent='sh400bow_poi',
#             axis=(0.0, 1.0, 0.0),
#             radius=0.085 )
# # code for sh400inside
# s.new_circle(name='sh400inside',
#             parent='sh400inside_circle_center',
#             axis=(1.0, 0.0, 0.0),
#             radius=0.1625 )
# # code for sh500pin
# s.new_circle(name='sh500pin',
#             parent='sh500pin_poi',
#             axis=(0.0, 1.0, 0.0),
#             radius=0.0925 )
# # code for sh500bow
# s.new_circle(name='sh500bow',
#             parent='sh500bow_poi',
#             axis=(0.0, 1.0, 0.0),
#             radius=0.09 )
# # code for sh500inside
# s.new_circle(name='sh500inside',
#             parent='sh500inside_circle_center',
#             axis=(1.0, 0.0, 0.0),
#             radius=0.175 )
# # code for sh900bow
# s.new_circle(name='sh900bow',
#             parent='sh900bow_poi',
#             axis=(0.0, 1.0, 0.0),
#             radius=0.11 )
# # code for sh900inside
# s.new_circle(name='sh900inside',
#             parent='sh900inside_circle_center',
#             axis=(1.0, 0.0, 0.0),
#             radius=0.21 )
# # code for sh1250pin
# s.new_circle(name='sh1250pin',
#             parent='sh1250pin_poi',
#             axis=(0.0, 1.0, 0.0),
#             radius=0.135 )
# # code for sh1250bow
# s.new_circle(name='sh1250bow',
#             parent='sh1250bow_poi',
#             axis=(0.0, 1.0, 0.0),
#             radius=0.13 )
# # code for sh1000bow_poi
# s.new_point(name='sh1000bow_poi',
#           parent='sh1000',
#           position=(0.0,
#                     0.0,
#                     0.958))
# # code for sh1000_visual
# s.new_visual(name='sh1000_visual',
#             parent='sh1000',
#             path=r'shackle_gp800.obj',
#             offset=(0, 0, 0),
#             rotation=(0, 0, 0),
#             scale=(1.0267952840300107, 1.0267952840300107, 1.0267952840300107) )
# # code for sh1500bow_poi
# s.new_point(name='sh1500bow_poi',
#           parent='sh1500',
#           position=(0.0,
#                     0.0,
#                     1.103))
# # code for sh1500inside_circle_center
# s.new_point(name='sh1500inside_circle_center',
#           parent='sh1500',
#           position=(0.0,
#                     0.0,
#                     0.738))
# # code for sh1500_visual
# s.new_visual(name='sh1500_visual',
#             parent='sh1500',
#             path=r'shackle_gp800.obj',
#             offset=(0, 0, 0),
#             rotation=(0, 0, 0),
#             scale=(1.182207931404073, 1.182207931404073, 1.182207931404073) )
# # This is the code for the elements managed by quick_action_4
# # First create the elements that need to exist before the connection can be made
# # The slaved system is here created with None as parent. This will be changed when the connection is created
# # code for sh800
# s.new_rigidbody(name='sh800',
#                 mass=1.1,
#                 cog=(0.0,
#                      0.0,
#                      0.34933333333333333),
#                 position=(0.0,
#                           0.0,
#                           -0.6279999999999999),
#                 rotation=(0.0,
#                           0.0,
#                           90.0),
#                 fixed =(True, True, True, True, True, True) )
# # code for sh800inside_circle_center
# s.new_point(name='sh800inside_circle_center',
#           parent='sh800',
#           position=(0.0,
#                     0.0,
#                     0.6279999999999999))
# # code for sh800inside
# s.new_circle(name='sh800inside',
#             parent='sh800inside_circle_center',
#             axis=(1.0, 0.0, 0.0),
#             radius=0.2 )
# # code for sh1000pin_poi
# s.new_point(name='sh1000pin_poi',
#           parent='sh1000',
#           position=(0.0,
#                     0.0,
#                     0.0))
# # code for sh1000pin
# s.new_circle(name='sh1000pin',
#             parent='sh1000pin_poi',
#             axis=(0.0, 1.0, 0.0),
#             radius=0.12 )
# # now create the connection
# s.new_geometriccontact(name = 'quick_action_4',
#                        item1 = 'sh800inside',
#                        item2 = 'sh1000pin')
# # code for sh1000bow
# s.new_circle(name='sh1000bow',
#             parent='sh1000bow_poi',
#             axis=(0.0, 1.0, 0.0),
#             radius=0.12 )
# # code for sh1500bow
# s.new_circle(name='sh1500bow',
#             parent='sh1500bow_poi',
#             axis=(0.0, 1.0, 0.0),
#             radius=0.14 )
# # code for sh1500inside
# s.new_circle(name='sh1500inside',
#             parent='sh1500inside_circle_center',
#             axis=(1.0, 0.0, 0.0),
#             radius=0.225 )
# # code for sh800bow_poi
# s.new_point(name='sh800bow_poi',
#           parent='sh800',
#           position=(0.0,
#                     0.0,
#                     0.9329999999999999))
# # code for sh800_visual
# s.new_visual(name='sh800_visual',
#             parent='sh800',
#             path=r'shackle_gp800.obj',
#             offset=(0, 0, 0),
#             rotation=(0, 0, 0),
#             scale=(1.0, 1.0, 1.0) )
# # This is the code for the elements managed by quick_action_5
# # First create the elements that need to exist before the connection can be made
# # The slaved system is here created with None as parent. This will be changed when the connection is created
# # code for sh700
# s.new_rigidbody(name='sh700',
#                 mass=0.9799999999999999,
#                 cog=(0.0,
#                      0.0,
#                      0.3468333333333333),
#                 position=(0.0,
#                           0.0,
#                           -0.6255),
#                 rotation=(0.0,
#                           0.0,
#                           90.0),
#                 fixed =(True, True, True, True, True, True) )
# # code for sh700inside_circle_center
# s.new_point(name='sh700inside_circle_center',
#           parent='sh700',
#           position=(0.0,
#                     0.0,
#                     0.6255))
# # code for sh700inside
# s.new_circle(name='sh700inside',
#             parent='sh700inside_circle_center',
#             axis=(1.0, 0.0, 0.0),
#             radius=0.2 )
# # code for sh800pin_poi
# s.new_point(name='sh800pin_poi',
#           parent='sh800',
#           position=(0.0,
#                     0.0,
#                     0.0))
# # code for sh800pin
# s.new_circle(name='sh800pin',
#             parent='sh800pin_poi',
#             axis=(0.0, 1.0, 0.0),
#             radius=0.11 )
# # now create the connection
# s.new_geometriccontact(name = 'quick_action_5',
#                        item1 = 'sh700inside',
#                        item2 = 'sh800pin')
# # code for sh800bow
# s.new_circle(name='sh800bow',
#             parent='sh800bow_poi',
#             axis=(0.0, 1.0, 0.0),
#             radius=0.105 )
# # code for sh700bow_poi
# s.new_point(name='sh700bow_poi',
#           parent='sh700',
#           position=(0.0,
#                     0.0,
#                     0.9305))
# # code for sh700_visual
# s.new_visual(name='sh700_visual',
#             parent='sh700',
#             path=r'shackle_gp800.obj',
#             offset=(0, 0, 0),
#             rotation=(0, 0, 0),
#             scale=(0.997320471596999, 0.997320471596999, 0.997320471596999) )
# # This is the code for the elements managed by quick_action_6
# # First create the elements that need to exist before the connection can be made
# # The slaved system is here created with None as parent. This will be changed when the connection is created
# # code for sh600
# s.new_rigidbody(name='sh600',
#                 mass=0.8800000000000001,
#                 cog=(0.0,
#                      0.0,
#                      0.3418333333333333),
#                 position=(0.0,
#                           0.0,
#                           -0.633),
#                 rotation=(0.0,
#                           0.0,
#                           90.0),
#                 fixed =(True, True, True, True, True, True) )
# # code for sh600inside_circle_center
# s.new_point(name='sh600inside_circle_center',
#           parent='sh600',
#           position=(0.0,
#                     0.0,
#                     0.633))
# # code for sh600inside
# s.new_circle(name='sh600inside',
#             parent='sh600inside_circle_center',
#             axis=(1.0, 0.0, 0.0),
#             radius=0.1875 )
# # code for sh700pin_poi
# s.new_point(name='sh700pin_poi',
#           parent='sh700',
#           position=(0.0,
#                     0.0,
#                     0.0))
# # code for sh700pin
# s.new_circle(name='sh700pin',
#             parent='sh700pin_poi',
#             axis=(0.0, 1.0, 0.0),
#             radius=0.1075 )
# # now create the connection
# s.new_geometriccontact(name = 'quick_action_6',
#                        item1 = 'sh600inside',
#                        item2 = 'sh700pin')
# # code for sh700bow
# s.new_circle(name='sh700bow',
#             parent='sh700bow_poi',
#             axis=(0.0, 1.0, 0.0),
#             radius=0.105 )
# # code for sh600pin_poi
# s.new_point(name='sh600pin_poi',
#           parent='sh600',
#           position=(0.0,
#                     0.0,
#                     0.0))
# # code for sh600bow_poi
# s.new_point(name='sh600bow_poi',
#           parent='sh600',
#           position=(0.0,
#                     0.0,
#                     0.9205))
# # code for sh600_visual
# s.new_visual(name='sh600_visual',
#             parent='sh600',
#             path=r'shackle_gp800.obj',
#             offset=(0, 0, 0),
#             rotation=(0, 0, 0),
#             scale=(0.9866023579849947, 0.9866023579849947, 0.9866023579849947) )
# # code for sh600pin
# s.new_circle(name='sh600pin',
#             parent='sh600pin_poi',
#             axis=(0.0, 1.0, 0.0),
#             radius=0.1025 )
# # code for sh600bow
# s.new_circle(name='sh600bow',
#             parent='sh600bow_poi',
#             axis=(0.0, 1.0, 0.0),
#             radius=0.1 )
# # code for quick_action_7
# s.new_cable(name='quick_action_7',
#             poiA='sh600pin',
#             poiB='sh500inside',
#             length=3.0,
#             EA=1000.0)
#
# # s.delete('sh900')

#
from DAVE.gui.main import Gui
Gui(s)
# Gui(s, geometry_scale=0.001, cog_scale=0.001)
