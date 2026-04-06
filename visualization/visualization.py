import simplepbr
from robots.constauto.robot import *
from direct.showbase.ShowBase import ShowBase
from direct.gui.OnscreenText import OnscreenText
from direct.task import Task
from potential import potential
import random
from game.game import Game, Dodecahedron

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




class Simulator3D(ShowBase, Game):
    def __init__(self, player, config, state):
        if not config.onlygenerate:
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

        if config.load_file == "":
            tmp = random.choice(state.dodecahedrons)
            state.global_start_node = tmp

        self.interpolation_move = 0
        self.step = 0
        self.robot = player
        self.config = config
        self.state = state

        tmp = Dodecahedron(self.state.global_start_node.x, self.state.global_start_node.y,
                           self.state.global_start_node.z)
        self.state.dodecahedrons.append(tmp)
        self.grabbed_tile = tmp

        self.x = tmp.x
        self.y = tmp.y
        self.z = tmp.z

        self.inter_x = self.x
        self.inter_y = self.y
        self.inter_z = self.z

        self.state.robot_coordinates = (self.x, self.y, self.z)

        # Model complete, store in file
        if self.config.load_file == "":
            f = open(self.config.store_file, "w")
            f.writelines(str(self.x) + " " +  str(self.y) + " " + str(self.z) + " ")
            for dodec in self.state.dodecahedrons:
                f.writelines(str(dodec.x) + " " + str(dodec.y)+ " " + str(dodec.z)+ " ")
            f.close()

        self.x_next = 0
        self.y_next = 0
        self.z_next = 0

        self.hidden_tile = None
        self.hidden = False
        if not self.config.onlygenerate:
            self.scene = self.loader.loadModel("./objects/robot.glb")
            self.scene.reparentTo(self.render)
            self.scene.setScale(4.0 / 8.0, 4.0 / 8.0, 4.0 / 8.0)
            self.scene.setPos(self.x, self.y, self.z)
            self.bounding_box = None

            for x in self.state.dodecahedrons:
                x.scene = self.loader.loadModel("./objects/dodeca.glb")
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
        for x in self.state.dodecahedrons:
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

        if not self.config.onlygenerate:
            self.add_axis(x_max + 0.5, x_min - 0.5, y_max + 0.5, y_min - 0.5,
                     z_max + 0.5, z_min - 0.5)
            self.bounding_box = self.add_bounding_box(x_max + 0.5, x_min - 0.5, y_max + 0.5, y_min - 0.5,
                                             z_max + 0.5, z_min - 0.5)
        if not self.config.global_bound_box and not self.config.onlygenerate:
            self.bounding_box.hide()

        # Add the move robot procedure.
        if not self.config.onlygenerate:
            self.taskMgr.add(self.moveRobotAnimation, "MoveRobot")

        # Add potential score
        if not self.config.onlygenerate:
            self.textObject = OnscreenText(text='Potential: 0', pos=(-0.7, 0.9), scale=0.07)


    def add_axis(self, x_max, x_min, y_max, y_min, z_max, z_min):
        vertical = LineNodePath(self.render, colorVec=Vec4(0, 0, 0, 1))
        vertical.setThickness(12)
        vertical.drawLines([((x_min, y_min, z_min), (x_max, y_min, z_min))])
        vertical.drawLines([((x_min, y_min, z_min), (x_min, y_max, z_min))])
        vertical.drawLines([((x_min, y_min, z_min), (x_min, y_min, z_max))])
        vertical.create()
        vertical.reparentTo(self.render)

    def add_bounding_box(self, x_max, x_min, y_max, y_min, z_max, z_min):
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

        cube = self.render.attachNewNode(snode)
        cube.setTransparency(True)
        cube.setColor(0.1, 0.1, 0.1, 0.7)
        return cube


    def hide_tile(self):
        if self.hidden_tile != None:
            self.hidden = not self.hidden
            if not self.hidden:
                self.hidden_tile.scene.show()
            else:
                self.hidden_tile.scene.hide()

    def hide_bounding_box(self):
        self.config.global_bound_box = not self.config.global_bound_box
        if not self.config.global_bound_box:
            self.bounding_box.show()
        else:
            self.bounding_box.hide()

    def stop(self):
        self.running = not self.running
        print("Pause")

    def slower(self):
        self.config.new_interpolation_steps += 3

    def faster(self):
        if self.config.new_interpolation_steps > 3:
            self.config.new_interpolation_steps -= 3

    def hide_not_pot_zero(self):
        tower_lst = []
        for tile in self.state.dodecahedrons:
            if (tile.pot_x, tile.pot_z) != (0, 0):
                tower_lst.append((tile.x, tile.y))

        print(tower_lst)
        for tile in self.state.dodecahedrons:
            if (tile.pot_x, tile.pot_z) == (0, 0) and not (tile.x, tile.y) in tower_lst:
                #tile.scene.hide()
                tile.scene.setTransparency(True)
                tile.scene.setColor(0.1, 0.1, 0.1, 0.3)


    def init_visualization(self):
        for dod in self.state.dodecahedrons:
            dod.scene.setPos(dod.x, dod.y, dod.z)

    # Define a procedure to move the robot.
    def moveRobotAnimation(self, task):
        if not self.running:
            return Task.cont
        
        steps = self.config.interpolation_steps
        if self.interpolation_move == 0:
            # Get next move from robot
            self.inter_x = self.x
            self.inter_y = self.y
            self.inter_z = self.z

            self.x_next, self.y_next, self.z_next = self.moveRobot()


        inter_x = self.inter_x + (self.x_next - self.inter_x) * self.interpolation_move / steps
        inter_y = self.inter_y + (self.y_next - self.inter_y) * self.interpolation_move / steps
        inter_z = self.inter_z + (self.z_next - self.inter_z) * self.interpolation_move / steps

        self.scene.setPos(inter_x, inter_y, inter_z)
        self.interpolation_move += 1

        if self.grabbed_tile != None:
            self.grabbed_tile.scene.setPos(inter_x, inter_y, inter_z)

        if self.interpolation_move == steps+1:
            self.textObject.setText("Potential_X: " + str(self.state.potential.potential_x(self.grabbed_tile)) + ", " + "Potential_Z: " + str(self.state.potential.potential_z(self.grabbed_tile)))
            self.interpolation_move = 0
            self.x = self.x_next
            self.y = self.y_next
            self.z = self.z_next

            self.state.robot_coordinates = (self.x, self.y, self.z)
            self.config.interpolation_steps = self.config.new_interpolation_steps

            if self.grabbed_tile != None:
                self.grabbed_tile.x = self.x
                self.grabbed_tile.y = self.y
                self.grabbed_tile.z = self.z

        return Task.cont
