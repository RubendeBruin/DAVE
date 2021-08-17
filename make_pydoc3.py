# import sys
# sys.path.extend(['C:\\Users\\Ruben\\source\\repos\\o3d\\x64\\Release', 'C:\\DATA\\DAVE\\PUBLIC\\DAVE', 'C:\\DATA\\DAVE\\PUBLIC\\DAVE\\src', 'C:/Users/Ruben/source/repos/o3d/x64/Release'])

import pdoc
import DAVE
import DAVE.frequency_domain
import DAVE.marine
import DAVE.scene
import DAVE.io.simplify

context = pdoc.Context()

modules = [DAVE.scene, DAVE.frequency_domain, DAVE.marine, DAVE.io.simplify]


for m in modules:

    module = pdoc.Module(m, context=context)
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

        f = open('html/' + filename,'w+', encoding='UTF-8')
        f.write(html)
        f.close()

        print(f"written {'html/' + filename}")