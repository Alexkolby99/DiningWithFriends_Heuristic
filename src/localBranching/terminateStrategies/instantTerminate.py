import os
import time
from gurobipy import GRB, Model
import numpy as np
import pandas as pd
from src.localBranching._interfaces import Terminate_base


class InstantTerminater(Terminate_base):

    def __init__(self,trackOptimization: bool) -> None:
        self.bestSolution = None
        self.trackOptimization = trackOptimization
        self.runTimes = [] 
        self.objValues = []
        self.solutionToBeat = None # is here for interface consistency

    def callback(self, model: Model, where: int) -> None:
        
        if where == GRB.Callback.MIPSOL:

            currentValue = model.cbGet(GRB.Callback.MIPSOL_OBJ)
            if self.bestSolution is None:
                self.bestSolution = currentValue

            if currentValue > self.bestSolution:
                self.bestSolution = currentValue
                if self.trackOptimization:
                    self.runTimes.append(time.time())
                    self.objValues.append(currentValue)
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