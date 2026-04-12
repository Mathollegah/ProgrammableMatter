# Visualization

## Purpose of this Module
The visualization module is used to create a 3D simulation of a configuration. Further, the simulation can be influenced by pressing keys like:

- s: to stop
- b: to hide or show the bounding box
- o: to make the simulation faster
- l: to make the simulation slower
- p: to hide all tiles with potential higher than zero

## How to use this Module
A object of the class is initialized with the player, the configuratioin and the state - like a game instance. To start the simulation the ```main()``` function of the object is called. This function runs a endless loop and continues the simulation until it is terminated by the user.
