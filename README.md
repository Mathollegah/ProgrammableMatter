# Programmable Matter

## What is programmable matter?
Programmable matter, as it is used in this project, is a set of rhombic dodecahedrons (tiles) which are connected to a single component. On this component, there is a robot running over and through the tiles. The robot can pick up (at most) one tile at a time and place it to a new position. Thereby, the robot createds a new configuration. The robot might have a global view of the configuration, logarithmic memory in the number of tiles, or just constant memory. The idea of this project is to generate efficcient algorithms for creating specific configurations.

## What does this project do?
A simulation tool for exploring programmable matter systems.

This project generates random structures of rhombic dodecahedrons and simulates how a robot can perform tasks on these structures. It includes a graphical interface for visualization and experimentation.

---

## Which features are supported?

- Random generation of rhombic dodecahedron structures
- Simulation of robotic interaction with the structure
- Graphical visualization of the system
- Designed for experimentation and research
- Building AI agents for solving tasks on programmable matter

---

## Who could be interested in this project?

This project is intended for:

- Researchers in programmable matter  
- Developers interested in simulation systems  
- Contributors who want to explore or extend the project  

---

## How to install the project?

Clone the repository and set up a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip3 install -r requirements.txt