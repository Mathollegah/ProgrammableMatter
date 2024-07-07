from robots.logauto.states.FindLocalMaximum import *
from robots.logauto.states.FindShiftableLine import *
from robots.logauto.states.MoveOnSurface import *
from robots.logauto.states.ShiftOrTake import *
import globalvars
import random



class LogRobot():
    def __init__(self):
        self.state = 'find_shiftable_row'#'move_random'
        self.x = globalvars.global_start_node.x
        self.y = globalvars.global_start_node.y
        self.z = globalvars.global_start_node.z

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
        self.tiles = globalvars.dodecahedrons

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
        for i in globalvars.dodecahedrons:
            if (i.x, i.y, i.z) == (self.x, self.y, self.z) and i != self.grabbed_tile:
                return i
        return None

    def next_move(self):
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
                self.state = 'switch_orientation'
                #self.state = 'terminate'


        if self.state == 'switch_orientation':
            if globalvars.global_switch:
                globalvars.global_switch = False
                for i in globalvars.dodecahedrons:
                    tmp = i.x
                    i.x = i.z
                    i.z = -tmp
                    i.scene.setPos(i.x, i.y, i.z)

                tmp = self.x
                self.x = self.z
                self.z = -tmp
                self.state = 'find_shiftable_row'

                for i in globalvars.dodecahedrons:
                    i.find_neighbours(globalvars.dodecahedrons)
                self.detect_neighbors()

        if self.state != 'terminate':
            self.act_move(pos)



















class SimpleLogRobot():
    def __init__(self):
        self.state = 'find_shiftable_row'#'move_random'
        self.x = globalvars.global_start_node.x
        self.y = globalvars.global_start_node.y
        self.z = globalvars.global_start_node.z

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
        self.tiles = globalvars.dodecahedrons

        # Robot procedurs
        self.find_local_maximum = FindLocalMaximum()
        self.shift_or_take = ShiftOrTake()
        self.shift_or_take.robot = self
        self.move_on_surface = SimpleMoveOnSurface()
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
        for i in globalvars.dodecahedrons:
            if (i.x, i.y, i.z) == (self.x, self.y, self.z) and i != self.grabbed_tile:
                return i
        return None

    def next_move(self):
        globalvars.global_z = self.z
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
                self.state = 'switch_orientation'
                #self.state = 'terminate'


        if self.state == 'switch_orientation':
            self.move_on_surface.reset()
            if globalvars.global_switch:
                globalvars.global_switch = False
                for i in globalvars.dodecahedrons:
                    tmp = i.x
                    i.x = i.z
                    i.z = -tmp
                    i.scene.setPos(i.x, i.y, i.z)

                tmp = self.x
                self.x = self.z
                self.z = -tmp
                self.state = 'find_shiftable_row'

                for i in globalvars.dodecahedrons:
                    i.find_neighbours(globalvars.dodecahedrons)
                self.detect_neighbors()

        if self.state != 'terminate':
            self.act_move(pos)
