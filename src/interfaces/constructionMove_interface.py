from abc import ABC, abstractmethod
from typing import List


class ConstructionMove_base(ABC):
    @abstractmethod
    def performMove(self, students: 'students', groups: List['groups'],t) -> bool:
        """
        Performs a move with the given students and groups.
        
        Returns True if the move was successful, False otherwise.
        """
        pass