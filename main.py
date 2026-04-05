import globalvars
from robots.constauto.robot import *
from potential import potential
import random
import argparse
from visualization.visualization import Simulator3D
from game.game import Dodecahedron, Game



def build_new_configuration():
    if globalvars.load_file == "" and not globalvars.random_configuration:
        globalvars.dodecahedrons = [Dodecahedron(0,0,0)]
        i=0
        while i < globalvars.number_of_tiles-1:
            x = random.choice(globalvars.dodecahedrons)

            d = random.choice(x.directions)

            if d[1] == None:
                if d[0] == 0:
                    tmp = Dodecahedron(x.x,x.y,x.z+1)
                    globalvars.dodecahedrons.append(tmp)
                    tmp.bottom = x
                    x.top = tmp
                    i = i+1

                if d[0] == 1:
                    tmp = Dodecahedron(x.x,x.y,x.z-1)
                    globalvars.dodecahedrons.append(tmp)
                    tmp.top = x
                    x.bottom = tmp
                    i = i + 1

                if d[0] == 2:
                    tmp = Dodecahedron(x.x+1,x.y,x.z)
                    globalvars.dodecahedrons.append(tmp)
                    tmp.back = x
                    x.front = tmp
                    i = i + 1

                if d[0] == 3:
                    tmp = Dodecahedron(x.x-1,x.y,x.z)
                    globalvars.dodecahedrons.append(tmp)
                    tmp.front = x
                    x.back = tmp
                    i = i + 1

                if d[0] == 4:
                    tmp = Dodecahedron(x.x-0.5,x.y+0.75,x.z+0.5)
                    globalvars.dodecahedrons.append(tmp)
                    tmp.downright2 = x
                    x.upleft1 = tmp
                    i = i + 1

                if d[0] == 5:
                    tmp = Dodecahedron(x.x-0.5,x.y-0.75,x.z+0.5)
                    globalvars.dodecahedrons.append(tmp)
                    tmp.downright1 = x
                    x.upleft2 = tmp
                    i = i + 1

                if d[0] == 6:
                    tmp = Dodecahedron(x.x+0.5,x.y+0.75,x.z+0.5)
                    globalvars.dodecahedrons.append(tmp)
                    tmp.downleft2 = x
                    x.upright1 = tmp
                    i = i + 1

                if d[0] == 7:
                    tmp = Dodecahedron(x.x+0.5,x.y-0.75,x.z+0.5)
                    globalvars.dodecahedrons.append(tmp)
                    tmp.downleft1 = x
                    x.upright2 = tmp
                    i = i + 1

                if d[0] == 8:
                    tmp = Dodecahedron(x.x-0.5,x.y+0.75,x.z-0.5)
                    globalvars.dodecahedrons.append(tmp)
                    tmp.upright2 = x
                    x.downleft1 = tmp
                    i = i + 1

                if d[0] == 9:
                    tmp = Dodecahedron(x.x-0.5,x.y-0.75,x.z-0.5)
                    globalvars.dodecahedrons.append(tmp)
                    tmp.upright1 = x
                    x.downleft2 = tmp
                    i = i + 1

                if d[0] == 10:
                    tmp = Dodecahedron(x.x+0.5,x.y+0.75,x.z-0.5)
                    globalvars.dodecahedrons.append(tmp)
                    tmp.upleft2 = x
                    x.downright1 = tmp
                    i = i + 1

                if d[0] == 11:
                    tmp = Dodecahedron(x.x+0.5,x.y-0.75,x.z-0.5)
                    globalvars.dodecahedrons.append(tmp)
                    tmp.upleft1 = x
                    x.downright2 = tmp
                    i = i + 1

                tmp.find_neighbours(globalvars.dodecahedrons)

                for x in globalvars.dodecahedrons:
                    x.directions = [(0, x.top), (1, x.bottom), (2, x.front), (3, x.back),
                                       (4, x.upleft1), (5, x.upleft2), (6, x.upright1), (7, x.upright2),
                                       (8, x.downleft1), (9, x.downleft2), (10, x.downright1), (11, x.downright2)]

    elif globalvars.load_file == "" and globalvars.random_configuration:
        build_random_configuration()

    else:
        f = open(globalvars.load_file, "r")
        txt = f.read()
        f.close()
        nodes = txt.split()
        nodes = [float(i) for i in nodes]
        tmp_robot_pos = nodes[:3]

        for i in range(len(nodes)//3-1):
            tmp = Dodecahedron(nodes[3*i+3], nodes[3*i+4], nodes[3*i+5])
            globalvars.dodecahedrons.append(tmp)
            tmp.find_neighbours(globalvars.dodecahedrons)

        for i in globalvars.dodecahedrons:
            if (i.x,i.y,i.z) == (tmp_robot_pos[0], tmp_robot_pos[1], tmp_robot_pos[2]):
                globalvars.global_start_node = i
                break



def build_random_configuration():
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
    boxsize = globalvars.boxsize
    components = {}
    component_counter = 0
    globalvars.dodecahedrons = []

    max_component = 0
    comp_name = None
    while max_component < globalvars.number_of_tiles:
        x,y,z = pick_position(boxsize)

        exists = False
        for tile in globalvars.dodecahedrons:
            if (tile.x == x) and (tile.y == y) and (tile.z == z):
                exists = True
                break

        if not exists:
            tmp = Dodecahedron(x, y, z)
            tmp.component = [component_counter]
            components[component_counter] = 1
            component_counter += 1
            globalvars.dodecahedrons.append(tmp)
            tmp.find_neighbours(globalvars.dodecahedrons)

            tmp.component = list(set(tmp.component))
            min_comp = min(tmp.component)

            val = 0
            for i in tmp.component:
                val += components[i]

            components[min_comp] = val

            for comp in tmp.component:
                for dod in globalvars.dodecahedrons:
                    if comp in dod.component:
                        dod.component = [min_comp]

            max_component = 0
            for i in components:
                if components[i] > max_component:
                    max_component = components[i]
                    comp_name = i

    new_dodecas = []
    for i in globalvars.dodecahedrons:
        if comp_name in i.component:
            new_dodecas.append(i)
    globalvars.dodecahedrons = new_dodecas

    dodeca = random.choice(globalvars.dodecahedrons)
    tmp_x = dodeca.x
    tmp_y = dodeca.y
    tmp_z = dodeca.z
    for i in globalvars.dodecahedrons:
        i.x -= tmp_x
        i.y -= tmp_y
        i.z -= tmp_z

    print("finished")
    print(len(globalvars.dodecahedrons))




ap = argparse.ArgumentParser()

ap.add_argument("--visualize", default=True, help="Whether to render the configuration or run the algorithm in the background.")
ap.add_argument("--tiles", default=100, help="Minimal number of tiles in random configuration.")
ap.add_argument("--infile", default="", help="Configuration to load.")
ap.add_argument("--outfile", default="demofile.txt", help="Configuration to load.")
ap.add_argument("--random", default=True, help="Whether a random configuration should be created.")
ap.add_argument("--boxsize", default=25, help="Size of box in which the random configuration is created..")
ap.add_argument("--printsteps", default=1000, help="Minimal number of tiles in random configuration.")
ap.add_argument("--onlygenerate", default=False, help="Minimal number of tiles in random configuration.")
ap.add_argument("--logarithmic", default=False, help="Whether to use logarithmic or constant memory.")
ap.add_argument("--runsilent", default=False, help="Whether to use logarithmic or constant memory.")
ap.add_argument("--trainmodel", default=False, help="Use this option to train an algorithm.")

args = vars(ap.parse_args())
globalvars.visualize = args["visualize"]
globalvars.number_of_tiles = int(args["tiles"])
globalvars.load_file = args["infile"]
globalvars.store_file = args["outfile"]
globalvars.random_configuration = args["random"]
globalvars.boxsize = int(args["boxsize"])
globalvars.printsteps = int(args["printsteps"])
globalvars.onlygenerate = bool(args["onlygenerate"])
globalvars.logarithmic_memory = bool(args["logarithmic"])
globalvars.run_silent = bool(args["runsilent"])
globalvars.trainmodel = bool(args["trainmodel"])


build_new_configuration()


if not globalvars.trainmodel:
    app = Simulator3D()

    if not globalvars.onlygenerate or globalvars.run_silent:
        print("Count: " + str(globalvars.global_move_count) + ", Potential_X: " + str(
            potential.potential_x(app.grabbed_tile)) + ", " + "Potential_Z: " + str(
            potential.potential_z(app.grabbed_tile)))

        #app.run()
        while not globalvars.visualize:
            app.moveRobotNoAnimation()

            if app.robot.state == 'terminate':
                print("Count: " + str(globalvars.global_move_count) + ", Potential_X: " + str(potential.potential_x(app.grabbed_tile)) + ", " + "Potential_Z: " + str(potential.potential_z(app.grabbed_tile)))
                break


        if globalvars.visualize:
            app.init_visualization()
            app.run()

        print("Number of Dodecahedrons: ", len(globalvars.dodecahedrons))
else:
    game = Game()