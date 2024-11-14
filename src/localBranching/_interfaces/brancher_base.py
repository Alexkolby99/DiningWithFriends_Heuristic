from abc import ABC, abstractmethod
from gurobipy import Model


class Brancher_base(ABC):

    @abstractmethod
    def nextBranch(self,objective: float,bestObjective: float, timeLeft: float) -> Model:
        pass
    
    @property
    @abstractmethod
    def initObjectiveValue(self):
        pass