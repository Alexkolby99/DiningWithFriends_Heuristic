from gurobipy import Model, LinExpr, Var


class LocalBranchConstraintHandler:

    def __init__(self) -> None:
        self.localBranchingConstraintName = 'localBranch'

    def removeLocalBranchingConstraint(self,model: Model) -> None:

        oldLocalBranchConstraint = model.getConstrByName(self.localBranchingConstraintName)
        if oldLocalBranchConstraint is not None:
            model.remove(oldLocalBranchConstraint)
    
    def addLocalBranchingConstraint(self,model: Model,variable: Var,k):

        lhs = LinExpr()
        for v in variable.values():
            try: 
                val = v.X
            except AttributeError:
                val = v.Start
            if val < 0.5:  # Binary variable is 0 in initial solution
                lhs.addTerms(1, v)
            else:  # Binary variable is 1 in initial solution
                lhs.addConstant(1)
                lhs.addTerms(-1, v)
        
        model.addConstr(lhs <= k, name=self.localBranchingConstraintName)