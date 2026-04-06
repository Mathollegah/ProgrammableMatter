import globalvars
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


class Game():
    def __init__(self, player, config, state):
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

        tmp = Dodecahedron(state.global_start_node.x, state.global_start_node.y,
                           state.global_start_node.z)
        state.dodecahedrons.append(tmp)
        self.grabbed_tile = tmp

        self.x = tmp.x
        self.y = tmp.y
        self.z = tmp.z

        state.robot_coordinates = (self.x, self.y, self.z)

        # Model complete, store in file
        if config.load_file == "":
            f = open(config.store_file, "w")
            f.writelines(str(self.x) + " " +  str(self.y) + " " + str(self.z) + " ")
            for dodec in state.dodecahedrons:
                f.writelines(str(dodec.x) + " " + str(dodec.y)+ " " + str(dodec.z)+ " ")
            f.close()

        self.x_next = 0
        self.y_next = 0
        self.z_next = 0

        self.hidden_tile = None
        self.hidden = False
        if not config.onlygenerate:
            self.scene = self.loader.loadModel("../../../../../objects/robot.glb")
            self.scene.reparentTo(self.render)
            self.scene.setScale(4.0 / 8.0, 4.0 / 8.0, 4.0 / 8.0)
            self.scene.setPos(self.x, self.y, self.z)
            self.bounding_box = None

            for x in state.dodecahedrons:
                x.scene = self.loader.loadModel("../../../../../objects/dodeca.glb")
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
        for x in state.dodecahedrons:
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


    def detect_occupied(self):
        for x in self.state.dodecahedrons:
            if (x.x, x.y, x.z) == (self.x, self.y, self.z):
                if x != self.grabbed_tile:
                    return True
        return False

    def detect_neighbors(self):
        # search neighbors
        movable = []
        for x in self.state.dodecahedrons:
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
        for i in self.state.dodecahedrons:
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
        for i in self.state.dodecahedrons:
            if (i.x, i.y, i.z) == (self.x, self.y, self.z):
                count = count + 1
                break
        if count > 1:
            raise Exception("Error: Position is occupied. Tile can not be placed.")

        if self.grabbed_tile == None:
            raise Exception("Error: Carrying no tile. Tile can not be placed.")

        self.grabbed_tile.find_neighbours(self.state.dodecahedrons)
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
            if self.state.logarithmic_memory:
                return self.x, self.y, self.z
            else:
                return x,y,z

        return self.x, self.y, self.z

    # Define a procedure to move the robot.
    def moveRobot(self):
        # Get next move from robot
        moves = self.detect_neighbors()
        occupied = self.detect_occupied()
        if moves != []:
            next_move = self.robot.next_move(moves, occupied)
            self.x_next, self.y_next, self.z_next = self.act_move(next_move)

            self.x = self.x_next
            self.y = self.y_next
            self.z = self.z_next

            self.state.robot_coordinates = (self.x, self.y, self.z)

            if self.grabbed_tile != None:
                self.grabbed_tile.x = self.x
                self.grabbed_tile.y = self.y
                self.grabbed_tile.z = self.z

            return self.x_next, self.y_next, self.z_next

        return None


