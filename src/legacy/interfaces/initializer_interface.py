from abc import ABC, abstractmethod
from typing import List


class Initializer_base(ABC):
    @abstractmethod
    def initializeGroups(self, boys: List['students'], girls: List['students'],t) -> List['groups']:
        """
        Initializes groups based on the provided lists of boys and girls.
        
        Returns a list of groups formed.
        """
        pass