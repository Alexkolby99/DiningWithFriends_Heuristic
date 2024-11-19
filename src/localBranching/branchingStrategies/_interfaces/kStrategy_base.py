from abc import ABC,abstractmethod
from gurobipy import Var

class KStrategy_base(ABC):

    @abstractmethod
    def getK(self,variable: Var,objVal: float) -> int:
        pass