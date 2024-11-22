from src.model import DinnerWithFriendsSolver
import gurobipy as gp
from gurobipy import GRB

class MaximizeFewestMeetsFactory():

    '''
    Maximizes the number of students the student that meets fewest students meets
    given a lower bound on the number of total meets: meetsValue
    '''

    def __init__(self,meetsValue) -> None:
        self.Z = None
        self.meetsValue = meetsValue
                

    def setObjectiveFunction(self,model: DinnerWithFriendsSolver) -> None:

        self.Z = model.model.addVar(vtype=GRB.INTEGER, name="Z")

        model.model.setObjective(self.Z, GRB.MAXIMIZE)

    def setAdditionalConstraints(self,model: DinnerWithFriendsSolver) -> None:
        
        assert self.Z is not None, 'Make sure to set the objective function first'

        for kid in model.Kids:
            # ensure that Z is bounded by the meets the kid with fewest meets have
            model.model.addConstr(gp.quicksum(model.meets[pair] for pair in model.Pairs if kid in pair) >= self.Z)

        # ensure the bound from below on the total number of meets
        model.model.addConstr(gp.quicksum(model.meets[i, j] for (i, j) in model.Pairs) >= self.meetsValue)