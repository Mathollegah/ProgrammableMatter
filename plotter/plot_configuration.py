from matplotlib import pyplot as plt
import matplotlib
from mpl_toolkits.mplot3d.art3d import Poly3DCollection, Line3DCollection
import numpy as np
import globalvars
import random

fig = plt.figure()
ax = fig.add_subplot(projection='3d')

ax.set(xlim3d=(-5, 5), xlabel='X')
ax.set(ylim3d=(-5, 5), ylabel='Y')
ax.set(zlim3d=(-5, 5), zlabel='Z')


def new_dodecahedron(ax, pos, color='cyan'):
    size = 0.35

    a1 = 0*np.pi/180
    a2 = 45*np.pi/180

    rot1 = np.array([[np.cos(a1),-np.sin(a1),0], [np.sin(a1),np.cos(a1),0], [0,0,1]])
    rot2 = np.array([[np.cos(a2),0,-np.sin(a2)], [0,1,0], [np.sin(a2),0,np.cos(a2)]])

    rot = rot1.dot(rot2)

    pos1 = np.array([pos])
    pos2 = np.array([pos, pos, pos, pos])

    # vertices of a rhombic dodecahedron
    l1 = np.array([[0,0,2]]).dot(rot) * size
    l2 = np.array([[1,1,1], [1,-1,1], [-1,-1,1], [-1,1,1]]).dot(rot) * size
    l3 = np.array([[2,0,0],[0,-2,0],[-2,0,0],[0,2,0]]).dot(rot) * size
    l4 = np.array([[1,1,-1], [1,-1,-1], [-1,-1,-1], [-1,1,-1]]).dot(rot) * size
    l5 = np.array([[0,0,-2]]).dot(rot) * size


    l1 += pos1
    l2 += pos2
    l3 += pos2
    l4 += pos2
    l5 += pos1

    v = np.concatenate((l1, l2, l3, l4, l5))
    ax.scatter3D(v[:, 0], v[:, 1], v[:, 2])

    # l1 0
    # l2 1-4
    # l3 5-8
    # l4 9-12
    # l5 13

    # generate list of sides' polygons of our dodecahedron
    verts = [[l1[0],l2[0],l3[0],l2[1]], [l1[0],l2[1],l3[1],l2[2]], [l1[0],l2[2],l3[2],l2[3]], [l1[0],l2[3],l3[3],l2[0]],
             [l5[0],l4[0],l3[0],l4[1]], [l5[0],l4[1],l3[1],l4[2]], [l5[0],l4[2],l3[2],l4[3]], [l5[0],l4[3],l3[3],l4[0]],
             [l2[1],l3[0],l4[1],l3[1]], [l2[2],l3[1],l4[2],l3[2]], [l2[3],l3[2],l4[3],l3[3]], [l2[0],l3[3],l4[0],l3[0]]]

    #tmp =list(l1)+list(l2)+list(l3)+list(l4)+list(l5)
    #print(tmp)
    #for i, val in enumerate(tmp):
    #    print("\coordinate[] (" + str(i) + ") at ("+str(val[0])+"+#1,-"+str(val[1])+"+#2,"+str(val[2])+")")

    #print(verts)



    # plot sides
    ax.add_collection3d(Poly3DCollection(verts,
     facecolors=color, linewidths=0.3, edgecolors='black', alpha=0.8))

def plot_with_matplotlib():
    for x in globalvars.dodecahedrons:
        lst_tmp=[x.bottom, x.top, x.upright1, x.upright1, x.upleft1, x.upleft2 , x.downright1, x.downright1, x.downleft1, x.downleft2, x.back, x.front]
        count = 0
        for i in lst_tmp:
            if i != None:
                count+=1
        #print(count)

        color = random.choice(['green', 'orange', 'cyan'])
        new_dodecahedron(ax, [x.x, x.y, x.z], color)
        break

    #print(len(dodecahedrons))
    plt.axis("off")
    plt.show()
