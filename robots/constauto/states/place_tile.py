from robots.constauto.states.helper.move_on_surface import *

class PlaceTile():
    def __init__(self):
        self.state = 'move_on_surface'
        self.x = 0
        self.move_on_surface = MoveOnSurface()
        self.move_on_bottom = MoveOnSurface()
        self.placed_tile = False
        self.directions = []
        self.last_move = None
        self.test_pos_last_move = None
        self.test_pos_state = 'move_front'
        self.detected_tile_below = False

    def reset(self):
        self.state = 'move_on_surface'
        self.x = 0
        self.move_on_surface.reset()
        self.move_on_bottom.reset()
        self.placed_tile = False
        self.directions = []
        self.last_move = None
        self.test_pos_last_move = None
        self.test_pos_state = 'move_front'
        self.detected_tile_below = False

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

    def move(self, moves):
        ret = None
        #print(self.state)
        if self.state == 'move_on_surface' and ret == None:
            ret = self.move_on_surface.move(moves)
            if self.move_on_surface.layer_switch_happend and not self.placed_tile:
                self.last_move = self.move_on_surface.free_spot_direction

                if self.last_move == 'F' or self.last_move == 'B':
                    self.state = 'one_intermediate_down'
                    return 'D'
                else:
                    self.state = 'place_tile_next'
                    return self.move_on_surface.free_spot_direction
            #elif self.move_on_surface.layer_switch_happend:
            #    ret = self.move_on_surface.move(moves)

            if self.move_on_surface.state == 'new_position' or self.move_on_surface.state == 'move_step_back':
                self.state = 'move_down'
                self.directions = []
                self.move_on_surface.continue_moving()


            if self.move_on_surface.state == 'terminate':
                if not self.placed_tile:
                    self.state = 'terminate'
                else:
                    self.state = 'placed_tile'

        if self.state == 'one_intermediate_down' and ret == None:
            self.state = 'place_tile_next'
            return self.move_on_surface.free_spot_direction

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
                    if self.placed_tile:
                        self.state = 'move_up'
                    else:
                        self.x = 0
                        self.state = 'test_position'
                        self.test_pos_state = 'move_front'
                        self.detected_tile_below = False

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

            if self.move_on_surface.layer_switch_happend:
                self.state = 'move_on_surface'
                self.move_on_surface.layer_switch_happend = False
            else:
                self.state = 'move_up'

        if self.state == 'test_position' and ret == None:
            run = True
            while (ret == None) and run:
                if self.test_pos_state == 'move_front' and (ret == None):
                    if 'D' in moves:
                        self.test_pos_state = 'place_before'
                        ret = 'B'

                    if not self.detected_tile_below:
                        for dir in moves:
                            if 'D' in dir:
                                self.detected_tile_below = True
                                break

                    if self.detected_tile_below and (ret == None):
                        for dir in moves:
                            if (dir != 'U') and ('U' in dir) and not ('D'+dir[1:]) in moves:
                                self.test_pos_last_move = 'D'+dir[1:]
                                ret = 'D'+dir[1:]
                                self.test_pos_state = 'place_half_below'

                    if ret == None:
                        if 'F' in moves:
                            ret = 'F'
                        else:
                            self.test_pos_state = 'move_back'

                if self.test_pos_state == 'move_back' and (ret == None):
                    if 'D' in moves:
                        self.test_pos_state = 'place_before'
                        ret = 'F'

                    if not self.detected_tile_below:
                        for dir in moves:
                            if 'D' in dir:
                                self.detected_tile_below = True
                                break

                    if self.detected_tile_below and (ret == None):
                        for dir in moves:
                            if (dir != 'U') and ('U' in dir) and not ('D' + dir[1:]) in moves:
                                self.test_pos_last_move = 'D'+dir[1:]
                                ret = 'D'+dir[1:]
                                self.test_pos_state = 'place_half_below'

                    if ret == None:
                        if 'B' in moves:
                            ret = 'B'
                        else:
                            self.test_pos_state = 'move_to_origin'

                if self.test_pos_state == 'place_half_below' and (ret == None):
                    ret = 'place_tile'
                    self.placed_tile = True
                    self.test_pos_state = 'return_to_tower'

                if self.test_pos_state == 'return_to_tower' and (ret == None):
                    ret = ''

                    if 'U' in self.test_pos_last_move:
                        ret = ret + 'D'
                    if 'D' in self.test_pos_last_move:
                        ret = ret + 'U'

                    if 'F' in self.test_pos_last_move:
                        ret = ret + 'B'
                    if 'B' in self.test_pos_last_move:
                        ret = ret + 'F'

                    if 'R' in self.test_pos_last_move:
                        ret = ret + 'L'
                    if 'L' in self.test_pos_last_move:
                        ret = ret + 'R'

                    self.test_pos_state = 'move_to_origin'

                if self.test_pos_state == 'place_before' and (ret == None):
                    ret = 'D'
                    self.test_pos_state = 'place_and_up'

                if self.test_pos_state == 'place_and_up' and (ret == None):
                    ret = 'place_tile'
                    self.placed_tile = True
                    self.test_pos_state = 'move_one_up'

                if self.test_pos_state == 'move_one_up' and (ret == None):
                    ret = 'U'
                    self.test_pos_state = 'move_to_origin'

                if self.test_pos_state == 'move_to_origin' and (ret == None):
                    if self.x > 0:
                        ret = 'B'
                    if self.x < 0:
                        ret = 'F'
                    if self.x == 0:
                        self.state = 'move_up'
                        run = False

                if ret == 'F':
                    self.x += 1
                if ret == 'B':
                    self.x -= 1
                if ret == 'place_tile':
                    self.move_on_surface.traverse_surface.return_to_starting_point()

        if self.state == 'move_one_down' and ret == None:
            ret = 'D'
            self.state = 'place_tile'

        if self.state == 'place_tile' and ret == None:
            ret = 'place_tile'
            self.placed_tile = True
            self.move_on_surface.traverse_surface.return_to_starting_point()
            self.state = 'test_position'

        if self.state == 'move_up' and ret == None:
            if 'U' in moves:
                ret = 'U'
            else:
                self.state = 'move_on_surface'
                self.move_on_surface.continue_moving()

        return ret

