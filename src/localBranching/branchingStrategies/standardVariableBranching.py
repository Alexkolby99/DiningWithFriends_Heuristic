from typing import List,Literal
from src.localBranching._interfaces import Brancher_base
from gurobipy import GRB, Model, Var
from src.model.gurobipyModel import DinnerWithFriendsSolver
from src.localBranching.branchingStrategies.utils import LocalBranchConstraintHandler
from src.localBranching.branchingStrategies._interfaces import KStrategy_base
from copy import copy

VARIABLES = Literal['meets','meetsAtE','meetsAtEInG']



class StandardVariableBranching(Brancher_base):

    def __init__(self,model:DinnerWithFriendsSolver,
                 variable: List[VARIABLES] | VARIABLES ,
                 kStrategy: KStrategy_base | List[KStrategy_base],
                 initialMaxTimePerVariable: float = 30,
                 maxTimePerVariable: float = 120,
                 changing: bool = False,
                 restarting: bool = False) -> None:
        
        self.restarting = restarting
        self.changing = changing
        self.indices = 0
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
        self.initialMaxTimePerVariable = maxTimePerVariable if self.n_variables == 1 else initialMaxTimePerVariable
        self.iterationsSinceImprovement = 0
        self.maxTimePerVariable = maxTimePerVariable


    @property
    def initObjectiveValue(self) -> float:
        return self._initObjectiveValue


    def selectIndices(self,objective,bestObjective):
        ## this is for a single variable with multiple k's
        if self.restarting:
            if objective > bestObjective:
                return 0
            else:
                return (self.indices + 1) % self.n_variables
        
        if not self.changing:
            return self.iter % self.n_variables
        
        if not objective > bestObjective:
            return (self.indices + 1) % self.n_variables

        return self.indices


    def nextBranch(self,objective: float,bestObjective: float, timeLeft: float) -> Model:

        timeLimit = self.initialMaxTimePerVariable

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

            else:
                self.iterationsSinceImprovement = 0#max(0,self.iterationsSinceImprovement-(self.n_variables-1))
                for idx,model in enumerate(self.models):
                    if idx != self.indices:
                        for var in model.getVars():
                            var.start = self.model.getVarByName(var.VarName).X

                        model.update()
                
            if self.iterationsSinceImprovement >= self.n_variables:
                timeLimit = self.maxTimePerVariable

            self.indices = self.selectIndices(objective,bestObjective)

            self.model = self.models[self.indices]
            branchingVariable = self.branchingVariable[self.indices]
            print(branchingVariable)
            self.kStrategy = self.kStrategies[self.indices]
                
            if self.iterationsSinceImprovement < self.n_variables:
                self.constraintHandler.removeLocalBranchingConstraint(self.model)
                self.constraintHandler.addLocalBranchingConstraint(self.model,
                                                                branchingVariable,
                                                                self.kStrategy.getK(getattr(self.dwfmodel,branchingVariable),objective))
                self.model.update()
                
            self.iter += 1

        self.model.setParam('timeLimit',min(timeLimit,timeLeft))
        

        return self.model

