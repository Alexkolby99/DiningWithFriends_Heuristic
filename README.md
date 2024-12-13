# DiningWithFriends_Heuristic
 This repository containing implementation of a heuristic solution methods for a group formation problem, named "dinning with friends" arising in danish public schools for bullying prevention. The repository contain two main implementations

 - Construction heuristic: A way to find a feasible but poor solution to the problem

 - Local branching heuristic: An improvement heuristic based on the local branching algorithm

 # Structure

 - **results**: Folder containing results generated for different instances
 - **src**: The source code of the project
    - **constructionMoves**: Moves that is used to repair groups in the construction heuristic
    - **interfaces**: Base classes 
    - **localBranching**: Contains all code related to the local branching algorithm
    - **model**: Gurobipy implementations of the linear integer program
    - **CascadeGrouping.py**: The construction heuristic
    - **event.py**: Helper class for the construction heuristic
    - **group.py**: Helper class for the construction heuristic
    - **student.py**: Helper class for the construction heuristic
 - **test**: Unit tests of some important central classes
 - **main_constructionHeuristic.py**: Used to find a feasible solution
 - **main_LocalBranching.py**: Used to run the local branching heuristic
 - **requirements.txt**: dependencies