class TraverseLayer():
    def __init__(self):
        self.state = 'find_boundary'
        self.start_pos = (0,0)
        self.last_move = 0
        self.sec_to_last_move = 2
        self.max = (0,0)
        self.min = (0,0)
        self.x = 0
        self.y = 0
        self.count = 0

        self.bound_pos = (-100, -100)
        self.north_pos = (-105, -105)
        self.last_move_2 = 0
        self.sec_to_last_move_2 = 0
        self.sec_move = False

        self.sec_start_pos = False

    def reset(self):
        self.state = 'find_boundary'
        self.start_pos = (0, 0)
        self.last_move = 0
        self.sec_to_last_move = 2
        self.max = (0, 0)
        self.min = (0, 0)
        self.x = 0
        self.y = 0
        self.count = 0

        self.bound_pos = (-100, -100)
        self.north_pos = (-105, -105)
        self.last_move_2 = 0
        self.sec_to_last_move_2 = 0
        self.sec_move = False

        self.sec_start_pos = False

    def update_bounds(self, move):
        if move == 0:
            self.y += 1

        if move == 1:
            self.y += 0.5
            self.x += 0.5

        if move == 2:
            self.y -= 0.5
            self.x += 0.5

        if move == 3:
            self.y -= 1

        if move == 4:
            self.y -= 0.5
            self.x -= 0.5

        if move == 5:
            self.y += 0.5
            self.x -= 0.5

        if self.x > self.max[0]:
            self.max = (self.x, self.max[1])

        if self.y > self.max[1]:
            self.max = (self.max[0], self.y)

        if self.x < self.min[0]:
            self.min = (self.x, self.min[1])

        if self.y < self.min[1]:
            self.min = (self.min[0], self.y)


    def move(self, possible_moves):
        if self.state == 'find_boundary':
            for i in [0,5,1]:
                if possible_moves[i][1]:
                    self.sec_to_last_move = self.last_move
                    self.last_move = possible_moves[i][0]
                    return possible_moves[i][0]

            for i in range(len(possible_moves)):
                if possible_moves[i][0]:
                    self.last_move = (i+1)%6
                    self.sec_to_last_move = i

            self.start_pos = (0, 0)
            self.state = 'follow_boundary'
            return -1

        if self.state == 'follow_boundary':
            if (self.x, self.y) == self.start_pos and self.sec_start_pos:
                self.state = 'terminate_completely'
                return -1

            self.sec_start_pos = True

            for i in range(6):
                if (self.last_move-self.sec_to_last_move +3)%6 != 0:
                    tmp = (self.last_move - 1 + i) % 6
                else:
                    tmp = (self.last_move - 2 + i) % 6

                if possible_moves[tmp][1]:
                    self.sec_to_last_move = self.last_move
                    self.last_move = tmp
                    self.update_bounds(tmp)
                    if tmp != 0 and (self.x != self.north_pos[0]): #tmp != 0 and tmp != 3 and (self.x != self.north_pos[0])
                        self.state = 'north'
                        self.count = 0
                        self.bound_pos = (self.x, self.y)
                    return possible_moves[tmp][0]

        if self.state == 'north':
            self.sec_to_last_move_2 = 2
            self.last_move_2 = 1
            if possible_moves[0][1]:
                self.update_bounds(0)
                self.count += 1
                #self.sec_to_last_move_2 = self.last_move
                #self.last_move_2 = possible_moves[0][0]
                return possible_moves[0][0]

            #if (self.max[1]-self.y) >= 1:
            #    self.count += 1
            #    self.state = 'terminate'
            #    return possible_moves[0][0]

            if self.bound_pos != (self.x, self.y):
                self.north_pos = (self.x, self.y)
                self.state = 'follow_new_boundary' # south xxxxxxxxxxx
                self.sec_move = False
            else:
                self.state = 'follow_boundary'
            return -1


        if self.state == 'follow_new_boundary':
            if (self.x, self.y) == self.bound_pos:
                self.state = 'follow_boundary'
                return -1

            if (self.x, self.y) == self.north_pos and self.sec_move:
                self.state = 'terminate'
                return 0

            self.sec_move = True

            for i in range(6):
                if (self.last_move_2-self.sec_to_last_move_2 +3)%6 != 0:
                    tmp = (self.last_move_2 - 1 + i) % 6
                else:
                    tmp = (self.last_move_2 - 2 + i) % 6

                if possible_moves[tmp][1]:
                    self.sec_to_last_move_2 = self.last_move_2
                    self.last_move_2 = tmp
                    self.update_bounds(tmp)
                    return possible_moves[tmp][0]

        return -1
