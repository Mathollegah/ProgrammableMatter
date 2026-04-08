from robots.constauto.states.helper.traverse_surface import *

class FindShiftableRow():
    def __init__(self, state):
        self.state = 'run'
        self.traverse_surface = TraverseOnSurfaceLog(state)
        self.gstate = state

        self.min_y = 0
        self.max_y = 0
        self.y = 0

    def reset(self):
        self.state = 'run'
        self.traverse_surface = TraverseOnSurfaceLog(self.gstate)

        self.min_y = 0
        self.max_y = 0
        self.y = 0

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
            return 'F'

        if direction == 'S':
            return 'B'

        if direction == 'NE':
            if 'UFR' in moves:
                return 'UFR'
            else:
                return 'DFR'

        if direction == 'NW':
            if 'UFL' in moves:
                return 'UFL'
            else:
                return 'DFL'

        if direction == 'SE':
            if 'UBR' in moves:
                return 'UBR'
            else:
                return 'DBR'

        if direction == 'SW':
            if 'UBL' in moves:
                return 'UBL'
            else:
                return 'DBL'



    def move(self, moves):
        if ('U' in moves) or ('D' in moves):
            self.state = 'terminate'
            return None

        half_up_exists = False
        for direction in moves:
            if 'U' in direction:
                self.max_y = max(self.y+0.5, self.max_y)
                half_up_exists = True
                break

        for direction in moves:
            if 'D' in direction:
                self.min_y = min(self.y-0.5, self.min_y)
                break

        if (self.y > self.min_y) and half_up_exists:
            self.state = 'terminate'
            return None

        if (self.max_y-self.min_y) >= 1:
            self.traverse_surface.return_to_starting_point()

        directions = self.translate_directions_to_2D(moves)
        tmp = self.traverse_surface.move(directions)

        if self.traverse_surface.state == 'terminate':
            self.state = 'no_shiftable_row_exists'

        tmp = self.translate_directions_to_3D(tmp, moves)
        if tmp != None:
            if 'U' in tmp:
                self.y += 0.5
            if 'D' in tmp:
                self.y -= 0.5
        return tmp

