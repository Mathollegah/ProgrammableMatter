class Potential:
    def __init__(self, state):
        self.state = state

    def potential_x(self, robot_tile):
        min_z = 1000000
        for tile in self.state.dodecahedrons:
            if tile.z < min_z:
                min_z = tile.z

        half = False
        if min_z % 1 != 0:
            half = True

        pot = 0

        for tile in self.state.dodecahedrons:
            if tile.bottom == None and tile != robot_tile:
                if half:
                    if tile.z % 1 == 0:
                        pot_tmp = (tile.z-min_z-0.5)
                    else:
                        pot_tmp = (tile.z-min_z)
                else:
                    if tile.z % 1 != 0:
                        pot_tmp = (tile.z-min_z-0.5)
                    else:
                        pot_tmp = (tile.z-min_z)
                tile.pot_x = pot_tmp
                pot += pot_tmp
            else:
                tile.pot_x = 0

        return pot


    def potential_z(self, robot_tile):
        min_x = 1000000
        for tile in self.state.dodecahedrons:
            if tile.x < min_x:
                min_x = tile.x

        half = False
        if min_x % 1 != 0:
            half = True

        pot = 0

        for tile in self.state.dodecahedrons:
            if tile.back == None and tile != robot_tile:
                if half:
                    if tile.x % 1 == 0:
                        pot_tmp = (tile.x-min_x-0.5)
                    else:
                        pot_tmp = (tile.x-min_x)
                else:
                    if tile.x % 1 != 0:
                        pot_tmp = (tile.x-min_x-0.5)
                    else:
                        pot_tmp = (tile.x-min_x)
                tile.pot_z = pot_tmp
                pot += pot_tmp
            else:
                tile.pot_z = 0
        return pot


    def potential(self, robot_tile):
        return self.potential_x(robot_tile) + self.potential_z(robot_tile)