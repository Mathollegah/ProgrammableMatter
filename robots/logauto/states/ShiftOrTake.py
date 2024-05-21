class ShiftOrTake():
    def __init__(self):
        self.state = 'set_initial_tile'
        self.removable_tile = None
        self.robot = None

    def reset(self):
        self.state = 'set_initial_tile'
        self.removable_tile = None

    def move(self, directions, tile):
        #[(0, self.top), (1, self.bottom), (2, self.front), (3, self.back),
        # (4, self.upleft1), (5, self.upleft2), (6, self.upright1), (7, self.upright2),
        # (8, self.downleft1), (9, self.downleft2), (10, self.downright1), (11, self.downright2)]

        if self.state == 'set_initial_tile':
            if directions[1][1] == None:
                self.state = 'place_tile'
                self.removable_tile = tile
                #print(self.removable_tile, self.robot.grabbed_tile)
                return directions[1][0]
            elif directions[3][1] != None:
                self.state = 'place_tile_next'
                self.removable_tile = tile
                #print(self.removable_tile, self.robot.grabbed_tile)
                return directions[1][0]
            else:
                self.state = 'terminate'
                self.removable_tile = tile
                #print(self.removable_tile, self.robot.grabbed_tile)
                return -12

        if self.state == 'place_tile_next':
            self.state = 'place_tile'
            return directions[3][0]

        if self.state == 'place_tile':
            if tile == None:
                self.state = 'take_next_tile'
                return 13 # place tile
            else:
                self.state = 'terminate'
                return -1

        if self.state == 'take_next_tile':
            #print(self.removable_tile.x, self.removable_tile.y, self.removable_tile.z, self.robot.x, self.robot.y, self.robot.z)
            if self.removable_tile.x > self.robot.x:
                return directions[2][0]
            if self.removable_tile.z > self.robot.z:
                return directions[0][0]

            if self.removable_tile.back != None:
                self.state = 'shift_tile_downleft2'
                self.removable_tile = self.removable_tile.back
                #print(self.removable_tile, self.robot.grabbed_tile)
            else:
                self.removable_tile = None
                self.state = 'terminate'

            #self.removable_tile = self.removable_tile.back
            return 12 # grab tile

        if self.state == 'shift_tile_downleft2':
            self.state = 'shift_tile_downright2'
            return directions[8][0]

        if self.state == 'shift_tile_downright2':
            self.state = 'place_tile'
            return directions[9][0]

