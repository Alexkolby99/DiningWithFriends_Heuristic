from typing import List
from src.localBranching._interfaces import Brancher_base
from gurobipy import GRB, Model, Var
from gurobipyModel import DinnerWithFriendsSolver
from src.localBranching.branchingStrategies.utils import LocalBranchConstraintHandler
from src.localBranching.branchingStrategies._interfaces import KStrategy_base


class StandardVariableBranching(Brancher_base):


    def __init__(self,model:DinnerWithFriendsSolver,variable: Var | List[Var],kStrategy: KStrategy_base,maxTimePerVariable: float = 300) -> None:
        self.branchingVariable = [variable] if not isinstance(variable,list) else variable
        self.constraintHandler = LocalBranchConstraintHandler()
        self.model = model
        self.model.model.setParam("DegenMoves", 1)
        self.kStrategy = kStrategy
        self._initObjectiveValue = sum([v.Start for v in self.model.meets.values()])

        self.iter = 0
        self.n_variables = len(self.branchingVariable)
        self.maxTimePerVariable = 10**16 if self.n_variables == 1 else maxTimePerVariable


    @property
    def initObjectiveValue(self) -> float:
        return self._initObjectiveValue

    def nextBranch(self,objective: float,bestObjective: float, timeLeft: float) -> Model:
        
        # handle if optimal solution is found, one need to check if also optimal to the full problem
        if objective is not None:
            if self.model.model.ObjBound == self.model.model.ObjVal:
                self.constraintHandler.removeLocalBranchingConstraint(self.model.model)
                self.model.model.setParam("TimeLimit", 1)
                self.model.model.optimize()
                if self.model.model.Status == GRB.status.OPTIMAL:
                    return None

            branchingVariable = self.branchingVariable[self.iter % self.n_variables]
            if  objective > bestObjective:
                self.constraintHandler.removeLocalBranchingConstraint(self.model.model)
                self.constraintHandler.addLocalBranchingConstraint(self.model.model,
                                                                branchingVariable,
                                                                self.kStrategy.getK(branchingVariable))
                self.model.model.update()
            
            self.iter += 1

        self.model.model.setParam('timeLimit',min(self.maxTimePerVariable,timeLeft))

        return self.model.model

