import globalvars

class FindShiftableLine():
    def __init__(self):
        self.x = 0
        self.y = 0
        self.z = 0
        self.tile_found = False

    def find_tile(self):
        global dodecahedrons
        self.tile_found = False

        for i in globalvars.dodecahedrons:
            tmp1 = (i.top != None) or (i.bottom != None)
            tmp2 = (i.upleft1 != None) or (i.upleft2 != None) or (i.upright1 != None) or (i.upright2 != None)
            tmp3 = (i.downleft1 != None) or (i.downleft2 != None) or (i.downright1 != None) or (i.downright2 != None)

            if tmp1 or (tmp2 and tmp3):
                self.x = i.x
                self.y = i.y
                self.z = i.z
                self.tile_found = True

