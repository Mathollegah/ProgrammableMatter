# simple_ai_game.py
import numpy as np
import gymnasium
from gymnasium import spaces
#from stable_baselines3 import RecurrentPPO
from sb3_contrib import RecurrentPPO
from game.game import Game, Dodecahedron
from configgen.configgen import Configgen

# -----------------------------
# Step 1: Define the Game Env
# -----------------------------
class RLRobot(gymnasium.Env, Game, Configgen):
    def __init__(self, config, state, max_steps=10000):
        self.config = config
        self.state = state
        self.switched_orientation = False # legacy flag
        self.build_new_configuration()
        super().__init__(self, config, state)

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

        # Current vision of the robot
        self.RL_state = np.array([1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0], dtype=np.float32)
        moves = self.detect_neighbors()
        occupied = self.detect_occupied()
        self.compute_state(moves, occupied)

        self.model = RecurrentPPO("MlpLstmPolicy", self, verbose=1, n_steps=64, policy_kwargs=dict(lstm_hidden_size=64),)
        self.max_steps = max_steps
        self.steps = 0

    def reset(self, seed=None, options=None):
        self.build_new_configuration()
        super().__init__(self, self.config, self.state)
        self.RL_state = np.array([1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0], dtype=np.float32)
        moves = self.detect_neighbors()
        occupied = self.detect_occupied()
        self.compute_state(moves, occupied)
        self.steps = 0
        return self.RL_state.copy(), {}
    
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
        
    def compute_state(self, moves, occupied):
        self.RL_state[:12] = [1.0 if move in moves else 0.0 for move in ['U', 'D', 'F', 'B', 'UBR', 'UBL', 'UFR', 'UFL', 'DBR', 'DBL', 'DFR', 'DFL']]
        self.RL_state[12] = 1.0 if occupied else 0.0
        self.RL_state[13] = 1.0 if self.grabbed_tile is not None else 0.0
    
    # Similar to moveRobot in game.py but callable from training class
    def step(self, action):
        # Potential before move
        x1 = self.state.potential.potential_x(self.grabbed_tile)
        z1 = self.state.potential.potential_z(self.grabbed_tile)
        reward2 = 0

        # Get next move from robot
        next_move = self.translate_action(action)
        moves = self.detect_neighbors()
        occupied = self.detect_occupied()
        if (not next_move in ['grab_tile', 'place_tile']) or (next_move == 'grab_tile' and self.grabbed_tile is None and occupied) or (next_move == 'place_tile' and self.grabbed_tile is not None and not occupied):
            if self.grabbed_tile is None and occupied and "U" in next_move:
                reward2 += 1
            elif not self.grabbed_tile is None and occupied and "D" in next_move:
                reward2 += 1
            
            self.x_next, self.y_next, self.z_next = self.act_move(next_move)

            if next_move == 'grab_tile' and not self.grabbed_tile is None:
                reward2 += 2

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
        self.compute_state(moves, occupied)

        # Calculate reward and check if done
        x2 = self.state.potential.potential_x(self.grabbed_tile)
        z2 = self.state.potential.potential_z(self.grabbed_tile)

        reward = (x1-x2) + (z1-z2)-1 + reward2*0.5 # smaller distance higher reward
        done = (x2 == 0 and z2 == 0)
        truncated = self.steps >= self.max_steps
        return self.RL_state.copy(), reward, done, truncated, {}
    
    def learn(self, total_timesteps=1000):
        self.model.learn(total_timesteps=total_timesteps)
        self.model.save("lstm_model")

    def move(self):
        action, _ = self.model.predict(self.state)
        self.state, reward, done, _ = self.step(action)

