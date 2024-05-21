from math import pi, sin, cos
import simplepbr
import globalvars
from robots.logauto.robot import *

from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection, Line3DCollection
import numpy as np
import random


class Dodecahedron:
    def __init__(self, _x, _y, _z):
        self.x = _x
        self.y = _y
        self.z = _z

        self.scene = None

        self.top = None
        self.bottom = None
        self.front = None
        self.back = None

        self.upleft1 = None
        self.upleft2 = None
        self.upright1 = None
        self.upright2 = None

        self.downleft1 = None
        self.downleft2 = None
        self.downright1 = None
        self.downright2 = None

        self.directions = [(0, self.top), (1, self.bottom), (2, self.front), (3, self.back),
                           (4, self.upleft1), (5, self.upleft2), (6, self.upright1), (7, self.upright2),
                           (8, self.downleft1), (9,self.downleft2), (10, self.downright1), (11,self.downright2)]

    def find_neighbours(self, lst):
        for x in lst:
            if (x.x, x.y, x.z+1) == (self.x, self.y, self.z):
                self.bottom = x
                x.top = self

            if (x.x, x.y, x.z-1) == (self.x, self.y, self.z):
                self.top = x
                x.bottom = self

            if (x.x+1, x.y, x.z) == (self.x, self.y, self.z):
                self.back = x
                x.front = self

            if (x.x-1, x.y, x.z) == (self.x, self.y, self.z):
                self.front = x
                x.back = self

            if (x.x - 0.5, x.y + 0.75, x.z + 0.5) == (self.x, self.y, self.z):
                self.downright2 = x
                x.upleft1 = self

            if (x.x - 0.5, x.y - 0.75, x.z + 0.5) == (self.x, self.y, self.z):
                self.downright1 = x
                x.upleft2 = self

            if (x.x + 0.5, x.y + 0.75, x.z + 0.5) == (self.x, self.y, self.z):
                self.downleft2 = x
                x.upright1 = self

            if (x.x + 0.5, x.y - 0.75, x.z + 0.5) == (self.x, self.y, self.z):
                self.downleft1 = x
                x.upright2 = self

            if (x.x - 0.5, x.y + 0.75, x.z - 0.5) == (self.x, self.y, self.z):
                self.upright2 = x
                x.downleft1 = self

            if (x.x - 0.5, x.y - 0.75, x.z - 0.5) == (self.x, self.y, self.z):
                self.upright1 = x
                x.downleft2 = self

            if (x.x + 0.5, x.y + 0.75, x.z - 0.5) == (self.x, self.y, self.z):
                self.upleft2 = x
                x.downright1 = self

            if (x.x + 0.5, x.y - 0.75, x.z - 0.5) == (self.x, self.y, self.z):
                self.upleft1 = x
                x.downright2 = self

    def delete_neighbor_links(self):
        if self.top != None:
            self.top.bottom = None
            self. top = None

        if self.bottom != None:
            self.bottom.top = None
            self.bottom = None

        if self.front != None:
            self.front.back = None
            self.front = None

        if self.back != None:
            self.back.front = None
            self.back = None

        if self.upleft1 != None:
            self.upleft1.downright2 = None
            self.upleft1 = None

        if self.upleft2 != None:
            self.upleft2.downright1 = None
            self.upleft2 = None

        if self.upright1 != None:
            self.upright1.downleft2 = None
            self.upright1 = None

        if self.upright2 != None:
            self.upright2.downleft1 = None
            self.upright2 = None

        if self.downleft1 != None:
            self.downleft1.upright2 = None
            self.downleft1 = None

        if self.downleft2 != None:
            self.downleft2.upright1 = None
            self.downleft2 = None

        if self.downright1 != None:
            self.downright1.upleft2 = None
            self.downright1 = None

        if self.downright2 != None:
            self.downright2.upleft1 = None
            self.downright2 = None


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

    # generate list of sides' polygons of our dodecahedron
    verts = [[l1[0],l2[0],l3[0],l2[1]], [l1[0],l2[1],l3[1],l2[2]], [l1[0],l2[2],l3[2],l2[3]], [l1[0],l2[3],l3[3],l2[0]],
             [l5[0],l4[0],l3[0],l4[1]], [l5[0],l4[1],l3[1],l4[2]], [l5[0],l4[2],l3[2],l4[3]], [l5[0],l4[3],l3[3],l4[0]],
             [l2[1],l3[0],l4[1],l3[1]], [l2[2],l3[1],l4[2],l3[2]], [l2[3],l3[2],l4[3],l3[3]], [l2[0],l3[3],l4[0],l3[0]]]

    # plot sides
    ax.add_collection3d(Poly3DCollection(verts,
     facecolors=color, linewidths=1, edgecolors='r', alpha=1.0))


