import globalvars


class TraverseOnSurfaceDFS():
    def __init__(self):
        self.x = 0
        self.y = 0

        self.known = []
        self.path = []

        self.next_dir = 'N'
        self.moved_back = False
        self.state = 'run'


    def reset(self):
        self.x = 0
        self.y = 0

        self.known = []
        self.path = []

        self.next_dir = 'N'
        self.moved_back = False
        self.state = 'run'

    def update_pos(self, ret):
        if len(ret) == 1:
            if ret == 'N':
                self.y += 2
            else:
                self.y -= 2
        else:
            if 'N' in ret:
                self.y += 1
            else:
                self.y -= 1

            if 'E' in ret:
                self.x += 1
            else:
                self.x -= 1

    def check_known(self, move):
        directions = ['N', 'NE', 'SE', 'S', 'SW', 'NW']
        index = directions.index(move)
        self.update_pos(move)
        if (self.x, self.y) in self.known:
            self.update_pos(directions[(index+3)%6])
            return True
        else:
            self.update_pos(directions[(index + 3) % 6])
            return False

    def return_to_starting_point(self):
        self.state = 'return'

    def move_simulator(self, moves):
        if self.state == 'return' and len(self.path) > 0:
            self.moved_back = True
            tmp, self.next_dir = self.path.pop()
            return tmp

        if self.state == 'return' and len(self.path) == 0:
            self.state = 'terminate'
            return None

        if len(self.path) == 0 and len(self.known) > 0 and self.next_dir == None:
            self.state = 'terminate'
            return None

        if len(self.path) > 0:
            if ((self.x, self.y) in self.known and not self.moved_back) or self.state == 'return':
                self.moved_back = True
                tmp, self.next_dir = self.path.pop()
                return tmp

        self.known.append((self.x, self.y))

        directions = ['N', 'NE', 'SE', 'S', 'SW', 'NW', None]
        index = directions.index(self.next_dir)
        for i in range(index, 6):
            if directions[i] in moves and not self.check_known(directions[i]):
                self.path.append((directions[(i+3)%6], directions[i+1]))
                self.moved_back = False
                self.next_dir = 'N'
                return directions[i]

        if len(self.path) == 0:
            self.state = 'terminate'
            return None

        self.moved_back = True
        tmp, self.next_dir = self.path.pop()
        return tmp

    def move(self, moves):
        if self.state != 'terminate':
            tmp = self.move_simulator(moves)
            if self.state == 'run':
                self.update_pos(tmp)
            return tmp
        return None


####################################################################################################
# Log Move On Surface                                                                              #
####################################################################################################

