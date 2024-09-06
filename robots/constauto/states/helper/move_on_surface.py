from robots.constauto.states.helper.traverse_surface import *


class MoveOnSurface():
    def __init__(self):
        self.state = 'move_up'
        self.traverse_surface = TraverseOnSurfaceLog()
        self.last_move = None
        self.directions = []
        self.level_change_possible = False
        self.last_move_3D = None
        self.last_move_reverted = None
        self.layer_switch_happend = False
        self.free_spot_direction = None

    def reset(self):
        self.state = 'move_up'
        self.traverse_surface = TraverseOnSurfaceLog()
        self.last_move = None
        self.directions = []
        self.level_change_possible = False
        self.last_move_3D = None
        self.last_move_reverted = None
        self.layer_switch_happend = False
        self.free_spot_direction = None

    def translate_directions_to_2D(self, moves):
        directions = []
        if 'F' in moves:
            directions.append('N')

        if 'B' in moves:
            directions.append('S')

        if ('UBR' in moves) or ('DBR' in moves):
            directions.append('SE')

        if ('UFR' in moves) or ('DFR' in moves):
            directions.append('NE')

        if ('UBL' in moves) or ('DBL' in moves):
            directions.append('SW')

        if ('UFL' in moves) or ('DFL' in moves):
            directions.append('NW')

        return directions

    def translate_directions_to_3D(self, direction, moves):
        if direction == 'N':
            if 'F' in moves:
                return 'F'
            return None

        if direction == 'S':
            if 'B' in moves:
                return 'B'
            return None

        if direction == 'NE':
            if 'UFR' in moves:
                return 'UFR'
            if 'DFR' in moves:
                return 'DFR'
            return None

        if direction == 'NW':
            if 'UFL' in moves:
                return 'UFL'
            if 'DFL' in moves:
                return 'DFL'
            return None

        if direction == 'SE':
            if 'UBR' in moves:
                return 'UBR'
            if 'DBR' in moves:
                return 'DBR'
            return None

        if direction == 'SW':
            if 'UBL' in moves:
                return 'UBL'
            if 'DBL' in moves:
                return 'DBL'
            return None

    def invert_move(self, move):
        ret = ''
        if 'U' in move:
            ret = ret + 'D'
        if 'D' in move:
            ret = ret + 'U'
        if 'F' in move:
            ret = ret + 'B'
        if 'B' in move:
            ret = ret + 'F'
        if 'R' in move:
            ret = ret + 'L'
        if 'L' in move:
            ret = ret + 'R'
        return ret

    def invert_move_2D(self, move):
        tmp = ''
        if 'N' in move:
            tmp = tmp + 'S'
        if 'S' in move:
            tmp = tmp + 'N'
        if 'E' in move:
            tmp = tmp + 'W'
        if 'W' in move:
            tmp = tmp + 'E'
        return tmp


    def continue_moving(self):
        self.state = 'move_down'

    def move(self, moves):
        if self.state == 'move_up':
            #TODO: Find level change
            tmp = self.translate_directions_to_2D(moves)
            if self.last_move != None:
                directions_2D = ['N', 'NE', 'SE', 'S', 'SW', 'NW']
                if not self.invert_move(self.last_move_3D) in moves:
                    self.level_change_possible = True

                if (directions_2D[(directions_2D.index(self.last_move)+3) % 6] in tmp) and self.level_change_possible:
                    print("layer switch happend")
                    self.layer_switch_happend = True
                    self.last_move_reverted = self.invert_move_2D(self.last_move)
                    self.free_spot_direction = self.translate_directions_to_3D(self.last_move_reverted, ['F', 'B', 'DFR', 'DFL', 'DBR', 'DBL'])
                    print(self.free_spot_direction)
                    #self.traverse_surface.return_to_starting_point()
                    self.traverse_surface.no_unique_point()
                    self.last_move = self.traverse_surface.move([self.last_move_reverted])
                    self.level_change_possible = False
                    self.state = 'move_down_and_take_move'
                    return None

            if 'U' in moves:
                return 'U'
            if self.traverse_surface.moved_back:# and self.traverse_surface.state != 'return':
                self.level_change_possible = False
                self.state = 'move_step_back'
            else:
                self.level_change_possible = False
                self.state = 'new_position'

        if self.state == 'move_down_and_take_move':
            self.state = 'take_move'
            return 'D'

        if self.state == 'move_down':
            if 'D' in moves:
                return 'D'
            self.state = 'move_up_and_detect_neighbors'
            self.directions = []

        if self.state == 'move_up_and_detect_neighbors':
            tmp = self.translate_directions_to_2D(moves)
            self.directions = self.directions + tmp
            self.directions = list(dict.fromkeys(self.directions))

            if 'U' in moves:
                return 'U'

            self.last_move = self.traverse_surface.move(self.directions)

            if self.traverse_surface.state == 'terminate':
                self.state = 'terminate'
                return None
            self.state = 'take_move'

        if self.state == 'take_move':
            tmp = self.translate_directions_to_3D(self.last_move, moves)
            #print("tmp", tmp)
            #print(self.traverse_surface.return_to_start)
            #print(self.last_move)
            if tmp == None:
                return 'D'
            else:
                self.last_move_3D = tmp
            self.state = 'move_up'
            return tmp

        return None
