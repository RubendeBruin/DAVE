"""
  This Source Code Form is subject to the terms of the Mozilla Public
  License, v. 2.0. If a copy of the MPL was not distributed with this
  file, You can obtain one at http://mozilla.org/MPL/2.0/.

  Ruben de Bruin - 2020


  Helper functions reporting nodes in Jupyter

"""
import fnmatch

from DAVE.tools import fancy_format, make_iterable
from IPython.core.display import display, HTML


def report(node, properties=None, long = False, _return_pdf_table = False) -> None:
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

    # TODO: Use Scene.give_documentation instead

    if isinstance(properties, str):
        properties = [properties]

    style = ' style="text-align:left"'

    html = []
    html.append('<table align="left" border="1">')
    html.append(f'<caption>Properties of {node.name} ({str(node.class_name)})</caption>')
    html.append(f'<tr><th{style}>Property</th><th{style}>Value</th><th{style}>Unit</th><th{style}>Remarks</th><th{style}>Explained</th></tr>')

    table = []
    table.append(['Property','Value','Unit','Remarks','Explained'])

    # get all properties for this node
    scene = node._scene
    all_properties = scene.give_properties_for_node(node)

    for prop in all_properties:

        # skip unmatching properties
        if properties is not None:
            matching = [fnmatch.fnmatch(prop, filter) for filter in properties]
            if not any(matching):
                continue

        value = getattr(node, prop)

        if value is None:
            continue
        if isinstance(value, (tuple,list)):
            if all([v is None for v in value]):
                continue


        doc = scene.give_documentation(node, prop)

        if long:
            help = doc.doc_long
        else:
            help = doc.doc_short

        value = fancy_format(value)

        units_br = str(doc.units).replace(',',',<br>')
        value_br = str(value).replace(',',',<br>')

        units_pdf = str(doc.units).replace(',',',\n')
        value_pdf = str(value).replace(',',',\n')

        html.append(f'<tr><td{style}>{prop}</td><td{style}>{value_br}</td><td{style}>{units_br}</td><td{style}>{doc.remarks}</td><td{style}>{help}</td></tr>')
        table.append([prop,value_pdf,units_pdf,doc.remarks, help])

    html.append('</table><BR CLEAR=LEFT>')

    if _return_pdf_table:
        return table
    else:
        display(HTML(''.join(html)))


