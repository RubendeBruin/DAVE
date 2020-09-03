# Import the orcaflex api
import sys
sys.path.append(r'C:\Program Files (x86)\Orcina\OrcaFlex\10.2\OrcFxAPI\Python')
import OrcFxAPI as ofx

import yaml

# Load the model
m = ofx.Model(r'c:\data\ofx.yml')

m.CalculateStatics()

p6DBuoy_static = ['X','Y','Z',
                  'Rotation 1','Rotation 2','Rotation 3']
pWinch_static = ['Tension','Stretched Length']

nodes = {}

for obj in m.objects:
    # print(obj.name)
    
    if obj.type == ofx.ot6DBuoy:
        props = p6DBuoy_static
    elif obj.type == ofx.otWinch:
        props = pWinch_static
    else:
        continue

    results = {}
        
    for p in props:
        value = obj.StaticResult(p)
        results[p] = float(value)

    nodes[obj.name] = results


s = yaml.dump(nodes, explicit_start=True)

with open(f'c:\data\ofx_results.yml','w') as f:
    f.write(s)
