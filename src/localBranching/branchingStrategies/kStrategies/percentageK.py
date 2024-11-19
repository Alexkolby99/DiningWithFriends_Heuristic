from src.localBranching.branchingStrategies._interfaces import KStrategy_base
from gurobipy import Var

class PercentageK(KStrategy_base):

    def __init__(self,percentage) -> None:
        self.percentage = percentage

    def getK(self,variable: Var, objVal: float):

        return int(len(variable) * self.percentage)

