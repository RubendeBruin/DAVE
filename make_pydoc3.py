import sys
sys.path.extend(['C:\\Users\\Ruben\\source\\repos\\o3d\\x64\\Release', 'C:\\DATA\\DAVE\\PUBLIC\\DAVE', 'C:\\DATA\\DAVE\\PUBLIC\\DAVE\\src', 'C:/Users/Ruben/source/repos/o3d/x64/Release'])

import pdoc
import DAVE

context = pdoc.Context()

module = pdoc.Module(DAVE, context=context)

pdoc.link_inheritance(context)

def recursive_htmls(mod):
    yield mod.name, mod.html()
    for submod in mod.submodules():
        yield from recursive_htmls(submod)

for module_name, html in recursive_htmls(module):

    filename = module_name.split('.')

    if len(filename) > 1:
        filename = filename[1] + '.html'
    else:
        filename = 'index.html'

    f = open('html/' + filename,'w+')
    f.write(html)
    f.close()