class UniquePoint():
    def __init__(self):
        self.state = 'UP'
        self.up_x = 0
        self.up_y = 0
        self.x = 0
        self.y = 0
        self.up_start_bound_dir = ''
        self.terminate = False
        self.is_up = False
        self.bound_dir = ''
        self.force_return = False

    def reset(self):
        self.state = 'UP'
        self.up_x = 0
        self.up_y = 0
        self.x = 0
        self.y = 0
        self.up_start_bound_dir = ''
        self.terminate = False
        self.is_up = False
        self.bound_dir = ''
        self.force_return = False

    def update_pos(self, ret):
        if len(ret) == 1:
            if ret == 'N':
                self.y += 2
            else:
                self.y -= 2
        else:
            if 'N' in ret:
                self.y += 1
            else:
                self.y -= 1

            if 'E' in ret:
                self.x += 1
            else:
                self.x -= 1

    def force_return_func(self):
        self.force_return = True

    def move(self, moves, bound_dir):
        move = None
        while (move == None) and (self.state != 'terminate'):
            if (self.state == 'UP') and (move == None):
                self.up_x = self.x
                self.up_y = self.y
                self.up_start_bound_dir = bound_dir
                self.bound_dir = bound_dir

                dirs = ['N', 'NE', 'SE', 'S', 'SW', 'NW']
                index = dirs.index(self.bound_dir)
                for i in range(len(dirs)):
                    if dirs[(index + i) % len(dirs)] in moves:
                        if i == 0:
                            self.bound_dir = dirs[(index + i - 1) % len(dirs)]
                        else:
                            self.bound_dir = dirs[(index + i - 2) % len(dirs)]
                        move = dirs[(index + i) % len(dirs)]
                        break

                self.state = 'UP2'

            if (self.state == 'UP2') and (move == None):
                if (self.y < self.up_y) or ((self.y == self.up_y) and (self.x < self.up_x)) or self.force_return:
                    self.is_up = False
                    self.state = 'UP_ret'

                    if self.bound_dir in moves and self.force_return:
                        dirs = ['N', 'NE', 'SE', 'S', 'SW', 'NW']
                        index = dirs.index(self.bound_dir)
                        self.bound_dir = dirs[(index-1)%6]
                else:
                    complete_cycle = False
                    dirs = ['N', 'NE', 'SE', 'S', 'SW', 'NW']
                    index = dirs.index(self.bound_dir)
                    for i in range(6):
                        if dirs[(index + i) % 6] == self.up_start_bound_dir:
                            complete_cycle = True
                            break

                        if dirs[(index + i) % 6] in moves:
                            break

                    if (self.y == self.up_y) and (self.x == self.up_x) and complete_cycle:
                        self.terminate = True
                        self.is_up = True
                        self.state = 'terminate'

                    if self.state == 'UP2':
                        dirs = ['N', 'NE', 'SE', 'S', 'SW', 'NW']
                        index = dirs.index(self.bound_dir)
                        for i in range(len(dirs)):
                            if dirs[(index + i) % len(dirs)] in moves:
                                if i == 0:
                                    self.bound_dir = dirs[(index + i - 1) % len(dirs)]
                                else:
                                    self.bound_dir = dirs[(index + i - 2) % len(dirs)]
                                move = dirs[(index + i) % len(dirs)]
                                break

            if (self.state == 'UP_ret') and (move == None):
                self.force_return = False
                if (self.y == self.up_y) and (self.x == self.up_x):
                    self.terminate = True
                    self.is_up = False
                    self.state = 'terminate'

                if self.state == 'UP_ret':
                    dirs = ['N', 'NW', 'SW', 'S', 'SE', 'NE']
                    index = dirs.index(self.bound_dir)
                    for i in range(len(dirs)):
                        if dirs[(index + i) % len(dirs)] in moves:
                            if i == 0:
                                self.bound_dir = dirs[(index + i - 1) % len(dirs)]
                            else:
                                self.bound_dir = dirs[(index + i - 2) % len(dirs)]
                            move = dirs[(index + i) % len(dirs)]
                            break

        if move != None:
            self.update_pos(move)
        return move, self.terminate, self.is_up



