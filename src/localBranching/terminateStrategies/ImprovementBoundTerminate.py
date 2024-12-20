import os
import time
from gurobipy import GRB, Model
import numpy as np
import pandas as pd
from src.localBranching._interfaces import Terminate_base


class ImprovementBoundTerminater(Terminate_base):

    def __init__(self,improvementPercentage: float,instantThreshhold: float,trackOptimization: bool) -> None:
        self.bestSolution = None
        self.trackOptimization = trackOptimization
        self.runTimes = []
        self.objValues = []
        self.improvementFactor = 1 + improvementPercentage
        self.InstantThreshhold = instantThreshhold
        self.solutionToBeat = None

    def updateSolutionToBeat(self,objValue,runTime):

        if self.solutionToBeat is None:
            self.solutionToBeat = objValue
        elif objValue >= self.solutionToBeat*self.improvementFactor or runTime < self.InstantThreshhold:
            self.solutionToBeat = objValue

    def callback(self, model: Model, where: int) -> None:
        # this has changed but minor no need to rerun
        if where == GRB.Callback.MIPSOL:

            currentValue = model.cbGet(GRB.Callback.MIPSOL_OBJ)
            if self.bestSolution is None:
                self.bestSolution = currentValue
                self.solutionToBeat = currentValue
                self.runTimes.append(time.time())
                self.objValues.append(currentValue)


            if currentValue > self.bestSolution:
                if self.trackOptimization:
                    self.runTimes.append(time.time())
                    self.objValues.append(currentValue)
                
                runtime = model.cbGet(GRB.Callback.RUNTIME)

                improvedEnough = currentValue > self.solutionToBeat * self.improvementFactor
                improvedFastEnough = (runtime < self.InstantThreshhold and currentValue > self.bestSolution)
                self.bestSolution = currentValue
                if improvedEnough or improvedFastEnough:
                    self.bestSolution = currentValue
                    model.terminate()

    
    def saveTracking(self,startTime: float,initialValue: float,path: str):

        if not self.trackOptimization:
            return None

        runTimes = np.array([startTime] + self.runTimes) - startTime
        objValues = [initialValue] + self.objValues

        performance = pd.DataFrame({
            'runTime': runTimes,      
            'Value':  objValues,      
            },index= ['Heuristic'] * len(runTimes))    
        
        dir = os.path.dirname(path)

        if not dir:
            dir = os.getcwd()

        if os.path.isdir(dir):
            performance.to_csv(path)
        else:
            raise FileNotFoundError('Unable to find the specified path')