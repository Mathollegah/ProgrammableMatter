# Game

## Purpose of this Module
The game module is the main part of the execution of the simulation. It makes sure that all moves that the robot does are executed correctly by updating the game state.

## How to use this Module
To create an object of this class the constructor is called with three arguments. The ```player``` is the robot which decides which moves are taken and on which the algorithm for reaching the goal runs. The ```config``` argument is a structure containing information on the the general sewtting. The ```state``` contains the actual state of the game, including the tiles and how they are placed.

When the module is created, the function ```moveRobot()``` has to be called. This functions executes a single move, by asking the robot for the next move and then performing the move according to the rules. Each robot has to contain a function ```next_move(moves, occupied)``` returning the next move to take.

## Specifics of the Robot
As mentioned before, the robot has to contain a function ```next_move(moves, occupied)``` which takes the directions in which a tile is adjacent (moves) and whether its own position is occupied, and returns a move. The moves that can be returned are:
'U', 'D', 'F', 'B', 'UBR', 'UBL', 'UFR', 'UFL', 'DBR', 'DBL', 'DFR', 'DFL', 'grab_tile', 'place_tile'.
Here U stands for up, D for down, F for front, B for back, L for left and R for right. When the move is illegal, e.g. the robot carries a tile and wants to pick up another one, then an error is thrown.

