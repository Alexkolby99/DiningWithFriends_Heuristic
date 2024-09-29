from abc import ABC, abstractmethod
from typing import List, Literal

class student_Base(ABC):

    @property
    @abstractmethod
    def identifier(self) -> int:
        '''
        return the unique identifier for the student
        '''
        pass
    
    @property
    @abstractmethod
    def gender(self)-> Literal[0,1]:
        '''
        return the gender of the student
        '''
        pass

    @property
    @abstractmethod
    def hostTimes(self) -> int:
        '''
        return the total number of times the student has been host
        '''
        pass

    @property
    @abstractmethod
    def studentsThatVisited(self) -> List['Students']:
        '''
        return the list of students that has visited self
        '''
        pass

    @property
    @abstractmethod
    def groups(self) -> List['Groups']:
        '''
        return the list of groups the student is assigned to at each event
        initially it is of length T and has None in all entries
        '''
        pass

    @abstractmethod
    def addHostTime(self) -> None:
        '''
        Increment host times by 1
        '''
        pass

    @abstractmethod
    def removeHostTime(self) -> None:
        '''
        subtract one from host times
        '''
        pass

    @abstractmethod 
    def assignGroup(self,group,t) -> None:
        '''
        assigns the group at position t in groups
        '''
        pass

    @abstractmethod
    def addStudentThatVisited(self,student) -> None:
        '''
        Adds a student to the visited list
        '''
        pass