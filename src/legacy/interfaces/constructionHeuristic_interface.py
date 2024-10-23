from abc import ABC, abstractmethod
from typing import List


class ConstructionHeuristic_base(ABC):

    @abstractmethod
    def constructSolution(self, boys: List['students'], girls: List['students']) -> List['Events']:
        """
        Constructs a solution based on the provided boys and girls lists.
        """
        pass