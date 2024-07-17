from robots.constauto.states.helper.move_on_surface import *

class PlaceTile():
    def __init__(self):
        self.state = 'move_on_surface'
        self.y = 0
        self.move_on_surface = MoveOnSurface()
        self.move_on_bottom = MoveOnSurface()
        self.placed_tile = False
        self.directions = []
        self.last_move = None

    def reset(self):
        self.state = 'move_on_surface'
        self.y = 0
        self.move_on_surface.reset()
        self.move_on_bottom.reset()
        self.placed_tile = False
        self.directions = []
        self.last_move = None

    def invert_moves(self, moves):
        tmp = []
        for i in moves:
            if len(i) == 1:
                if i == 'U':
                    tmp.append('D')
                elif i == 'D':
                    tmp.append('U')
                else:
                    tmp.append(i)
            else:
                if i[0] == 'U':
                    tmp.append('D'+i[1:])
                else:
                    tmp.append('U' + i[1:])
        return tmp

    def update_height(self, move):
        if move == 'U':
            self.y += 1
        elif move == 'D':
            self.y -= 1
        elif 'U' in move:
            self.y += 0.5
        elif 'D' in move:
            self.y -= 0.5

    def move(self, moves):
        ret = None

        if self.state == 'move_on_surface' and ret == None:
            ret = self.move_on_surface.move(moves)
            if self.move_on_surface.state == 'new_position' or self.move_on_surface.state == 'move_step_back':
                self.state = 'move_down'
                self.directions = []
                self.move_on_surface.continue_moving()


            if self.move_on_surface.state == 'terminate':
                if not self.placed_tile:
                    self.state = 'terminate'
                else:
                    self.state = 'placed_tile'

        if self.state == 'move_down' and ret == None:
            self.directions = self.directions + moves
            self.directions = list(dict.fromkeys(self.directions))

            dir_found = False
            if not self.placed_tile:
                for i in self.directions:
                    if (i != 'U') and not (i in moves) and not ('D' in i):
                        self.last_move = i
                        ret = i
                        dir_found = True
                        self.state = 'place_tile_next'

            if not dir_found:
                if 'D' in moves:
                    ret = 'D'
                else:
                    self.y = 0
                    self.state = 'test_position'

        if self.state == 'place_tile_next' and ret == None:
            ret = 'place_tile'
            self.placed_tile = True
            self.move_on_surface.traverse_surface.return_to_starting_point()
            self.state = 'return_to_tower'

        if self.state == 'return_to_tower' and ret == None:
            ret = ''

            if 'U' in self.last_move:
                ret = ret + 'D'
            if 'D' in self.last_move:
                ret = ret + 'U'

            if 'F' in self.last_move:
                ret = ret + 'B'
            if 'B' in self.last_move:
                ret = ret + 'F'

            if 'R' in self.last_move:
                ret = ret + 'L'
            if 'L' in self.last_move:
                ret = ret + 'R'

            self.state = 'move_up'


        if self.state == 'test_position' and ret == None:
            new_moves = self.invert_moves(moves)
            ret = self.move_on_bottom.move(new_moves)

            if ret != None:
                ret = self.invert_moves([ret])[0]
                self.update_height(ret)

            if self.move_on_bottom.state == 'new_position':
                self.move_on_bottom.continue_moving()
                if self.y >= 1 and self.move_on_bottom.traverse_surface.state != 'return' and not self.placed_tile:
                    self.state = 'move_one_down'
                if self.y <= -1 and self.move_on_bottom.traverse_surface.state != 'return' and not self.placed_tile:
                    self.y = 0
                    self.move_on_bottom.traverse_surface.return_to_starting_point()

            if self.move_on_bottom.state == 'move_step_back':
                self.move_on_bottom.continue_moving()
                if self.y >= 1 and not self.placed_tile:
                    self.state = 'move_one_down'

            if self.move_on_bottom.state == 'terminate':
                self.move_on_bottom.reset()
                self.state = 'move_up'

        if self.state == 'move_one_down' and ret == None:
            ret = 'D'
            self.state = 'place_tile'

        if self.state == 'place_tile' and ret == None:
            ret = 'place_tile'
            self.placed_tile = True
            self.move_on_bottom.traverse_surface.return_to_starting_point()
            self.move_on_surface.traverse_surface.return_to_starting_point()
            self.state = 'test_position'

        if self.state == 'move_up' and ret == None:
            if 'U' in moves:
                ret = 'U'
            else:
                self.state = 'move_on_surface'
                self.move_on_surface.continue_moving()

        return ret

