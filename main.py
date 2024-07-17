from math import pi, sin, cos
import simplepbr
import globalvars
from robots.constauto.robot import *
from direct.showbase.ShowBase import ShowBase
from direct.gui.OnscreenText import OnscreenText
from direct.task import Task
from potential import potential
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
        self.robot = ConstRobot()

        tmp = Dodecahedron(globalvars.global_start_node.x, globalvars.global_start_node.y,
                           globalvars.global_start_node.z)
        globalvars.dodecahedrons.append(tmp)
        self.grabbed_tile = tmp

        self.x = tmp.x
        self.y = tmp.y
        self.z = tmp.z

        # Model complete, store in file
        if globalvars.load_file == "":
            f = open(globalvars.store_file, "w")
            f.writelines(str(self.x) + " " +  str(self.y) + " " + str(self.z) + " ")
            for dodec in globalvars.dodecahedrons:
                f.writelines(str(dodec.x) + " " + str(dodec.y)+ " " + str(dodec.z)+ " ")
            f.close()



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

        # Add potential score
        self.textObject = OnscreenText(text='Potential: 0', pos=(-0.7, 0.9), scale=0.07)


    def stop(self):
        self.running = not self.running
        print("Pause")

    def switch_orientation(self):
        globalvars.global_switch = True

    def detect_occupied(self):
        for x in globalvars.dodecahedrons:
            if (x.x, x.y, x.z) == (self.x, self.y, self.z):
                if x != self.grabbed_tile:
                    return True
        return False

    def detect_neighbors(self):
        # search neighbors
        movable = []
        for x in globalvars.dodecahedrons:
            if (x.x, x.y, x.z) == (self.x, self.y, self.z + 1):
                movable.append('U')

            if (x.x, x.y, x.z) == (self.x, self.y, self.z - 1):
                movable.append('D')

            if (x.x, x.y, x.z) == (self.x + 1, self.y, self.z):
                movable.append('F')

            if (x.x, x.y, x.z) == (self.x - 1, self.y, self.z):
                movable.append('B')

            if (x.x, x.y, x.z) == (self.x-0.5, self.y+0.75, self.z+0.5):
                movable.append('UBR')

            if (x.x, x.y, x.z) == (self.x-0.5, self.y-0.75, self.z+0.5):
                movable.append('UBL')

            if (x.x, x.y, x.z) == (self.x+0.5, self.y+0.75, self.z+0.5):
                movable.append('UFR')

            if (x.x, x.y, x.z) == (self.x+0.5, self.y-0.75, self.z+0.5):
                movable.append('UFL')

            if (x.x, x.y, x.z) == (self.x-0.5, self.y+0.75, self.z-0.5):
                movable.append('DBR')

            if (x.x, x.y, x.z) == (self.x-0.5, self.y-0.75, self.z-0.5):
                movable.append('DBL')

            if (x.x, x.y, x.z) == (self.x+0.5, self.y+0.75, self.z-0.5):
                movable.append('DFR')

            if (x.x, x.y, x.z) == (self.x+0.5, self.y-0.75, self.z-0.5):
                movable.append('DFL')

        return movable

    def grab_tile(self):
        tile = None
        for i in globalvars.dodecahedrons:
            if (i.x, i.y, i.z) == (self.x, self.y, self.z):
                tile = i
                break

        if tile != None and self.grabbed_tile == None:
            tile.delete_neighbor_links()
            self.grabbed_tile = tile
        else:
            if tile == None:
                raise Exception("Error: Could not grab tile. There is no tile.")
            else:
                raise Exception("Error: Could not grab tile. Already carrying one.")

    def place_tile(self):
        count = 0
        for i in globalvars.dodecahedrons:
            if (i.x, i.y, i.z) == (self.x, self.y, self.z):
                count = count + 1
                break
        if count > 1:
            raise Exception("Error: Position is occupied. Tile can not be placed.")

        if self.grabbed_tile == None:
            raise Exception("Error: Carrying no tile. Tile can not be placed.")

        self.grabbed_tile.find_neighbours(globalvars.dodecahedrons)
        self.grabbed_tile = None

    def act_move(self, pos):
        # move robot
        if pos == 'U':
            return self.x, self.y, self.z + 1

        if pos == 'D':
            return self.x, self.y, self.z - 1

        if pos == 'F':
            return self.x + 1, self.y, self.z

        if pos == 'B':
            return self.x - 1, self.y, self.z

        if pos == 'UBR':
            return self.x - 0.5, self.y + 0.75, self.z + 0.5

        if pos == 'UBL':
            return self.x - 0.5, self.y - 0.75, self.z + 0.5

        if pos == 'UFR':
            return self.x + 0.5, self.y + 0.75, self.z + 0.5

        if pos == 'UFL':
            return self.x + 0.5, self.y - 0.75, self.z + 0.5

        if pos == 'DBR':
            return self.x - 0.5, self.y + 0.75, self.z - 0.5

        if pos == 'DBL':
            return self.x - 0.5, self.y - 0.75, self.z - 0.5

        if pos == 'DFR':
            return self.x + 0.5, self.y + 0.75, self.z - 0.5

        if pos == 'DFL':
            return self.x + 0.5, self.y - 0.75, self.z - 0.5

        if pos == 'grab_tile':
            self.grab_tile()
            return self.x, self.y, self.z

        if pos == 'place_tile':
            self.place_tile()
            return self.x, self.y, self.z

        return self.x, self.y, self.z

    # Define a procedure to move the robot.
    def moveRobot(self, task):
        if not self.running:
            return Task.cont

        steps = 10 #yyyyyyyyyyyyyyyyyyyyyyyy
        if self.interpolation_move == 0:
            # Get next move from robot
            moves = self.detect_neighbors()
            occupied = self.detect_occupied()
            if moves != []:
                next_move = self.robot.next_move(moves, occupied)
                self.x_next, self.y_next, self.z_next = self.act_move(next_move)

        inter_x = self.x + (self.x_next - self.x) * self.interpolation_move / steps
        inter_y = self.y + (self.y_next - self.y) * self.interpolation_move / steps
        inter_z = self.z + (self.z_next - self.z) * self.interpolation_move / steps

        self.scene.setPos(inter_x, inter_y, inter_z)
        self.interpolation_move += 1

        if self.grabbed_tile != None:
            self.grabbed_tile.scene.setPos(inter_x, inter_y, inter_z)

        if self.interpolation_move == steps+1:
            self.textObject.setText("Potential_X: " + str(potential.potential_x(self.grabbed_tile)) + ", " + "Potential_Z: " + str(potential.potential_z(self.grabbed_tile)))
            self.interpolation_move = 0
            self.x = self.x_next
            self.y = self.y_next
            self.z = self.z_next

            if self.grabbed_tile != None:
                self.grabbed_tile.x = self.x
                self.grabbed_tile.y = self.y
                self.grabbed_tile.z = self.z

        return Task.cont



# Build configuration
def build_new_configuration():
    if globalvars.load_file == "":
        globalvars.dodecahedrons = [Dodecahedron(0,0,0)]
        for i in range(globalvars.number_of_times):
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




build_new_configuration()

app = Simulator3D()

app.run()
