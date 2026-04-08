from game.game import Dodecahedron
import random

class Configgen():
    def __init__(self, config, state):
        self.config = config
        self.state = state

    def build_new_configuration(self):
        if self.config.load_file == "" and not self.config.random_configuration:
            self.state.dodecahedrons = [Dodecahedron(0,0,0)]
            i=0
            while i < self.config.number_of_tiles-1:
                x = random.choice(self.state.dodecahedrons)

                d = random.choice(x.directions)

                if d[1] == None:
                    if d[0] == 0:
                        tmp = Dodecahedron(x.x,x.y,x.z+1)
                        self.state.dodecahedrons.append(tmp)
                        tmp.bottom = x
                        x.top = tmp
                        i = i+1

                    if d[0] == 1:
                        tmp = Dodecahedron(x.x,x.y,x.z-1)
                        self.state.dodecahedrons.append(tmp)
                        tmp.top = x
                        x.bottom = tmp
                        i = i + 1

                    if d[0] == 2:
                        tmp = Dodecahedron(x.x+1,x.y,x.z)
                        self.state.dodecahedrons.append(tmp)
                        tmp.back = x
                        x.front = tmp
                        i = i + 1

                    if d[0] == 3:
                        tmp = Dodecahedron(x.x-1,x.y,x.z)
                        self.state.dodecahedrons.append(tmp)
                        tmp.front = x
                        x.back = tmp
                        i = i + 1

                    if d[0] == 4:
                        tmp = Dodecahedron(x.x-0.5,x.y+0.75,x.z+0.5)
                        self.state.dodecahedrons.append(tmp)
                        tmp.downright2 = x
                        x.upleft1 = tmp
                        i = i + 1

                    if d[0] == 5:
                        tmp = Dodecahedron(x.x-0.5,x.y-0.75,x.z+0.5)
                        self.state.dodecahedrons.append(tmp)
                        tmp.downright1 = x
                        x.upleft2 = tmp
                        i = i + 1

                    if d[0] == 6:
                        tmp = Dodecahedron(x.x+0.5,x.y+0.75,x.z+0.5)
                        self.state.dodecahedrons.append(tmp)
                        tmp.downleft2 = x
                        x.upright1 = tmp
                        i = i + 1

                    if d[0] == 7:
                        tmp = Dodecahedron(x.x+0.5,x.y-0.75,x.z+0.5)
                        self.state.dodecahedrons.append(tmp)
                        tmp.downleft1 = x
                        x.upright2 = tmp
                        i = i + 1

                    if d[0] == 8:
                        tmp = Dodecahedron(x.x-0.5,x.y+0.75,x.z-0.5)
                        self.state.dodecahedrons.append(tmp)
                        tmp.upright2 = x
                        x.downleft1 = tmp
                        i = i + 1

                    if d[0] == 9:
                        tmp = Dodecahedron(x.x-0.5,x.y-0.75,x.z-0.5)
                        self.state.dodecahedrons.append(tmp)
                        tmp.upright1 = x
                        x.downleft2 = tmp
                        i = i + 1

                    if d[0] == 10:
                        tmp = Dodecahedron(x.x+0.5,x.y+0.75,x.z-0.5)
                        self.state.dodecahedrons.append(tmp)
                        tmp.upleft2 = x
                        x.downright1 = tmp
                        i = i + 1

                    if d[0] == 11:
                        tmp = Dodecahedron(x.x+0.5,x.y-0.75,x.z-0.5)
                        self.state.dodecahedrons.append(tmp)
                        tmp.upleft1 = x
                        x.downright2 = tmp
                        i = i + 1

                    tmp.find_neighbours(self.state.dodecahedrons)

                    for x in self.state.dodecahedrons:
                        x.directions = [(0, x.top), (1, x.bottom), (2, x.front), (3, x.back),
                                        (4, x.upleft1), (5, x.upleft2), (6, x.upright1), (7, x.upright2),
                                        (8, x.downleft1), (9, x.downleft2), (10, x.downright1), (11, x.downright2)]

        elif self.config.load_file == "" and self.config.random_configuration:
            self.build_random_configuration()
        else:
            f = open(self.config.load_file, "r")
            txt = f.read()
            f.close()
            nodes = txt.split()
            nodes = [float(i) for i in nodes]
            tmp_robot_pos = nodes[:3]

            for i in range(len(nodes)//3-1):
                tmp = Dodecahedron(nodes[3*i+3], nodes[3*i+4], nodes[3*i+5])
                self.state.dodecahedrons.append(tmp)
                tmp.find_neighbours(self.state.dodecahedrons)

            for i in self.state.dodecahedrons:
                if (i.x,i.y,i.z) == (tmp_robot_pos[0], tmp_robot_pos[1], tmp_robot_pos[2]):
                    self.state.global_start_node = i
                    break



    def build_random_configuration(self):
        def pick_position(boxsize):
            x = random.choice(list(range(boxsize)))
            y = random.choice(list(range(boxsize)))
            z = random.choice(list(range(boxsize)))
            if y%2 == 1:
                x = x+0.5
                z = z+0.5
            y = y * 0.75
            return x, y, z

        print("Generate configuration")
        boxsize = self.config.boxsize
        components = {}
        component_counter = 0
        self.state.dodecahedrons = []

        max_component = 0
        comp_name = None
        while max_component < self.config.number_of_tiles:
            x,y,z = pick_position(boxsize)

            exists = False
            for tile in self.state.dodecahedrons:
                if (tile.x == x) and (tile.y == y) and (tile.z == z):
                    exists = True
                    break

            if not exists:
                tmp = Dodecahedron(x, y, z)
                tmp.component = [component_counter]
                components[component_counter] = 1
                component_counter += 1
                self.state.dodecahedrons.append(tmp)
                tmp.find_neighbours(self.state.dodecahedrons)

                tmp.component = list(set(tmp.component))
                min_comp = min(tmp.component)

                val = 0
                for i in tmp.component:
                    val += components[i]

                components[min_comp] = val

                for comp in tmp.component:
                    for dod in self.state.dodecahedrons:
                        if comp in dod.component:
                            dod.component = [min_comp]

                max_component = 0
                for i in components:
                    if components[i] > max_component:
                        max_component = components[i]
                        comp_name = i

        new_dodecas = []
        for i in self.state.dodecahedrons:
            if comp_name in i.component:
                new_dodecas.append(i)
        self.state.dodecahedrons = new_dodecas

        dodeca = random.choice(self.state.dodecahedrons)
        tmp_x = dodeca.x
        tmp_y = dodeca.y
        tmp_z = dodeca.z
        for i in self.state.dodecahedrons:
            i.x -= tmp_x
            i.y -= tmp_y
            i.z -= tmp_z

        print("finished")
        print(len(self.state.dodecahedrons))

    
