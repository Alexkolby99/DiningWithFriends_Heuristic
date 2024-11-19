from src.localBranching.branchingStrategies._interfaces import KStrategy_base
from gurobipy import Var

class adaptiveK(KStrategy_base):

    def __init__(self,percentage,factor,threshold) -> None:
        self.percentage = percentage
        self.increaseFactor = factor
        self.bestSolution = None
        self.threshold = threshold

    def getK(self,variable: Var,objVal: float):

        k = int(len(variable) * self.percentage)

        if self.bestSolution is None:
            self.bestSolution = objVal
        
        elif objVal <= self.bestSolution + self.threshold:
            k = k*self.increaseFactor

        self.bestSolution = objVal

        return k

