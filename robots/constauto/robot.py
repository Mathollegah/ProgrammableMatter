from robots.constauto.states.find_shiftable_row import *
from robots.constauto.states.locally_highest_row import *
from robots.constauto.states.shift_or_take import *

from robots.constauto.states.place_tile import *


class ConstRobot():
    def __init__(self, state):
        self.state = 'find_shiftable_row'
        self.print_state = 'find_shiftable_row'
        self.carrying_tile = True
        self.switched_orientation = False
        self.gstate = state

        self.find_shiftable_row = FindShiftableRow(state)
        self.locally_highest_row = LocallyHighestRow()
        self.shift_or_take = ShiftOrTake()
        self.place_tile = PlaceTile(state)

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
        if self.gstate.logarithmic_memory:
            if not self.switched_orientation:
                self.gstate.robot_z_coord = self.gstate.robot_coordinates[2]
            else:
                self.gstate.robot_z_coord = self.gstate.robot_coordinates[0]
        if self.gstate.robot_z_coord < self.gstate.min_z_coord:
            self.gstate.min_z_coord = self.gstate.robot_z_coord
        ret = None
        force_exit = False
        neighbors = self.switch_orientation(neighbors, self.switched_orientation)
        neighbors = self.switch_orientation(neighbors, self.switched_orientation)
        neighbors = self.switch_orientation(neighbors, self.switched_orientation)
        while ret == None and self.state != 'terminate' and not force_exit:
            if self.state == 'find_shiftable_row' and ret == None:
                self.print_state = 'find_shiftable_row'
                ret = self.find_shiftable_row.move(neighbors)
                if self.find_shiftable_row.state == 'terminate':
                    self.find_shiftable_row.reset()
                    self.state = 'locally_highest_row'
                if self.find_shiftable_row.state == 'no_shiftable_row_exists':
                    self.find_shiftable_row.reset()
                    if self.switched_orientation:
                        self.state = 'terminate'
                    else:
                        self.state.min_z_coord = 10000
                        self.switched_orientation = True
                        force_exit = True
                        self.state = 'find_shiftable_row'
                        break

            if self.state == 'locally_highest_row' and ret == None:
                self.print_state = 'locally_highest_row'
                ret = self.locally_highest_row.move(neighbors)
                if self.locally_highest_row.state == 'terminate':
                    self.locally_highest_row.reset()
                    self.state = 'shift_or_take'

            if self.state == 'shift_or_take' and ret == None:
                self.print_state = 'shift_or_take'
                ret = self.shift_or_take.move(neighbors, occupied, self.carrying_tile)
                if self.shift_or_take.state == 'terminate_place':
                    self.shift_or_take.reset()
                    self.state = 'place_tile'

                if self.shift_or_take.state == 'terminate_shift':
                    self.shift_or_take.reset()
                    self.state = 'move_one_down'

            if self.state == 'place_tile' and ret == None:
                if not self.place_tile.placed_tile:
                    self.print_state = 'place_tile'
                else:
                    self.print_state = 'take_initial_tile'
                ret = self.place_tile.move(neighbors)
                if self.place_tile.state == 'terminate':
                    self.place_tile.reset()

                    if self.switched_orientation:
                        self.state = 'terminate'
                    else:
                        self.gstate.min_z_coord = 10000
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
                if self.gstate.logarithmic_memory:
                    self.state = 'move_one_down'
                else:
                    self.state = 'find_shiftable_row'

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
