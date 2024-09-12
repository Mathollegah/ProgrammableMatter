from math import pi, sin, cos
import simplepbr
import globalvars
from robots.constauto.robot import *
from direct.showbase.ShowBase import ShowBase
from direct.gui.OnscreenText import OnscreenText
from direct.task import Task
from potential import potential
import random
import argparse

##############################################################################

from direct.showbase.ShowBase import ShowBase
from direct.showbase.DirectObject import DirectObject
from panda3d.core import GeomVertexFormat, GeomVertexData
from panda3d.core import Geom, GeomTriangles, GeomVertexWriter
from panda3d.core import Texture, GeomNode
from panda3d.core import PerspectiveLens
from panda3d.core import Light, Spotlight
from panda3d.core import LVector3
from direct.directtools.DirectGeometry import LineNodePath
from panda3d.core import Vec4

from panda3d.core import (
    Geom,
    GeomNode,
    GeomTriangles,
    GeomVertexData,
    GeomVertexFormat,
    GeomVertexWriter,
)

def add_axis(render, x_max, x_min, y_max, y_min, z_max, z_min):
    vertical = LineNodePath(render, colorVec=Vec4(0, 0, 0, 1))
    vertical.setThickness(12)
    vertical.drawLines([((x_min, y_min, z_min), (x_max, y_min, z_min))])
    vertical.drawLines([((x_min, y_min, z_min), (x_min, y_max, z_min))])
    vertical.drawLines([((x_min, y_min, z_min), (x_min, y_min, z_max))])
    vertical.create()
    vertical.reparentTo(render)

