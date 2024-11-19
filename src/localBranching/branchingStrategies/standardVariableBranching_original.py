from typing import List
from src.localBranching._interfaces import Brancher_base
from gurobipy import GRB, Model, Var
from gurobipyModel import DinnerWithFriendsSolver
from src.localBranching.branchingStrategies.utils import LocalBranchConstraintHandler
from src.localBranching.branchingStrategies._interfaces import KStrategy_base


class StandardVariableBranching(Brancher_base):


    def __init__(self,model:DinnerWithFriendsSolver,variable: Var | List[Var],kStrategy: KStrategy_base | List[KStrategy_base],maxTimePerVariable: float = 300) -> None:
        self.branchingVariable = [variable] if not isinstance(variable,list) else variable
        self.constraintHandler = LocalBranchConstraintHandler()
        self.model = model
        self.model.model.setParam("DegenMoves", 1)
        self.kStrategy = [kStrategy] if not isinstance(kStrategy,list) else kStrategy
        self._initObjectiveValue = sum([v.Start for v in self.model.meets.values()])

        self.iter = 0
        self.n_variables = len(self.branchingVariable)
        self.maxTimePerVariable = 10**16 if self.n_variables == 1 else maxTimePerVariable
        self.iterationsSinceImprovement = 0


    @property
    def initObjectiveValue(self) -> float:
        return self._initObjectiveValue

    def nextBranch(self,objective: float,bestObjective: float, timeLeft: float) -> Model:
        timelimit = self.maxTimePerVariable
        if objective is not None:
            if not objective > bestObjective:
                self.iterationsSinceImprovement += 1
            else:
                self.iterationsSinceImprovement = 0
                timelimit = self.maxTimePerVariable

            if self.iterationsSinceImprovement >= 3:
                timelimit = 10**16

        # handle if optimal solution is found, one need to check if also optimal to the full problem
        if objective is not None:
            if self.model.model.ObjBound == self.model.model.ObjVal:
                self.constraintHandler.removeLocalBranchingConstraint(self.model.model)
                self.model.model.setParam("TimeLimit", 1)
                self.model.model.optimize()
                if self.model.model.Status == GRB.status.OPTIMAL:
                    return None

            branchingVariable = self.branchingVariable[self.iter % self.n_variables]
            kStrategy = self.kStrategy[self.iter % self.n_variables]
            
            self.constraintHandler.removeLocalBranchingConstraint(self.model.model)
            self.constraintHandler.addLocalBranchingConstraint(self.model.model,
                                                            branchingVariable,
                                                            kStrategy.getK(branchingVariable))
            self.model.model.update()
            
            self.iter += 1

        self.model.model.setParam('timeLimit',min(timelimit,timeLeft))

        return self.model.model

