from abc import abstractmethod, ABC
from typing import List

class group_Base(ABC):

    @property
    @abstractmethod
    def members(self) -> List['Students']:
        '''
        List of all the members
        '''
        pass

    @property
    @abstractmethod
    def host(self) -> 'Student':
        '''
        The host of the group
        '''
        pass


    @property
    @abstractmethod
    def size(self) -> int:
        '''
        returns the length of members
        '''
        pass

    @property
    @abstractmethod
    def t(self) -> int:
        '''
        the timestamp associated with the group
        '''
        pass

    @abstractmethod
    def addMember(self,member) -> None:
        '''
        method that adds member to the members list
        '''
        pass

    @abstractmethod
    def removeMember(self,member) -> None:
        '''
        method that removes member from the members list
        '''
        pass