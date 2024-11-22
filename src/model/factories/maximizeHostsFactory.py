from src.model import DinnerWithFriendsSolver
import gurobipy as gp
from gurobipy import GRB

class MaximizeHostsFactory():

    '''
    Maximizes the number of students that host an event
    given a lower bound on the number of total meets: meetsValue
    and a bound on the number of students that the student that meets fewest students few: fewestMeetsValue
    '''

    def __init__(self,meetsValue,fewestMeetsValue) -> None:
        self.meetsValue = meetsValue
        self.fewestMeetsValue = fewestMeetsValue
        self.isHostOnce = None
                

    def setObjectiveFunction(self,model: DinnerWithFriendsSolver) -> None:

        self.isHostOnce = model.model.addVars((model.Kids), vtype=GRB.BINARY, name="meets")

        model.model.setObjective(gp.quicksum(self.isHostOnce[kid] for kid in model.Kids), GRB.MAXIMIZE)

    def setAdditionalConstraints(self,model: DinnerWithFriendsSolver) -> None:
        
        assert self.isHostOnce is not None, 'Make sure to set the objective function first'

        for kid in model.Kids:
            # ensure isHostOnce can only be one, if the kid actually hosts an event
            model.model.addConstr(gp.quicksum(self.isHostOnce[kid]) <= gp.quicksum(model.isHost[kid,e] for e in model.Events)) 
            # ensures the kid that meet fewest meets at least self.fewestMeetsValue 
            model.model.addConstr(gp.quicksum(model.meets[pair] for pair in model.Pairs if kid in pair) >= self.fewestMeetsValue)

        # ensure that the total number of meets is bound from below by self.meetsValue
        model.model.addConstr(gp.quicksum(model.meets[i, j] for (i, j) in model.Pairs) >= self.meetsValue)