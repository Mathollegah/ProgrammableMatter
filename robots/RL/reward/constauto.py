from robots.constauto.robot import ConstRobot

class RewardConstauto():
    def __init__(self, rl_inst, config, state):
        self.rl_inst = rl_inst
        self.config = config
        self.state = state

        self.robot = ConstRobot(state)
        self.prediction = ""


    def reward(self, action):
        move = self.rl_inst.translate_action(action)

        if self.prediction == move:
            reward = 1.0
        else:
            reward = -1.0
        return reward
    
    def done(self):
        x1 = self.state.potential.potential_x(self.rl_inst.grabbed_tile)
        z1 = self.state.potential.potential_z(self.rl_inst.grabbed_tile)
        return (x1 == 0 and z1 == 0)
    
    def truncated(self):
        moves = self.rl_inst.detect_neighbors()
        return self.rl_inst.steps >= self.rl_inst.max_steps or moves == []
    
    def predict(self):
        self.prediction = self.robot.next_move(self.rl_inst.detect_neighbors(), self.rl_inst.detect_occupied())