def add_bounding_box(render, x_max, x_min, y_max, y_min, z_max, z_min):
    # the bounding box is hardly inspired from https://github.com/panda3d/panda3d/blob/master/samples/procedural-cube/main.py
    def normalized(*args):
        myVec = LVector3(*args)
        myVec.normalize()
        return myVec

    def makeSquare(x1, y1, z1, x2, y2, z2):
        format = GeomVertexFormat.getV3n3cpt2()
        vdata = GeomVertexData('square', format, Geom.UHDynamic)

        vertex = GeomVertexWriter(vdata, 'vertex')
        normal = GeomVertexWriter(vdata, 'normal')
        color = GeomVertexWriter(vdata, 'color')
        texcoord = GeomVertexWriter(vdata, 'texcoord')

        # make sure we draw the sqaure in the right plane
        if x1 != x2:
            vertex.addData3(x1, y1, z1)
            vertex.addData3(x2, y1, z1)
            vertex.addData3(x2, y2, z2)
            vertex.addData3(x1, y2, z2)

            normal.addData3(normalized(2 * x1 - 1, 2 * y1 - 1, 2 * z1 - 1))
            normal.addData3(normalized(2 * x2 - 1, 2 * y1 - 1, 2 * z1 - 1))
            normal.addData3(normalized(2 * x2 - 1, 2 * y2 - 1, 2 * z2 - 1))
            normal.addData3(normalized(2 * x1 - 1, 2 * y2 - 1, 2 * z2 - 1))

        else:
            vertex.addData3(x1, y1, z1)
            vertex.addData3(x2, y2, z1)
            vertex.addData3(x2, y2, z2)
            vertex.addData3(x1, y1, z2)

            normal.addData3(normalized(2 * x1 - 1, 2 * y1 - 1, 2 * z1 - 1))
            normal.addData3(normalized(2 * x2 - 1, 2 * y2 - 1, 2 * z1 - 1))
            normal.addData3(normalized(2 * x2 - 1, 2 * y2 - 1, 2 * z2 - 1))
            normal.addData3(normalized(2 * x1 - 1, 2 * y1 - 1, 2 * z2 - 1))

        texcoord.addData2f(0.0, 1.0)
        texcoord.addData2f(0.0, 0.0)
        texcoord.addData2f(1.0, 0.0)
        texcoord.addData2f(1.0, 1.0)

        # Quads aren't directly supported by the Geom interface
        # you might be interested in the CardMaker class if you are
        # interested in rectangle though
        tris = GeomTriangles(Geom.UHDynamic)
        tris.addVertices(0, 1, 3)
        tris.addVertices(1, 2, 3)

        square = Geom(vdata)
        square.addPrimitive(tris)
        return square

    square0 = makeSquare(x_min, y_min, z_min, x_max, y_min, z_max)
    square1 = makeSquare(x_min, y_max, z_min, x_max, y_max, z_max)
    square2 = makeSquare(x_min, y_max, z_max, x_max, y_min, z_max)
    square3 = makeSquare(x_min, y_max, z_min, x_max, y_min, z_min)
    square4 = makeSquare(x_min, y_min, z_min, x_min, y_max, z_max)
    square5 = makeSquare(x_max, y_min, z_min, x_max, y_max, z_max)
    snode = GeomNode('square')
    snode.addGeom(square0)
    snode.addGeom(square1)
    snode.addGeom(square2)
    snode.addGeom(square3)
    snode.addGeom(square4)
    snode.addGeom(square5)

    cube = render.attachNewNode(snode)
    cube.setTransparency(True)
    cube.setColor(0.1, 0.1, 0.1, 0.7)
    return cube





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

        self.hide = False
        self.pot_x = None
        self.pot_z = None

        self.directions = [(0, self.top), (1, self.bottom), (2, self.front), (3, self.back),
                           (4, self.upleft1), (5, self.upleft2), (6, self.upright1), (7, self.upright2),
                           (8, self.downleft1), (9,self.downleft2), (10, self.downright1), (11,self.downright2)]

        self.component = []

    def find_neighbours(self, lst):
        for x in lst:
            if (x.x, x.y, x.z+1) == (self.x, self.y, self.z):
                self.bottom = x
                x.top = self
                self.component = self.component + x.component

            if (x.x, x.y, x.z-1) == (self.x, self.y, self.z):
                self.top = x
                x.bottom = self
                self.component = self.component + x.component

            if (x.x+1, x.y, x.z) == (self.x, self.y, self.z):
                self.back = x
                x.front = self
                self.component = self.component + x.component

            if (x.x-1, x.y, x.z) == (self.x, self.y, self.z):
                self.front = x
                x.back = self
                self.component = self.component + x.component

            if (x.x - 0.5, x.y + 0.75, x.z + 0.5) == (self.x, self.y, self.z):
                self.downright2 = x
                x.upleft1 = self
                self.component = self.component + x.component

            if (x.x - 0.5, x.y - 0.75, x.z + 0.5) == (self.x, self.y, self.z):
                self.downright1 = x
                x.upleft2 = self
                self.component = self.component + x.component

            if (x.x + 0.5, x.y + 0.75, x.z + 0.5) == (self.x, self.y, self.z):
                self.downleft2 = x
                x.upright1 = self
                self.component = self.component + x.component

            if (x.x + 0.5, x.y - 0.75, x.z + 0.5) == (self.x, self.y, self.z):
                self.downleft1 = x
                x.upright2 = self
                self.component = self.component + x.component

            if (x.x - 0.5, x.y + 0.75, x.z - 0.5) == (self.x, self.y, self.z):
                self.upright2 = x
                x.downleft1 = self
                self.component = self.component + x.component

            if (x.x - 0.5, x.y - 0.75, x.z - 0.5) == (self.x, self.y, self.z):
                self.upright1 = x
                x.downleft2 = self
                self.component = self.component + x.component

            if (x.x + 0.5, x.y + 0.75, x.z - 0.5) == (self.x, self.y, self.z):
                self.upleft2 = x
                x.downright1 = self
                self.component = self.component + x.component

            if (x.x + 0.5, x.y - 0.75, x.z - 0.5) == (self.x, self.y, self.z):
                self.upleft1 = x
                x.downright2 = self
                self.component = self.component + x.component

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
        if not globalvars.onlygenerate:
            ShowBase.__init__(self)
            simplepbr.init()
        self.accept('s', self.stop)
        self.accept('h', self.hide_tile)
        self.accept('b', self.hide_bounding_box)

        self.accept('o', self.faster)
        self.accept('l', self.slower)

        self.accept('p', self.hide_not_pot_zero)

        self.running = True
        self.count = 0

        if globalvars.load_file == "":
            tmp = random.choice(globalvars.dodecahedrons)
            #for i in globalvars.dodecahedrons:
            #    if i.z > tmp.x:
            #        tmp = i
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

        globalvars.robot_coordinates = (self.x, self.y, self.z)

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

        self.hidden_tile = None
        self.hidden = False
        if not globalvars.onlygenerate:
            self.scene = self.loader.loadModel("models/robot.glb")
            self.scene.reparentTo(self.render)
            self.scene.setScale(4.0 / 8.0, 4.0 / 8.0, 4.0 / 8.0)
            self.scene.setPos(self.x, self.y, self.z)
            self.bounding_box = None

            for x in globalvars.dodecahedrons:
                x.scene = self.loader.loadModel("models/dodeca.glb")
                x.scene.reparentTo(self.render)
                x.scene.setTransparency(True)
                x.scene.setColor(1, 1, 1, 1.0)
                x.scene.setScale(1.0/2.75, 1.0/2.75, 1.0/2.75)
                x.scene.setPos(x.x, x.y, x.z)

        # Add bounding box
        x_max=-100
        x_min=100
        y_max = -100
        y_min = 100
        z_max = -100
        z_min = 100
        for x in globalvars.dodecahedrons:
            if x.x > x_max:
                x_max = x.x
            if x.x < x_min:
                x_min = x.x

            if x.y > y_max:
                y_max = x.y
            if x.y < y_min:
                y_min = x.y

            if x.z > z_max:
                z_max = x.z
            if x.z < z_min:
                z_min = x.z

        if not globalvars.onlygenerate:
            add_axis(self.render, x_max + 0.5, x_min - 0.5, y_max + 0.5, y_min - 0.5,
                     z_max + 0.5, z_min - 0.5)
            self.bounding_box = add_bounding_box(self.render, x_max + 0.5, x_min - 0.5, y_max + 0.5, y_min - 0.5,
                                             z_max + 0.5, z_min - 0.5)
        if not globalvars.global_bound_box and not globalvars.onlygenerate:
            self.bounding_box.hide()

        # Add the move robot procedure.
        if not globalvars.onlygenerate:
            self.taskMgr.add(self.moveRobot, "MoveRobot")

        # Add potential score
        if not globalvars.onlygenerate:
            self.textObject = OnscreenText(text='Potential: 0', pos=(-0.7, 0.9), scale=0.07)

    def hide_tile(self):
        if self.hidden_tile != None:
            self.hidden = not self.hidden
            if not self.hidden:
                self.hidden_tile.scene.show()
            else:
                self.hidden_tile.scene.hide()

    def hide_bounding_box(self):
        globalvars.global_bound_box = not globalvars.global_bound_box
        if not globalvars.global_bound_box:
            self.bounding_box.show()
        else:
            self.bounding_box.hide()

    def stop(self):
        self.running = not self.running
        print("Pause")

    def slower(self):
        globalvars.new_interpolation_steps += 3

    def faster(self):
        if globalvars.new_interpolation_steps > 3:
            globalvars.new_interpolation_steps -= 3

    def hide_not_pot_zero(self):
        tower_lst = []
        for tile in globalvars.dodecahedrons:
            if (tile.pot_x, tile.pot_z) != (0, 0):
                tower_lst.append((tile.x, tile.y))

        print(tower_lst)
        for tile in globalvars.dodecahedrons:
            if (tile.pot_x, tile.pot_z) == (0, 0) and not (tile.x, tile.y) in tower_lst:
                #tile.scene.hide()
                tile.scene.setTransparency(True)
                tile.scene.setColor(0.1, 0.1, 0.1, 0.3)

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
            if not x.hide:
                if not self.robot.switched_orientation:
                    if (x.x, x.y, x.z) == (self.x, self.y, self.z + 1):
                        movable.append('U')
                else:
                    if (x.x, x.y, x.z) == (self.x + 1, self.y, self.z):
                        movable.append('F')

                if (self.hidden_tile == None) or (self.x,self.y,self.z) != (self.hidden_tile.x, self.hidden_tile.y, self.hidden_tile.z):
                    if (x.x, x.y, x.z) == (self.x, self.y, self.z - 1):
                        movable.append('D')

                    if not self.robot.switched_orientation:
                        if (x.x, x.y, x.z) == (self.x + 1, self.y, self.z):
                            movable.append('F')
                    else:
                        if (x.x, x.y, x.z) == (self.x, self.y, self.z + 1):
                            movable.append('U')

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

        if pos == 'place_and_hide_tile':
            #print("Was here")
            self.grabbed_tile.hide = True
            self.hidden_tile = self.grabbed_tile
            self.place_tile()
            return self.x, self.y, self.z

        if pos == 'grab_tile_and_show_hidden_tile':
            self.hidden_tile.hide = False
            x = self.hidden_tile.x
            y = self.hidden_tile.y
            z = self.hidden_tile.z
            self.hidden_tile = None
            self.grab_tile()
            if globalvars.logarithmic_memory:
                return self.x, self.y, self.z
            else:
                return x,y,z

        return self.x, self.y, self.z

    def init_visualization(self):
        for dod in globalvars.dodecahedrons:
            dod.scene.setPos(dod.x, dod.y, dod.z)

    # Define a procedure to move the robot.
    def moveRobot(self, task):
        if not self.running:
            return Task.cont
        #print(self.robot.place_tile.move_on_surface.traverse_surface.state)
        #print(self.robot.place_tile.move_on_surface.traverse_surface.path)
        steps = globalvars.interpolation_steps
        if self.interpolation_move == 0:
            # Get next move from robot
            moves = self.detect_neighbors()
            occupied = self.detect_occupied()
            if moves != []:
                next_move = self.robot.next_move(moves, occupied)
                #print(self.robot.state, moves)
                self.x_next, self.y_next, self.z_next = self.act_move(next_move)
                #print(self.robot.place_tile.state)
                #print(self.robot.place_tile.move_on_surface.traverse_surface.bound_dir, self.robot.place_tile.move_on_surface.traverse_surface.state, self.robot.place_tile.move_on_surface.traverse_surface.up_inst.bound_dir)
                #print(self.robot.place_tile.move_on_surface.traverse_surface.up_inst.state)


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

            globalvars.robot_coordinates = (self.x, self.y, self.z)
            globalvars.interpolation_steps = globalvars.new_interpolation_steps

            if self.grabbed_tile != None:
                self.grabbed_tile.x = self.x
                self.grabbed_tile.y = self.y
                self.grabbed_tile.z = self.z

        return Task.cont


    def moveRobotNoAnimation(self):
        if not self.running:
            return

        self.count += 1

        # Get next move from robot
        moves = self.detect_neighbors()
        occupied = self.detect_occupied()
        if moves != []:
            next_move = self.robot.next_move(moves, occupied)
            self.x_next, self.y_next, self.z_next = self.act_move(next_move)
            #print(next_move)
            #if (self.hidden_tile != None) and (self.x_next, self.y_next, self.z_next) == (
            #self.hidden_tile.x, self.hidden_tile.y, self.hidden_tile.z) and (next_move != 'place_and_hide_tile'):
            #    raise "Went over hidden tile! That should not happen!"

            #if (self.hidden_tile != None) and (self.x, self.y, self.z) == (
            #self.hidden_tile.x, self.hidden_tile.y, self.hidden_tile.z) and (next_move != 'U') and (next_move != 'D') and (next_move != 'place_and_hide_tile') and (self.robot.place_tile.test_pos_state == 'move_front'):
            #    print(self.robot.place_tile.state)
            #    print(self.robot.place_tile.test_pos_state)
            #    raise "Went in not allowed direction!"
            if next_move != None:
                globalvars.global_move_count += 1
                if self.robot.print_state == 'find_shiftable_row':
                    if globalvars.logarithmic_memory:
                        globalvars.movecounter['find_shiftable_row'] += 1
                    else:
                        globalvars.movecounter['find_shiftable_row'] += 3
                        globalvars.global_move_count += 2
                if self.robot.print_state == 'locally_highest_row':
                    globalvars.movecounter['locally_highest_row'] += 1
                if self.robot.print_state == 'shift_or_take':
                    globalvars.movecounter['shift_or_take'] += 1
                if self.robot.print_state == 'place_tile':
                    if globalvars.logarithmic_memory:
                        globalvars.movecounter['place_tile'] += 1
                    else:
                        globalvars.movecounter['place_tile'] += 2
                        globalvars.global_move_count += 1
                if self.robot.print_state == 'take_initial_tile':
                    globalvars.movecounter['take_initial_tile'] += 1
                #globalvars.movecounter['move_pebble'] = 0

        if self.count%globalvars.printsteps == 0:
            pot_x = potential.potential_x(self.grabbed_tile)
            pot_z = potential.potential_z(self.grabbed_tile)
            print("Count: " + str(globalvars.global_move_count) + ", Potential_X: " + str(pot_x) + ", " + "Potential_Z: " + str(pot_z))

            if (pot_x, pot_z) == globalvars.pot:
                globalvars.pot_equal_count += 1
                if globalvars.pot_equal_count > 120*1000/globalvars.printsteps:
                    self.robot.state = 'terminate'
                    print("ERROR")
                    return
            else:
                globalvars.pot = (pot_x, pot_z)
                globalvars.pot_equal_count = 0


        self.x = self.x_next
        self.y = self.y_next
        self.z = self.z_next

        globalvars.robot_coordinates = (self.x, self.y, self.z)

        if self.grabbed_tile != None:
            self.grabbed_tile.x = self.x
            self.grabbed_tile.y = self.y
            self.grabbed_tile.z = self.z

