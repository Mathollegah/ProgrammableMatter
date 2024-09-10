import globalvars
from robots.constauto.states.find_shiftable_row import *
from robots.constauto.states.locally_highest_row import *
from robots.constauto.states.shift_or_take import *

from robots.constauto.states.place_tile import *

import globalvars

class ConstRobot():
    def __init__(self):
        self.state = 'find_shiftable_row'
        self.carrying_tile = True
        self.switched_orientation = False

        self.find_shiftable_row = FindShiftableRow()
        self.locally_highest_row = LocallyHighestRow()
        self.shift_or_take = ShiftOrTake()
        self.place_tile = PlaceTile()

    def switch_orientation(self, moves, switched):
        if not switched:
            return moves

        tmp = []
        for i in moves:
            if i == 'U':
                tmp.append('F')

            if i == 'F':
                tmp.append('D')

            if i == 'D':
                tmp.append('B')

            if i == 'B':
                tmp.append('U')

            if i == 'UFR':
                tmp.append('DFR')

            if i == 'DFR':
                tmp.append('DBR')

            if i == 'DBR':
                tmp.append('UBR')

            if i == 'UBR':
                tmp.append('UFR')

            if i == 'UFL':
                tmp.append('DFL')

            if i == 'DFL':
                tmp.append('DBL')

            if i == 'DBL':
                tmp.append('UBL')

            if i == 'UBL':
                tmp.append('UFL')

        return tmp

    def switch_orientation_move(self, move, switched):
        if not switched:
            return move

        if move == 'F':
            return 'U'

        if move == 'D':
            return 'F'

        if move == 'B':
            return 'D'

        if move == 'U':
            return 'B'

        if move == 'UFR':
            return 'UBR'

        if move == 'DFR':
            return 'UFR'

        if move == 'DBR':
            return 'DFR'

        if move == 'UBR':
            return 'DBR'

        if move == 'UFL':
            return 'UBL'

        if move == 'DFL':
            return 'UFL'

        if move == 'DBL':
            return 'DFL'

        if move == 'UBL':
            return 'DBL'

        return move


    def next_move(self, neighbors, occupied):
        if globalvars.logarithmic_memory:
            if not self.switched_orientation:
                globalvars.robot_z_coord = globalvars.robot_coordinates[2]
            else:
                globalvars.robot_z_coord = globalvars.robot_coordinates[0]
        if globalvars.robot_z_coord < globalvars.min_z_coord:
            globalvars.min_z_coord = globalvars.robot_z_coord

        ret = None
        force_exit = False
        neighbors = self.switch_orientation(neighbors, self.switched_orientation)
        neighbors = self.switch_orientation(neighbors, self.switched_orientation)
        neighbors = self.switch_orientation(neighbors, self.switched_orientation)
        while ret == None and self.state != 'terminate' and not force_exit:
            if self.state == 'find_shiftable_row' and ret == None:
                if not globalvars.logarithmic_memory:
                    # Approximation of moves to collect pebbles
                    globalvars.movecounter['find_shiftable_row'] += 3
                    globalvars.global_move_count += 2
                else:
                    globalvars.movecounter['find_shiftable_row'] += 1

                ret = self.find_shiftable_row.move(neighbors)
                if self.find_shiftable_row.state == 'terminate':
                    if not globalvars.logarithmic_memory:
                        # Approximation of extra steps to place pebbles when collecting the start position pebble
                        globalvars.movecounter['move_pebble'] += self.find_shiftable_row.traverse_surface.pebble_move_count*2
                        globalvars.global_move_count += self.find_shiftable_row.traverse_surface.pebble_move_count*2

                    self.find_shiftable_row.reset()
                    self.state = 'locally_highest_row'
                if self.find_shiftable_row.state == 'no_shiftable_row_exists':
                    self.find_shiftable_row.reset()
                    if self.switched_orientation:
                        self.state = 'terminate'
                    else:
                        globalvars.min_z_coord = 10000
                        self.switched_orientation = True
                        force_exit = True
                        self.state = 'find_shiftable_row'
                        break

            if self.state == 'locally_highest_row' and ret == None:
                globalvars.movecounter['locally_highest_row'] += 1
                ret = self.locally_highest_row.move(neighbors)
                if self.locally_highest_row.state == 'terminate':
                    self.locally_highest_row.reset()
                    self.state = 'shift_or_take'

            if self.state == 'shift_or_take' and ret == None:
                globalvars.movecounter['shift_or_take'] += 1

                ret = self.shift_or_take.move(neighbors, occupied, self.carrying_tile)
                if self.shift_or_take.state == 'terminate_place':
                    self.shift_or_take.reset()
                    self.state = 'place_tile'

                if self.shift_or_take.state == 'terminate_shift':
                    self.shift_or_take.reset()
                    self.state = 'move_one_down'

            if self.state == 'place_tile' and ret == None:
                if not self.place_tile.placed_tile:
                    globalvars.movecounter['place_tile'] += 1
                    if not globalvars.logarithmic_memory:
                        # This step is taken two times to collect the pebble marking the hidden tile
                        globalvars.global_move_count += 1
                        globalvars.movecounter['take_initial_tile'] += 1
                else:
                    globalvars.movecounter['take_initial_tile'] += 1

                ret = self.place_tile.move(neighbors)
                if self.place_tile.state == 'terminate':
                    self.place_tile.reset()

                    if self.switched_orientation:
                        self.state = 'terminate'
                    else:
                        globalvars.min_z_coord = 10000
                        self.switched_orientation = True
                        self.state = 'find_shiftable_row'
                        break

                if ret == 'place_tile':
                    ret = 'place_and_hide_tile'

                if self.place_tile.state == 'placed_tile':
                    self.place_tile.reset()
                    self.state = 'take_initial_tile'

            if self.state == 'take_initial_tile' and ret == None:
                ret = 'grab_tile_and_show_hidden_tile'
                self.state = 'move_one_down'

            if self.state == 'move_one_down' and ret == None:
                ret = 'D'
                self.state = 'find_shiftable_row'


        if ret == 'grab_tile':
            self.carrying_tile = True
        if ret == 'place_tile':
            self.carrying_tile = False

        tmp = self.switch_orientation_move(ret, self.switched_orientation)
        tmp = self.switch_orientation_move(tmp, self.switched_orientation)
        tmp = self.switch_orientation_move(tmp, self.switched_orientation)
        return tmp #self.switch_orientation_move(ret, self.switched_orientation)
