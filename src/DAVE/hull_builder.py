

# h = Hull()
#
#
# frame1 = [(0,0),(10,0),(0,5)]
#
# boolean geometry
#
# # PyMesh <-- difficult to install and depends on CGAL / C++
#
# vtkBooleanOperationPolyDataFilter # <-- should work

from vedo import *

#
frame1 = (0,0,
          0.1, 0,
          0.9,0,
          1.0,0.1,
          1,1)

frame2 = (0,-0.1,
          0.1, -0.1,
          0.1, 0.3,
          1,0.3,
          1,1)

def vertices(frame,x):

    # guess symmetry
    n = len(frame)//2
    ys = [frame[2*i] for i in range(n)]
    zs = [frame[2*i+1] for i in range(n)]

    r = [(x, ys[i],zs[i]) for i in range(n)]

    if np.min(ys)>=0:
        mirror = [(x, -ys[i],zs[i]) for i in reversed(range(n)) if ys[i]!=0 ] # duplicate except points on the centerline
        r = [*mirror, *r]


    if r[-1] != r[0]: # close the loop
        r.append(r[0])

    return r

f1 = vertices(frame1,0)
f2 = vertices(frame2,5)

import matplotlib.pyplot as plt

def plotframe(fr):
    plt.plot([f[1] for f in fr],[f[2] for f in fr],'k.-')
    for i in range(len(fr)):
        plt.text(fr[i][1],fr[i][2],str(i))

plotframe(f1)
plt.show()

plotframe(f2)
plt.show()


def build_triangles(f1,f2):
    """
    Builds triangles between two frames

    Args:
        f1: list of [x,y,z]
        f2: lift of [x,y,z]

    Returns:
        points : list of [x,y,z] containing vertices
        triangles : list of [i,j,k] with the indices

    """

    # i = counter
    # n = amount
    # p1 = point on list 1
    # p2 = point on list 2

    i1 = 0
    i2 = 0
    # p1 = f1[i1]
    # p2 = f2[i2]

    n1 = len(f1)
    n2 = len(f2)

    o1 = 0   # previous indices
    o2 = 0

    crossed1 = False
    crossed2 = False


    triangles = list()

    while True:

        if i1==3:
            print('wait')

        p1 = f1[i1]
        p2 = f2[i2]

        if i1==n1-1:
            i2+=1
        elif i2==n2-1:
            i1+=1
                # finish the halfs simultaneously
        else:

            a1 = f1[i1+1]  # advance
            a2 = f2[i2+1]

            # are we crossing the center-line on either of them?
            crossed1 = a1[1] * p1[1] <= 0 or crossed1
            crossed2 = a2[1] * p2[1] <= 0 or crossed2

            if crossed1 and not crossed2:
                i2 += 1
            elif crossed2 and not crossed1:
                i1 += 1
            else:

                l1 = np.linalg.norm(np.array(a1) - p2)  # Line to next point on frame 1
                l2 = np.linalg.norm(np.array(a2) - p1)

                if l1 > l2:
                    i2 += 1
                else:
                    i1 += 1

        # we now have point i1 and i2
        if i1==o1:
            # triangle between i1, i2 and o2
            triangles.append((i1,o2+n1, i2+n1))
        else:
            triangles.append((o1, i2+n1, i1))

        o1 = i1
        o2 = i2

        if i1==n1-1 and i2==n2-1:
            break

    return [*f1,*f2], triangles

def combine_meshes(mesha, meshb):
    """Merges the faces and indices of both meshes"""

    va = mesha.points()
    fa = mesha.faces()

    vb = meshb.points()
    fb = meshb.faces()

    nva = len(va)
    points = [*va, *vb]

    fbp = [(a[0]+nva, a[1]+nva, a[2]+nva) for a in fb]

    faces = [*fa, *fbp]

    return Mesh([points, faces])

points, triangles = build_triangles(f1, f2)
midship = Mesh([points, triangles])

bow = [(10,0,2)]
points, triangles = build_triangles(f2, bow)  # stern to bow
front = Mesh([points, triangles])

# m = midship + front

m = combine_meshes(midship, front)

stern = [(0,0.5,0.5)]
points, triangles = build_triangles(stern, f1)
back = Mesh([points, triangles])

# m = m + back
m = combine_meshes(m, back)

print(len(m.points()))
m.clean()
print(len(m.points()))

# Invert normals
p = m.points()
v = m.faces()
vi = [(p[2], p[1], p[0]) for p in v]

m = Mesh([p, vi])

m.write(r'c:\data\hull.stl')

# Do a boolean
c = Sphere(pos=(2,1,0),r=0.3, res=8)
# c = Cube(pos=(2,0.5,0), side=1)
c.write(r'c:\data\sphere.stl')

m2 = m.boolean('plus',c)

# And plot
p = Plotter(axes=5)
p.add(m2)

p.show(axes=1)

# But the mesh does not look nice.