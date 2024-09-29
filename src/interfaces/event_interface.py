from abc import abstractmethod, ABC
from typing import List

class event_Base(ABC):

    @property
    @abstractmethod
    def groups(self) -> List['Groups']:
        pass

    @property
    @abstractmethod
    def timeStamp(self) -> int:
        pass

    @property
    @abstractmethod
    def hosts(self) -> List['students']:
        pass

    @abstractmethod
    def addGroup(self,group) -> None:
        pass

    @abstractmethod
    def removeGroup(self,group) -> None:
        pass