fig = plt.figure()
ax = fig.add_subplot(projection='3d')

ax.set(xlim3d=(-5, 5), xlabel='X')
ax.set(ylim3d=(-5, 5), ylabel='Y')
ax.set(zlim3d=(-5, 5), zlabel='Z')

# Build configuration
if globalvars.load_file == "":
    globalvars.dodecahedrons = [Dodecahedron(0,0,0)]
    for i in range(140):
        x = random.choice(globalvars.dodecahedrons)

        d = random.choice(x.directions)

        if d[1] == None:
            if d[0] == 0:
                tmp = Dodecahedron(x.x,x.y,x.z+1)
                globalvars.dodecahedrons.append(tmp)
                tmp.bottom = x
                x.top = tmp

            if d[0] == 1:
                tmp = Dodecahedron(x.x,x.y,x.z-1)
                globalvars.dodecahedrons.append(tmp)
                tmp.top = x
                x.bottom = tmp

            if d[0] == 2:
                tmp = Dodecahedron(x.x+1,x.y,x.z)
                globalvars.dodecahedrons.append(tmp)
                tmp.back = x
                x.front = tmp

            if d[0] == 3:
                tmp = Dodecahedron(x.x-1,x.y,x.z)
                globalvars.dodecahedrons.append(tmp)
                tmp.front = x
                x.back = tmp

            if d[0] == 4:
                tmp = Dodecahedron(x.x-0.5,x.y+0.75,x.z+0.5)
                globalvars.dodecahedrons.append(tmp)
                tmp.downright2 = x
                x.upleft1 = tmp

            if d[0] == 5:
                tmp = Dodecahedron(x.x-0.5,x.y-0.75,x.z+0.5)
                globalvars.dodecahedrons.append(tmp)
                tmp.downright1 = x
                x.upleft2 = tmp

            if d[0] == 6:
                tmp = Dodecahedron(x.x+0.5,x.y+0.75,x.z+0.5)
                globalvars.dodecahedrons.append(tmp)
                tmp.downleft2 = x
                x.upright1 = tmp

            if d[0] == 7:
                tmp = Dodecahedron(x.x+0.5,x.y-0.75,x.z+0.5)
                globalvars.dodecahedrons.append(tmp)
                tmp.downleft1 = x
                x.upright2 = tmp

            if d[0] == 8:
                tmp = Dodecahedron(x.x-0.5,x.y+0.75,x.z-0.5)
                globalvars.dodecahedrons.append(tmp)
                tmp.upright2 = x
                x.downleft1 = tmp

            if d[0] == 9:
                tmp = Dodecahedron(x.x-0.5,x.y-0.75,x.z-0.5)
                globalvars.dodecahedrons.append(tmp)
                tmp.upright1 = x
                x.downleft2 = tmp

            if d[0] == 10:
                tmp = Dodecahedron(x.x+0.5,x.y+0.75,x.z-0.5)
                globalvars.dodecahedrons.append(tmp)
                tmp.upleft2 = x
                x.downright1 = tmp

            if d[0] == 11:
                tmp = Dodecahedron(x.x+0.5,x.y-0.75,x.z-0.5)
                globalvars.dodecahedrons.append(tmp)
                tmp.upleft1 = x
                x.downright2 = tmp

            tmp.find_neighbours(globalvars.dodecahedrons)

            for x in globalvars.dodecahedrons:
                x.directions = [(0, x.top), (1, x.bottom), (2, x.front), (3, x.back),
                                   (4, x.upleft1), (5, x.upleft2), (6, x.upright1), (7, x.upright2),
                                   (8, x.downleft1), (9, x.downleft2), (10, x.downright1), (11, x.downright2)]

