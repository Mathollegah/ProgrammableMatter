import os
import sys

# Ensure the repository root is on sys.path when pytest runs from a different directory.
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

import globalvars
from robots.constauto.robot import ConstRobot
from potential.potential import Potential
from game.game import Game
from configgen.configgen import Configgen


class SolveConfig:
    def __init__(self,max_steps=100000, file="tests/testconfigs/hole.txt"):
        self.state = globalvars.State()
        self.config = globalvars.Config()
        self.config.load_file = file
        self.config.trainmodel = True
        self.state.potential = Potential(self.state)

        self.configgen = Configgen(self.config, self.state)
        self.configgen.build_new_configuration()
        self.game = Game(ConstRobot(self.state), self.config, self.state)
        self.max_steps = max_steps
        self.steps = 0

    def test_with_fixture(self):
        for i in range(self.max_steps):
            self.steps = i+1
            self.game.moveRobot()

            if self.game.state.potential.potential_x(self.game.grabbed_tile) == 0 and self.game.state.potential.potential_z(self.game.grabbed_tile) == 0:
                break

def test_config_with_hole():
    inst = SolveConfig(file="tests/testconfigs/hole.txt")
    inst.test_with_fixture()

    assert inst.steps < inst.max_steps
    assert inst.game.state.potential.potential_x(inst.game.grabbed_tile) == 0
    assert inst.game.state.potential.potential_z(inst.game.grabbed_tile) == 0

def test_shifting_complete_row():
    inst = SolveConfig(file="tests/testconfigs/simpleshift.txt")
    inst.test_with_fixture()

    assert inst.steps < inst.max_steps
    assert inst.game.state.potential.potential_x(inst.game.grabbed_tile) == 0
    assert inst.game.state.potential.potential_z(inst.game.grabbed_tile) == 0

def test_shifting_complete_row_in_2D():
    inst = SolveConfig(file="tests/testconfigs/simpleshift2.txt")
    inst.test_with_fixture()

    assert inst.steps < inst.max_steps
    assert inst.game.state.potential.potential_x(inst.game.grabbed_tile) == 0
    assert inst.game.state.potential.potential_z(inst.game.grabbed_tile) == 0
