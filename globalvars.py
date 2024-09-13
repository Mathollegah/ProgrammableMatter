load_file = "tests/hole.txt"
store_file = "demofile.txt"
#load_file = "tests/simpleshift.txt"
load_file = "demofile.txt"
#load_file = ""
load_file = "tests/potnotzero.txt"
#load_file = "tests/randomerror.txt"
#load_file = "tests/randomerror2.txt"
#load_file = "tests/randomerror3.txt"
#load_file = "tests/randomconf1.txt"
#load_file = "tests/layerswitch2.txt"
number_of_tiles = 40
printsteps = 1000

dodecahedrons = []

global_start_node = None
global_switch = False

global_bound_box = False
interpolation_steps = 30
new_interpolation_steps = interpolation_steps
random_configuration = True
boxsize = 30

movecounter = {}

visualize = False
onlygenerate = False

logarithmic_memory = False

robot_coordinates = (0, 0, 0)
robot_z_coord = 0
min_z_coord = 10000000

global_move_count = 0

pot = (100000, 00000)
pot_equal_count = 0

run_silent = True