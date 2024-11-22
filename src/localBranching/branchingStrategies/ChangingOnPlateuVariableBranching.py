from typing import List,Literal
from src.localBranching._interfaces import Brancher_base
from gurobipy import GRB, Model
from src.model.gurobipyModel import DinnerWithFriendsSolver
from src.localBranching.branchingStrategies.utils import LocalBranchConstraintHandler
from src.localBranching.branchingStrategies._interfaces import KStrategy_base

VARIABLES = Literal['meets','meetsAtE','meetsAtEInG']

class ChangingOnPlateuVariableBranching(Brancher_base):

    def __init__(self,model:DinnerWithFriendsSolver,variable: List[VARIABLES] | VARIABLES ,kStrategy: KStrategy_base | List[KStrategy_base],maxTimePerVariable: float = 300) -> None:       

        self.branchingVariables = [variable] if not isinstance(variable,list) else variable
        self.kStrategies = [kStrategy] if not isinstance(kStrategy,list) else kStrategy

        assert len(self.kStrategies) == len(self.branchingVariables), 'Ensure the number of k strategies is equal to the number of variables'
        assert len(self.kStrategies) > 0 and len(self.branchingVariables) > 0, 'Empty variable or kstrategy is given'

        self.branchingVariable = self.branchingVariables.pop()
        self.constraintHandler = LocalBranchConstraintHandler()
        self.dwfmodel = model

        self.model = model.model
        self.kStrategy = self.kStrategies.pop()
        self._initObjectiveValue = sum([v.Start for v in model.meets.values()])
        self.timeLimit = 10**16 if len(self.branchingVariables) == 0 else maxTimePerVariable


    @property
    def initObjectiveValue(self) -> float:
        return self._initObjectiveValue

    def nextBranch(self,objective: float,bestObjective: float, timeLeft: float) -> Model:


        # handle if optimal solution is found, one need to check if also optimal to the full problem
        if objective is not None:
            if self.model.ObjBound == self.model.ObjVal:
                self.constraintHandler.removeLocalBranchingConstraint(self.model)
                self.model.setParam("TimeLimit", 1)
                self.model.optimize()
                if self.model.Status == GRB.status.OPTIMAL:
                    return None

            if not objective > bestObjective:
                self.branchingVariable = self.branchingVariables.pop()   
                self.kStrategy = self.kStrategies.pop()
                if len(self.branchingVariables) == 0:
                    self.timeLimit = 10**16             

            self.constraintHandler.removeLocalBranchingConstraint(self.model)
            self.constraintHandler.addLocalBranchingConstraint(self.model,
                                                            self.branchingVariable,
                                                            self.kStrategy.getK(getattr(self.dwfmodel,self.branchingVariable),objective))
            
            self.model.update()

        self.model.setParam('timeLimit',min(self.timeLimit,timeLeft))
        

        return self.model

