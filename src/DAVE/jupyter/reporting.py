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

import fnmatch

from DAVE.tools import fancy_format, make_iterable

import DAVE.scene as ds

from IPython.core.display import display, HTML

cdir = Path(dirname(__file__))
DAVE_REPORT_PROPS = pd.read_csv(cdir / '../resources/proplist.csv')

def report(node, properties=None, long = False) -> None:
    """Produces a HTML table with properties of the provided node.

    The amount of properties that is reported may be limited by specifying the names of the the properties that should be reported.

    Args:
        node : any Scene node
        properties : names of properties that should be reported. Can contain ? and * wildcards (? matches a single char, * matches any number of chars)
        long : use short or long description

    Examples:

        >>> report(s['Cheetah'])

        >>> report(s['Cheetah'], short=False)

        >>> report(s['Cheetah'], properties='position')  # report only the position

        >>> report(s['Cheetah'], properties='*position')  # report any property that ends with "position"

        >>> report(s['Cheetah'], properties=['*position*', '*force??'])  # also report all properties that and with "force" and then two additional characters. For example force_x (but not force itself)




    """

    style = ' style="text-align:left"'

    html = []
    html.append('<table align="left" border="1">')
    html.append(f'<caption>Properties of {node.name}</caption>')
    html.append(f'<tr><th{style}>Property</th><th{style}>Value</th><th{style}>Unit</th><th{style}>Remarks</th><th{style}>Explained</th></tr>')

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

                matching = [fnmatch.fnmatch(prop, filter) for filter in properties]

                if not any(matching):
                    continue

            code = "node.{}".format(prop)
            value = eval(code)

            if not long:
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

            value = fancy_format(value)

            units = str(units).replace(',',',<br>')
            value = str(value).replace(',',',<br>')


            html.append(f'<tr><td{style}>{prop}</td><td{style}>{value}</td><td{style}>{units}</td><td{style}>{remarks}</td><td{style}>{help}</td></tr>')

    html.append('</table><BR CLEAR=LEFT>')

    display(HTML(''.join(html)))


