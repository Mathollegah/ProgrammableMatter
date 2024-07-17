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
                    pot += (tile.z-min_z-0.5)
                else:
                    pot += (tile.z-min_z)
            else:
                if tile.z % 1 != 0:
                    pot += (tile.z-min_z-0.5)
                else:
                    pot += (tile.z-min_z)

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
                    pot += (tile.x-min_x-0.5)
                else:
                    pot += (tile.x-min_x)
            else:
                if tile.x % 1 != 0:
                    pot += (tile.x-min_x-0.5)
                else:
                    pot += (tile.x-min_x)

    return pot
