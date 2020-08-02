"""
  This Source Code Form is subject to the terms of the Mozilla Public
  License, v. 2.0. If a copy of the MPL was not distributed with this
  file, You can obtain one at http://mozilla.org/MPL/2.0/.

  Ruben de Bruin - 2020


  Helper functions reporting nodes in Jupyter

"""

import pandas as pd
from os.path import dirname
from pathlib import Path

cdir = Path(dirname(__file__))
DAVE_REPORT_PROPS = pd.read_csv(cdir / '../resources/proplist.csv')

###

from DAVE import *

import DAVE.scene as nodes

s = Scene()
node = s.new_rigidbody('demo')


def report(node, properties=None, short = True):

    for index, row in DAVE_REPORT_PROPS.iterrows():

        class_name = row['class']
        class_type = eval(class_name)

        if isinstance(node, class_type):
            prop = row['property']

            help = row['doc']
            if pd.isna(help):
                continue

            prop_ = prop + ' '
            contains = [a in prop_ for a in properties]

            if any(contains):

                code = "node.{}".format(prop)
                result = eval(code)

                if short:
                    help = help.split('\n')[0]

                print(f'{node.name} : {prop} : {result} : {help}')



###
properties = ['force ', 'moment ']
short = True

report(node, properties, short = False)