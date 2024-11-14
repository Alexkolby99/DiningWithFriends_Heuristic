
from abc import ABC, abstractmethod
from gurobipy import Model

class Terminate_base(ABC):

    @abstractmethod
    def callback(self,model: Model,where: int) -> None:
        pass

    @abstractmethod
    def saveTracking(self,startTime: float,initialValue: float,path: str):
        pass