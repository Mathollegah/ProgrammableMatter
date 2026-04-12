# simple_ai_game.py
import numpy as np
import gymnasium
from gymnasium import spaces
#from stable_baselines3 import RecurrentPPO
from sb3_contrib import RecurrentPPO
from game.game import Game, Dodecahedron
from configgen.configgen import Configgen
from robots.RL.reward.simple_potential import RewardSimplePotential
from robots.RL.reward.constauto import RewardConstauto

class RLRobotBase():
    def __init__(self, config, state, max_steps=10000):
        # Discrete moves:
        # 0) 'U'
        # 1) 'D'
        # 2) 'F'
        # 3) 'B'
        # 4) 'UBR'
        # 5) 'UBL'
        # 6) 'UFR'
        # 7) 'UFL'
        # 8) 'DBR'
        # 9) 'DBL'
        # 10) 'DFR'
        # 11) 'DFL'
        # 12) 'grab_tile'
        # 13) 'place_tile'
        self.action_space = spaces.Discrete(14)

        # Observation space declaration
        # 0-11 are whether the direction is occupied, as before
        # 12 is whether the robots position is occupied
        # 13 is whether the robot is holding a tile
        self.observation_space = spaces.Box(
            low=0.0,
            high=1.0,
            shape=(14,),
            dtype=np.float32
        )


    def translate_action(self, action):
        if action == 0:
            return 'U'
        elif action == 1:
            return 'D'
        elif action == 2:
            return 'F'
        elif action == 3:
            return 'B'
        elif action == 4:
            return 'UBR'
        elif action == 5:
            return 'UBL'
        elif action == 6:
            return 'UFR'
        elif action == 7:
            return 'UFL'
        elif action == 8:
            return 'DBR'
        elif action == 9:
            return 'DBL'
        elif action == 10:
            return 'DFR'
        elif action == 11:
            return 'DFL'
        elif action == 12:
            return 'grab_tile'
        elif action == 13:
            return 'place_tile'
        
    def compute_state_noargs(self):
        moves = self.detect_neighbors()
        occupied = self.detect_occupied()
        self.compute_state(moves, occupied)

    def compute_state(self, moves, occupied):
        self.RL_state[:12] = [1.0 if move in moves else 0.0 for move in ['U', 'D', 'F', 'B', 'UBR', 'UBL', 'UFR', 'UFL', 'DBR', 'DBL', 'DFR', 'DFL']]
        self.RL_state[12] = 1.0 if occupied else 0.0
        self.RL_state[13] = 1.0 if self.grabbed_tile is not None else 0.0
    

class RLRobotLearn(RLRobotBase, gymnasium.Env, Game, Configgen):
    def __init__(self, config, state, max_steps=10000):
        self.config = config
        self.state = state
        self.max_steps = max_steps
        self.steps = 0
        self.switched_orientation = False

        Configgen.__init__(self, config, state)
        self.build_new_configuration()

        gymnasium.Env.__init__(self)
        Game.__init__(self, self, config, state)
        RLRobotBase.__init__(self, config, state)

        # Current vision of the robot
        self.RL_state = np.array([1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0], dtype=np.float32)
        self.compute_state_noargs()

        self.model = RecurrentPPO("MlpLstmPolicy", self, verbose=1, n_steps=64, policy_kwargs=dict(lstm_hidden_size=64),)
        self.max_steps = max_steps
        self.steps = 0

        if config.reward_function == "simple_potential":
            self.reward_inst = RewardSimplePotential(self, config, state)
        elif config.reward_function == "constauto":
            self.reward_inst = RewardConstauto(self, config, state)
        else:
            raise ValueError("Invalid reward function specified")

    def reset(self, seed=None, options=None):
        self.build_new_configuration()
        Game.__init__(self, self, self.config, self.state)
        self.RL_state = np.array([1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0], dtype=np.float32)
        self.compute_state_noargs()
        self.steps = 0
        return self.RL_state.copy(), {}

        # Similar to moveRobot in game.py but callable from training class
    def step(self, action):
        # Get next move from robot
        next_move = self.translate_action(action)
        occupied = self.detect_occupied()
        self.reward_inst.predict()
        if (not next_move in ['grab_tile', 'place_tile']) or (next_move == 'grab_tile' and self.grabbed_tile is None and occupied) or (next_move == 'place_tile' and self.grabbed_tile is not None and not occupied):
            self.x_next, self.y_next, self.z_next = self.act_move(next_move)

            self.x = self.x_next
            self.y = self.y_next
            self.z = self.z_next

            self.state.robot_coordinates = (self.x, self.y, self.z)

            if self.grabbed_tile != None:
                self.grabbed_tile.x = self.x
                self.grabbed_tile.y = self.y
                self.grabbed_tile.z = self.z

        # Update step count
        self.steps += 1

        # Update state
        self.compute_state_noargs()

        reward = self.reward_inst.reward(action)
        done = self.reward_inst.done()
        truncated = self.reward_inst.truncated()
        return self.RL_state.copy(), reward, done, truncated, {}
    

    def learn(self, total_timesteps=1000, continue_learning=False):
        if continue_learning:
            self.model = RecurrentPPO.load("lstm_model", env=self)
        while True:
            self.model.learn(total_timesteps=total_timesteps)
            self.model.save("lstm_model")



class RLRobotPlay(RLRobotBase, gymnasium.Env):
    def __init__(self, config, state):
        self.config = config
        self.state = state
        self.switched_orientation = False # legacy flag
        self.grabbed_tile = [] # legacy variable
        gymnasium.Env.__init__(self)
        RLRobotBase.__init__(self, config, state)
        self.model = RecurrentPPO.load("lstm_model")
        self.RL_state = np.array([1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0], dtype=np.float32)

    def next_move(self, moves, occupied):
        self.compute_state(moves, occupied)
        action, _ = self.model.predict(self.RL_state)

        if action == 12:
            self.grabbed_tile = []
        if action == 13:
            self.grabbed_tile = None

        return self.translate_action(action)

