# Potentials

## Purpose of this Module
The potentials are used how close a configuration is to the desires shape. The current potentials make sure - when reaching zero - that all tiles build towers which are as close as possible to the bounding box as possible. This makes sure that the structure is hole-free, which makes it easier to build new structures from that. Also other potentials are possible and might be implemented later on.

The potenials might also be used for reinforcement learning or other learning techniques for agents. Thus, the potentials might be used as reward.

## How to use this Module
The constructor is called with the ```state``` struct, which contains the information on the tiles and how they are placed. The currently used potentials are ```potential_x(tile)``` and ```potential_x(tile)```, which take the tile carried by the root (or None) as argument, since this tile is not part of the potential evaluation.