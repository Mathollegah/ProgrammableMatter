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