# Build configuration
def build_new_configuration():
    if globalvars.load_file == "" and not globalvars.random_configuration:
        globalvars.dodecahedrons = [Dodecahedron(0,0,0)]
        i=0
        while i < globalvars.number_of_tiles-1:
            x = random.choice(globalvars.dodecahedrons)

            d = random.choice(x.directions)

            if d[1] == None:
                if d[0] == 0:
                    tmp = Dodecahedron(x.x,x.y,x.z+1)
                    globalvars.dodecahedrons.append(tmp)
                    tmp.bottom = x
                    x.top = tmp
                    i = i+1

                if d[0] == 1:
                    tmp = Dodecahedron(x.x,x.y,x.z-1)
                    globalvars.dodecahedrons.append(tmp)
                    tmp.top = x
                    x.bottom = tmp
                    i = i + 1

                if d[0] == 2:
                    tmp = Dodecahedron(x.x+1,x.y,x.z)
                    globalvars.dodecahedrons.append(tmp)
                    tmp.back = x
                    x.front = tmp
                    i = i + 1

                if d[0] == 3:
                    tmp = Dodecahedron(x.x-1,x.y,x.z)
                    globalvars.dodecahedrons.append(tmp)
                    tmp.front = x
                    x.back = tmp
                    i = i + 1

                if d[0] == 4:
                    tmp = Dodecahedron(x.x-0.5,x.y+0.75,x.z+0.5)
                    globalvars.dodecahedrons.append(tmp)
                    tmp.downright2 = x
                    x.upleft1 = tmp
                    i = i + 1

                if d[0] == 5:
                    tmp = Dodecahedron(x.x-0.5,x.y-0.75,x.z+0.5)
                    globalvars.dodecahedrons.append(tmp)
                    tmp.downright1 = x
                    x.upleft2 = tmp
                    i = i + 1

                if d[0] == 6:
                    tmp = Dodecahedron(x.x+0.5,x.y+0.75,x.z+0.5)
                    globalvars.dodecahedrons.append(tmp)
                    tmp.downleft2 = x
                    x.upright1 = tmp
                    i = i + 1

                if d[0] == 7:
                    tmp = Dodecahedron(x.x+0.5,x.y-0.75,x.z+0.5)
                    globalvars.dodecahedrons.append(tmp)
                    tmp.downleft1 = x
                    x.upright2 = tmp
                    i = i + 1

                if d[0] == 8:
                    tmp = Dodecahedron(x.x-0.5,x.y+0.75,x.z-0.5)
                    globalvars.dodecahedrons.append(tmp)
                    tmp.upright2 = x
                    x.downleft1 = tmp
                    i = i + 1

                if d[0] == 9:
                    tmp = Dodecahedron(x.x-0.5,x.y-0.75,x.z-0.5)
                    globalvars.dodecahedrons.append(tmp)
                    tmp.upright1 = x
                    x.downleft2 = tmp
                    i = i + 1

                if d[0] == 10:
                    tmp = Dodecahedron(x.x+0.5,x.y+0.75,x.z-0.5)
                    globalvars.dodecahedrons.append(tmp)
                    tmp.upleft2 = x
                    x.downright1 = tmp
                    i = i + 1

                if d[0] == 11:
                    tmp = Dodecahedron(x.x+0.5,x.y-0.75,x.z-0.5)
                    globalvars.dodecahedrons.append(tmp)
                    tmp.upleft1 = x
                    x.downright2 = tmp
                    i = i + 1

                tmp.find_neighbours(globalvars.dodecahedrons)

                for x in globalvars.dodecahedrons:
                    x.directions = [(0, x.top), (1, x.bottom), (2, x.front), (3, x.back),
                                       (4, x.upleft1), (5, x.upleft2), (6, x.upright1), (7, x.upright2),
                                       (8, x.downleft1), (9, x.downleft2), (10, x.downright1), (11, x.downright2)]

    elif globalvars.load_file == "" and globalvars.random_configuration:
        build_random_configuration()

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


