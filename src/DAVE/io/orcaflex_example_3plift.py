from DAVE import *
from DAVE.io.orcaflex import *

s = Scene()

# code for Body
s.new_rigidbody(name='Body',
                mass=10.0,
                cog=(1.7,
                     3.6,
                     -2.0),
                fixed = False)
# code for Point1_1
s.new_point(name='Point1_1',
          position=(1.0,
                    -3.0,
                    11.0))
# code for Point2_1
s.new_point(name='Point2_1',
          position=(7.0,
                    5.0,
                    10.0))
# code for Point3_1
s.new_point(name='Point3_1',
          position=(-7.0,
                    4.0,
                    10.0))
# code for Point1
s.new_point(name='Point1',
          parent='Body',
          position=(0.0,
                    -3.0,
                    0.0))
# code for Point2
s.new_point(name='Point2',
          parent='Body',
          position=(7.0,
                    5.0,
                    4.0))
# code for Point3
s.new_point(name='Point3',
          parent='Body',
          position=(-7.0,
                    4.0,
                    3.0))
# code for Cable2
s.new_cable(name='Cable2',
            endA='Point2_1',
            endB='Point2',
            length=6.0,
            EA=100.0)
# code for Cable1
s.new_cable(name='Cable1',
            endA='Point1_1',
            endB='Point1',
            length=10.0,
            EA=400.0)
# code for Cable3
s.new_cable(name='Cable3',
            endA='Point3',
            endB='Point3_1',
            length=7.0,
            EA=200.0)

s.solve_statics()

run_statics_collect(s)

# yml_filename = r"c:\data\3plift.yml"
# py_file = r"c:\data\3plift.py"
# ofx_api_path = r'C:\Program Files (x86)\Orcina\OrcaFlex\10.2\OrcFxAPI\Python'
#
# export_ofx_yml(s, yml_filename)
# write_ofx_run_and_collect_script(py_file=py_file, yml_file=yml_filename, ofx_path=ofx_api_path)
#
# sum_filename = r"c:\data\3plift_sum.yml"
#
# results = compare_statics(s, sum_filename)
#
# import pandas as pd
#
# df = pd.DataFrame.from_dict(results)
#
#
# for r in results:
#     print(r)


