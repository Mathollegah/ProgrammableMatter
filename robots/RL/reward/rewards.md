# Reewards

This folder contains classes which are used to specify the reward the RL robot gets for a move. All reward classes have to have the following functions:

- ```reward(action)```: This function returns the actual reward of a move (action)
- ```done()```: This function returns whether the problem is solved
- ```truncated()```: This function returns if the problem is aborted, e.g. due to an illegal move
- ```predict()```: This function is called before the actual move of the robot is executed and allows to do some premove evaluation, e.g. let another robot predicat a move

## Which reward classes are currently implemented?
### RewardSimplePotential
This class rewards a reduction in the potential that the robot wants to optimize.

### RewardConstauto
This class rewards, when the same move is taken as the constrobot would take. Thus, the reward should initiate that the RL behaves like the Constrobot.