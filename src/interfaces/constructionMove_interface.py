from abc import ABC, abstractmethod
from typing import List


class ConstructionMove_base(ABC):
    @abstractmethod
    def performMove(self, target, groups: List['groups']) -> bool:
        """
        Performs a move with the given students and groups.
        
        Returns True if the move was successful, False otherwise.
        """
        pass