def build_random_configuration():
    def pick_position(boxsize):
        x = random.choice(list(range(boxsize)))
        y = random.choice(list(range(boxsize)))
        z = random.choice(list(range(boxsize)))
        if y%2 == 1:
            x = x+0.5
            z = z+0.5
        y = y * 0.75
        return x, y, z

    print("Generate configuration")
    boxsize = globalvars.boxsize
    components = {}
    component_counter = 0
    globalvars.dodecahedrons = []

    max_component = 0
    comp_name = None
    while max_component < globalvars.number_of_tiles:
        x,y,z = pick_position(boxsize)

        exists = False
        for tile in globalvars.dodecahedrons:
            if (tile.x == x) and (tile.y == y) and (tile.z == z):
                exists = True
                break

        if not exists:
            tmp = Dodecahedron(x, y, z)
            tmp.component = [component_counter]
            components[component_counter] = 1
            component_counter += 1
            globalvars.dodecahedrons.append(tmp)
            tmp.find_neighbours(globalvars.dodecahedrons)

            tmp.component = list(set(tmp.component))
            min_comp = min(tmp.component)

            val = 0
            for i in tmp.component:
                val += components[i]

            components[min_comp] = val

            for comp in tmp.component:
                for dod in globalvars.dodecahedrons:
                    if comp in dod.component:
                        dod.component = [min_comp]

            max_component = 0
            for i in components:
                if components[i] > max_component:
                    max_component = components[i]
                    comp_name = i

    new_dodecas = []
    for i in globalvars.dodecahedrons:
        if comp_name in i.component:
            new_dodecas.append(i)
    globalvars.dodecahedrons = new_dodecas

    dodeca = random.choice(globalvars.dodecahedrons)
    tmp_x = dodeca.x
    tmp_y = dodeca.y
    tmp_z = dodeca.z
    for i in globalvars.dodecahedrons:
        i.x -= tmp_x
        i.y -= tmp_y
        i.z -= tmp_z

    print("finished")
    print(len(globalvars.dodecahedrons))




