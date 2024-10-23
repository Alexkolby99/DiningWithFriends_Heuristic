import gurobipy as gp
from gurobipyModel import DinnerWithFriendsSolver
class fixedK:

    def __init__(self,k) -> None:
        self.k = k

    def getK(self):

        return self.k


class localBranching:

    def __init__(self,kStrategy: fixedK,model: gp.Model) -> None:
        self.kStrategy = kStrategy
        self.model = model
        self.localBranchingConstraintName = 'LocalBranch'
        self.bestSolution = 0
        self.iterationsSinceImprovement = 0
        
    
    def performLocalBranching(self,timeLimitPerBranch,maxIters):
        self.model.setParam("TimeLimit", timeLimitPerBranch*2)
        for i in range(maxIters):
            self.model.optimize()
            if self.model.ObjVal > self.bestSolution:
                self.bestSolution = self.model.ObjVal
                self.kStrategy.K = 150
                self.model.setParam("TimeLimit", timeLimitPerBranch)
                self.iterationsSinceImprovement = 0
            else:
                self.kStrategy.k = self.kStrategy.k + 50
                self.model.setParam("TimeLimit", self.model.getParamInfo('TimeLimit')[2]*2)
                self.iterationsSinceImprovement += 1

            if self.iterationsSinceImprovement > 5:
                return self.bestSolution
            
            self.addLocalBranchingConstraint()

    def addLocalBranchingConstraint(self):
        k = self.kStrategy.getK()
        
        oldLocalBranchConstraint = self.model.getConstrByName(self.localBranchingConstraintName)
        if oldLocalBranchConstraint is not None:
            self.model.remove(oldLocalBranchConstraint)
            
        lhs = gp.LinExpr()
        for v in self.model.getVars():
            v.Start = v.X
            if v.X < 0.5:  # Binary variable is 0 in initial solution
                lhs.addTerms(1, v)
            else:  # Binary variable is 1 in initial solution
                lhs.addConstant(1)
                lhs.addTerms(-1, v)
        
        self.model.addConstr(lhs <= k, name=self.localBranchingConstraintName)
        self.model.update()

if __name__ == '__main__':

    maxIters = 20
    timeLimitPerBranch = 30

    dwf = DinnerWithFriendsSolver()
    dwf.readData('exampleData.json')
    dwf.setFeasibleSolution()
    model = dwf.model

    localBrancher = localBranching(fixedK(150),model)
    localBrancher.performLocalBranching(timeLimitPerBranch,maxIters)