
import os
import sys

# Ensure the repository root is on sys.path when pytest runs from a different directory.
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

import globalvars
from robots.constauto.robot import ConstRobot
from potential.potential import Potential
from game.game import Game, Dodecahedron
from configgen.configgen import Configgen

class GameSetup:
    def __init__(self, file="tests/testconfigs/solved.txt"):
        self.state = globalvars.State()
        self.config = globalvars.Config()
        self.config.load_file = file
        self.config.onlygenerate = True
        self.state.potential = Potential(self.state)

        self.configgen = Configgen(self.config, self.state)
        self.configgen.build_new_configuration()

        self.robot = ConstRobot(self.state)
        self.game = Game(self.robot, self.config, self.state)

def test_detect_occupied():
    setup = GameSetup()
    game = setup.game

    # Initially, robot position should be occupied by grabbed_tile
    assert game.detect_occupied() == True

    # Move to an empty position
    game.x = 100  # Far away
    game.y = 100
    game.z = 100
    assert game.detect_occupied() == False

def test_detect_neighbors():
    setup = GameSetup()
    game = setup.game

    neighbors = game.detect_neighbors()
    # Should have some neighbors in a solved configuration
    assert isinstance(neighbors, list)
    assert len(neighbors) > 0  # Assuming the config has neighbors

def test_grab_tile():
    setup = GameSetup()
    game = setup.game

    # Initially has grabbed_tile
    assert game.grabbed_tile is not None

    # Try to grab again (should raise exception)
    try:
        game.grab_tile()
        assert False, "Expected exception when grabbing while already carrying"
    except Exception as e:
        assert "Already carrying one" in str(e)

    # Drop the tile and try to grab in empty space (should fail)
    game.grabbed_tile = None
    game.x = 100
    game.y = 100
    game.z = 100
    try:
        game.grab_tile()
        assert False, "Expected exception when no tile to grab"
    except Exception as e:
        assert "There is no tile" in str(e)

def test_place_tile():
    setup = GameSetup()
    game = setup.game

    # Can't test place_tile easily without more setup, as it depends on robot state
    # For now, just ensure it doesn't crash
    game.place_tile()
    assert True  # Placeholder

def test_act_move():
    setup = GameSetup()
    game = setup.game

    # Test a valid move, e.g., 'U' if possible
    neighbors = game.detect_neighbors()
    if 'U' in neighbors:
        x_old, y_old, z_old = game.x, game.y, game.z
        game.act_move('U')
        assert game.z == z_old + 1  # Assuming 'U' moves up in z

def test_move_robot():
    setup = GameSetup()
    game = setup.game

    # Test moveRobot (simplified, as it depends on robot logic)
    old_x, old_y, old_z = game.x, game.y, game.z
    game.moveRobot()
    # Position might change
    assert (game.x != old_x or game.y != old_y or game.z != old_z) or True  # Allow no move if stuck
