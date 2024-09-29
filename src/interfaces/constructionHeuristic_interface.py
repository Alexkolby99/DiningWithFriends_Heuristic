from abc import ABC, abstractmethod
from typing import List


class ConstructionHeuristic_base(ABC):
    @property
    @abstractmethod
    def initialization(self) -> str:
        """
        Description of the initialization process.
        """
        pass

    @property
    @abstractmethod
    def moves(self) -> List['constructionMoves']:
        """
        Returns a list of possible construction moves.
        """
        pass

    @abstractmethod
    def constructSolution(self, boys: List['students'], girls: List['students']) -> List['Events']:
        """
        Constructs a solution based on the provided boys and girls lists.
        """
        pass