from abc import ABC,abstractmethod
from src.model import DinnerWithFriendsSolver

class ModelFactory_base(ABC):

    @abstractmethod
    def setObjectiveFunction(self,model: DinnerWithFriendsSolver) -> None:
        pass

    @abstractmethod
    def setAdditionalConstraints(self,model: DinnerWithFriendsSolver) -> None:
        pass