ap = argparse.ArgumentParser()

ap.add_argument("--visualize", default=False, help="Whether to render the configuration or run the algorithm in the background.")
ap.add_argument("--tiles", default=100, help="Minimal number of tiles in random configuration.")
ap.add_argument("--infile", default="C:\\Users\\bergm\\PycharmProjects\\SimulatorAnalysis\\configurations\\tiles180\\config015.txt", help="Configuration to load.")
ap.add_argument("--outfile", default="demofile.txt", help="Configuration to load.")
ap.add_argument("--random", default=True, help="Whether a random configuration should be created.")
ap.add_argument("--boxsize", default=25, help="Size of box in which the random configuration is created..")
ap.add_argument("--printsteps", default=1000, help="Minimal number of tiles in random configuration.")
ap.add_argument("--onlygenerate", default=False, help="Minimal number of tiles in random configuration.")
ap.add_argument("--logarithmic", default=False, help="Whether to use logarithmic or constant memory.")
ap.add_argument("--runsilent", default=False, help="Whether to use logarithmic or constant memory.")

args = vars(ap.parse_args())
globalvars.visualize = args["visualize"]
globalvars.number_of_tiles = int(args["tiles"])
globalvars.load_file = args["infile"]
globalvars.store_file = args["outfile"]
globalvars.random_configuration = args["random"]
globalvars.boxsize = int(args["boxsize"])
globalvars.printsteps = int(args["printsteps"])
globalvars.onlygenerate = bool(args["onlygenerate"])
globalvars.logarithmic_memory = bool(args["logarithmic"])
globalvars.run_silent = bool(args["runsilent"])

