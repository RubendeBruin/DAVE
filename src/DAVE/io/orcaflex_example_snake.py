from DAVE import *
from DAVE.io.orcaflex import *

s = Scene()

# auto generated pyhton code
# By beneden
# Time: 2020-09-04 11:42:26 UTC

# To be able to distinguish the important number (eg: fixed positions) from
# non-important numbers (eg: a position that is solved by the static solver) we use a dummy-function called 'solved'.
# For anything written as solved(number) that actual number does not influence the static solution
def solved(number):
    return number

# code for base0
s.new_axis(name='base0',
           position=(0.0,
                     0.0,
                     0.0),
           rotation=(0.0,
                     0.0,
                     0.0),
           fixed =(True, True, True, True, True, True) )
# code for Poi_1
s.new_point(name='Poi_1',
          position=(10.0,
                    0.0,
                    0.0))
# code for base1
s.new_rigidbody(name='base1',
                mass=1.0,
                cog=(1.0,
                     0.0,
                     0.0),
                parent='base0',
                position=(2.0,
                          0.0,
                          0.0),
                rotation=(0.0,
                          solved(86.34581694281958),
                          0.0),
                fixed =(True, True, True, True, False, True) )
# code for base2
s.new_rigidbody(name='base2',
                mass=1.0,
                cog=(1.0,
                     0.0,
                     0.0),
                parent='base1',
                position=(2.0,
                          0.0,
                          0.0),
                rotation=(0.0,
                          solved(-0.46863800593441024),
                          0.0),
                fixed =(True, True, True, True, False, True) )
# code for base3
s.new_rigidbody(name='base3',
                mass=1.0,
                cog=(1.0,
                     0.0,
                     0.0),
                parent='base2',
                position=(2.0,
                          0.0,
                          0.0),
                rotation=(0.0,
                          solved(-0.6062112638784851),
                          0.0),
                fixed =(True, True, True, True, False, True) )
# code for base4
s.new_rigidbody(name='base4',
                mass=1.0,
                cog=(1.0,
                     0.0,
                     0.0),
                parent='base3',
                position=(2.0,
                          0.0,
                          0.0),
                rotation=(0.0,
                          solved(-0.814562825874697),
                          0.0),
                fixed =(True, True, True, True, False, True) )
# code for base5
s.new_rigidbody(name='base5',
                mass=1.0,
                cog=(1.0,
                     0.0,
                     0.0),
                parent='base4',
                position=(2.0,
                          0.0,
                          0.0),
                rotation=(0.0,
                          solved(-1.1520253709247628),
                          0.0),
                fixed =(True, True, True, True, False, True) )
# code for base6
s.new_rigidbody(name='base6',
                mass=1.0,
                cog=(1.0,
                     0.0,
                     0.0),
                parent='base5',
                position=(2.0,
                          0.0,
                          0.0),
                rotation=(0.0,
                          solved(-1.7520632892703707),
                          0.0),
                fixed =(True, True, True, True, False, True) )
# code for base7
s.new_rigidbody(name='base7',
                mass=1.0,
                cog=(1.0,
                     0.0,
                     0.0),
                parent='base6',
                position=(2.0,
                          0.0,
                          0.0),
                rotation=(0.0,
                          solved(-2.9775475381485426),
                          0.0),
                fixed =(True, True, True, True, False, True) )
# code for base8
s.new_rigidbody(name='base8',
                mass=1.0,
                cog=(1.0,
                     0.0,
                     0.0),
                parent='base7',
                position=(2.0,
                          0.0,
                          0.0),
                rotation=(0.0,
                          solved(-6.118399673973392),
                          0.0),
                fixed =(True, True, True, True, False, True) )
# code for base9
s.new_rigidbody(name='base9',
                mass=1.0,
                cog=(1.0,
                     0.0,
                     0.0),
                parent='base8',
                position=(2.0,
                          0.0,
                          0.0),
                rotation=(0.0,
                          solved(-18.420666987454272),
                          0.0),
                fixed =(True, True, True, True, False, True) )
# code for base10
s.new_rigidbody(name='base10',
                mass=1.0,
                cog=(1.0,
                     0.0,
                     0.0),
                parent='base9',
                position=(2.0,
                          0.0,
                          0.0),
                rotation=(0.0,
                          solved(-76.17315348527703),
                          0.0),
                fixed =(True, True, True, True, False, True) )
# code for base11
s.new_rigidbody(name='base11',
                mass=1.0,
                cog=(1.0,
                     0.0,
                     0.0),
                parent='base10',
                position=(2.0,
                          0.0,
                          0.0),
                rotation=(0.0,
                          solved(-43.33815240003529),
                          0.0),
                fixed =(True, True, True, True, False, True) )
# code for base12
s.new_rigidbody(name='base12',
                mass=1.0,
                cog=(1.0,
                     0.0,
                     0.0),
                parent='base11',
                position=(2.0,
                          0.0,
                          0.0),
                rotation=(0.0,
                          solved(-10.409642842100775),
                          0.0),
                fixed =(True, True, True, True, False, True) )
# code for base13
s.new_rigidbody(name='base13',
                mass=1.0,
                cog=(1.0,
                     0.0,
                     0.0),
                parent='base12',
                position=(2.0,
                          0.0,
                          0.0),
                rotation=(0.0,
                          solved(-4.2688210542917755),
                          0.0),
                fixed =(True, True, True, True, False, True) )
# code for base14
s.new_rigidbody(name='base14',
                mass=1.0,
                cog=(1.0,
                     0.0,
                     0.0),
                parent='base13',
                position=(2.0,
                          0.0,
                          0.0),
                rotation=(0.0,
                          solved(-2.29788607954429),
                          0.0),
                fixed =(True, True, True, True, False, True) )
# code for base15
s.new_rigidbody(name='base15',
                mass=1.0,
                cog=(1.0,
                     0.0,
                     0.0),
                parent='base14',
                position=(2.0,
                          0.0,
                          0.0),
                rotation=(0.0,
                          solved(-1.4315793537309895),
                          0.0),
                fixed =(True, True, True, True, False, True) )
# code for Poi
s.new_point(name='Poi',
          parent='base15',
          position=(2.0,
                    0.0,
                    0.0))
# code for Cable
s.new_cable(name='Cable',
            endA='Poi_1',
            endB='Poi',
            length=7.0,
            EA=100000.0)

s.solve_statics()

yml_filename = r"c:\data\snake15.yml"

export_ofx_yml(s, yml_filename)

yml_filename = r"snake15.yml"  # without path
py_file = r"c:\data\snake15.py"
ofx_api_path = r'C:\Program Files (x86)\Orcina\OrcaFlex\10.2\OrcFxAPI\Python'

write_ofx_run_and_collect_script(py_file=py_file, yml_file=yml_filename, ofx_path=ofx_api_path)

sum_filename = r"c:\data\snake15_sum.yml"

results = compare_statics(s, sum_filename)

import pandas as pd

df = pd.DataFrame.from_dict(results)


for r in results:
    print(r)


