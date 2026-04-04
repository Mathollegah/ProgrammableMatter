class ShiftOrTake():
    def __init__(self):
        self.state = 'place_initial_tile'

    def reset(self):
        self.state = 'place_initial_tile'

    def move(self, moves, occupied, carrying_tile):
        if self.state == 'place_initial_tile':
            if (not 'F' in moves) and ('D' in moves):
                self.state = 'terminate_place'
                return None

            if (not 'F' in moves) and (not 'D' in moves):
                self.state = 'place_tile'
                return 'D'

            if (not 'D' in moves):
                self.state = 'place_tile'
                return 'D'

            self.state = 'place_next'
            return 'D'

        if self.state == 'place_next':
            if not 'F' in moves:
                self.state = 'place_tile'
                return 'F'
            self.state = 'terminate_place'
            return 'U'

        if self.state == 'place_tile':
            self.state = 'move_up'
            return 'place_tile'

        if self.state == 'move_up':
            if 'U' in moves:
                return 'U'
            self.state = 'move_back'
            return None

        if self.state == 'move_back':
            if 'B' in moves:
                return 'B'
            self.state = 'place_next_tile'
            return 'grab_tile'

        if self.state == 'place_next_tile':
            if (not 'F' in moves) and ('D' in moves):
                self.state = 'terminate_shift'
                return None

            self.state = 'move_DFR'
            return 'DFL'

        if self.state == 'move_DFR':
            self.state = 'move_decision'
            return 'DFR'

        if self.state == 'move_decision':
            if not occupied:
                self.state = 'move_up'
                return 'place_tile'
            self.state = 'terminate_next'
            return 'U'

        if self.state == 'terminate_next':
            self.state = 'terminate_place'
            return None

