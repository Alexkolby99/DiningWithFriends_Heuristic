from src.localBranching._interfaces import Brancher_base
from gurobipy import GRB, Model, Var
from gurobipyModel import DinnerWithFriendsSolver
from src.localBranching.branchingStrategies.utils import LocalBranchConstraintHandler
from src.localBranching.branchingStrategies._interfaces import KStrategy_base


class SingleVariableBranching(Brancher_base):


    def __init__(self,model:DinnerWithFriendsSolver,variable: Var,kStrategy: KStrategy_base) -> None:
        self.branchingVariable = variable
        self.constraintHandler = LocalBranchConstraintHandler()
        self.model = model
        self.model.model.setParam("DegenMoves", 1)
        self.kStrategy = kStrategy
        self._initObjectiveValue = sum([v.Start for v in self.model.meets.values()])


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

            if  objective > bestObjective:
                self.constraintHandler.removeLocalBranchingConstraint(self.model.model)
                self.constraintHandler.addLocalBranchingConstraint(self.model.model,
                                                                self.branchingVariable,
                                                                self.kStrategy.getK(self.branchingVariable))
                self.model.model.update()

        self.model.model.setParam('timeLimit',timeLeft)

        return self.model.model

