from src.model.gurobipyModel import DinnerWithFriendsSolver
import gurobipy as gp
from gurobipy import GRB

class MaximizeMeetsFactory():

    '''
    Maximizes the total number of meets among students
    '''

    def setObjectiveFunction(self,model: DinnerWithFriendsSolver) -> None:

        model.model.setObjective(gp.quicksum(model.meets[i, j] for (i, j) in model.Pairs), GRB.MAXIMIZE)

    def setAdditionalConstraints(self,model: DinnerWithFriendsSolver) -> None:
        
        pass