else:
    f = open(globalvars.load_file, "r")
    txt = f.read()
    f.close()
    nodes = txt.split()
    nodes = [float(i) for i in nodes]
    tmp_robot_pos = nodes[:3]

    for i in range(len(nodes)//3-1):
        tmp = Dodecahedron(nodes[3*i+3], nodes[3*i+4], nodes[3*i+5])
        globalvars.dodecahedrons.append(tmp)
        tmp.find_neighbours(globalvars.dodecahedrons)

    for i in globalvars.dodecahedrons:
        if (i.x,i.y,i.z) == (tmp_robot_pos[0], tmp_robot_pos[1], tmp_robot_pos[2]):
            globalvars.global_start_node = i
            break


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

    #print(len(dodecahedrons))
    plt.show()




class Simulator3D(ShowBase):

    def __init__(self):
        ShowBase.__init__(self)
        simplepbr.init()
        self.accept('s', self.stop)
        self.accept('q', self.switch_orientation)

        self.running = True

        if globalvars.load_file == "":
            tmp = random.choice(globalvars.dodecahedrons)
            globalvars.global_start_node = tmp

        self.interpolation_move = 0
        self.step = 0
        self.robot = Robot()

        # Model complete, store in file
        if globalvars.load_file == "":
            f = open(globalvars.store_file, "w")
            f.writelines(str(self.robot.x) + " " +  str(self.robot.y) + " " + str(self.robot.z) + " ")
            for dodec in globalvars.dodecahedrons:
                f.writelines(str(dodec.x) + " " + str(dodec.y)+ " " + str(dodec.z)+ " ")
            f.close()


        tmp = Dodecahedron(self.robot.x, self.robot.y, self.robot.z)
        globalvars.dodecahedrons.append(tmp)
        self.robot.grabbed_tile = tmp

        self.x = tmp.x
        self.y = tmp.y
        self.z = tmp.z

        self.x_next = 0
        self.y_next = 0
        self.z_next = 0

        self.scene = self.loader.loadModel("models/robot.glb")
        self.scene.reparentTo(self.render)
        self.scene.setScale(4.0 / 8.0, 4.0 / 8.0, 4.0 / 8.0)
        self.scene.setPos(self.x, self.y, self.z)

        for x in globalvars.dodecahedrons:
            x.scene = self.loader.loadModel("models/dodeca.glb")
            x.scene.reparentTo(self.render)
            x.scene.setScale(1.0/2.75, 1.0/2.75, 1.0/2.75)
            x.scene.setPos(x.x, x.y, x.z)

        # Add the move robot procedure.
        self.taskMgr.add(self.moveRobot, "MoveRobot")


    def stop(self):
        self.running = not self.running
        print("Pause")

    def switch_orientation(self):
        global global_switch
        global_switch = True

    # Define a procedure to move the robot.
    def moveRobot(self, task):
        if not self.running:
            return Task.cont

        steps = 8 #yyyyyyyyyyyyyyyyyyyyyyyy
        if self.interpolation_move == 0:
            self.robot.next_move()
            self.x_next = self.robot.x
            self.y_next = self.robot.y
            self.z_next = self.robot.z

        inter_x = self.x + (self.x_next - self.x) * self.interpolation_move / steps
        inter_y = self.y + (self.y_next - self.y) * self.interpolation_move / steps
        inter_z = self.z + (self.z_next - self.z) * self.interpolation_move / steps

        self.scene.setPos(inter_x, inter_y, inter_z)
        self.interpolation_move += 1

        if self.robot.grabbed_tile != None:
            self.robot.grabbed_tile.scene.setPos(inter_x, inter_y, inter_z)

        if self.interpolation_move == steps+1:
            self.interpolation_move = 0
            self.x = self.x_next
            self.y = self.y_next
            self.z = self.z_next

            if self.robot.grabbed_tile != None:
                self.robot.grabbed_tile.x = self.x
                self.robot.grabbed_tile.y = self.y
                self.robot.grabbed_tile.z = self.z

        return Task.cont



# Robot Motion --------------------------------------------------------------------------








# Robot Motion End ----------------------------------------------------------------------







#plot_with_matplotlib()

app = Simulator3D()

app.run()
