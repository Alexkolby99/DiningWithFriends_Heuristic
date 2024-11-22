from typing import List,Literal
from src.localBranching._interfaces import Brancher_base
from gurobipy import GRB, Model, Var
from src.model.gurobipyModel import DinnerWithFriendsSolver
from src.localBranching.branchingStrategies.utils import LocalBranchConstraintHandler
from src.localBranching.branchingStrategies._interfaces import KStrategy_base
from copy import copy

VARIABLES = Literal['meets','meetsAtE','meetsAtEInG']



class StandardVariableBranching(Brancher_base):

    def __init__(self,model:DinnerWithFriendsSolver,variable: List[VARIABLES] | VARIABLES ,kStrategy: KStrategy_base | List[KStrategy_base],maxTimePerVariable: float = 60) -> None:
        
        self.branchingVariable = [variable] if not isinstance(variable,list) else variable
        self.kStrategies = [kStrategy] if not isinstance(kStrategy,list) else kStrategy

        assert len(self.kStrategies) == len(self.branchingVariable), 'Ensure the number of k strategies is equal to the number of variables'
        assert len(self.kStrategies) > 0 and len(self.branchingVariable) > 0, 'Empty variable or kstrategy is given'

        self.constraintHandler = LocalBranchConstraintHandler()
        self.dwfmodel = model
        model.model.setParam("DegenMoves", 1)
        self.models = [model.model.copy() for _ in self.branchingVariable]
        for _model in self.models:
            for var in _model.getVars():
                var.Start = model.model.getVarByName(var.VarName).Start

            _model.update()

        self.model = self.models[0]
        self._initObjectiveValue = sum([v.Start for v in model.meets.values()])

        self.iter = 0
        self.n_variables = len(self.branchingVariable)
        self.maxTimePerVariable = 10**16 if self.n_variables == 1 else maxTimePerVariable
        self.iterationsSinceImprovement = 0


    @property
    def initObjectiveValue(self) -> float:
        return self._initObjectiveValue

    def nextBranch(self,objective: float,bestObjective: float, timeLeft: float) -> Model:

        timeLimit = self.maxTimePerVariable

        # handle if optimal solution is found, one need to check if also optimal to the full problem
        if objective is not None:
            if self.model.ObjBound == self.model.ObjVal:
                self.constraintHandler.removeLocalBranchingConstraint(self.model)
                self.model.setParam("TimeLimit", 1)
                self.model.optimize()
                if self.model.Status == GRB.status.OPTIMAL:
                    return None

            if not objective > bestObjective:
                self.iterationsSinceImprovement += 1
                self.kStrategy.percentage = self.kStrategy.percentage * 2

            else:
                self.iterationsSinceImprovement = 0
                for idx,model in enumerate(self.models):
                    if idx != max(0,(self.iter - 1)) % self.n_variables:
                        for var in model.getVars():
                            var.start = self.model.getVarByName(var.VarName).X

                        model.update()
                
            if self.iterationsSinceImprovement >= self.n_variables:
                timeLimit = 10**16

            self.model = self.models[self.iter % self.n_variables]
            branchingVariable = self.branchingVariable[self.iter % self.n_variables]
            print(branchingVariable)
            self.kStrategy = self.kStrategies[self.iter % self.n_variables]
            
            if self.iterationsSinceImprovement < self.n_variables:
                self.constraintHandler.removeLocalBranchingConstraint(self.model)
                self.constraintHandler.addLocalBranchingConstraint(self.model,
                                                                branchingVariable,
                                                                self.kStrategy.getK(getattr(self.dwfmodel,branchingVariable),objective))
                self.model.update()
            
            self.iter += 1

        self.model.setParam('timeLimit',min(timeLimit,timeLeft))
        

        return self.model

