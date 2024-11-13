import math
import gurobipy as gp
import numpy as np
import pandas as pd
from gurobipyModel import DinnerWithFriendsSolver
from gurobipy import GRB
import time
from typing import List
   


class branchingInformation_MeetsAtEInG_fixedk:

    def __init__(self,k) -> None:
        self.k = k

    def getBranchPriority(self,model: DinnerWithFriendsSolver) -> List:
        
        return [model.meetsAtEInG]

    def getks(self) -> List[int]:

        return [self.k]


class branchingInformation_MeetsAtEInG_percentage:

    def __init__(self,percentage) -> None:
        
        self.percentage = percentage
        self._ks = None

    def getBranchPriority(self,model: DinnerWithFriendsSolver) -> List:

        self._ks = [int(len(model.meetsAtEInG)*self.percentage)]

        return [model.meetsAtEInG]

    def getks(self) -> List[int]:

        if self._ks is None:
            raise ValueError('Make sure to run getBranchPriority first to initialize the k')

        return self._ks

class localBranching:

    def __init__(self,model: DinnerWithFriendsSolver,branchingInformer: branchingInformation_MeetsAtEInG_fixedk) -> None:
        self.model = model
        self.localBranchingConstraintName = 'LocalBranch'
        self.bestSolution = sum([v.Start for v in self.model.meets.values()]) # obtain the initial solution from the self.meets variable
        self.iterationsSinceImprovement = 0
        self.bestSolution_callBack = 0
        self.timeSpentInBranch = 0
        self.intervalTimeInBranch = 60
        self.branchPriority = branchingInformer.getBranchPriority(self.model)
        self.ks = branchingInformer.getks()
        self.branchingVariable = self.branchPriority.pop()
        self.k = self.ks.pop()
        
    
    def performLocalBranching(self,timeLimitPerBranch,maxIters):
        
        objValues = []
        runTimes = []

        def callback(model,where):

            if where == GRB.Callback.MIPSOL:

                currentValue = model.cbGet(GRB.Callback.MIPSOL_OBJ)

                if currentValue > self.bestSolution_callBack:

                    runTime = time.time()
                    objValues.append(currentValue)
                    runTimes.append(runTime)
                    self.bestSolution_callBack = currentValue 



        self.model.model.setParam("TimeLimit", self.intervalTimeInBranch)
        self.model.model.setParam("DegenMoves", 1)
        newTime = self.intervalTimeInBranch

        for i in range(maxIters):
            self.model.model.optimize(callback)
            self.timeSpentInBranch += newTime
            if self.model.model.ObjVal > self.bestSolution:
                self.bestSolution = self.model.model.ObjVal
                self.iterationsSinceImprovement = 0
            elif self.timeSpentInBranch < timeLimitPerBranch:
                newTime = min(self.intervalTimeInBranch,timeLimitPerBranch-self.timeSpentInBranch)
                self.model.model.setParam("TimeLimit", newTime)
                
                continue
            else:
                if len(self.branchPriority) == 0:
                    break
                self.branchingVariable = self.branchPriority.pop()
                self.k = self.ks.pop()

            self.model.model.setParam("TimeLimit", self.intervalTimeInBranch)
            self.timeSpentInBranch = 0
            self.addLocalBranchingConstraint()
        return objValues, runTimes
    
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


    maxIters = 100
    timeLimitPerBranch = 600
    timeLimitForPureSolve = 60*60

    l = 4
    u = 5
    n_events = 6

    for i in [22,23,24,25,26,27,28]:
        try:
            n_girls = i // 2
            n_boys = i-n_girls



            data = {   "n_girls": n_girls,
            "n_boys": n_boys,
            "numOfEvents": n_events,
            "minNumGuests": l,
            "maxNumGuests": u
            }


            # df = pd.DataFrame()
            # dwf = DinnerWithFriendsSolver()
            # dwf.readData(data)
            # dwf.setFeasibleSolution()


            # startTime = time.time()
            # objValues,runTimes = dwf.solveModel(timeLimitForPureSolve)
            # endTime = time.time()
            # times = np.array(runTimes + [endTime]) - startTime


            # solver_entries = pd.DataFrame({
            # 'runTime': times,      
            # 'Value':  objValues + objValues[-1:]          
            # },index= ['Solver'] * len(times))

            # df = pd.concat([df, solver_entries])

            # bound = dwf.model.ObjBound

            # df['BestBound'] = bound

            # df['OptimalityGap'] = df['Value'] / df['BestBound']

            # N = n_girls+n_boys

            # df.to_csv(f'results/baseModelResults/SolverSolution_size{N}.csv')
            df = pd.DataFrame()
            dwf = DinnerWithFriendsSolver()
            dwf.readData(data)
            dwf.setFeasibleSolution()

            N = n_girls+n_boys



            branchingInformer = branchingInformation_MeetsAtEInG_percentage(0.15) #branchingInformation_MeetsAtEInG_fixedk(50)

            localBrancher = localBranching(dwf,branchingInformer)
            startTime = time.time()
            objValues,runTimes = localBrancher.performLocalBranching(timeLimitPerBranch,maxIters)
            endTime = time.time()
            times = np.array(runTimes + [endTime]) - startTime
            heuristic_entries = pd.DataFrame({
            'runTime': times,      
            'Value':  objValues + objValues[-1:]          
            },index= ['Heuristic'] * len(times))


            df = pd.concat([df, heuristic_entries])

            df.to_csv(f'results/baseModelResults/15PercentageK_initPureSolve_meetsAtEInG/HeuristicSolution_size{N}.csv')
        except Exception as e:
            print(f'{i} failed with error {e}')