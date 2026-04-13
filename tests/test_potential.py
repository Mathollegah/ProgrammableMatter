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

class LoadConfig:
    def __init__(self,max_steps=100000, file="tests/testconfigs/solved.txt"):
        self.state = globalvars.State()
        self.config = globalvars.Config()
        self.config.load_file = file
        self.state.potential = Potential(self.state)

        self.configgen = Configgen(self.config, self.state)
        self.configgen.build_new_configuration()

def test_tiles_without_potential_are_not_considered():
    inst = LoadConfig()
    potential = inst.state.potential

    continue_loop = True
    while continue_loop:
        continue_loop = False
        assert potential.potential_x(None) == 0
        assert potential.potential_z(None) == 0

        for i, tile in enumerate(inst.state.dodecahedrons):
            if tile.top == None and tile.front == None:
                tile.delete_neighbor_links()
                inst.state.dodecahedrons.pop(i)
                continue_loop = True
                break


def test_potential_calculation():
    inst = LoadConfig()
    potential = inst.state.potential

    assert potential.potential_x(None) == 0
    assert potential.potential_z(None) == 0

    for tile in inst.state.dodecahedrons:
        top = False
        front = False
        if tile.top != None: top = True
        if tile.front != None: front = True

        tile.delete_neighbor_links()

        pot_x = potential.potential_x(tile)
        pot_z = potential.potential_z(tile)

        if top: assert pot_x != 0
        if not top: assert pot_x == 0
        if front: assert pot_z != 0
        if not front: assert pot_z == 0

        tile.find_neighbours(inst.state.dodecahedrons)

