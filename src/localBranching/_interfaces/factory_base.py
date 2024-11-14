from abc import ABC, abstractmethod
from src.localBranching._interfaces import Brancher_base,Terminate_base


class Factory_base(ABC):

    @abstractmethod
    def getBrancher(self) -> Brancher_base:
        pass

    @abstractmethod
    def getTerminater(self) -> Terminate_base:
        pass