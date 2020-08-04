"""
rigging.py

This module supplies additional functionality for working with rigging.


"""

"""
  This Source Code Form is subject to the terms of the Mozilla Public
  License, v. 2.0. If a copy of the MPL was not distributed with this
  file, You can obtain one at http://mozilla.org/MPL/2.0/.

  Ruben de Bruin - 2019
"""


# Superseeded by the sling node
#
# def create_sling(s, name, Ltotal, LeyeA, LeyeB, LspliceA, LspliceB, diameter, EA, mass, endA = None, endB=None, sheave=None):
#     """
#     Creates a new sling and adds it to scene s.
#
#     endA
#     eyeA (cable)
#     splice (body , mass/2)
#     nodeA (cable)     [optional: runs over sheave]
#     splice (body, mass/2)
#     eyeB (cable)
#     endB
#
#     Args:
#         s:     The scene in which the sling should be created
#         name:  Name prefix
#         Ltotal: Total length measured between the inside of the eyes of the sling is pulled straight.
#         LeyeA: Total inside length in eye A if stretched flat
#         LeyeB: Total inside length in eye B if stretched flat
#         LspliceA: Length of the splice at end A
#         LspliceB: Length of the splice at end B
#         diameter: Diameter of the sling
#         EA: EA of the wire
#         mass: total mass
#         endA : Sheave or poi to fix end A of the sling to [optional]
#         endB : Sheave or poi to fix end A of the sling to [optional]
#         sheave : Sheave or poi for the nodeA part of the sling
#
#     Returns:
#
#     """
#
#     # create the two splices
#
#     sa = s.new_rigidbody(name + '_spliceA', mass = mass/2, fixed=False)
#     a1= s.new_point(name + '_spliceA1', parent=sa, position = (LspliceA/2, diameter/2, 0))
#     a2 = s.new_point(name + '_spliceA2', parent=sa, position=(LspliceA / 2, -diameter / 2, 0))
#     am = s.new_point(name + '_spliceAM', parent=sa, position=(-LspliceA / 2, 0, 0))
#
#     s.new_visual(name + '_spliceA_visual', parent=sa,  path=r'cylinder 1x1x1 lowres.obj',
#                  offset=(-LspliceA/2, 0.0, 0.0),
#                  rotation=(0.0, 90.0, 0.0),
#                  scale=(LspliceA, 2*diameter, diameter))
#
#     sb = s.new_rigidbody(name + '_spliceB', mass = mass/2, rotation = (0,0,180),fixed=False)
#     b1 = s.new_point(name + '_spliceB1', parent=sb, position = (LspliceB/2, diameter/2, 0))
#     b2 = s.new_point(name + '_spliceB2', parent=sb, position=(LspliceB / 2, -diameter / 2, 0))
#     bm = s.new_point(name + '_spliceBM', parent=sb, position=(-LspliceB / 2, 0, 0))
#
#     s.new_visual(name + '_spliceB_visual', parent=sb, path=r'cylinder 1x1x1 lowres.obj',
#                  offset=(-LspliceB / 2, 0.0, 0.0),
#                  rotation=(0.0, 90.0, 0.0),
#                  scale=(LspliceB, 2 * diameter, diameter))
#
#     # nodeA part
#
#     # The stiffness of the nodeA part is corrected to account for the stiffness of the splices.
#     # It is considered that the stiffness of the splices is two times that of the wire.
#     #
#     # Springs in series: 1/Ktotal = 1/k1 + 1/k2 + 1/k3
#
#     Lmain = Ltotal-LspliceA-LspliceB-LeyeA-LeyeB
#     ka = (2*EA / LspliceA)
#     kb = (2*EA / LspliceB)
#     kmain = (EA / Lmain)
#     k_total = 1 / ((1/ka) + (1/kmain) + (1/kb))
#
#     EAmain = k_total * Lmain
#
#     s.new_cable(name, endA = am, endB = bm, length=Lmain, EA=EAmain, diameter=diameter, sheaves=sheave)
#
#     # eyes
#     if endA is None:
#         endA = []
#     if endB is None:
#         endB = []
#
#     s.new_cable(name + '_eyeA', endA = a1, endB=a2, length = LeyeA * 2 - diameter, EA=EA, diameter=diameter, sheaves = endA)
#     s.new_cable(name + '_eyeB', endA=b1, endB=b2, length=LeyeB * 2 - diameter, EA = EA, diameter=diameter, sheaves = endB)
#


