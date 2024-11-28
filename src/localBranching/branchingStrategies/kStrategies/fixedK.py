from src.localBranching.branchingStrategies._interfaces import KStrategy_base
from gurobipy import Var

class FixedK(KStrategy_base):

    def __init__(self,k) -> None:
        self.k = k

    def getK(self,variable: Var, objVal: float):

        return self.k

