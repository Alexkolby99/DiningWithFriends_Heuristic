from abc import abstractmethod, ABC

class constructionHeurestic_Base(ABC):

    @abstractmethod
    def constructFeasibleSolution(self):
        pass