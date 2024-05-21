from math import pi, sin, cos
import simplepbr

from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection, Line3DCollection
import numpy as np
import random

load_file = "tests/hole.txt"
store_file = "demofile.txt"
#load_file = "demofile.txt"

dodecahedrons = []
global_start_node = None

global_switch = False

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
if load_file == "":
    dodecahedrons = [Dodecahedron(0,0,0)]
    for i in range(10):
        x = random.choice(dodecahedrons)

        d = random.choice(x.directions)

        if d[1] == None:
            if d[0] == 0:
                tmp = Dodecahedron(x.x,x.y,x.z+1)
                dodecahedrons.append(tmp)
                tmp.bottom = x
                x.top = tmp

            if d[0] == 1:
                tmp = Dodecahedron(x.x,x.y,x.z-1)
                dodecahedrons.append(tmp)
                tmp.top = x
                x.bottom = tmp

            if d[0] == 2:
                tmp = Dodecahedron(x.x+1,x.y,x.z)
                dodecahedrons.append(tmp)
                tmp.back = x
                x.front = tmp

            if d[0] == 3:
                tmp = Dodecahedron(x.x-1,x.y,x.z)
                dodecahedrons.append(tmp)
                tmp.front = x
                x.back = tmp

            if d[0] == 4:
                tmp = Dodecahedron(x.x-0.5,x.y+0.75,x.z+0.5)
                dodecahedrons.append(tmp)
                tmp.downright2 = x
                x.upleft1 = tmp

            if d[0] == 5:
                tmp = Dodecahedron(x.x-0.5,x.y-0.75,x.z+0.5)
                dodecahedrons.append(tmp)
                tmp.downright1 = x
                x.upleft2 = tmp

            if d[0] == 6:
                tmp = Dodecahedron(x.x+0.5,x.y+0.75,x.z+0.5)
                dodecahedrons.append(tmp)
                tmp.downleft2 = x
                x.upright1 = tmp

            if d[0] == 7:
                tmp = Dodecahedron(x.x+0.5,x.y-0.75,x.z+0.5)
                dodecahedrons.append(tmp)
                tmp.downleft1 = x
                x.upright2 = tmp

            if d[0] == 8:
                tmp = Dodecahedron(x.x-0.5,x.y+0.75,x.z-0.5)
                dodecahedrons.append(tmp)
                tmp.upright2 = x
                x.downleft1 = tmp

            if d[0] == 9:
                tmp = Dodecahedron(x.x-0.5,x.y-0.75,x.z-0.5)
                dodecahedrons.append(tmp)
                tmp.upright1 = x
                x.downleft2 = tmp

            if d[0] == 10:
                tmp = Dodecahedron(x.x+0.5,x.y+0.75,x.z-0.5)
                dodecahedrons.append(tmp)
                tmp.upleft2 = x
                x.downright1 = tmp

            if d[0] == 11:
                tmp = Dodecahedron(x.x+0.5,x.y-0.75,x.z-0.5)
                dodecahedrons.append(tmp)
                tmp.upleft1 = x
                x.downright2 = tmp

            tmp.find_neighbours(dodecahedrons)

            for x in dodecahedrons:
                x.directions = [(0, x.top), (1, x.bottom), (2, x.front), (3, x.back),
                                   (4, x.upleft1), (5, x.upleft2), (6, x.upright1), (7, x.upright2),
                                   (8, x.downleft1), (9, x.downleft2), (10, x.downright1), (11, x.downright2)]

