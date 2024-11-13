import math
import gurobipy as gp
import numpy as np
import pandas as pd
from gurobipyModel import DinnerWithFriendsSolver
from gurobipy import GRB
import time
from typing import List
   


class branchingInformation_MeetsAtEInG_percentage:

    def __init__(self,percentage) -> None:
        
        self.percentage = percentage
        self._ks = None

    def getBranchPriority(self,model: DinnerWithFriendsSolver) -> List:

        self._ks = [int(len(model.meets)*self.percentage)]

        return [model.meets]

    def getks(self) -> List[int]:

        if self._ks is None:
            raise ValueError('Make sure to run getBranchPriority first to initialize the k')

        return self._ks

class localBranching:

    def __init__(self,model: DinnerWithFriendsSolver,branchingInformer: branchingInformation_MeetsAtEInG_percentage) -> None:
        self.model = model
        self.localBranchingConstraintName = 'LocalBranch'
        self.bestSolution = sum([v.Start for v in self.model.meets.values()]) # obtain the initial solution from the self.meets variable
        self.iterationsSinceImprovement = 0
        self.bestSolution_callBack = 0
        self.branchPriority = branchingInformer.getBranchPriority(self.model)
        self.ks = branchingInformer.getks()
        self.branchingVariable = self.branchPriority.pop()
        self.k = self.ks.pop()
        self.bound = self.optimize_groups(model.numKids,model.maxNumGuests,model.minNumGuests,model.numOfEvents)
    

    def optimize_groups(self,N, u, l,e):

        c_u = sum([i for i in range(u)])
        c_l = sum([i for i in range(l)])
        max_objective = None

        max_g_u = N // u  # Start with maximum feasible g_u

        for g_u in range(max_g_u, -1, -1):  # Iterate from max_g_u down to 0
            if (N - g_u * u) % l == 0:
                g_l = (N - g_u * u) // l
                if g_l >= 0:
                    objective_value = c_u * g_u + c_l * g_l
                    if max_objective is None or objective_value > max_objective:
                        max_objective = objective_value

        return max_objective * e
        
    def performLocalBranching(self,timeLimit):
        start = time.time()
        objValues = [self.bestSolution]
        runTimes = [start]

        def callback(model,where):

            if where == GRB.Callback.MIPSOL:

                currentValue = model.cbGet(GRB.Callback.MIPSOL_OBJ)

                if currentValue > self.bestSolution:

                    runTime = time.time()
                    objValues.append(currentValue)
                    runTimes.append(runTime)

                if currentValue > self.bestSolution:
                    model.terminate()

        self.model.model.setParam("TimeLimit", timeLimit)
        self.model.model.setParam("DegenMoves", 1)

        while True:
            self.model.model.optimize(callback)
            if self.model.model.ObjVal > self.bestSolution:
                self.bestSolution = self.model.model.ObjVal                
            
            timeSpent = time.time() - start
            if timeSpent >= timeLimit:
                break

            # handle if optimal solution is found, one need to check if also optimal to the full problem
            if self.model.model.ObjBound == self.model.model.ObjVal:
                self.removeLocalBranchConstraint()
                self.model.model.setParam("TimeLimit", 1)
                self.model.model.optimize()
                if self.model.model.Status == GRB.status.OPTIMAL:
                    break

            newTime = timeLimit-timeSpent
            self.model.model.setParam("TimeLimit", newTime)
            self.addLocalBranchingConstraint()

        objValues.append(self.bestSolution)
        runTimes.append(time.time())
        runTimes = np.array(runTimes) - start 

        performance = pd.DataFrame({
            'runTime': runTimes,      
            'Value':  objValues,
            'bound': self.bound        
            },index= ['Heuristic'] * len(runTimes))    
         
        return performance
    
    def removeLocalBranchConstraint(self):

        oldLocalBranchConstraint = self.model.model.getConstrByName(self.localBranchingConstraintName)
        if oldLocalBranchConstraint is not None:
            self.model.model.remove(oldLocalBranchConstraint)

    def addLocalBranchingConstraint(self):
        
        self.removeLocalBranchConstraint()

        lhs = gp.LinExpr()
        for v in self.branchingVariable.values():
            try: 
                val = v.X
            except AttributeError:
                val = v.Start
            if val < 0.5:  # Binary variable is 0 in initial solution
                lhs.addTerms(1, v)
            else:  # Binary variable is 1 in initial solution
                lhs.addConstant(1)
                lhs.addTerms(-1, v)
        
        self.model.model.addConstr(lhs <= self.k, name=self.localBranchingConstraintName)
        self.model.model.update()

if __name__ == '__main__':

    timeLimit = 3600

    l = 4
    u = 5
    n_events = 6

    for i in [21,22,23,24,25,26,27,28]:
        try:
            n_girls = i // 2
            n_boys = i-n_girls



            data = {   "n_girls": n_girls,
            "n_boys": n_boys,
            "numOfEvents": n_events,
            "minNumGuests": l,
            "maxNumGuests": u
            }

            dwf = DinnerWithFriendsSolver()
            dwf.readData(data)
            dwf.setFeasibleSolution()

            N = n_girls+n_boys

            branchingInformer = branchingInformation_MeetsAtEInG_percentage(0.15)

            localBrancher = localBranching(dwf,branchingInformer)
            performance = localBrancher.performLocalBranching(timeLimit)

            performance.to_csv(f'results/properResults/15PercentageK_Meets/HeuristicSolution_size{i}.csv')
        except Exception as e:
            print(f'{i} failed with error {e}')