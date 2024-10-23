from ortools.sat.python import cp_model
from exactImplementation import DinnerWithFriendsSolver
class fixedK:

    def __init__(self,k) -> None:
        self.k = k

    def getK(self):

        return self.k


class localBranching:

    def __init__(self,kStrategy: fixedK,model: cp_model.CpModel) -> None:
        self.kStrategy = kStrategy
        self.model = model
        self.localBranchingConstraintName = 'LocalBranch'
        self.bestSolution = 0
        self.solver = cp_model.CpSolver()
        
    
    def performLocalBranching(self,timeLimitPerBranch,maxIters):
        self.model.setParam("TimeLimit", timeLimitPerBranch*2)
        for i in range(maxIters):
            self.model.optimize()
            if self.model.ObjVal > self.bestSolution:
                self.bestSolution = self.model.ObjVal
                self.kStrategy.K = 150
                self.model.setParam("TimeLimit", timeLimitPerBranch)
            else:
                self.kStrategy.k = self.kStrategy.k + 50
                self.model.setParam("TimeLimit", self.model.getParamInfo('TimeLimit')[2]*2)
            model = self.addLocalBranchingConstraint()

    def addLocalBranchingConstraint(self):
        k = self.kStrategy.getK()
        model = self.model.copy()

        # Iterate over all binary variables to construct the expression
        for v in model:
            initial_solution_value = self.solver.Value(v)  # Get the solution value for the variable
            if initial_solution_value < 0.5:  # Binary variable is 0 in initial solution
                lhs += v  # Add the variable (since it contributes positively)
            else:  # Binary variable is 1 in initial solution
                lhs += 1 - v  # Add constant 1 and subtract the variable
            
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