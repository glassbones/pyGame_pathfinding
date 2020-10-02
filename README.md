# pyGame_pathfinding

**Goal:** Create an app that visits every vertex of a graph with as few movements and as possible.

![pyGame_demo](demo/bpy_anim.gif)

**How it works:** The program loads the maze and itterates over vertices detecting dead ends and connecting paths leading to them to identify branches it will need to travel. All cells left are part of a circuit that it must complete to visit every part of the maze. (depending on the maze that circuit may be multiple circuits connected by 'bridges'. After the maze is processed it itterates around the circuit using the A star algorithmn and stopping at any vertex that leads to a branch of dead ends.

**Complete:** 
App functionality!
Maze completion.
A Star searching.
Dead end detection.
Loop detection. 

**TODO:** 
Add depth first and breadth first searching.
Add GUI.
Add maze upload and save.

**Comments:**
This project led to a whole rabbit whole of problem solving and research. I'm a very visual learner so I decided to use the pyGame library to render the maze and the algorithms used to solve it. 
