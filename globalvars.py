from dataclasses import dataclass


@dataclass
class State:
    robot_coordinates = (0, 0, 0)
    robot_z_coord = 0
    min_z_coord = 10000000
    dodecahedrons = []
    global_start_node = None
    global_move_count = 0
    pot = (100000, 00000)
    logarithmic_memory = False
    potential = None


@dataclass
class Config:
    load_file = "tests/hole.txt"
    store_file = "demofile.txt"
    number_of_tiles = 40
    printsteps = 1000
    global_bound_box = False
    interpolation_steps = 30
    new_interpolation_steps = interpolation_steps
    random_configuration = True
    boxsize = 30
    visualize = False
    onlygenerate = False
    run_silent = True
    trainmodel = False

