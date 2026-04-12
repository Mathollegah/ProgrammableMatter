class RewardSimplePotential():
    def __init__(self, rl_inst, config, state):
        self.rl_inst = rl_inst
        self.config = config
        self.state = state

        self.x1 = self.state.potential.potential_x(self.rl_inst.grabbed_tile)
        self.z1 = self.state.potential.potential_z(self.rl_inst.grabbed_tile)
        self.x2 = self.x1
        self.z2 = self.z1

    def reward(self, action):
        self.x2 = self.x1
        self.z2 = self.z1
        self.x1 = self.state.potential.potential_x(self.rl_inst.grabbed_tile)
        self.z1 = self.state.potential.potential_z(self.rl_inst.grabbed_tile)
        reward = (self.x1-self.x2) + (self.z1-self.z2)-0.1
        return reward
    
    def done(self):
        return (self.x1 == 0 and self.z1 == 0)
    
    def truncated(self):
        moves = self.rl_inst.detect_neighbors()
        return self.rl_inst.steps >= self.rl_inst.max_steps or moves == []
    
    def predict(self):
        pass
