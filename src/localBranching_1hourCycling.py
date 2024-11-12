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


class branchingInformation_Step_percentage:

    def __init__(self,percentage) -> None:
        
        self.percentage = percentage
        self._ks = None

    def getBranchPriority(self,model: DinnerWithFriendsSolver) -> List:

        self._ks = [int(len(model.meetsAtEInG)*self.percentage),int(len(model.meetsAtE)*self.percentage),int(len(model.meets)*self.percentage)][::-1]

        return [model.meetsAtEInG,model.meetsAtE,model.meets][::-1]

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
        self.branchPriority = branchingInformer.getBranchPriority(self.model)
        self.ks = branchingInformer.getks()
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

                if currentValue > self.bestSolution_callBack:

                    runTime = time.time()
                    objValues.append(currentValue)
                    runTimes.append(runTime)
                    self.bestSolution_callBack = currentValue 

                if currentValue > self.bestSolution and model.cbGet(GRB.Callback.RUNTIME) < 300:
                    model.terminate()

                if currentValue > self.bestSolution + self.bound*0.02:
                    model.terminate()


        self.model.model.setParam("TimeLimit", 600)
        self.model.model.setParam("DegenMoves", 1)

        iter = 0
        while True:
            self.model.model.optimize(callback)
                
            if self.model.model.ObjVal > self.bestSolution:
                self.bestSolution = self.model.model.ObjVal                
            
            timeSpent = time.time() - start
            if timeSpent >= timeLimit:
                break
            else:
                newTime = min(600,timeLimit-timeSpent)
                self.model.model.setParam("TimeLimit", newTime)
                self.addLocalBranchingConstraint(iter)
            
            iter += 1

        return objValues, runTimes
    
    def removeLocalBranchConstraint(self):

        oldLocalBranchConstraint = self.model.model.getConstrByName(self.localBranchingConstraintName)
        if oldLocalBranchConstraint is not None:
            self.model.model.remove(oldLocalBranchConstraint)

    def addLocalBranchingConstraint(self,iter):
        
        self.removeLocalBranchConstraint()

        lhs = gp.LinExpr()
        for v in self.branchPriority[iter%len(self.branchPriority)].values():
            try: 
                val = v.X
            except AttributeError:
                val = v.Start
            if val < 0.5:  # Binary variable is 0 in initial solution
                lhs.addTerms(1, v)
            else:  # Binary variable is 1 in initial solution
                lhs.addConstant(1)
                lhs.addTerms(-1, v)
        
        self.model.model.addConstr(lhs <= self.ks[iter%len(self.branchPriority)], name=self.localBranchingConstraintName)
        self.model.model.update()

if __name__ == '__main__':


    timeLimit = 3600
    timeLimitForPureSolve = 60*60

    l = 4
    u = 5
    n_events = 6

    for i in [23,24,25,27,28]:
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



            branchingInformer = branchingInformation_Step_percentage(0.15) #branchingInformation_MeetsAtEInG_fixedk(50)

            localBrancher = localBranching(dwf,branchingInformer)
            startTime = time.time()
            objValues,runTimes = localBrancher.performLocalBranching(timeLimit)
            endTime = time.time()
            times = np.array(runTimes + [endTime]) - startTime
            heuristic_entries = pd.DataFrame({
            'runTime': times,      
            'Value':  objValues + objValues[-1:]          
            },index= ['Heuristic'] * len(times))


            df = pd.concat([df, heuristic_entries])

            df.to_csv(f'results/15PercentageK_initPureSolve_Cycling_1hour/HeuristicSolution_size{i}.csv')
        except Exception as e:
            print(f'{i} failed with error {e}')