class UniquePointOrg():
    def __init__(self):
        self.state = 'Init'
        self.up_x = 0
        self.up_y = 0
        self.x = 0
        self.y = 0
        self.up_start_bound_dir = ''
        self.terminate = False
        self.is_up = False
        self.bound_dir = ''
        self.force_return = False
        self.last_move = ''
        self.delta = 0

        self.dist_to_start = 0

    def reset(self):
        self.state = 'Init'
        self.up_x = 0
        self.up_y = 0
        self.x = 0
        self.y = 0
        self.up_start_bound_dir = ''
        self.terminate = False
        self.is_up = False
        self.bound_dir = ''
        self.force_return = False
        self.last_move = ''
        self.delta = 0
        self.dist_to_start = 0

    def update_pos(self, ret):
        if len(ret) == 1:
            if ret == 'N':
                self.y += 2
            else:
                self.y -= 2
        else:
            if 'N' in ret:
                self.y += 1
            else:
                self.y -= 1

            if 'E' in ret:
                self.x += 1
            else:
                self.x -= 1

    def force_return_func(self):
        self.force_return = True
        self.state = 'UP_ret'

    def move_clockwise(self, moves):
        self.dist_to_start += 1

        dirs = ['N', 'NW', 'SW', 'S', 'SE', 'NE']
        index = dirs.index(self.bound_dir)
        for i in range(len(dirs)):
            if dirs[(index + i) % len(dirs)] in moves:
                if i == 0:
                    self.bound_dir = dirs[(index + i - 1) % len(dirs)]
                else:
                    self.bound_dir = dirs[(index + i - 2) % len(dirs)]
                move = dirs[(index + i) % len(dirs)]
                return move

    def move_counterclockwise(self, moves):
        self.dist_to_start -= 1

        if self.bound_dir in moves and self.force_return:
            dirs = ['N', 'NW', 'SW', 'S', 'SE', 'NE']
            index = dirs.index(self.bound_dir)
            self.bound_dir = dirs[(index - 1) % 6]

        dirs = ['N', 'NE', 'SE', 'S', 'SW', 'NW']
        index = dirs.index(self.bound_dir)
        for i in range(len(dirs)):
            if dirs[(index + i) % len(dirs)] in moves:
                if i == 0:
                    self.bound_dir = dirs[(index + i - 1) % len(dirs)]
                else:
                    self.bound_dir = dirs[(index + i - 2) % len(dirs)]
                move = dirs[(index + i) % len(dirs)]
                return move

    def update_delta(self, move):
        dirs = ['N', 'NE', 'SE', 'S', 'SW', 'NW']
        index = dirs.index(self.last_move)

        if dirs[(index+1)%6] == move:
            self.delta = (self.delta + 1) % 5

        if dirs[(index-1)%6] == move:
            self.delta = (self.delta - 1) % 5

        if dirs[(index-2)%6] == move:
            self.delta = (self.delta - 2) % 5

        if dirs[(index-3)%6] == move:
            self.delta = (self.delta - 3) % 5


    def move(self, moves, bound_dir):
        move = None
        while (move == None) and (self.state != 'terminate'):
            if (self.state == 'Init') and (move == None):
                if (not 'NE' in moves) or (not 'NW' in moves):
                    self.state = 'terminate'
                    return None, True, False
                else:
                    self.up_x = self.x
                    self.up_y = self.y
                    self.up_start_bound_dir = bound_dir
                    self.bound_dir = 'NE'

                    self.state = 'FFC'
                    self.delta = 0
                    self.update_pos('NW')
                    self.last_move = 'NW'
                    return 'NW', False, False

            if (self.state == 'FFC') and (move == None):
                if self.y <= 0:
                    if self.last_move == 'SW' and self.delta == 0:
                        self.state = 'FL'
                    else:
                        self.state = 'UP_ret'
                else:
                    move = self.move_clockwise(moves)


            if (self.state == 'FL') and (move == None):
                if self.y <= 0:
                    if self.last_move == 'SW':
                        if self.delta == 0:
                            self.state = 'FL'
                            move = self.move_clockwise(moves)
                        elif self.delta == 1:
                            self.state = 'RetP'
                        else:
                            self.state = 'UP_ret'
                    else:
                        self.state = 'UP_ret'
                else:
                    move = self.move_clockwise(moves)


            if ((self.state == 'UP_ret') or (self.state == 'RetP')) and (move == None):
                if (self.y == self.up_y) and (self.x == self.up_x):
                    self.terminate = True
                    self.is_up = False
                    if self.state == 'RetP':
                        self.is_up = True
                    self.state = 'terminate'

                if self.state == 'UP_ret' or (self.state == 'RetP'):
                    move = self.move_counterclockwise(moves)
                self.force_return = False

        if move != None:
            self.update_pos(move)
            self.update_delta(move)
            self.last_move = move
        #print("UP output: ", self.state,)
        return move, self.terminate, self.is_up