# Superseeded by Shackle node
# def create_shackle_gphd(s, name, wll):
#     """
#     Green-Pin Heavy Duty Bow Shackle BN
#
#     visual from: https://www.traceparts.com/en/product/green-pinr-p-6036-green-pinr-heavy-duty-bow-shackle-bn-hdgphm0800-mm?CatalogPath=TRACEPARTS%3ATP04001002006&Product=10-04072013-086517&PartNumber=HDGPHM0800
#     details from: https://www.greenpin.com/sites/default/files/2019-04/brochure-april-2019.pdf
#
#     wll a b c d e f g h i j k weight
#     [t] [mm]  [kg]
#     120 95 95 208 95 147 400 238 647 453 428 50 110
#     150 105 108 238 105 169 410 275 688 496 485 50 160
#     200 120 130 279 120 179 513 290 838 564 530 70 235
#     250 130 140 299 130 205 554 305 904 614 565 70 295
#     300 140 150 325 140 205 618 305 996 644 585 80 368
#     400 170 175 376 164 231 668 325 1114 690 665 70 560
#     500 180 185 398 164 256 718 350 1190 720 710 70 685
#     600 200 205 444 189 282 718 375 1243 810 775 70 880
#     700 210 215 454 204 308 718 400 1263 870 820 70 980
#     800 210 220 464 204 308 718 400 1270 870 820 70 1100
#     900 220 230 485 215 328 718 420 1296 920 860 70 1280
#     1000 240 240 515 215 349 718 420 1336 940 900 70 1460
#     1250 260 270 585 230 369 768 450 1456 1025 970 70 1990
#     1500 280 290 625 230 369 818 450 1556 1025 1010 70 2400
#
#     Returns:
#
#     """
#     data = dict()
#     # key = wll in t
#     # dimensions a..k in [mm]
#     #             a     b    c   d     e    f    g    h     i     j    k   weight[kg]
#     # index       0     1    2    3    4    5    6    7     8     9    10   11
#     data[120] =  (95 ,  95, 208, 95 , 147, 400, 238, 647 , 453 , 428 , 50, 110)
#     data[150] =  (105, 108, 238, 105, 169, 410, 275, 688 , 496 , 485 , 50, 160)
#     data[200] =  (120, 130, 279, 120, 179, 513, 290, 838 , 564 , 530 , 70, 235)
#     data[250] =  (130, 140, 299, 130, 205, 554, 305, 904 , 614 , 565 , 70, 295)
#     data[300] =  (140, 150, 325, 140, 205, 618, 305, 996 , 644 , 585 , 80, 368)
#     data[400] =  (170, 175, 376, 164, 231, 668, 325, 1114, 690 , 665 , 70, 560)
#     data[500] =  (180, 185, 398, 164, 256, 718, 350, 1190, 720 , 710 , 70, 685)
#     data[600] =  (200, 205, 444, 189, 282, 718, 375, 1243, 810 , 775 , 70, 880)
#     data[700] =  (210, 215, 454, 204, 308, 718, 400, 1263, 870 , 820 , 70, 980)
#     data[800] =  (210, 220, 464, 204, 308, 718, 400, 1270, 870 , 820 , 70, 1100)
#     data[900] =  (220, 230, 485, 215, 328, 718, 420, 1296, 920 , 860 , 70, 1280)
#     data[1000] = (240, 240, 515, 215, 349, 718, 420, 1336, 940 , 900 , 70, 1460)
#     data[1250] = (260, 270, 585, 230, 369, 768, 450, 1456, 1025, 970 , 70, 1990)
#     data[1500] = (280, 290, 625, 230, 369, 818, 450, 1556, 1025, 1010, 70, 2400)
#
#     if wll not in data:
#         for key in data.keys():
#             print(key)
#         raise ValueError('No data available for a Green-Pin Heavy Duty Bow Shackle BN with wll {wll}. Available values printed above')
#
#     values = data[wll]
#
#     weight = values[11] / 1000  # convert to tonne
#     pin_dia = values[1] / 1000
#     bow_dia = values[0] / 1000
#     bow_length_inside = values[5] / 1000
#     bow_circle_inside = values[6] / 1000
#
#     cogz = 0.5 * pin_dia + bow_length_inside / 3  # estimated
#
#     # origin is at center of pin
#     # z-axis up
#     # y-axis in direction of pin
#
#
#     body = s.new_rigidbody(name=name,
#                     mass=weight,
#                     cog=(0.0,
#                          0.0,
#                          cogz))
#     # pin
#     pin_poi = s.new_point(name=name + 'pin_poi',
#                           parent=body,
#                           position=(0.0,
#                         0.0,
#                         0.0))
#     s.new_circle(name=name + 'pin',
#                  parent=pin_poi,
#                  axis=(0.0, 1.0, 0.0),
#                  radius=pin_dia/2)
#
#     # bow
#     bow_poi = s.new_point(name=name + 'bow_poi',
#                           parent=body,
#                           position=(0.0,
#                         0.0,
#                         0.5*pin_dia + bow_length_inside + 0.5 * bow_dia))
#     s.new_circle(name=name + 'bow',
#                  parent=bow_poi,
#                  axis=(0.0, 1.0, 0.0),
#                  radius=bow_dia/2)
#
#     # inside circle
#     inside_poi = s.new_point(name =name + 'inside_circle_center',
#                              parent = body,
#                              position = (0,0,
#                                        0.5*pin_dia + bow_length_inside - 0.5*bow_circle_inside))
#     s.new_circle(name =name + 'inside',
#                  parent = inside_poi,
#                  axis = (1.0,0,0),
#                  radius = bow_circle_inside/2)
#
#     # determine the scale for the shackle
#     # based on a GP800
#     #
#
#     actual_size = 0.5*pin_dia + 0.5*bow_dia + bow_length_inside
#     gp800_size = 0.5 * 0.210 + 0.5 * 0.220 + 0.718
#
#     scale = actual_size / gp800_size
#
#     # code for GP800_visual
#     s.new_visual(name=name + '_visual',
#                  parent=body,
#                  path=r'shackle_gp800.obj',
#                  offset=(0, 0, 0),
#                  rotation=(0, 0, 0),
#                  scale=(scale, scale, scale))
#
#     return body
# #
# # # def sheave_connect_context_menu(sheave1, sheave2, callback, pos):
# # #     # sheave1, sheave2 : sheave elements
# # #     # callback : function to be called with code to run
# # #     # pos : globLoc = self.treeView.mapToGlobal(event.pos())
# # #
# #     drop = sheave1.name
# #     onto = sheave2.name
# # #
# # #     # pop up a contect menu
# # #     menu = QMenu()
# # #
# # #     info = f"... About create a Pin-Hole connection with {drop} as pin and and {onto} as hole:"
# # #
# # #     menu.addAction(info, None)
# # #     menu.addSeparator()
# # #
# # #     name = f"{drop} inside {onto}"
# # #
# # #     def create_master():
# # #         code = f"s.new_geometriccontact('{name}','{drop}','{onto}')"
# # #         callback(code)
# # #
# # #     def create_slave():
# #         code = f"s.new_geometriccontact('{name}','{drop}','{onto}', inverse_relation = True)"
# # #         callback(code)
# # #
# # #     menu.addAction(f"Create pin-hole connection with {onto} as nodeA", create_master)
# # #     menu.addAction(f"Create pin-hole connection with {drop} as nodeA", create_slave)
# # #
# # #
# # #     menu.exec_(pos)