else:
    f = open(load_file, "r")
    txt = f.read()
    f.close()
    nodes = txt.split()
    nodes = [float(i) for i in nodes]
    tmp_robot_pos = nodes[:3]

    for i in range(len(nodes)//3-1):
        tmp = Dodecahedron(nodes[3*i+3], nodes[3*i+4], nodes[3*i+5])
        dodecahedrons.append(tmp)
        tmp.find_neighbours(dodecahedrons)

    for i in dodecahedrons:
        if (i.x,i.y,i.z) == (tmp_robot_pos[0], tmp_robot_pos[1], tmp_robot_pos[2]):
            global_start_node = i
            break


def plot_with_matplotlib():
    global dodecahedrons
    for x in dodecahedrons:
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
        global global_direction
        global global_start_node
        ShowBase.__init__(self)
        simplepbr.init()
        self.accept('s', self.stop)
        self.accept('q', self.switch_orientation)

        self.running = True

        if load_file == "":
            tmp = random.choice(dodecahedrons)
            global_start_node = tmp

        self.interpolation_move = 0
        self.step = 0
        self.robot = Robot()

        # Model complete, store in file
        if load_file == "":
            f = open(store_file, "w")
            f.writelines(str(self.robot.x) + " " +  str(self.robot.y) + " " + str(self.robot.z) + " ")
            for dodec in dodecahedrons:
                f.writelines(str(dodec.x) + " " + str(dodec.y)+ " " + str(dodec.z)+ " ")
            f.close()


        tmp = Dodecahedron(self.robot.x, self.robot.y, self.robot.z)
        dodecahedrons.append(tmp)
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

        for x in dodecahedrons:
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
class FindLocalMaximum():
    def __init__(self):
        self.state = 'go_top'

    def reset(self):
        self.state = 'go_top'

    def move(self, directions):
        #print(self.state)
        if self.state == 'go_top':
            # Go straight top
            if directions[0][1] != None:
                return directions[0][0]

            # Go halve step top
            if directions[4][1] != None:
                return directions[4][0]

            if directions[5][1] != None:
                return directions[5][0]

            if directions[6][1] != None:
                return directions[6][0]

            if directions[7][1] != None:
                return directions[7][0]

            # Search on same level
            self.state = 'go_back'

        if self.state == 'go_back':
            if directions[3][1] != None:
                if (directions[0][1], directions[4][1], directions[5][1], directions[6][1], directions[7][1]) == (None, None, None, None, None):
                    return directions[3][0]
                else:
                    self.state = 'go_top'
            else:
                # Search on same level (other direction)
                self.state = 'go_front'

        if self.state == 'go_front':
            if directions[2][1] != None:
                if (directions[0][1], directions[4][1], directions[5][1], directions[6][1], directions[7][1]) == (
                None, None, None, None, None):
                    return directions[2][0]
                else:
                    self.state = 'go_top'
                    return -1

            else:
                # Local maximum reached
                if (directions[0][1], directions[4][1], directions[5][1], directions[6][1], directions[7][1]) == (
                None, None, None, None, None):
                    self.state = 'terminate'
                else:
                    self.state = 'go_top'
                return -1


class ShiftOrTake():
    def __init__(self):
        self.state = 'set_initial_tile'
        self.removable_tile = None
        self.robot = None

    def reset(self):
        self.state = 'set_initial_tile'
        self.removable_tile = None

    def move(self, directions, tile):
        #[(0, self.top), (1, self.bottom), (2, self.front), (3, self.back),
        # (4, self.upleft1), (5, self.upleft2), (6, self.upright1), (7, self.upright2),
        # (8, self.downleft1), (9, self.downleft2), (10, self.downright1), (11, self.downright2)]

        if self.state == 'set_initial_tile':
            if directions[1][1] == None:
                self.state = 'place_tile'
                self.removable_tile = tile
                #print(self.removable_tile, self.robot.grabbed_tile)
                return directions[1][0]
            elif directions[3][1] != None:
                self.state = 'place_tile_next'
                self.removable_tile = tile
                #print(self.removable_tile, self.robot.grabbed_tile)
                return directions[1][0]
            else:
                self.state = 'terminate'
                self.removable_tile = tile
                #print(self.removable_tile, self.robot.grabbed_tile)
                return -12

        if self.state == 'place_tile_next':
            self.state = 'place_tile'
            return directions[3][0]

        if self.state == 'place_tile':
            if tile == None:
                self.state = 'take_next_tile'
                return 13 # place tile
            else:
                self.state = 'terminate'
                return -1

        if self.state == 'take_next_tile':
            #print(self.removable_tile.x, self.removable_tile.y, self.removable_tile.z, self.robot.x, self.robot.y, self.robot.z)
            if self.removable_tile.x > self.robot.x:
                return directions[2][0]
            if self.removable_tile.z > self.robot.z:
                return directions[0][0]

            if self.removable_tile.back != None:
                self.state = 'shift_tile_downleft2'
                self.removable_tile = self.removable_tile.back
                #print(self.removable_tile, self.robot.grabbed_tile)
            else:
                self.removable_tile = None
                self.state = 'terminate'

            #self.removable_tile = self.removable_tile.back
            return 12 # grab tile

        if self.state == 'shift_tile_downleft2':
            self.state = 'shift_tile_downright2'
            return directions[8][0]

        if self.state == 'shift_tile_downright2':
            self.state = 'place_tile'
            return directions[9][0]


class TraverseLayer():
    def __init__(self):
        self.state = 'find_boundary'
        self.start_pos = (0,0)
        self.last_move = 0
        self.sec_to_last_move = 2
        self.max = (0,0)
        self.min = (0,0)
        self.x = 0
        self.y = 0
        self.count = 0

        self.bound_pos = (-100, -100)
        self.north_pos = (-105, -105)
        self.last_move_2 = 0
        self.sec_to_last_move_2 = 0
        self.sec_move = False

        self.sec_start_pos = False

    def reset(self):
        self.state = 'find_boundary'
        self.start_pos = (0, 0)
        self.last_move = 0
        self.sec_to_last_move = 2
        self.max = (0, 0)
        self.min = (0, 0)
        self.x = 0
        self.y = 0
        self.count = 0

        self.bound_pos = (-100, -100)
        self.north_pos = (-105, -105)
        self.last_move_2 = 0
        self.sec_to_last_move_2 = 0
        self.sec_move = False

        self.sec_start_pos = False

    def update_bounds(self, move):
        if move == 0:
            self.y += 1

        if move == 1:
            self.y += 0.5
            self.x += 0.5

        if move == 2:
            self.y -= 0.5
            self.x += 0.5

        if move == 3:
            self.y -= 1

        if move == 4:
            self.y -= 0.5
            self.x -= 0.5

        if move == 5:
            self.y += 0.5
            self.x -= 0.5

        if self.x > self.max[0]:
            self.max = (self.x, self.max[1])

        if self.y > self.max[1]:
            self.max = (self.max[0], self.y)

        if self.x < self.min[0]:
            self.min = (self.x, self.min[1])

        if self.y < self.min[1]:
            self.min = (self.min[0], self.y)


    def move(self, possible_moves):
        if self.state == 'find_boundary':
            for i in [0,5,1]:
                if possible_moves[i][1]:
                    self.sec_to_last_move = self.last_move
                    self.last_move = possible_moves[i][0]
                    return possible_moves[i][0]

            for i in range(len(possible_moves)):
                if possible_moves[i][0]:
                    self.last_move = (i+1)%6
                    self.sec_to_last_move = i

            self.start_pos = (0, 0)
            self.state = 'follow_boundary'
            return -1

        if self.state == 'follow_boundary':
            if (self.x, self.y) == self.start_pos and self.sec_start_pos:
                self.state = 'terminate_completely'
                return -1

            self.sec_start_pos = True

            for i in range(6):
                if (self.last_move-self.sec_to_last_move +3)%6 != 0:
                    tmp = (self.last_move - 1 + i) % 6
                else:
                    tmp = (self.last_move - 2 + i) % 6

                if possible_moves[tmp][1]:
                    self.sec_to_last_move = self.last_move
                    self.last_move = tmp
                    self.update_bounds(tmp)
                    if tmp != 0 and (self.x != self.north_pos[0]): #tmp != 0 and tmp != 3 and (self.x != self.north_pos[0])
                        self.state = 'north'
                        self.count = 0
                        self.bound_pos = (self.x, self.y)
                    return possible_moves[tmp][0]

        if self.state == 'north':
            self.sec_to_last_move_2 = 2
            self.last_move_2 = 1
            if possible_moves[0][1]:
                self.update_bounds(0)
                self.count += 1
                #self.sec_to_last_move_2 = self.last_move
                #self.last_move_2 = possible_moves[0][0]
                return possible_moves[0][0]

            #if (self.max[1]-self.y) >= 1:
            #    self.count += 1
            #    self.state = 'terminate'
            #    return possible_moves[0][0]

            if self.bound_pos != (self.x, self.y):
                self.north_pos = (self.x, self.y)
                self.state = 'follow_new_boundary' # south xxxxxxxxxxx
                self.sec_move = False
            else:
                self.state = 'follow_boundary'
            return -1


        if self.state == 'follow_new_boundary':
            if (self.x, self.y) == self.bound_pos:
                self.state = 'follow_boundary'
                return -1

            if (self.x, self.y) == self.north_pos and self.sec_move:
                self.state = 'terminate'
                return 0

            self.sec_move = True

            for i in range(6):
                if (self.last_move_2-self.sec_to_last_move_2 +3)%6 != 0:
                    tmp = (self.last_move_2 - 1 + i) % 6
                else:
                    tmp = (self.last_move_2 - 2 + i) % 6

                if possible_moves[tmp][1]:
                    self.sec_to_last_move_2 = self.last_move_2
                    self.last_move_2 = tmp
                    self.update_bounds(tmp)
                    return possible_moves[tmp][0]

        return -1


class MoveOnSurface():
    def __init__(self):
        self.state = 'move_bot'
        self.surface_state = 'TC'
        self.unique_point_state = 'computing'
        self.last_move = -1
        self.move_decision = 0
        self.check_placing_flag = False
        # front, back, left1, left2, right1, right2
        self.movable = [False, False, False, False, False, False]
        self.move_algorithm = TraverseLayer()

    def reset(self):
        self.state = 'move_bot'
        self.surface_state = 'TC'
        self.check_placing_flag = False
        self.movable = [False, False, False, False, False, False]
        self.move_algorithm.reset()

    def take_move_decision(self):
        # (0, north), (1, south), (2, westnorth), (3, westsouth), (4, eastnorth), (5, eastsouth)
        possible_moves = []
        for i in [0,5,3,1,2,4]:
            possible_moves.append((i, self.movable[i]))

        tmp = self.move_algorithm.move(possible_moves)
        if self.move_algorithm.state == 'terminate':
            self.check_placing_flag = True

        if self.move_algorithm.state == 'terminate_completely':
            self.state = 'terminate_completely'
        return tmp

    def move(self, directions):
        self.check_placing_flag = False

        if self.state == 'move_bot':
            if directions[2][1] == None:
                if self.movable[0]:
                    self.state = 'terminate'
                    self.check_placing_flag = True
                    return directions[2][0]

            if directions[3][1] == None:
                if self.movable[1]:
                    self.state = 'terminate'
                    self.check_placing_flag = True
                    return directions[3][0]

            if directions[4][1] == None:
                if self.movable[2]:
                    self.state = 'terminate'
                    self.check_placing_flag = True
                    return directions[4][0]

            if directions[5][1] == None:
                if self.movable[3]:
                    self.state = 'terminate'
                    self.check_placing_flag = True
                    return directions[5][0]

            if directions[6][1] == None:
                if self.movable[4]:
                    self.state = 'terminate'
                    self.check_placing_flag = True
                    return directions[6][0]

            if directions[7][1] == None:
                if self.movable[5]:
                    self.state = 'terminate'
                    self.check_placing_flag = True
                    return directions[7][0]


            if directions[2][1] != None:
                self.movable[0] = True

            if directions[3][1] != None:
                self.movable[1] = True

            if directions[4][1] != None or directions[8][1] != None:
                self.movable[2] = True

            if directions[5][1] != None or directions[9][1] != None:
                self.movable[3] = True

            if directions[6][1] != None or directions[10][1] != None:
                self.movable[4] = True

            if directions[7][1] != None or directions[11][1] != None:
                self.movable[5] = True


            if directions[1][1] != None:
                return directions[1][0]
            else:
                self.check_placing_flag = True
                self.movable = [False, False, False, False, False, False]
                self.state = 'check_neighbors'
                return -1 # Do not move to give time for placing decision

        if self.state == 'check_neighbors':
            if directions[2][1] != None:
                self.movable[0] = True

            if directions[3][1] != None:
                self.movable[1] = True

            if directions[4][1] != None or directions[8][1] != None:
                self.movable[2] = True

            if directions[5][1] != None or directions[9][1] != None:
                self.movable[3] = True

            if directions[6][1] != None or directions[10][1] != None:
                self.movable[4] = True

            if directions[7][1] != None or directions[11][1] != None:
                self.movable[5] = True

            # Move to top and take decision
            if directions[0][1] != None:
                return directions[0][0]
            else:
                self.move_decision = self.take_move_decision()
                if self.move_decision == -1:
                    return -1
                self.state = 'take_move'

        if self.state == 'take_move':
            self.movable = [False, False, False, False, False, False]

            if self.move_algorithm.state == 'terminate':
                self.check_placing_flag = True
                self.state = 'terminate'
                self.last_move = directions[2][0]
                return directions[2][0]

            if self.move_decision == 0 and directions[2][1] != None:
                self.state = 'move_bot'
                self.last_move = directions[2][0]
                return directions[2][0]

            if self.move_decision == 1 and directions[3][1] != None:
                self.state = 'move_bot'
                self.last_move = directions[3][0]
                return directions[3][0]

            if self.move_decision == 2 and directions[4][1] != None:
                self.state = 'move_bot'
                self.last_move = directions[4][0]
                return directions[4][0]

            if self.move_decision == 2 and directions[8][1] != None:
                self.state = 'move_bot'
                self.last_move = directions[8][0]
                return directions[8][0]

            if self.move_decision == 3 and directions[5][1] != None:
                self.state = 'move_bot'
                self.last_move = directions[5][0]
                return directions[5][0]

            if self.move_decision == 3 and directions[9][1] != None:
                self.state = 'move_bot'
                self.last_move = directions[9][0]
                return directions[9][0]

            if self.move_decision == 4 and directions[6][1] != None:
                self.state = 'move_bot'
                self.last_move = directions[6][0]
                return directions[6][0]

            if self.move_decision == 4 and directions[10][1] != None:
                self.state = 'move_bot'
                self.last_move = directions[10][0]
                return directions[10][0]

            if self.move_decision == 5 and directions[7][1] != None:
                self.state = 'move_bot'
                self.last_move = directions[7][0]
                return directions[7][0]

            if self.move_decision == 5 and directions[11][1] != None:
                self.state = 'move_bot'
                self.last_move = directions[11][0]
                return directions[11][0]

            # go straight down
            return directions[1][0]

        return -1

class FindShiftableLine():
    def __init__(self):
        self.x = 0
        self.y = 0
        self.z = 0
        self.tile_found = False

    def find_tile(self):
        global dodecahedrons
        self.tile_found = False

        for i in dodecahedrons:
            tmp1 = (i.top != None) or (i.bottom != None)
            tmp2 = (i.upleft1 != None) or (i.upleft2 != None) or (i.upright1 != None) or (i.upright2 != None)
            tmp3 = (i.downleft1 != None) or (i.downleft2 != None) or (i.downright1 != None) or (i.downright2 != None)

            if tmp1 or (tmp2 and tmp3):
                self.x = i.x
                self.y = i.y
                self.z = i.z
                self.tile_found = True


class Robot():
    def __init__(self):
        global dodecahedrons
        self.state = 'find_shiftable_row'#'move_random'
        self.x = global_start_node.x
        self.y = global_start_node.y
        self.z = global_start_node.z

        self.x_max = self.x
        self.x_min = self.x
        self.y_max = self.y
        self.y_min = self.y
        self.z_max = self.z
        self.z_min = self.z

        self.goto_x = 0
        self.goto_y = 0
        self.goto_z = 0

        self.grabbed_tile = None
        self.removable_tile = None
        self.tiles = dodecahedrons

        # Robot procedurs
        self.find_local_maximum = FindLocalMaximum()
        self.shift_or_take = ShiftOrTake()
        self.shift_or_take.robot = self
        self.move_on_surface = MoveOnSurface()
        self.find_shiftable_line = FindShiftableLine()

        # Neighbors
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

    def detect_neighbors(self):
        # reset neighbors
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

        # search neighbors
        for x in self.tiles:
            if (x.x, x.y, x.z + 1) == (self.x, self.y, self.z):
                self.bottom = x

            if (x.x, x.y, x.z - 1) == (self.x, self.y, self.z):
                self.top = x

            if (x.x + 1, x.y, x.z) == (self.x, self.y, self.z):
                self.back = x

            if (x.x - 1, x.y, x.z) == (self.x, self.y, self.z):
                self.front = x

            if (x.x - 0.5, x.y + 0.75, x.z + 0.5) == (self.x, self.y, self.z):
                self.downright2 = x

            if (x.x - 0.5, x.y - 0.75, x.z + 0.5) == (self.x, self.y, self.z):
                self.downright1 = x

            if (x.x + 0.5, x.y + 0.75, x.z + 0.5) == (self.x, self.y, self.z):
                self.downleft2 = x

            if (x.x + 0.5, x.y - 0.75, x.z + 0.5) == (self.x, self.y, self.z):
                self.downleft1 = x

            if (x.x - 0.5, x.y + 0.75, x.z - 0.5) == (self.x, self.y, self.z):
                self.upright2 = x

            if (x.x - 0.5, x.y - 0.75, x.z - 0.5) == (self.x, self.y, self.z):
                self.upright1 = x

            if (x.x + 0.5, x.y + 0.75, x.z - 0.5) == (self.x, self.y, self.z):
                self.upleft2 = x

            if (x.x + 0.5, x.y - 0.75, x.z - 0.5) == (self.x, self.y, self.z):
                self.upleft1 = x

    def grab_tile(self):
        tile = None
        for i in self.tiles:
            if (i.x, i.y, i.z) == (self.x, self.y, self.z):
                tile = i
                break

        if tile != None and self.grabbed_tile == None:
            tile.delete_neighbor_links()
            self.grabbed_tile = tile

    def place_tile(self):
        self.grabbed_tile.find_neighbours(self.tiles)
        self.grabbed_tile = None

    def random_move(self, directions):
        for _ in range(10):
            i = random.choice(directions)
            if i[1] != None:
                return i[0]

    def act_move(self, pos):
        # move robot
        if pos == 0:
            self.z += 1

        if pos == 1:
            self.z -= 1

        if pos == 2:
            self.x += 1

        if pos == 3:
            self.x -= 1

        if pos == 4:
            self.x -= 0.5
            self.y += 0.75
            self.z += 0.5

        if pos == 5:
            self.x -= 0.5
            self.y -= 0.75
            self.z += 0.5

        if pos == 6:
            self.x += 0.5
            self.y += 0.75
            self.z += 0.5

        if pos == 7:
            self.x += 0.5
            self.y -= 0.75
            self.z += 0.5

        if pos == 8:
            self.x -= 0.5
            self.y += 0.75
            self.z -= 0.5

        if pos == 9:
            self.x -= 0.5
            self.y -= 0.75
            self.z -= 0.5

        if pos == 10:
            self.x += 0.5
            self.y += 0.75
            self.z -= 0.5

        if pos == 11:
            self.x += 0.5
            self.y -= 0.75
            self.z -= 0.5

        if pos == 12:
            self.grab_tile()
            if self.grabbed_tile == self.removable_tile:
                self.removable_tile = None

        if pos == 13:
            self.place_tile()

        if pos == 15:
            #TODO: remove later
            self.x = self.goto_x
            self.y = self.goto_y
            self.z = self.goto_z

        # update known box
        if self.x_max < self.x:
            self.x_max = self.x

        if self.x_min > self.x:
            self.x_min = self.x

        if self.y_max < self.y:
            self.y_max = self.y

        if self.y_min > self.y:
            self.y_min = self.y

        if self.z_max < self.z:
            self.z_max = self.z

        if self.z_min > self.z:
            self.z_min = self.z

    def find_tile_at_current_position(self):
        for i in dodecahedrons:
            if (i.x, i.y, i.z) == (self.x, self.y, self.z) and i != self.grabbed_tile:
                return i
        return None

    def next_move(self):
        print(self.state)
        pos = -1
        self.detect_neighbors()
        directions = [(0, self.top), (1, self.bottom), (2, self.front), (3, self.back),
                      (4, self.upleft1), (5, self.upleft2), (6, self.upright1), (7, self.upright2),
                      (8, self.downleft1), (9, self.downleft2), (10, self.downright1), (11, self.downright2)]

        move_possible = True

        if self.state == 'move_random' and move_possible:
            move_possible = False
            pos = self.random_move(directions)

        if self.state == 'find_local_maximum' and move_possible:
            self.shift_or_take.reset()
            move_possible = False
            pos = self.find_local_maximum.move(directions)
            if self.find_local_maximum.state == 'terminate':
                self.find_local_maximum.reset()
                self.state = 'shift_or_take'

        if self.state == 'shift_or_take' and move_possible:
            move_possible = False
            tile = self.find_tile_at_current_position()
            pos = self.shift_or_take.move(directions, tile)
            if self.shift_or_take.state == 'terminate':
                if self.shift_or_take.removable_tile != None:
                    self.removable_tile = self.shift_or_take.removable_tile
                    self.move_on_surface.reset()#xxxxxxxxxx
                    self.state = 'move_on_surface'
                else:
                    self.removable_tile = self.shift_or_take.removable_tile
                    self.state = 'move_one_step_down'
                self.shift_or_take.reset()


        if self.state == 'move_on_surface' and move_possible:
            move_possible = False
            pos = self.move_on_surface.move(directions)

            if self.move_on_surface.state == 'terminate_completely':
                self.state = 'switch_orientation'

            if self.grabbed_tile != None and self.move_on_surface.state == 'terminate':
                if pos == -1:
                    self.move_on_surface.reset()
                    self.state = 'place_tile'

        if self.state == 'place_tile' and move_possible:
            move_possible = False
            pos = 13
            self.state = 'goto_removable_tile'

            if self.move_on_surface != None:
                self.move_on_surface.move_algorithm.reset()

        if self.state == 'goto_removable_tile' and move_possible:
            #TODO: find path to tile
            move_possible = False

            self.goto_x = self.removable_tile.x
            self.goto_y = self.removable_tile.y
            self.goto_z = self.removable_tile.z

            pos = 15
            self.state = 'grab_tile'

        if self.state == 'grab_tile' and move_possible:
            move_possible = False
            pos = 12
            self.removable_tile = None
            self.state = 'find_shiftable_row'
            self.shift_or_take.reset()

        if self.state == 'move_one_step_down' and move_possible:
            move_possible = False
            pos = directions[1][0]
            self.state = 'find_shiftable_row'

        if self.state == 'find_shiftable_row' and move_possible:
            move_possible = False
            self.find_shiftable_line.find_tile()
            if self.find_shiftable_line.tile_found:
                self.goto_x = self.find_shiftable_line.x
                self.goto_y = self.find_shiftable_line.y
                self.goto_z = self.find_shiftable_line.z
                pos = 15
                self.state = 'find_local_maximum'
            else:
                self.state = 'terminate'


        if self.state == 'switch_orientation':
            global global_switch
            global dodecahedrons

            if global_switch:
                global_switch = False
                for i in dodecahedrons:
                    tmp = i.x
                    i.x = i.z
                    i.z = -tmp
                    i.scene.setPos(i.x, i.y, i.z)

                tmp = self.x
                self.x = self.z
                self.z = -tmp
                self.state = 'find_shiftable_row'

                for i in dodecahedrons:
                    i.find_neighbours(dodecahedrons)
                self.detect_neighbors()

        if self.state != 'terminate':
            self.act_move(pos)


# Robot Motion End ----------------------------------------------------------------------







#plot_with_matplotlib()

app = Simulator3D()

app.run()