class TraverseOnSurfaceLog():
    def __init__(self):
        self.up_inst = UniquePointOrg()
        self.state = 'TC'
        self.last_move = ''
        self.bound_dir = ''
        self.up_caller = ''

        self.x = 0
        self.y = 0

        self.x_start = None
        self.y_start = None

        self.up_x = 0
        self.up_y = 0

        self.is_up = False
        self.return_to_start = False
        self.moved_back = False

        self.moved = False
        self.special_return_handling = False
        self.RStoTB = False

        self.pebble_move_count = 0
        self.robot_coords = None
        self.last_state = None

    def reset(self):
        self.state = 'TC'
        self.last_move = ''
        self.bound_dir = ''
        self.up_caller = ''

        self.x = 0
        self.y = 0

        self.x_start = None
        self.y_start = None

        self.up_x = 0
        self.up_y = 0

        self.is_up = False
        self.return_to_start = False
        self.moved_back = False

        self.moved = False
        self.special_return_handling = False
        self.RStoTB = False

        self.pebble_move_count = 0
        self.robot_coords = None
        self.last_state = None

    def update_pos(self, ret):
        if len(ret) == 1:
            if ret == 'N':
                self.y += 2
            else:
                self.y -= 2
        else:
            if 'N' in ret:
                self.y += 1
            else:
                self.y -= 1

            if 'E' in ret:
                self.x += 1
            else:
                self.x -= 1

    def no_unique_point(self):
        if self.state == 'UP':
            self.up_inst.force_return_func()

    def return_to_starting_point(self):
        self.return_to_start = True
        #self.last_move = self.translate_move(self.last_move)
        #print("Was here", self.bound_dir, self.state, self.up_inst.state, self.up_inst.bound_dir)
        #self.bound_dir = self.translate_move(self.bound_dir)
        if self.state == 'UP':
            self.up_inst.force_return_func()
        self.special_return_handling = True
        if self.state == 'RS':
            self.state = 'TC'
        elif self.state == 'TB2':
            self.state = 'TB'
        elif self.state == 'TC':
            self.state = 'RS'
        #if 'UP' in self.state:
        #    self.up_inst.state = 'UP_ret'

    def translate_move(self, move):
        if move == None:
            return None
        tmp = ''
        for i in move:
            if i == 'E':
                tmp = tmp + 'W'
            elif i == 'W':
                tmp = tmp + 'E'
            else:
                tmp = tmp + i
        return tmp


    def move(self, moves):
        #print(self.bound_dir)
        #print(self.state, self.return_to_start)
        up_moves = [i for i in moves]
        if self.return_to_start:
            tmp_moves = [self.translate_move(i) for i in moves]
            moves = tmp_moves

            self.last_move = self.translate_move(self.last_move)
            self.bound_dir = self.translate_move(self.bound_dir)

            if self.special_return_handling:
                self.special_return_handling = False
                if self.bound_dir in moves and self.state != 'UP':
                    dirs = ['N', 'NE', 'SE', 'S', 'SW', 'NW']
                    index = dirs.index(self.bound_dir)
                    self.bound_dir = dirs[(index + 1) % 6]

        move = None

        if self.x_start == None:
            self.robot_coords = globalvars.robot_coordinates
            self.x_start = self.x
            self.y_start = self.y

        #if self.x == self.x_start and self.y == self.y_start and self.return_to_start:
        if self.robot_coords == globalvars.robot_coordinates and self.return_to_start:
            self.state = 'terminate'

        self.moved_back = True

        #if self.bound_dir == 'NE' and not ('SE' in moves):
        #    print("Was here!!!!!!!!!!!!!!!!!!!!!!!!!!")
        #    self.bound_dir = 'SE'

        while (move == None) and (self.state != 'terminate'):
            #print(self.state, self.bound_dir, self.return_to_start)
            if (self.state == 'TC') and (move == None):
                self.moved_back = False
                #if self.x == self.x_start and self.y == self.y_start and self.moved:
                if self.robot_coords == globalvars.robot_coordinates and self.moved:
                    self.state = 'terminate'

                if self.state != 'terminate':
                    if 'N' in moves:
                        move = 'N'
                        self.state = 'TC'
                    else:
                        self.state = 'UP'
                        self.bound_dir = 'N'
                        self.up_caller = 'TC'
                self.last_state = 'TC'

            if (self.state == 'RS') and (move == None):
                self.last_state = 'RS'
                if 'S' in moves:
                    move = 'S'
                else:
                    self.bound_dir = 'S'
                    self.state = 'TB'
                    self.RStoTB = True

            if (self.state == 'TB') and (move == None):
                self.moved_back = False
                dirs = ['N', 'NE', 'SE', 'S', 'SW', 'NW']
                index = dirs.index(self.bound_dir)
                #print("State in TB bound dir1:", self.bound_dir)
                #print(moves, up_moves)
                for i in range(6):
                    if dirs[(index + i) % len(dirs)] in moves:
                        move = dirs[(index + i) % len(dirs)]
                        #print("IN TB move:", move, self.bound_dir, i)
                        if i == 0:
                            #print("Was herreeeee")
                            self.bound_dir = dirs[(index + i - 1) % len(dirs)]
                        else:
                            self.bound_dir = dirs[(index + i - 2) % len(dirs)]
                        self.state = 'TB'
                        break
                #print("State in TB bound dir2:", self.bound_dir)
                self.state = 'TB2'
                self.last_state = 'TB'

            if (self.state == 'TB2') and (move == None):
                self.state = 'TB'
                if self.bound_dir == 'N':
                    self.state = 'UP'
                    self.up_caller = 'TB'
                #                                                and not self.bound_dir in moves
                if (not ('S' in moves) and ((('S' in self.bound_dir or len(moves)==1) and (not self.bound_dir in moves or not self.RStoTB or self.return_to_start)  and (self.last_move != 'S' or self.last_state != 'RS')) or ('NE' == self.bound_dir) and (not 'SE' in moves))): ##xxxxxxxxxxxx
                    self.state = 'TC'
                elif not 'N' in moves and not 'S' in moves and not 'NE' in moves and not 'SE' in moves:
                    self.state = 'TC'
                #elif not ('N' in moves) and  self.robot_coords == globalvars.robot_coordinates and not 'NW' in moves and not 'SW' in moves:
                #    self.state = 'terminate'

                self.RStoTB = False
                self.last_state = 'TB2'


            if (self.state == 'UP') and (move == None):
                if self.return_to_start:
                    move, terminate, is_up = self.up_inst.move(up_moves,  self.translate_move(self.bound_dir))
                else:
                    move, terminate, is_up = self.up_inst.move(up_moves, self.bound_dir)

                if not globalvars.logarithmic_memory:
                    # Extrasteps needed to place pebble as counter
                    globalvars.global_move_count += 2*self.up_inst.dist_to_start
                    #self.pebble_move_count += 2*self.up_inst.dist_to_start

                if terminate:
                    self.up_inst.reset()
                    if is_up:
                        if self.up_caller == 'TC':
                            self.state = 'TB'

                        if self.up_caller == 'TB':
                            self.state = 'RS'
                    else:
                        if self.up_caller == 'TC':
                            self.state = 'RS'

                        if self.up_caller == 'TB':
                            self.state = 'TB'

                # Directly return to avoid translation of move
                if move != None:
                    #self.last_move = move
                    self.update_pos(move)
                    if self.return_to_start:
                        self.bound_dir = self.translate_move(self.bound_dir)
                    #print("Move and Bound Dir UP: ", move, self.bound_dir, self.state)
                    #print(moves, up_moves)
                    return move

        if self.return_to_start:
            move = self.translate_move(move)
            self.bound_dir = self.translate_move(self.bound_dir)

        if (self.state != 'UP') and (move != None):
            self.last_move = move
            self.update_pos(move)

        self.moved = True
        #print("Move and Bound Dir: ", move, self.bound_dir, self.state)
        #print(moves, up_moves, self.return_to_start)
        return move
