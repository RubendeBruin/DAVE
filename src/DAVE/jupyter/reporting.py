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

import DAVE.scene as ds

cdir = Path(dirname(__file__))
DAVE_REPORT_PROPS = pd.read_csv(cdir / '../resources/proplist.csv')

def report(node, properties=None, short = True):

    result = pd.DataFrame(columns= ['value','unit','remarks','description'])

    for index, row in DAVE_REPORT_PROPS.iterrows():

        class_name = row['class']
        code = 'ds.' + class_name
        class_type = eval(code, {'ds':ds})

        if isinstance(node, class_type):
            prop = row['property']

            help = row['doc']
            if pd.isna(help):
                continue

            if properties is not None:

                prop_ = prop + ' '
                contains = [a in prop_ for a in properties]

                if not any(contains):
                    continue

            code = "node.{}".format(prop)
            value = eval(code)

            if short:
                help = help.split('\n')[0]

            # split anything between [ ] or ( ) from the help

            start = help.find('[')
            end = help.find(']')
            if end>start:
                units = help[start+1:end]
                help = help[:start] + help[end+1:]
            else:
                units = ''

            start = help.find('(')
            end = help.find(')')
            if end > start:
                remarks = help[start + 1:end]
                help = help[:start] + help[end + 1:]
            else:
                remarks = ''

            result.loc[prop] = (value, units, remarks, help)

    return result

