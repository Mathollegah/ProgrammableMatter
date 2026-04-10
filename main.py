import globalvars
from robots.constauto.robot import *
import potential.potential as potential
import argparse
from visualization.visualization import Simulator3D
from robots.RL.RL import RLRobotLearn, RLRobotPlay




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
ap.add_argument("--useAI", default=False, help="Use the trained AI model.")

args = vars(ap.parse_args())

state = globalvars.State()
config = globalvars.Config()
pot = potential.Potential(state)

config.visualize = args["visualize"]
config.number_of_tiles = int(args["tiles"])
config.load_file = args["infile"]
config.store_file = args["outfile"]
config.random_configuration = args["random"]
config.boxsize = int(args["boxsize"])
config.printsteps = int(args["printsteps"])
config.onlygenerate = bool(args["onlygenerate"])
state.logarithmic_memory = bool(args["logarithmic"])
state.potential = pot
config.run_silent = bool(args["runsilent"])
config.trainmodel = bool(args["trainmodel"])


if not config.trainmodel:
    if not bool(args["useAI"]):
        app = Simulator3D(ConstRobot(state), config, state)
    else:
        app = Simulator3D(RLRobotPlay(config, state), config, state)

    app.main()
else:
    app = RLRobotLearn(config, state, max_steps=50)
    app.learn(total_timesteps=50000)
