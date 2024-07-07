import globalvars
import random


class ConstRobot():
    def __init__(self):
        self.state = 'random_move'
        self.carrying_tile = True

    def next_move(self, neighbors):
        if self.state == 'random_move':
            #return random.choice(neighbors)

            if 'U' in neighbors:
                return 'U'
            elif 'F' in neighbors:
                return 'F'
            else:
                return ''

