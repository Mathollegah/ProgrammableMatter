from robots.logauto.states.TraverseLayer import *

class MoveOnSurface():
    def __init__(self):
        self.state = 'move_bot'
        self.surface_state = 'TC'
        self.unique_point_state = 'computing'
        self.last_move = -1
        self.move_decision = 0
        self.check_placing_flag = False
        # front, back, left1, left2, right1, right2
        self.movable = [False, False, False, False, False, False]
        self.move_algorithm = TraverseLayer()

    def reset(self):
        self.state = 'move_bot'
        self.surface_state = 'TC'
        self.check_placing_flag = False
        self.movable = [False, False, False, False, False, False]
        self.move_algorithm.reset()

    def take_move_decision(self):
        # (0, north), (1, south), (2, westnorth), (3, westsouth), (4, eastnorth), (5, eastsouth)
        possible_moves = []
        for i in [0,5,3,1,2,4]:
            possible_moves.append((i, self.movable[i]))

        tmp = self.move_algorithm.move(possible_moves)
        if self.move_algorithm.state == 'terminate':
            self.check_placing_flag = True

        if self.move_algorithm.state == 'terminate_completely':
            self.state = 'terminate_completely'
        return tmp

    def move(self, directions):
        self.check_placing_flag = False

        if self.state == 'move_bot':
            if directions[2][1] == None:
                if self.movable[0]:
                    self.state = 'terminate'
                    self.check_placing_flag = True
                    return directions[2][0]

            if directions[3][1] == None:
                if self.movable[1]:
                    self.state = 'terminate'
                    self.check_placing_flag = True
                    return directions[3][0]

            if directions[4][1] == None:
                if self.movable[2]:
                    self.state = 'terminate'
                    self.check_placing_flag = True
                    return directions[4][0]

            if directions[5][1] == None:
                if self.movable[3]:
                    self.state = 'terminate'
                    self.check_placing_flag = True
                    return directions[5][0]

            if directions[6][1] == None:
                if self.movable[4]:
                    self.state = 'terminate'
                    self.check_placing_flag = True
                    return directions[6][0]

            if directions[7][1] == None:
                if self.movable[5]:
                    self.state = 'terminate'
                    self.check_placing_flag = True
                    return directions[7][0]


            if directions[2][1] != None:
                self.movable[0] = True

            if directions[3][1] != None:
                self.movable[1] = True

            if directions[4][1] != None or directions[8][1] != None:
                self.movable[2] = True

            if directions[5][1] != None or directions[9][1] != None:
                self.movable[3] = True

            if directions[6][1] != None or directions[10][1] != None:
                self.movable[4] = True

            if directions[7][1] != None or directions[11][1] != None:
                self.movable[5] = True


            if directions[1][1] != None:
                return directions[1][0]
            else:
                self.check_placing_flag = True
                self.movable = [False, False, False, False, False, False]
                self.state = 'check_neighbors'
                return -1 # Do not move to give time for placing decision

        if self.state == 'check_neighbors':
            if directions[2][1] != None:
                self.movable[0] = True

            if directions[3][1] != None:
                self.movable[1] = True

            if directions[4][1] != None or directions[8][1] != None:
                self.movable[2] = True

            if directions[5][1] != None or directions[9][1] != None:
                self.movable[3] = True

            if directions[6][1] != None or directions[10][1] != None:
                self.movable[4] = True

            if directions[7][1] != None or directions[11][1] != None:
                self.movable[5] = True

            # Move to top and take decision
            if directions[0][1] != None:
                return directions[0][0]
            else:
                self.move_decision = self.take_move_decision()
                if self.move_decision == -1:
                    return -1
                self.state = 'take_move'

        if self.state == 'take_move':
            self.movable = [False, False, False, False, False, False]

            if self.move_algorithm.state == 'terminate':
                self.check_placing_flag = True
                self.state = 'terminate'
                self.last_move = directions[2][0]
                return directions[2][0]

            if self.move_decision == 0 and directions[2][1] != None:
                self.state = 'move_bot'
                self.last_move = directions[2][0]
                return directions[2][0]

            if self.move_decision == 1 and directions[3][1] != None:
                self.state = 'move_bot'
                self.last_move = directions[3][0]
                return directions[3][0]

            if self.move_decision == 2 and directions[4][1] != None:
                self.state = 'move_bot'
                self.last_move = directions[4][0]
                return directions[4][0]

            if self.move_decision == 2 and directions[8][1] != None:
                self.state = 'move_bot'
                self.last_move = directions[8][0]
                return directions[8][0]

            if self.move_decision == 3 and directions[5][1] != None:
                self.state = 'move_bot'
                self.last_move = directions[5][0]
                return directions[5][0]

            if self.move_decision == 3 and directions[9][1] != None:
                self.state = 'move_bot'
                self.last_move = directions[9][0]
                return directions[9][0]

            if self.move_decision == 4 and directions[6][1] != None:
                self.state = 'move_bot'
                self.last_move = directions[6][0]
                return directions[6][0]

            if self.move_decision == 4 and directions[10][1] != None:
                self.state = 'move_bot'
                self.last_move = directions[10][0]
                return directions[10][0]

            if self.move_decision == 5 and directions[7][1] != None:
                self.state = 'move_bot'
                self.last_move = directions[7][0]
                return directions[7][0]

            if self.move_decision == 5 and directions[11][1] != None:
                self.state = 'move_bot'
                self.last_move = directions[11][0]
                return directions[11][0]

            # go straight down
            return directions[1][0]

        return -1