globalvars.movecounter['find_shiftable_row'] = 0
globalvars.movecounter['locally_highest_row'] = 0
globalvars.movecounter['shift_or_take'] = 0
globalvars.movecounter['place_tile'] = 0
globalvars.movecounter['take_initial_tile'] = 0
globalvars.movecounter['move_pebble'] = 0

build_new_configuration()


app = Simulator3D()

if not globalvars.onlygenerate or globalvars.run_silent:
    print("Count: " + str(globalvars.global_move_count) + ", Potential_X: " + str(
        potential.potential_x(app.grabbed_tile)) + ", " + "Potential_Z: " + str(
        potential.potential_z(app.grabbed_tile)))

    #app.run()
    while not globalvars.visualize:
        app.moveRobotNoAnimation()

        #if app.count == 23000:
        #    break

        #if app.robot.switched_orientation:
        #    app.stop()
        #    app.init_visualization()
        #    app.run()
        #    break

        #if potential.potential_x(app.grabbed_tile) <= 369 and app.robot.state == 'place_tile':
        #    app.stop()
        #    app.init_visualization()
        #    app.run()
        #    break

        #if potential.potential_x(app.grabbed_tile) == 43 and app.robot.place_tile.move_on_surface.traverse_surface.return_to_start:
        #    app.stop()
        #    break

        #if potential.potential_x(app.grabbed_tile) == 0 and potential.potential_z(app.grabbed_tile) == 44:
        #    app.stop()
        #    break

        #if app.robot.switched_orientation and potential.potential_z(app.grabbed_tile) == 22:
        #    app.stop()
        #    print(app.robot.state)
        #    print(app.robot.place_tile.state)
        #    break

        #if app.robot.switched_orientation:
            #if app.hidden_tile != None:
            #    app.hidden_tile.hide = False
            #    app.hidden_tile = None
            #break

        if app.robot.state == 'terminate':
            print("Count: " + str(globalvars.global_move_count) + ", Potential_X: " + str(potential.potential_x(app.grabbed_tile)) + ", " + "Potential_Z: " + str(potential.potential_z(app.grabbed_tile)))
            print(globalvars.movecounter)
            break


    if globalvars.visualize:
        app.init_visualization()
        app.run()

    print("Number of Dodecahedrons: ", len(globalvars.dodecahedrons))