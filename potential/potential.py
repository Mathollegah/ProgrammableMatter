import globalvars


def potential_x(robot_tile):
    min_z = 1000000
    for tile in globalvars.dodecahedrons:
        if tile.z < min_z:
            min_z = tile.z

    half = False
    if min_z % 1 != 0:
        half = True

    pot = 0

    for tile in globalvars.dodecahedrons:
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


def potential_z(robot_tile):
    min_x = 1000000
    for tile in globalvars.dodecahedrons:
        if tile.x < min_x:
            min_x = tile.x

    half = False
    if min_x % 1 != 0:
        half = True

    pot = 0

    for tile in globalvars.dodecahedrons:
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


def potential(robot_tile):
    return potential_x(robot_tile) + potential_z(robot_tile)

